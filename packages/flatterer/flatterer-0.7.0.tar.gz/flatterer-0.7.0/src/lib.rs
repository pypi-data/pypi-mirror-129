mod postgresql;
mod schema_analysis;

use std::collections::HashMap;
use std::convert::TryInto;
use std::fmt;
use std::fs::{canonicalize, create_dir_all, remove_dir_all, File};
use std::io::{self, BufReader, Error as IoError, ErrorKind, Read, Write};
use std::path::PathBuf;
use std::{panic, thread};

use smartstring::alias::String as SmartString;
use anyhow::{Context, Result};
use crossbeam_channel::{bounded, Receiver, Sender};
use csv::{ByteRecord, Reader, ReaderBuilder, Writer, WriterBuilder};
use itertools::Itertools;
use pyo3::prelude::*;
use pyo3::types::PyIterator;
use regex::Regex;
use serde::{Deserialize, Serialize};
use serde_json::{json, Deserializer, Map, Value};
use smallvec::{smallvec, SmallVec};
use xlsxwriter::Workbook;
use yajlish::ndjson_handler::{NdJsonHandler, Selector};
use yajlish::Parser;

#[pymodule]
fn flatterer(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn flatten_rs(
        _py: Python,
        input_file: String,
        output_dir: String,
        csv: bool,
        xlsx: bool,
        path: String,
        main_table_name: String,
        emit_path: Vec<Vec<String>>,
        json_lines: bool,
        force: bool,
        fields: String,
        only_fields: bool,
        inline_one_to_one: bool,
        schema: String,
        table_prefix: String,
        path_separator: String,
        schema_titles: String,
    ) -> PyResult<()> {
        let flat_files_res = FlatFiles::new(
            output_dir.to_string(),
            csv,
            xlsx,
            force,
            main_table_name,
            emit_path,
            inline_one_to_one,
            schema,
            table_prefix,
            path_separator,
            schema_titles,
        );

        let mut selectors = vec![];

        if path != "" {
            selectors.push(Selector::Identifier(format!("\"{}\"", path.to_string())));
        }

        if flat_files_res.is_err() {
            let err = flat_files_res.unwrap_err();
            return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                "{:?}",
                err
            )));
        }

        let mut flat_files = flat_files_res.unwrap(); //already checked error

        if fields != "" {
            if let Err(err) = flat_files.use_fields_csv(fields, only_fields) {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )));
            }
        }

        let file;

        match File::open(&input_file) {
            Ok(input) => {
                file = BufReader::new(input);
            }
            Err(err) => {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "Can not open file `{}`: {:?}",
                    input_file,
                    anyhow::Error::new(err)
                )));
            }
        };

        if json_lines {
            if let Err(err) = flatten_from_jl(file, flat_files) {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )));
            }
        } else {
            if let Err(err) = flatten(file, flat_files, selectors) {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )));
            }
        }

        Ok(())
    }

    #[pyfn(m)]
    fn iterator_flatten_rs(
        py: Python,
        mut objs: &PyIterator,
        output_dir: String,
        csv: bool,
        xlsx: bool,
        main_table_name: String,
        emit_path: Vec<Vec<String>>,
        force: bool,
        fields: String,
        only_fields: bool,
        inline_one_to_one: bool,
        schema: String,
        table_prefix: String,
        path_separator: String,
        schema_titles: String,
    ) -> PyResult<()> {
        let flat_files_res = FlatFiles::new(
            output_dir.to_string(),
            csv,
            xlsx,
            force,
            main_table_name,
            emit_path,
            inline_one_to_one,
            schema,
            table_prefix,
            path_separator,
            schema_titles,
        );

        if flat_files_res.is_err() {
            let err = flat_files_res.unwrap_err();
            return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                "{:?}",
                err
            )));
        }

        let mut flat_files = flat_files_res.unwrap(); //already checked error

        if fields != "" {
            if let Err(err) = flat_files.use_fields_csv(fields, only_fields) {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )));
            }
        }

        let (sender, receiver) = bounded(1000);

        let handler = thread::spawn(move || -> PyResult<()> {
            for value in receiver {
                flat_files.process_value(value);
                if let Err(err) = flat_files.create_rows() {
                    return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "{:?}",
                        err
                    )));
                }
            }

            if let Err(err) = flat_files.write_files() {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )));
            }
            Ok(())
        });

        let mut gilpool;

        loop {
            unsafe {
                gilpool = py.new_pool();
            }

            let obj = objs.next();
            if obj.is_none() {
                break;
            }

            let result = obj.unwrap(); //checked for none

            let json_bytes = PyAny::extract::<&[u8]>(result?)?;

            match serde_json::from_slice::<Value>(&json_bytes) {
                Ok(value) => {
                    if let Err(err) = sender.send(value) {
                        return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                            "{:?}",
                            err
                        )));
                    }
                }
                Err(err) => {
                    return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "{:?}",
                        err
                    )))
                }
            }

            drop(gilpool)
        }

        drop(sender);

        match handler.join() {
            Ok(result) => {
                if let Err(err) = result {
                    return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "{:?}",
                        err
                    )));
                }
            }
            Err(err) => {
                return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "{:?}",
                    err
                )))
            }
        }
        Ok(())
    }

    Ok(())
}

#[derive(Hash, Clone, Debug)]
pub enum PathItem {
    Key(SmartString),
    Index(usize),
}

impl fmt::Display for PathItem {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            PathItem::Key(key) => write!(f, "{}", key),
            PathItem::Index(index) => write!(f, "{}", index),
        }
    }
}

#[derive(Debug)]
pub struct FlatFiles {
    output_path: PathBuf,
    csv: bool,
    xlsx: bool,
    main_table_name: String,
    emit_obj: SmallVec<[SmallVec<[String; 5]>; 5]>,
    row_number: u128,
    date_regexp: Regex,
    table_rows: HashMap<String, Vec<Map<String, Value>>>,
    tmp_csvs: HashMap<String, csv::Writer<File>>,
    table_metadata: HashMap<String, TableMetadata>,
    only_fields: bool,
    inline_one_to_one: bool,
    one_to_many_arrays: SmallVec<[SmallVec<[SmartString; 5]>; 5]>,
    one_to_one_arrays: SmallVec<[SmallVec<[SmartString; 5]>; 5]>,
    schema: String,
    table_prefix: String,
    path_separator: String,
    order_map: HashMap<String, usize>,
    field_titles_map: HashMap<String, String>,
}

#[derive(Serialize, Debug)]
pub struct TableMetadata {
    field_type: Vec<String>,
    fields: Vec<String>,
    field_counts: Vec<u32>,
    rows: u32,
    ignore: bool,
    ignore_fields: Vec<bool>,
    order: Vec<usize>,
    field_titles: Vec<String>,
    table_name_with_separator: String,
}

impl TableMetadata {
    fn new(
        table_name: &str,
        main_table_name: &str,
        path_separator: &str,
        table_prefix: &str,
    ) -> TableMetadata {
        let table_name_with_separator = if table_name == main_table_name {
            "".to_string()
        } else {
            let mut full_path = format!("{}{}", table_name, path_separator);
            if table_prefix != "" {
                full_path.replace_range(0..table_prefix.len(), "");
            }
            full_path
        };

        TableMetadata {
            fields: vec![],
            field_counts: vec![],
            field_type: vec![],
            rows: 0,
            ignore: false,
            ignore_fields: vec![],
            order: vec![],
            field_titles: vec![],
            table_name_with_separator,
        }
    }
}

#[derive(Debug, Deserialize)]
struct FieldsRecord {
    table_name: String,
    field_name: String,
    field_type: String,
    field_title: Option<String>,
}

struct JLWriter {
    pub buf: Vec<u8>,
    pub buf_sender: Sender<Vec<u8>>,
}

impl Write for JLWriter {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        if buf == [b'\n'] {
            self.buf_sender.send(self.buf.clone()).unwrap();
            self.buf.clear();
            Ok(buf.len())
        } else {
            self.buf.extend_from_slice(buf);
            Ok(buf.len())
        }
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

impl FlatFiles {
    pub fn new(
        output_dir: String,
        csv: bool,
        xlsx: bool,
        force: bool,
        main_table_name: String,
        emit_obj: Vec<Vec<String>>,
        inline_one_to_one: bool,
        schema: String,
        table_prefix: String,
        path_separator: String,
        schema_titles: String,
    ) -> Result<FlatFiles> {
        smartstring::validate();
        let output_path = PathBuf::from(output_dir.clone());
        if output_path.is_dir() {
            if force {
                remove_dir_all(&output_path)
                    .context(format!("Can not remove output path `{}`", output_dir))?;
            } else {
                return Err(anyhow::Error::new(IoError::new(
                    ErrorKind::AlreadyExists,
                    format!("Directory {} already exists", output_dir),
                )));
            }
        }
        if csv {
            let csv_path = output_path.join("csv");
            create_dir_all(&csv_path)
                .context(format!("Can not create output path `{}`", output_dir))?;
        }

        let tmp_path = output_path.join("tmp");
        create_dir_all(&tmp_path)
            .context(format!("Can not create output path `{}`", output_dir))?;

        let order_map;
        let field_titles_map;

        if schema != "" {
            let schema_analysis =
                schema_analysis::schema_analysis(&schema, &path_separator, schema_titles)?;
            order_map = schema_analysis.field_order_map;
            field_titles_map = schema_analysis.field_titles_map;
        } else {
            order_map = HashMap::new();
            field_titles_map = HashMap::new()
        }

        let mut smallvec_emit_obj: SmallVec<[SmallVec<[String; 5]>; 5]> = smallvec![];

        for emit_vec in emit_obj {
            smallvec_emit_obj.push(SmallVec::from_vec(emit_vec))
        }

        Ok(FlatFiles {
            output_path,
            csv,
            xlsx,
            main_table_name: [table_prefix.clone(), main_table_name].concat(),
            emit_obj: smallvec_emit_obj,
            row_number: 1,
            date_regexp: Regex::new(r"^([1-3]\d{3})-(\d{2})-(\d{2})([T ](\d{2}):(\d{2}):(\d{2}(?:\.\d*)?)((-(\d{2}):(\d{2})|Z)?))?$").unwrap(),
            table_rows: HashMap::new(),
            tmp_csvs: HashMap::new(),
            table_metadata: HashMap::new(),
            only_fields: false,
            inline_one_to_one,
            one_to_many_arrays: SmallVec::new(),
            one_to_one_arrays: SmallVec::new(),
            schema,
            table_prefix,
            path_separator,
            order_map,
            field_titles_map
        })
    }

    fn handle_obj(
        &mut self,
        mut obj: Map<String, Value>,
        emit: bool,
        full_path: SmallVec<[PathItem; 10]>,
        no_index_path: SmallVec<[SmartString; 5]>,
        one_to_many_full_paths: SmallVec<[SmallVec<[PathItem; 10]>; 5]>,
        one_to_many_no_index_paths: SmallVec<[SmallVec<[SmartString; 5]>; 5]>,
        one_to_one_key: bool,
    ) -> Option<Map<String, Value>> {
        let mut to_insert: SmallVec<[(String, Value); 30]> = smallvec![];
        let mut to_delete: SmallVec<[String; 30]> = smallvec![];

        let mut one_to_one_array: SmallVec<[(String, Value); 30]> = smallvec![];

        for (key, value) in obj.iter_mut() {
            if let Some(arr) = value.as_array() {
                let mut str_count = 0;
                let mut obj_count = 0;
                let arr_length = arr.len();
                for array_value in arr {
                    if array_value.is_object() {
                        obj_count += 1
                    };
                    if array_value.is_string() {
                        str_count += 1
                    };
                }
                if arr_length == 0 {
                    to_delete.push(key.clone());
                }
                if str_count == arr_length {
                    let keys: Vec<String> = arr
                        .iter()
                        .map(|val| (val.as_str().unwrap().to_string())) //value known as str
                        .collect();
                    let new_value = json!(keys.join(","));
                    to_insert.push((key.clone(), new_value))
                } else if obj_count == arr_length {
                    to_delete.push(key.clone());
                    let mut removed_array = value.take(); // obj.remove(&key).unwrap(); //key known
                    let my_array = removed_array.as_array_mut().unwrap(); //key known as array
                    for (i, array_value) in my_array.iter_mut().enumerate() {
                        let my_value = array_value.take();

                        let mut new_full_path = full_path.clone();
                        new_full_path.push(PathItem::Key(SmartString::from(key)));
                        new_full_path.push(PathItem::Index(i));

                        let mut new_one_to_many_full_paths = one_to_many_full_paths.clone();
                        new_one_to_many_full_paths.push(new_full_path.clone());

                        let mut new_no_index_path = no_index_path.clone();
                        new_no_index_path.push(SmartString::from(key));

                        let mut new_one_to_many_no_index_paths = one_to_many_no_index_paths.clone();
                        new_one_to_many_no_index_paths.push(new_no_index_path.clone());

                        if self.inline_one_to_one
                            && !self.one_to_many_arrays.contains(&new_no_index_path)
                        {
                            if arr_length == 1 {
                                one_to_one_array.push((key.clone(), my_value.clone()));
                                if !self.one_to_one_arrays.contains(&new_no_index_path) {
                                    self.one_to_one_arrays.push(new_no_index_path.clone())
                                }
                            } else if arr_length > 1 {
                                self.one_to_one_arrays.retain(|x| x != &new_no_index_path);
                                self.one_to_many_arrays.push(new_no_index_path.clone())
                            }
                        }

                        if let Value::Object(my_obj) = my_value {
                            if !one_to_one_key {
                                self.handle_obj(
                                    my_obj,
                                    true,
                                    new_full_path,
                                    new_no_index_path,
                                    new_one_to_many_full_paths,
                                    new_one_to_many_no_index_paths,
                                    false,
                                );
                            }
                        }
                    }
                } else {
                    let json_value = json!(format!("{}", value));
                    to_insert.push((key.clone(), json_value));
                }
            }
        }

        let mut one_to_one_array_keys = vec![];

        for (key, value) in one_to_one_array {
            one_to_one_array_keys.push(key.clone());
            obj.insert(key, value);
        }

        for (key, value) in obj.iter_mut() {
            if value.is_object() {
                let my_value = value.take();
                to_delete.push(key.clone());

                let mut new_full_path = full_path.clone();
                new_full_path.push(PathItem::Key(SmartString::from(key)));
                let mut new_no_index_path = no_index_path.clone();
                new_no_index_path.push(SmartString::from(key));

                let mut emit_child = false;
                if self
                    .emit_obj
                    .iter()
                    .any(|emit_path| emit_path == &new_no_index_path)
                {
                    emit_child = true;
                }
                if let Value::Object(my_value) = my_value {
                    let new_obj = self.handle_obj(
                        my_value,
                        emit_child,
                        new_full_path,
                        new_no_index_path,
                        one_to_many_full_paths.clone(),
                        one_to_many_no_index_paths.clone(),
                        one_to_one_array_keys.contains(&key),
                    );
                    if let Some(mut my_obj) = new_obj {
                        for (new_key, new_value) in my_obj.iter_mut() {
                            let mut object_key = String::with_capacity(100);
                            object_key.push_str(key);
                            object_key.push_str(&self.path_separator);
                            object_key.push_str(new_key);

                            to_insert.push((object_key, new_value.take()));
                        }
                    }
                }
            }
        }
        for key in to_delete {
            obj.remove(&key);
        }
        for (key, value) in to_insert {
            obj.insert(key, value);
        }

        if emit {
            self.process_obj(
                obj,
                no_index_path,
                one_to_many_full_paths,
                one_to_many_no_index_paths,
            );
            None
        } else {
            Some(obj)
        }
    }

    pub fn process_obj(
        &mut self,
        mut obj: Map<String, Value>,
        no_index_path: SmallVec<[SmartString; 5]>,
        one_to_many_full_paths: SmallVec<[SmallVec<[PathItem; 10]>; 5]>,
        one_to_many_no_index_paths: SmallVec<[SmallVec<[SmartString; 5]>; 5]>,
    ) {
        let mut path_iter = one_to_many_full_paths
            .iter()
            .zip(one_to_many_no_index_paths)
            .peekable();

        if one_to_many_full_paths.len() == 0 {
            obj.insert(
                String::from("_link"),
                Value::String(self.row_number.to_string()),
            );
        }

        while let Some((full, no_index)) = path_iter.next() {
            if path_iter.peek().is_some() {
                obj.insert(
                    [
                        "_link_".to_string(),
                        no_index.iter().join(&self.path_separator),
                    ]
                    .concat(),
                    Value::String(
                        [
                            self.row_number.to_string(),
                            ".".to_string(),
                            full.iter().join("."),
                        ]
                        .concat(),
                    ),
                );
            } else {
                obj.insert(
                    String::from("_link"),
                    Value::String(
                        [
                            self.row_number.to_string(),
                            ".".to_string(),
                            full.iter().join("."),
                        ]
                        .concat(),
                    ),
                );
            }
        }

        obj.insert(
            ["_link_", &self.main_table_name].concat(),
            Value::String(self.row_number.to_string()),
        );

        let mut table_name = [
            self.table_prefix.clone(),
            no_index_path.join(&self.path_separator),
        ]
        .concat();

        if no_index_path.len() == 0 {
            table_name = self.main_table_name.clone();
        }

        if !self.table_rows.contains_key(&table_name) {
            self.table_rows.insert(table_name, vec![obj]);
        } else {
            let current_list = self.table_rows.get_mut(&table_name).unwrap(); //key known
            current_list.push(obj)
        }
    }

    pub fn create_rows(&mut self) -> Result<()> {
        for (table, rows) in self.table_rows.iter_mut() {
            let output_csv_path = self.output_path.join(format!("tmp/{}.csv", table));
            if !self.tmp_csvs.contains_key(table) {
                self.tmp_csvs.insert(
                    table.clone(),
                    WriterBuilder::new()
                        .flexible(true)
                        .from_path(&output_csv_path)
                        .context(format!(
                            "Can not create csv file `{}`",
                            &output_csv_path.to_string_lossy()
                        ))?,
                );
            }

            if !self.table_metadata.contains_key(table) {
                self.table_metadata.insert(
                    table.clone(),
                    TableMetadata::new(
                        table,
                        &self.main_table_name,
                        &self.path_separator,
                        &self.table_prefix,
                    ),
                );
            }

            let table_metadata = self.table_metadata.get_mut(table).unwrap(); //key known
            let writer = self.tmp_csvs.get_mut(table).unwrap(); //key known

            for row in rows {
                let mut output_row: SmallVec<[String; 30]> = smallvec![];
                for (num, field) in table_metadata.fields.iter().enumerate() {
                    if let Some(value) = row.get_mut(field) {
                        table_metadata.field_counts[num] += 1;
                        output_row.push(value_convert(
                            value.take(),
                            &mut table_metadata.field_type,
                            num,
                            &self.date_regexp,
                        ));
                    } else {
                        output_row.push("".to_string());
                    }
                }
                for (key, value) in row {
                    if !table_metadata.fields.contains(key) && !self.only_fields {
                        table_metadata.fields.push(key.clone());
                        table_metadata.field_counts.push(1);
                        table_metadata.field_type.push("".to_string());
                        table_metadata.ignore_fields.push(false);
                        let full_path =
                            format!("{}{}", table_metadata.table_name_with_separator, key);

                        if let Some(title) = self.field_titles_map.get(&full_path) {
                            table_metadata.field_titles.push(title.clone());
                        } else {
                            table_metadata.field_titles.push(key.clone());
                        }

                        output_row.push(value_convert(
                            value.take(),
                            &mut table_metadata.field_type,
                            table_metadata.fields.len() - 1,
                            &self.date_regexp,
                        ));
                    }
                }
                if output_row.len() > 0 {
                    table_metadata.rows += 1;
                    writer.write_record(&output_row)?;
                }
            }
        }
        for val in self.table_rows.values_mut() {
            val.clear();
        }
        Ok(())
    }

    pub fn process_value(&mut self, value: Value) {
        if let Value::Object(obj) = value {
            self.handle_obj(obj, true, smallvec![], smallvec![], smallvec![], smallvec![], false);
            self.row_number += 1;
        }
    }

    pub fn use_fields_csv(&mut self, filepath: String, only_fields: bool) -> Result<()> {
        let mut fields_reader =
            Reader::from_path(&filepath).context(format!("Can not open file `{}`", filepath))?;

        if only_fields {
            self.only_fields = true;
        }

        for row in fields_reader.deserialize() {
            let row: FieldsRecord =
                row.context(format!("Failed to read row from `{}`", filepath))?;

            if !self.table_metadata.contains_key(&row.table_name) {
                self.table_metadata.insert(
                    row.table_name.clone(),
                    TableMetadata::new(
                        &row.table_name,
                        &self.main_table_name,
                        &self.path_separator,
                        &self.table_prefix,
                    ),
                );
            }
            let table_metadata = self.table_metadata.get_mut(&row.table_name).unwrap(); //key known
            table_metadata.fields.push(row.field_name.clone());
            table_metadata.field_counts.push(0);
            table_metadata.field_type.push(row.field_type);
            table_metadata.ignore_fields.push(false);
            match row.field_title {
                Some(field_title) => table_metadata.field_titles.push(field_title),
                None => table_metadata.field_titles.push(row.field_name),
            }
        }

        return Ok(());
    }

    pub fn mark_ignore(&mut self) {
        let one_to_many_table_names = self
            .one_to_many_arrays
            .iter()
            .map(|item| item.join(&self.path_separator))
            .collect_vec();

        for metadata in self.table_metadata.values_mut() {
            for (num, field) in metadata.fields.iter().enumerate() {
                let full_path = format!("{}{}", metadata.table_name_with_separator, field);
                for one_to_many_table_name in &one_to_many_table_names {
                    if full_path.starts_with(one_to_many_table_name)
                        && !metadata
                            .table_name_with_separator
                            .starts_with(one_to_many_table_name)
                    {
                        metadata.ignore_fields[num] = true;
                    }
                }
            }
        }

        for table_path in &self.one_to_one_arrays {
            let table_name = format!(
                "{}{}",
                self.table_prefix,
                table_path.iter().join(&self.path_separator)
            );
            if let Some(table_metadata) = self.table_metadata.get_mut(&table_name) {
                table_metadata.ignore = true
            }
        }
    }

    pub fn determine_order(&mut self) -> Result<()> {
        for metadata in self.table_metadata.values_mut() {
            let mut fields_to_order: Vec<(usize, usize)> = vec![];

            for (num, field) in metadata.fields.iter().enumerate() {
                let full_path = format!("{}{}", metadata.table_name_with_separator, field);

                let schema_order: usize;

                if field.starts_with("_link") {
                    schema_order = 0
                } else if let Some(order) = self.order_map.get(&full_path) {
                    schema_order = order.clone()
                } else {
                    schema_order = usize::MAX;
                }
                fields_to_order.push((schema_order, num))
            }

            fields_to_order.sort();

            for (_, field_order) in fields_to_order.iter() {
                metadata.order.push(field_order.clone());
            }
        }
        Ok(())
    }

    pub fn write_files(&mut self) -> Result<()> {
        self.mark_ignore();
        self.determine_order()?;

        for (file, tmp_csv) in self.tmp_csvs.iter_mut() {
            tmp_csv
                .flush()
                .context(format!("Can not flush file `{}`", file))?;
        }

        if self.csv {
            self.write_csvs()?;
            self.write_postgresql()?;
            self.write_sqlite()?;
        };

        if self.xlsx {
            self.write_xlsx()?;
        };

        let tmp_path = self.output_path.join("tmp");
        remove_dir_all(&tmp_path).context(format!(
            "Can not remove output path `{}`",
            tmp_path.to_string_lossy()
        ))?;

        self.write_data_package()?;
        self.write_fields_csv()?;

        Ok(())
    }

    pub fn write_data_package(&mut self) -> Result<()> {
        let metadata_file = File::create(self.output_path.join("data_package.json"))?;

        let mut resources = vec![];

        for table_name in self.table_metadata.keys().sorted() {
            let metadata = self.table_metadata.get(table_name).unwrap();
            let mut fields = vec![];
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }
            let table_order = metadata.order.clone();

            for order in table_order {
                if metadata.ignore_fields[order] {
                    continue;
                }
                let field = json!({
                    "name": metadata.field_titles[order],
                    "type": metadata.field_type[order],
                    "count": metadata.field_counts[order],
                });
                fields.push(field);
            }

            let mut resource = json!({
                "profile": "tabular-data-resource",
                "name": table_name,
                "schema": {
                    "fields": fields,
                    "primaryKey": "_link"
                }
            });
            if self.csv {
                resource.as_object_mut().unwrap().insert(
                    "path".to_string(),
                    Value::String(format!("csv/{}.csv", table_name)),
                );
            }

            resources.push(resource)
        }

        let data_package = json!({
            "profile": "tabular-data-package",
            "resources": resources
        });

        serde_json::to_writer_pretty(metadata_file, &data_package)?;

        Ok(())
    }

    pub fn write_fields_csv(&mut self) -> Result<()> {
        let mut fields_writer = Writer::from_path(self.output_path.join("fields.csv"))?;

        fields_writer.write_record([
            "table_name",
            "field_name",
            "field_type",
            "field_title",
            "count",
        ])?;
        for table_name in self.table_metadata.keys().sorted() {
            let metadata = self.table_metadata.get(table_name).unwrap();
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }
            let table_order = metadata.order.clone();
            for order in table_order {
                if metadata.ignore_fields[order] {
                    continue;
                }
                fields_writer.write_record([
                    table_name,
                    &metadata.fields[order],
                    &metadata.field_type[order],
                    &metadata.field_titles[order],
                    &metadata.field_counts[order].to_string(),
                ])?;
            }
        }

        Ok(())
    }

    pub fn write_csvs(&mut self) -> Result<()> {
        let tmp_path = self.output_path.join("tmp");
        let csv_path = self.output_path.join("csv");

        for table_name in self.tmp_csvs.keys() {
            let metadata = self.table_metadata.get(table_name).unwrap(); //key known
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }

            let csv_reader = ReaderBuilder::new()
                .has_headers(false)
                .flexible(true)
                .from_path(tmp_path.join(format!("{}.csv", table_name)))?;

            let mut csv_writer =
                WriterBuilder::new().from_path(csv_path.join(format!("{}.csv", table_name)))?;

            let mut non_ignored_fields = vec![];

            let table_order = metadata.order.clone();

            for order in table_order {
                if !metadata.ignore_fields[order] {
                    non_ignored_fields.push(metadata.field_titles[order].clone())
                }
            }

            csv_writer.write_record(&non_ignored_fields)?;

            let mut output_row = ByteRecord::new();

            for row in csv_reader.into_byte_records() {
                let this_row = row?;
                let table_order = metadata.order.clone();

                for order in table_order {
                    if metadata.ignore_fields[order] {
                        continue;
                    }
                    if order >= this_row.len() {
                        output_row.push_field(b"");
                    } else {
                        output_row.push_field(&this_row[order]);
                    }
                }

                csv_writer.write_byte_record(&output_row)?;
                output_row.clear();
            }
        }

        Ok(())
    }

    pub fn write_xlsx(&mut self) -> Result<()> {
        let tmp_path = self.output_path.join("tmp");

        let workbook = Workbook::new_with_options(
            &self.output_path.join("output.xlsx").to_string_lossy(),
            true,
            Some(&tmp_path.to_string_lossy()),
            false,
        );

        for table_name in self.tmp_csvs.keys() {
            let metadata = self.table_metadata.get(table_name).unwrap(); //key known
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }
            let mut new_table_name = table_name.clone();
            new_table_name.truncate(31);
            let mut worksheet = workbook.add_worksheet(Some(&new_table_name))?;

            let csv_reader = ReaderBuilder::new()
                .has_headers(false)
                .flexible(true)
                .from_path(tmp_path.join(format!("{}.csv", table_name)))?;

            let mut col_index = 0;

            let table_order = metadata.order.clone();

            for order in table_order {
                if !metadata.ignore_fields[order] {
                    worksheet.write_string(
                        0,
                        col_index,
                        &metadata.field_titles[order].clone(),
                        None,
                    )?;
                    col_index += 1;
                }
            }

            for (row_num, row) in csv_reader.into_records().enumerate() {
                col_index = 0;
                let this_row = row?;

                let table_order = metadata.order.clone();

                for order in table_order {
                    if metadata.ignore_fields[order] {
                        continue;
                    }
                    if order >= this_row.len() {
                        continue;
                    }

                    let cell = &this_row[order];

                    if metadata.field_type[order] == "number" {
                        if let Ok(number) = cell.parse::<f64>() {
                            worksheet.write_number(
                                (row_num + 1).try_into()?,
                                col_index,
                                number,
                                None,
                            )?;
                        } else {
                            worksheet.write_string(
                                (row_num + 1).try_into()?,
                                col_index,
                                cell,
                                None,
                            )?;
                        };
                    } else {
                        worksheet.write_string((row_num + 1).try_into()?, col_index, cell, None)?;
                    }
                    col_index += 1
                }
            }
        }
        workbook.close()?;

        return Ok(());
    }

    pub fn write_postgresql(&mut self) -> Result<()> {
        let postgresql_dir_path = self.output_path.join("postgresql");
        create_dir_all(&postgresql_dir_path)?;

        let mut postgresql_schema =
            File::create(postgresql_dir_path.join("postgresql_schema.sql"))?;
        let mut postgresql_load = File::create(postgresql_dir_path.join("postgresql_load.sql"))?;

        for table_name in self.table_metadata.keys().sorted() {
            let metadata = self.table_metadata.get(table_name).unwrap();
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }
            let table_order = metadata.order.clone();
            write!(
                postgresql_schema,
                "CREATE TABLE \"{ }\"(\n",
                table_name.to_lowercase()
            )?;

            let mut fields = Vec::new();
            for order in table_order {
                if metadata.ignore_fields[order] {
                    continue;
                }
                fields.push(format!(
                    "    \"{}\" {}",
                    metadata.field_titles[order].to_lowercase(),
                    postgresql::to_postgresql_type(&metadata.field_type[order])
                ));
            }
            write!(postgresql_schema, "{}", fields.join(",\n"))?;
            write!(postgresql_schema, "{}", ");\n\n")?;

            let csv_path = canonicalize(
                self.output_path
                    .join("csv")
                    .join(format!("{}.csv", table_name)),
            )?;

            write!(
                postgresql_load,
                "\\copy \"{}\" from '{}' with CSV HEADER\n",
                table_name.to_lowercase(),
                csv_path.to_string_lossy()
            )?;
        }

        Ok(())
    }

    pub fn write_sqlite(&mut self) -> Result<()> {
        let sqlite_dir_path = self.output_path.join("sqlite");
        create_dir_all(&sqlite_dir_path)?;

        let mut sqlite_schema = File::create(sqlite_dir_path.join("sqlite_schema.sql"))?;
        let mut sqlite_load = File::create(sqlite_dir_path.join("sqlite_load.sql"))?;

        write!(sqlite_load, "{}", ".mode csv \n")?;

        for table_name in self.table_metadata.keys().sorted() {
            let metadata = self.table_metadata.get(table_name).unwrap();
            if metadata.rows == 0 || metadata.ignore {
                continue;
            }
            let table_order = metadata.order.clone();
            write!(
                sqlite_schema,
                "CREATE TABLE \"{ }\"(\n",
                table_name.to_lowercase()
            )?;

            let mut fields = Vec::new();
            for order in table_order {
                if metadata.ignore_fields[order] {
                    continue;
                }
                fields.push(format!(
                    "    \"{}\" {}",
                    metadata.field_titles[order].to_lowercase(),
                    postgresql::to_postgresql_type(&metadata.field_type[order])
                ));
            }
            write!(sqlite_schema, "{}", fields.join(",\n"))?;
            write!(sqlite_schema, "{}", ");\n\n")?;

            let csv_path = canonicalize(
                self.output_path
                    .join("csv")
                    .join(format!("{}.csv", table_name)),
            )?;

            write!(
                sqlite_load,
                ".import '{}' {} --skip 1 \n",
                csv_path.to_string_lossy(),
                table_name.to_lowercase()
            )?;
        }

        Ok(())
    }
}

fn value_convert(
    value: Value,
    field_type: &mut Vec<String>,
    num: usize,
    date_re: &Regex,
) -> String {
    //let value_type = output_fields.get("type");
    let value_type = &field_type[num];

    match value {
        Value::String(val) => {
            if value_type != &"text".to_string() {
                if date_re.is_match(&val) {
                    field_type[num] = "date".to_string();
                } else {
                    field_type[num] = "text".to_string();
                }
            }
            val
        }
        Value::Null => {
            if value_type == &"".to_string() {
                field_type[num] = "null".to_string();
            }
            "".to_string()
        }
        Value::Number(number) => {
            if value_type != &"text".to_string() {
                field_type[num] = "number".to_string();
            }
            number.to_string()
        }
        Value::Bool(bool) => {
            if value_type != &"text".to_string() {
                field_type[num] = "boolean".to_string();
            }
            bool.to_string()
        }
        Value::Array(_) => {
            if value_type != &"text".to_string() {
                field_type[num] = "text".to_string();
            }
            format!("{}", value)
        }
        Value::Object(_) => {
            if value_type != &"text".to_string() {
                field_type[num] = "text".to_string();
            }
            format!("{}", value)
        }
    }
}

pub fn flatten_from_jl<R: Read>(input: R, mut flat_files: FlatFiles) -> Result<()> {
    let (value_sender, value_receiver) = bounded(1000);

    let thread = thread::spawn(move || -> Result<()> {
        for value in value_receiver {
            flat_files.process_value(value);
            flat_files.create_rows()?
        }

        flat_files.write_files()?;
        Ok(())
    });

    let stream = Deserializer::from_reader(input).into_iter::<Value>();
    for value_result in stream {
        let value = value_result?;
        value_sender.send(value)?;
    }
    drop(value_sender);

    match thread.join() {
        Ok(result) => {
            if let Err(err) = result {
                return Err(err);
            }
        }
        Err(err) => panic::resume_unwind(err),
    }

    Ok(())
}

pub fn flatten<R: Read>(
    mut input: BufReader<R>,
    mut flat_files: FlatFiles,
    selectors: Vec<Selector>,
) -> Result<()> {
    let (buf_sender, buf_receiver): (Sender<Vec<u8>>, Receiver<Vec<u8>>) = bounded(1000);

    let thread = thread::spawn(move || -> Result<()> {
        for buf in buf_receiver.iter() {
            let value = serde_json::from_slice::<Value>(&buf)?;
            flat_files.process_value(value);
            flat_files.create_rows()?;
        }

        flat_files.write_files()?;
        Ok(())
    });

    let mut jl_writer = JLWriter {
        buf: vec![],
        buf_sender,
    };

    let mut handler = NdJsonHandler::new(&mut jl_writer, selectors);
    let mut parser = Parser::new(&mut handler);

    parser.parse(&mut input)?;

    drop(jl_writer);

    match thread.join() {
        Ok(result) => {
            if let Err(err) = result {
                return Err(err);
            }
        }
        Err(err) => panic::resume_unwind(err),
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::read_to_string;
    use tempfile::TempDir;

    #[test]
    fn full_test() {
        let tmp_dir = TempDir::new().unwrap();
        let output_dir = tmp_dir.path().join("output");
        let output_path = output_dir.to_string_lossy().into_owned();
        let flat_files = FlatFiles::new(
            output_path.clone(),
            true,
            true,
            true,
            "main".to_string(),
            vec![],
            false,
            "".to_string(),
            "".to_string(),
            "_".to_string(),
            "".to_string(),
        )
        .unwrap();
        flatten(
            BufReader::new(File::open("fixtures/basic.json").unwrap()),
            flat_files,
            vec![],
        )
        .unwrap();

        for test_file in [
            "data_package.json",
            "fields.csv",
            "csv/main.csv",
            "csv/platforms.csv",
        ] {
            let expected =
                read_to_string(format!("fixtures/expected_basic/{}", test_file)).unwrap();
            println!("{}", expected);
            let output = read_to_string(format!("{}/{}", output_path.clone(), test_file)).unwrap();
            println!("{}", output);
            assert_eq!(expected, output);
        }
    }

    #[test]
    fn full_test_inline() {
        let tmp_dir = TempDir::new().unwrap();
        let output_dir = tmp_dir.path().join("output");
        let output_path = output_dir.to_string_lossy().into_owned();
        let flat_files = FlatFiles::new(
            output_path.clone(),
            true,
            true,
            true,
            "main".to_string(),
            vec![],
            true,
            "".to_string(),
            "".to_string(),
            "_".to_string(),
            "".to_string(),
        )
        .unwrap();
        flatten(
            BufReader::new(File::open("fixtures/basic.json").unwrap()),
            flat_files,
            vec![],
        )
        .unwrap();

        for test_file in [
            "data_package.json",
            "fields.csv",
            "csv/main.csv",
            "csv/platforms.csv",
        ] {
            let expected =
                read_to_string(format!("fixtures/expected_basic_inline/{}", test_file)).unwrap();
            println!("{}", expected);
            let output = read_to_string(format!("{}/{}", output_path.clone(), test_file)).unwrap();
            println!("{}", output);
            assert!(expected == output);
        }
    }

    #[test]
    fn check_nesting() {
        let myjson = json!({
            "a": "a",
            "c": ["a", "b", "c"],
            "d": {"da": "da", "db": "2005-01-01"},
            "e": [{"ea": 1, "eb": "eb2"},
                  {"ea": 2, "eb": "eb2"}],
        });

        let tmp_dir = TempDir::new().unwrap();

        let mut flat_files = FlatFiles::new(
            tmp_dir.path().join("output").to_string_lossy().into_owned(),
            true,
            true,
            true,
            "main".to_string(),
            vec![],
            false,
            "".to_string(),
            "".to_string(),
            "_".to_string(),
            "".to_string(),
        )
        .unwrap();

        flat_files.process_value(myjson.clone());

        let expected_table_rows = json!({
          "e": [
            {
              "_link": "1.e.0",
              "_link_main": "1",
              "ea": 1,
              "eb": "eb2"
            },
            {
              "_link": "1.e.1",
              "_link_main": "1",
              "ea": 2,
              "eb": "eb2"
            }
          ],
          "main": [
            {
              "_link": "1",
              "_link_main": "1",
              "a": "a",
              "c": "a,b,c",
              "d_da": "da",
              "d_db": "2005-01-01"
            }
          ]
        });

        //println!("{}", serde_json::to_value(&flat_files.table_rows).unwrap());

        assert_eq!(
            expected_table_rows,
            serde_json::to_value(&flat_files.table_rows).unwrap()
        );

        flat_files.create_rows().unwrap();

        let expected_metadata = json!({
          "e": {
            "table_name_with_separator": "e_",
            "field_type": [
              "number",
              "text",
              "text",
              "text",
            ],
            "fields": [
              "ea",
              "eb",
              "_link",
              "_link_main",
            ],
            "field_counts": [
              2,
              2,
              2,
              2
            ],
            "rows": 2,
            "ignore": false,
            "order": [],
            "ignore_fields": [
              false,
              false,
              false,
              false
            ],
            "field_titles": [
              "ea",
              "eb",
              "_link",
              "_link_main",
            ],
          },
          "main": {
            "table_name_with_separator": "",
            "field_type": [
              "text",
              "text",
              "text",
              "date",
              "text",
              "text",
            ],
            "fields": [
              "a",
              "c",
              "d_da",
              "d_db",
              "_link",
              "_link_main",
            ],
            "field_titles": [
              "a",
              "c",
              "d_da",
              "d_db",
              "_link",
              "_link_main",
            ],
            "order": [],
            "field_counts": [
              1,
              1,
              1,
              1,
              1,
              1
            ],
            "rows": 1,
            "ignore": false,
            "ignore_fields": [
              false,
              false,
              false,
              false,
              false,
              false
            ]
          }
        });

        //println!(
        //    "{}",
        //    serde_json::to_string_pretty(&flat_files.table_metadata).unwrap()
        //);
        assert_eq!(
            json!({"e": [],"main": []}),
            serde_json::to_value(&flat_files.table_rows).unwrap()
        );
        assert_eq!(
            expected_metadata,
            serde_json::to_value(&flat_files.table_metadata).unwrap()
        );

        flat_files.process_value(myjson.clone());
        flat_files.create_rows().unwrap();

        let expected_metadata = json!(
        {
          "e": {
            "field_type": [
              "number",
              "text",
              "text",
              "text",
            ],
            "fields": [
              "ea",
              "eb",
              "_link",
              "_link_main",
            ],
            "field_titles": [
              "ea",
              "eb",
              "_link",
              "_link_main",
            ],
            "field_counts": [
              4,
              4,
              4,
              4
            ],
            "rows": 4,
            "ignore": false,
            "order": [],
            "ignore_fields": [
              false,
              false,
              false,
              false
            ],
            "table_name_with_separator": "e_",
          },
          "main": {
            "field_type": [
              "text",
              "text",
              "text",
              "date",
              "text",
              "text",
            ],
            "fields": [
              "a",
              "c",
              "d_da",
              "d_db",
              "_link",
              "_link_main",
            ],
            "field_titles": [
              "a",
              "c",
              "d_da",
              "d_db",
              "_link",
              "_link_main",
            ],
            "field_counts": [
              2,
              2,
              2,
              2,
              2,
              2
            ],
            "rows": 2,
            "ignore": false,
            "order": [],
            "ignore_fields": [
              false,
              false,
              false,
              false,
              false,
              false
            ],
            "table_name_with_separator": "",
          }
        });

        //println!(
        //    "{}",
        //    serde_json::to_string_pretty(&flat_files.table_metadata).unwrap()
        //);
        assert_eq!(
            json!({"e": [],"main": []}),
            serde_json::to_value(&flat_files.table_rows).unwrap()
        );
        assert_eq!(
            expected_metadata,
            serde_json::to_value(&flat_files.table_metadata).unwrap()
        );
    }

    #[test]
    fn test_inline_o2o_when_o2o() {
        let json1 = json!({
            "id": "1",
            "e": [{"ea": 1, "eb": "eb2"}]
        });
        let json2 = json!({
            "id": "2",
            "e": [{"ea": 2, "eb": "eb2"}],
        });

        let tmp_dir = TempDir::new().unwrap();

        let mut flat_files = FlatFiles::new(
            tmp_dir.path().join("output").to_string_lossy().into_owned(),
            true,
            true,
            true,
            "main".to_string(),
            vec![],
            true,
            "".to_string(),
            "".to_string(),
            "_".to_string(),
            "".to_string(),
        )
        .unwrap();

        flat_files.process_value(json1);
        flat_files.process_value(json2);

        flat_files.create_rows().unwrap();
        flat_files.mark_ignore();

        println!(
            "{}",
            serde_json::to_string_pretty(&flat_files.table_metadata).unwrap()
        );
        assert!(flat_files.table_metadata.get("e").unwrap().ignore == true);
        assert!(
            flat_files.table_metadata.get("main").unwrap().ignore_fields
                == vec![false, false, false, false, false]
        );
    }

    #[test]
    fn test_inline_o2o_when_o2m() {
        let json1 = json!({
            "id": "1",
            "e": [{"ea": 1, "eb": "eb2"}]
        });
        let json2 = json!({
            "id": "2",
            "e": [{"ea": 2, "eb": "eb2"}, {"ea": 3, "eb": "eb3"}],
        });

        let tmp_dir = TempDir::new().unwrap();

        let mut flat_files = FlatFiles::new(
            tmp_dir.path().join("output").to_string_lossy().into_owned(),
            true,
            true,
            true,
            "main".to_string(),
            vec![],
            true,
            "".to_string(),
            "".to_string(),
            "_".to_string(),
            "".to_string(),
        )
        .unwrap();

        flat_files.process_value(json1);
        flat_files.process_value(json2);

        flat_files.create_rows().unwrap();
        flat_files.mark_ignore();

        println!(
            "{}",
            serde_json::to_string_pretty(&flat_files.table_metadata).unwrap()
        );
        assert!(flat_files.table_metadata.get("e").unwrap().ignore == false);
        assert!(
            flat_files.table_metadata.get("main").unwrap().ignore_fields
                == vec![false, true, true, false, false]
        );
    }
}
