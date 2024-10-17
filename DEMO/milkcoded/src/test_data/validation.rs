use super::*;
use anyhow::{anyhow, Result};
use chrono::NaiveDateTime;
use invariants::Validation;
use log::info;

pub fn validate_milk(
    context: &mut MilkDatabaseTest,
    bottle_id: &String,
    time: NaiveDateTime,
) -> Result<Validation> {
    let milk = context
        .bottles
        .iter()
        .find(|bottle| &bottle.id.to_string() == bottle_id)
        .ok_or(anyhow!("No corresponding milk in database"))?;
    info!("Validating milk: {:?}", milk);

    let baby = context
        .babies
        .iter()
        .find(|baby| baby.id == BABY_ID)
        .ok_or(anyhow!("No corresponding baby in database"))?;

    // First checking that the mother is correct
    if milk.expressed_by != MOTHER_ID {
        info!("Incorrect mother for milk: {}", milk.id);
        return Ok(Validation::IncorrectMother(
            context
                .mothers
                .iter()
                .find(|mother| mother.id == milk.expressed_by)
                .unwrap()
                .name
                .clone(),
        ));
    }

    // Checking if the milk has any allergens
    if baby.allergens.is_some() {
        for allergen in baby.allergens.as_ref().unwrap().split_whitespace() {
            if milk
                .additives
                .as_ref()
                .is_some_and(|additives| additives.contains(allergen))
            {
                info!("Allergenated milk detected: {}", milk.id);
                return Ok(Validation::Allergenated(allergen.to_string()));
            }
        }
    }

    // Checking if the milk is expired
    if milk.expiry < time {
        info!("Expired milk detected: {}", milk.id);
        return Ok(Validation::Expired(milk.expiry.to_string()));
    }

    // If all checks pass, the milk is valid
    info!("Valid milk detected: {}", milk.id);
    Ok(Validation::Valid(
        context
            .babies
            .iter()
            .find(|baby| baby.id == BABY_ID)
            .unwrap()
            .name
            .clone(),
    ))
}
