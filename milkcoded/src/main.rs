use anyhow::Result;
use log::info;
use uuid::Uuid;

use detection::detect;
use encode::encode;

mod detection;
mod encode;

fn main() {
    let uuid = Uuid::new_v4();
    encode(uuid.to_string(), "qr.svg".to_string()).unwrap();

    // std::thread::sleep(std::time::Duration::from_secs(3));
    let id = match detect() {
        Ok(id) => id,
        Err(e) => {
            println!("Error: {}", e);
            return;
        }
    };

    println!("Detected: {}", id);
}
