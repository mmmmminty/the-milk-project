use anyhow::Result;
use std::fs;
use std::path::{Path, PathBuf};
use uuid::Uuid;

pub struct Label {
    pub volume: i32,
    pub additives: String,
    pub mother: String,
    pub baby: String,
    pub expiry: String,
    pub id: String,
    pub code: PathBuf,
}

pub fn generate_label(volume: i32, additives: &str, mother: &str, baby: &str) -> Result<PathBuf> {
    
}
