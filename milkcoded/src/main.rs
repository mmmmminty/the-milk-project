use anyhow::Result;
use chrono::{NaiveDate, NaiveDateTime};
use log::{debug, error, info, warn};
use simplelog::*;
use std::fs::File;
use uuid::Uuid;

use detection::{detect, detect_threaded};
use encode::encode;
use test_data::{init_test_data, invariants::Validation, label::generate_label, validation::validate_milk};

mod database;
mod detection;
mod encode;
mod test_data;

fn init_logging() {
    let file = File::create("milk.log").unwrap();
    CombinedLogger::init(vec![
        TermLogger::new(
            LevelFilter::Info,
            Config::default(),
            TerminalMode::Mixed,
            ColorChoice::Auto,
        ),
        WriteLogger::new(LevelFilter::Debug, Config::default(), file),
    ])
    .unwrap();
}

fn main() -> Result<()> {
    init_logging();
    info!("Starting Milk Project");
    let mut test_data = init_test_data();
    info!("Test data initialized");

    info!("Starting main loop");
    loop {
        println!("Enter F to scan for a feed, E to create a new label, or Q to quit");
        print!(">> ");
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();
        let input = input.trim();

        match input {
            "F" => {
                debug!("Input: F");
                let bottle_id = match detect() {
                    Ok(bottle_id) => bottle_id,
                    Err(e) => {
                        warn!("Error detecting bottle: {:?}", e);
                        println!("Error detecting bottle, please try again.");
                        continue;
                    }
                };
                let test_date: NaiveDateTime = NaiveDate::from_ymd_opt(2024, 10, 14)
                    .unwrap()
                    .and_hms_opt(12, 30, 0)
                    .unwrap();

                match validate_milk(&mut test_data, &bottle_id, test_date) {
                    Ok(validation) => match validation {
                        Validation::Valid(baby) => {
                            println!("Milk is all good for {}!", baby);
                        }
                        Validation::Expired(date) => {
                            println!("Milk is expired, expired on {}!", date);
                        }
                        Validation::Allergenated(allergen) => {
                            println!("Baby is allergic to {}, which is contained in the milk!", allergen);
                        }
                        Validation::IncorrectMother(mother) => {
                            println!("This milk is from {}, who is not the mother of the selected baby!", mother);
                        }
                    },
                    Err(e) => {
                        warn!("Error validating milk: {:?}", e);
                        println!("Error validating milk, please try again.");
                        continue;
                    }
                };
            }
            "E" => {
                debug!("Input: E");
                println!("Enter the following fields to create a new label:");
                print!("Volume (mL): ");
                let mut volume = String::new();
                std::io::stdin().read_line(&mut volume).unwrap();
                let volume: i32 = volume.trim().parse().unwrap();

                print!("Additives (Comma-seperated): ");
                let mut additives = String::new();
                std::io::stdin().read_line(&mut additives).unwrap();
                let additives = additives.trim();

                print!("Mother: ");
                let mut mother = String::new();
                std::io::stdin().read_line(&mut mother).unwrap();
                let mother = mother.trim();

                print!("Baby: ");
                let mut baby = String::new();
                std::io::stdin().read_line(&mut baby).unwrap();
                let baby = baby.trim();

                let path = match generate_label(volume, additives, mother, baby) {
                    Ok(path) => path,
                    Err(e) => {
                        warn!("Error generating label: {:?}", e);
                        println!("Error generating label, please try again.");
                        continue;
                    }
                };
            }
            "Q" => {
                debug!("Input: Q");
                break;
            }
            _ => {
                debug!("Input: {}", input);
                println!("Invalid input, please try again.");
            }
        }
    }

    info!("Milk Project Exited");
    Ok(())
}
