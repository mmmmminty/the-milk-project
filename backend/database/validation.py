from database.tables.milk import fetch_milk
from database.tables.additives import fetch_additives
from database.database import get_db_cursor
from datetime import datetime

from utils.logger_config import logger
from enum import Enum

class ValidationType(Enum):
    OK_VALID_FEED = "Milk is safe for baby"
    ERR_NOT_EXPRESSED_FOR = "Milk was not expressed for this baby"
    ERR_EXPIRED = "Milk has expired"
    ERR_CONTAINS_ALLERGEN = "Milk contains allergens"

def validate(milk_id, baby_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT * FROM ExpressedFor
                WHERE milk_id = %s AND baby_id = %s;
                """,
                (milk_id, baby_id)
            )

            # If the milk is not expressed for the baby, return ERR and search for who this milk entry is for.
            if not cur.fetchone():
                cur.execute(
                    """
                    SELECT baby_id FROM ExpressedFor
                    WHERE milk_id = %s;
                    """,
                    (milk_id,)
                )

                true_baby_id = cur.fetchone()[0]

                logger.info(f"Milk {milk_id} and Baby {baby_id} are not linked, true baby is {true_baby_id}")
                return (ValidationType.ERR_NOT_EXPRESSED_FOR, true_baby_id)
            
            milk = fetch_milk(milk_id)
            additives = fetch_additives(milk_id)

            # If the milk has expired, return ERR and the expiry date.
            if milk["expiry"] < datetime.now():
                logger.info(f"Milk {milk_id} has expired")
                return (ValidationType.ERR_EXPIRED, milk["expiry"])
            
            # TODO: If the milk contains allergens, return ERR and the allergens.
            # if not validate_allergy(baby_id):
            #     logger.info(f"Milk {milk_id} contains allergens: {allergens}")
            #     return (ValidationType.ERR_CONTAINS_ALLERGEN, allergens)
            
            # If the milk is safe for the baby, return OK.
            logger.info(f"Milk {milk_id} is safe for Baby {baby_id}")
            return (ValidationType.OK_VALID_FEED, None)
        
        except Exception as e:
            logger.error(f"Error cross-referencing milk and baby: {e}")
            return None