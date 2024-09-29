use anyhow::Result;
use chrono::{NaiveDate, NaiveDateTime};
use log::info;
use uuid::Uuid;

use detection::detect;
use encode::encode;
use test_data::{init_test_data, validate_milk};

mod detection;
mod encode;
mod database;
mod test_data;

fn main() {
    info!("Starting Milk Project");
    let mut test_data = init_test_data();
    info!("Test data initialized");

    loop {
        println!("Enter F to scan for a feed, E to create a new label, or Q to quit");
        println!(">> ");
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();
        let input = input.trim();
        
        match input {
            "F" => {
                let barcode = detect().unwrap();
                let test_date: NaiveDateTime = NaiveDate::from_ymd_opt(2024, 10, 14).unwrap().and_hms_opt(12, 30, 0).unwrap();
                validate_milk(&mut test_data, test_date);              
            },
            "E" => {
                let milk = encode(Uuid::new_v4().to_string(), "tmp".to_string());
                println!("Milk: {:?}", milk);
            },
            "Q" => {
                break;
            },
            _ => {
                println!("Invalid input");
            }
        }
    }
}
