from datetime import datetime, timedelta

from backend.logger_config import logger
from backend.database.additives.additives import fetch_additives
from backend.database.milk.milk import fetch_milk

ADDITIVE_DEFAULT_EXPIRY_MODIFIER = 0

# Call this when calculating the expiry timestamp for a milk that has just been created.
def calculate_expiry_timestamp(expressionDate, frozen, defrosted):
    expressionDate = datetime.fromisoformat(expressionDate)
    if (frozen):
        expiry = None
    elif (defrosted): 
        # ASSUMES THIS GETS RUN AS SOON AS MILK IS DEFROSTED
        expiry = datetime.now() + timedelta(hours=24)
    else:
        expiry = expressionDate + timedelta(hours=48)
    return expiry

# Call this when calculating the new expiry timestamp for a milk that has been modified.
def calculate_expiry_timestamp_from_milk(milk_id):
    milk = fetch_milk(milk_id)
    additives = fetch_additives(milk_id)

    if milk:
        expressionDate = milk.get('expressionDate')
        frozen = milk.get('frozen')
        defrosted = milk.get('defrosted')

        expiry = calculate_expiry_timestamp(expressionDate, frozen, defrosted)
        if additives:
            additive_expiry_modifier = additive_expiry_strategy_minimum(additives)
            expiry += timedelta(hours=additive_expiry_modifier)

        logger.info(f"Calculated expiry for milk {milk_id}: {expiry}")
        return expiry
    else:
        logger.info(f"Failed to calculate expiry for milk as it does not exist: {milk_id}")
        return None
    
# This doesn't change according to our current requirements, but it could be modified to do so. 
# Currently just returns the minimum expiry modifier of all additives.
def additive_expiry_strategy_minimum(additives):
    min_modifier = float('inf')
    for additive in additives:
        custom_modifier = additive.get('customExpiryModifier', ADDITIVE_DEFAULT_EXPIRY_MODIFIER)
        if custom_modifier < min_modifier:
            min_modifier = custom_modifier

    return min_modifier
