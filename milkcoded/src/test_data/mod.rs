use crate::database::*;
use chrono::{NaiveDate, NaiveDateTime};
use uuid::{Uuid, uuid};

const MILK_UUID_A: Uuid = uuid!("65e89efb-f055-472f-a77d-c3ea8fbecc13");
const MILK_UUID_B: Uuid = uuid!("0e2d9e02-297c-4135-8eb1-0133190f759c");
const MILK_UUID_C: Uuid = uuid!("d494dd8b-9154-4fae-b3e6-92f008e53781");
const MOTHER_ID: i32 = 393;
const BABY_ID: i32 = 482;

pub fn init_test_data() -> MilkDatabaseTest {
    let mother = Mother {
        id: MOTHER_ID,
        name: String::from("Theresa Jenkins"),
        age: 34,
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
        expiry: NaiveDate::from_ymd_opt(2024, 10, 18).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 12).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_by: MOTHER_ID,
    };

    // Expired Milk
    let milk_b = Milk {
        id: MILK_UUID_B,
        volume: 150,
        additives: Some(String::from("HG7")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 15).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 9).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_by: MOTHER_ID,
    };

    // Allergenated Milk
    let milk_c = Milk {
        id: MILK_UUID_C,
        volume: 80,
        additives: Some(String::from("JJ6 CC4 RA1")),
        expiry: NaiveDate::from_ymd_opt(2024, 10, 18).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_at: NaiveDate::from_ymd_opt(2024, 10, 12).unwrap().and_hms_opt(12, 30, 0).unwrap(),
        expressed_by: MOTHER_ID,
    };

    MilkDatabaseTest {
        mothers: vec![mother],
        babies: vec![baby],
        bottles: vec![milk_a, milk_b, milk_c],
        feeds: vec![],
    }
}

pub fn validate_milk(context: &mut MilkDatabaseTest, time: NaiveDateTime) -> bool {
    let now = chrono::Utc::now().naive_utc();
    // if milk.expiry < now {
    //     return false;
    // }

    // if let Some(allergens) = &milk.additives {
    //     if allergens.contains("AB3") {
    //         return false;
    //     }
    // }

    // true
    todo!()
}