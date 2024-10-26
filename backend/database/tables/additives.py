from utils.constants import ADDITIVE_DEFAULT_EXPIRY_MODIFIER
from database.database import get_db_cursor
from utils.logger_config import logger

def add_additive_to_milk(additive, milk_id):
    additive = additive.upper()

    with get_db_cursor() as cur:
        try: 
            # This will create a new contains table tied to the same additive if it already exists, otherwise it will create a new additive.
            cur.execute(
                """
                SELECT id FROM Additive WHERE name = %s;
                """,
                (additive,)
            )
            additive_entry = cur.fetchone()

            if not additive_entry:
                cur.execute(
                    """
                    INSERT INTO Additive (name, customExpiry)
                    VALUES (%s, %s)
                    """,
                    (additive, ADDITIVE_DEFAULT_EXPIRY_MODIFIER)
                )

            cur.execute(
                """
                INSERT INTO Contains (additive, milk_id)
                VALUES (%s, %s);
                """,
                (additive, milk_id)
            )
        except Exception as e:
            logger.error(f"Error adding additive to milk: {e}")
            return False
    
    logger.info(f"Additive {additive} added to milk {milk_id}")
    return True

def fetch_additives(milk_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT Additive.name, Contains.amount, Additive.customExpiryModifier FROM Contains 
                JOIN Additive ON Contains.additive_name = Additive.name
                WHERE milk_id = %s;
                """,
                (milk_id,)
            )
            additives = cur.fetchall()

            if not additives:
                logger.info(f"No additives found for milk {milk_id}")
                return None
            else:
                logger.info(f"Fetched additives for milk {milk_id}")
                additive_dict = {additive['name']: (additive['amount'], additive['customExpiryModifier']) for additive in additives}
                return additive_dict
            
        except Exception as e:
            logger.error(f"Error fetching additives: {e}")
            return None