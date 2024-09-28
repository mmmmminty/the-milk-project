use anyhow::Result;
use log::info;

use detection::detect;
use encode::encode;

mod detection;
mod encode;

fn main() {
    let id = match detect() {
        Ok(id) => id,
        Err(e) => {
            println!("Error: {}", e);
            return;
        }
    };

    println!("Detected: {}", id);
    encode(id, "qr.svg".to_string()).unwrap();
}

