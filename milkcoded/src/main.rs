use anyhow::Result;
use chrono::{NaiveDate, NaiveDateTime};
use log::*;
use rustyline::{history::FileHistory, Editor};
use simplelog::*;
use std::{fs::File, process::Command};

#[allow(unused_imports)]
use detection::{detect, detect_threaded};
use encode::encode;
use test_data::{
    init_test_data, invariants::Validation, label::generate_label, validation::validate_milk,
};

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
    let mut rl = Editor::<(), FileHistory>::new().unwrap();
    info!("Starting Milk Project");
    let mut test_data = init_test_data()?;
    info!("Test data initialized");
    info!("Starting main loop");
    loop {
        let input =
            rl.readline("Enter F to scan for a feed, E to create a new label, or Q to quit\n>> ");
        let input = match input {
            Ok(input) => input.trim().to_string(),
            Err(_) => {
                warn!("Error reading input");
                println!("Error reading input, please try again.");
                continue;
            }
        };

        match input.as_str() {
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
                    Ok(validation) => {
                        match validation {
                            Validation::Valid(baby) => {
                                println!("Milk is all good for {}!", baby);
                            }
                            Validation::Expired(date) => {
                                println!("Milk is expired, expired on {}!", date);
                            }
                            Validation::Allergenated(allergen) => {
                                println!(
                                    "Baby is allergic to {}, which is contained in the milk!",
                                    allergen
                                );
                            }
                            Validation::IncorrectMother(mother) => {
                                println!("This milk is from {}, who is not the mother of the selected baby!", mother);
                            }
                        }
                    }
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
                let volume: i32 = loop {
                    let input = rl.readline("Volume (mL): ");
                    match input {
                        Ok(input) => match input.trim().parse() {
                            Ok(volume) => break volume,
                            Err(_) => {
                                println!("Invalid input for volume, please enter a number.");
                                continue;
                            }
                        },
                        Err(_) => {
                            warn!("Error reading input for volume");
                            println!("Error reading input, please try again.");
                            continue;
                        }
                    }
                };

                let additives = loop {
                    let input = rl.readline("Additives (Comma-separated): ");
                    match input {
                        Ok(input) => break input.trim().to_string(),
                        Err(_) => {
                            warn!("Error reading input for additives");
                            println!("Error reading input, please try again.");
                            continue;
                        }
                    }
                };

                let mother = loop {
                    let input = rl.readline("Mother: ");
                    match input {
                        Ok(input) => break input.trim().to_string(),
                        Err(_) => {
                            warn!("Error reading input for mother");
                            println!("Error reading input, please try again.");
                            continue;
                        }
                    }
                };

                let baby = loop {
                    let input = rl.readline("Baby: ");
                    match input {
                        Ok(input) => break input.trim().to_string(),
                        Err(_) => {
                            warn!("Error reading input for baby");
                            println!("Error reading input, please try again.");
                            continue;
                        }
                    }
                };

                match generate_label(volume, &additives, &mother, &baby, None) {
                    Ok(label) => {
                        println!("Label generated successfully, saved to {}.", label.code);
                        if let Err(e) = Command::new("open").arg(&label.code).spawn() {
                            warn!("Failed to open label: {:?}", e);
                            println!("Failed to open label, but I promise it's there!");
                        }
                    }
                    Err(e) => {
                        warn!("Error generating label: {:?}", e);
                        println!("Error generating label, please try again.");
                        continue;
                    }
                };

                info!("Label generated successfully");
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
