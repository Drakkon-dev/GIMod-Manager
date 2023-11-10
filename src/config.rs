use serde::{
    Serialize,
    Deserialize
};
use std::fs::File;
use std::io::{
    prelude::*,
    Error
};

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub app_title: String,
    pub game_name: String,
    pub migoto_path: String,
    pub migoto_executable_name: String,
    pub position_relative: (f32, f32),
    pub size_relative: (f32, f32),
    pub game_proc_name: String,
    pub debug: bool,
}

pub fn get_config(file_path: &str) -> Config {
    //TODO Make a system to check if the settings file exists if not make it

    // Default for when the settings file cant be opened or read
    let mut config: Config = Config { 
        app_title: "GIMod Manager".to_string(),
        game_name: "Genshin Impact".to_string(),
        migoto_path: "Path/to/3DMigoto/Directory".to_string(),
        migoto_executable_name: "3DMigoto Loader.exe".to_string(),
        position_relative: (60.0, 5.0),
        size_relative: (35.0, 90.0),
        game_proc_name: "GenshinImpact.exe".to_string(),
        debug: true
    };

    // Reads the file and sets the parsed values into a struct
    match open_file(file_path) {
        Ok(mut file) => {
            let mut buffer: String = String::new();
            match file.read_to_string(&mut buffer) {
                Ok(_) => {
                    println!("File contents:\n{}", buffer);
                    config = serde_json::from_str(&buffer).unwrap();
                    config
                }
                Err(err) => {
                    eprintln!("Error: Could not read file: {}", err);
                    config
                }
            }
        }
        Err(err) => {
            eprintln!("Error: Could not open settings file: {}", err);
            config
        }
    }

}

fn open_file(file_path: &str) -> Result<File, Error> {
    let file: File = File::open(file_path)?;
    Ok(file)
}