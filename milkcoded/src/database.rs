use sqlx::FromRow;
use chrono::NaiveDateTime;
use uuid::Uuid;

#[derive(Debug, FromRow)]
pub struct MilkDatabaseTest {
    pub mothers: Vec<Mother>,
    pub babies: Vec<Baby>,
    pub bottles: Vec<Milk>,
    pub feeds: Vec<Feed>,
}

#[derive(Debug, FromRow)]
pub struct Mother {
    pub id: i32,
    pub name: String,
    pub age: i32,
}

#[derive(Debug, FromRow)]
pub struct Baby {
    pub id: i32,
    pub name: String,
    pub age: i32,
    pub allergens: Option<String>,
}

#[derive(Debug, FromRow)]
pub struct IsMotherOf {
    pub mother_id: i32,
    pub baby_id: i32,
}

#[derive(Debug, FromRow)]
pub struct Milk {
    pub id: Uuid,
    pub volume: i32,
    pub additives: Option<String>,
    pub expiry: NaiveDateTime,
    pub expressed_at: NaiveDateTime,
    pub expressed_by: i32,
}

#[derive(Debug, FromRow)]
pub struct Feed {
    pub baby: i32,
    pub milk: i32,
    pub volume: i32,
    pub feed_time: NaiveDateTime,
}