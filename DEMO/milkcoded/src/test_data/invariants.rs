pub enum Validation {
    Valid(String),
    Expired(String),
    Allergenated(String),
    IncorrectMother(String),
}
