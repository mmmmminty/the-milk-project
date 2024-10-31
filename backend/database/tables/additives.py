from utils.constants import ADDITIVE_DEFAULT_EXPIRY_MODIFIER
from database.database import get_db_cursor
from utils.logger_config import logger

def add_additive_to_milk(additive, amount, milk_id):
    additive = additive.upper()

    with get_db_cursor() as cur:
        try: 
            # This will create a new contains table tied to the same additive if it already exists, otherwise it will create a new additive.
            cur.execute(
                """
                SELECT name FROM Additive WHERE name = %s;
                """,
                (additive,)
            )
            additive_entry = cur.fetchone()

            if not additive_entry:
                create_additive(additive, ADDITIVE_DEFAULT_EXPIRY_MODIFIER)

            # Checking if the additive already exists in the milk, updating the quantity if it does, otherwise creating a new entry
            cur.execute(
                """
                SELECT * FROM Contains WHERE additive_name = %s AND milk_id = %s;
                """,
                (additive, milk_id)
            )
            existing = cur.fetchone()

            if existing:
                existing_amount = existing[2]
                cur.execute(
                    """
                    UPDATE Contains
                    SET amount = %s
                    WHERE additive_name = %s AND milk_id = %s;
                    """,
                    (amount + existing_amount, additive, milk_id)
                )
                logger.info(f"Additive {additive} quantity increased by {amount} in milk {milk_id}")

            else:
                cur.execute(
                    """
                    INSERT INTO Contains (additive_name, milk_id, amount)
                    VALUES (%s, %s, %s);
                    """,
                    (additive, milk_id, amount)
                )
                logger.info(f"{amount} of Additive {additive} added to milk {milk_id}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error adding additive to milk: {e}")
            return False
    
def fetch_additives(milk_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT Additive.name, Contains.amount, Additive.custom_expiry_modifier FROM Contains 
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
                additive_dict = {}
                for additive in additives:
                    additive_dict[additive[0]] = (additive[1], additive[2])

                logger.info(f"Fetched additives for milk {milk_id}")
                return additive_dict
            
        except Exception as e:
            logger.error(f"Error fetching additives: {e}")
            return None
        
def create_additive(additive, expiry_modifier):
    additive = additive.upper()

    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                INSERT INTO Additive (name, custom_expiry_modifier)
                VALUES (%s, %s)
                RETURNING name;
                """,
                (additive, expiry_modifier)
            )
            additive = cur.fetchone()[0]
            logger.info(f"Created additive {additive} with expiry modifier {expiry_modifier}")
            return additive
        
        except Exception as e:
            logger.error(f"Error creating additive: {e}")
            return None
        
def fetch_all_additives():
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT name FROM Additive;
                """
            )
            additives = cur.fetchall()

            if not additives:
                logger.info(f"No additives found")
                return None
            else:
                additive_list = [additive[0] for additive in additives]
                logger.info(f"Fetched all additives")
                return additive_list
            
        except Exception as e:
            logger.error(f"Error fetching additives: {e}")
            return None

def fetch_additive_by_name(additive):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT * FROM Additive WHERE name = %s;
                """,
                (additive,)
            )
            additive = cur.fetchone()

            if not additive:
                logger.info(f"No additive found with name {additive}")
                return None
            else:
                logger.info(f"Fetched additive {additive}")
                additive = dict(zip([desc[0] for desc in cur.description], additive))
                return additive
            
        except Exception as e:
            logger.error(f"Error fetching additive: {e}")
            return None

def update_additive_expiry_modifier(additive, modifier):
    additive = additive.upper()

    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE Additive
                SET custom_expiry_modifier = %s
                WHERE name = %s;
                """,
                (modifier, additive)
            )
            logger.info(f"Updated expiry modifier for additive {additive} to {modifier}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating expiry modifier: {e}")
            return False