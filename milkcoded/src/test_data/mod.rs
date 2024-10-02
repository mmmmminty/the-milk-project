use crate::database::*;
use anyhow::Result;
use chrono::NaiveDate;
use uuid::{uuid, Uuid};

pub mod invariants;
pub mod label;
pub mod validation;

pub const MILK_UUID_A: Uuid = uuid!("65e89efb-f055-472f-a77d-c3ea8fbecc13");
pub const MILK_UUID_B: Uuid = uuid!("0e2d9e02-297c-4135-8eb1-0133190f759c");
pub const MILK_UUID_C: Uuid = uuid!("d494dd8b-9154-4fae-b3e6-92f008e53781");
pub const MILK_UUID_D: Uuid = uuid!("ce2cadf6-0d1d-4e44-a7df-ee0bf6b71280");
pub const MOTHER_ID: i32 = 393;
pub const WRONG_MOTHER_ID: i32 = 999;
pub const BABY_ID: i32 = 482;

pub fn init_test_data() -> Result<MilkDatabaseTest> {
    let mother = Mother {
        id: MOTHER_ID,
        name: String::from("Theresa Jenkins"),
        age: 34,
    };

    let wrong_mother = Mother {
        id: WRONG_MOTHER_ID,
        name: String::from("Melissa Broxton"),
        age: 39,
    };

    let baby = Baby {
        id: BABY_ID,
        name: String::from("Bruno Jenkins"),
        age: 18,
        allergens: Some(String::from("AB3 CC4 RB7")),
    };

    // Valid Milk
    let milk_a = Milk {
        id: MILK_UUID_A,
        volume: 100,
        additives: Some(String::from("GL4")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 18)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 12)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_by: MOTHER_ID,
    };

    // Expired Milk
    let milk_b = Milk {
        id: MILK_UUID_B,
        volume: 150,
        additives: Some(String::from("HG7")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 12)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 6)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_by: MOTHER_ID,
    };

    // Allergenated Milk
    let milk_c = Milk {
        id: MILK_UUID_C,
        volume: 80,
        additives: Some(String::from("JJ6 CC4 RA1")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 18)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 12)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_by: MOTHER_ID,
    };

    // Invalid Mother
    let milk_d = Milk {
        id: MILK_UUID_D,
        volume: 150,
        additives: Some(String::from("")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 18)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 12)
            .unwrap()
            .and_hms_opt(12, 30, 0)
            .unwrap(),
        expressed_by: 999,
    };

    // label::generate_label(milk_a.volume, milk_a.additives.as_ref().unwrap(), &mother.name, &baby.name, Some(&milk_a.id.to_string()))?;
    // label::generate_label(milk_b.volume, milk_b.additives.as_ref().unwrap(), &mother.name, &baby.name, Some(&milk_b.id.to_string()))?;
    // label::generate_label(milk_c.volume, milk_c.additives.as_ref().unwrap(), &mother.name, &baby.name, Some(&milk_c.id.to_string()))?;
    // label::generate_label(milk_d.volume, milk_d.additives.as_ref().unwrap(), &wrong_mother.name, &baby.name, Some(&milk_d.id.to_string()))?;

    Ok(MilkDatabaseTest {
        mothers: vec![mother, wrong_mother],
        babies: vec![baby],
        bottles: vec![milk_a, milk_b, milk_c, milk_d],
        feeds: vec![],
    })
}
