from backend.database.database import get_db_cursor
from backend.logger_config import logger
from datetime import datetime, timedelta

from backend.utils.expiry import calculate_expiry_timestamp

# Returns a list of all the milk records in the database
def fetch_milks():
    with get_db_cursor() as cur:
        try: 
            cur.execute("SELECT id FROM Milk;")
            milk_data = cur.fetchall()
            milk_list = [milk[0] for milk in milk_data]
            logger.info(f"Fetched milk list: {milk_list}")
            return milk_list
        
        except Exception as e:
            logger.error(f"Error fetching milks: {e}")
            return None

# Returns a single milk record from the database
def fetch_milk(id): 
    with get_db_cursor() as cur: 
        try:
            cur.execute("SELECT * FROM Milk WHERE id = %s;", (id,))  # Parameterized query to prevent SQL injection
            milk_data = cur.fetchone()  

            if milk_data:
                columns = [desc[0] for desc in cur.description]  # Get the column names
                milk = dict(zip(columns, milk_data))  # Map column names to values
                logger.info(f"Fetched milk: {milk}")
                return milk
            else:
                logger.info(f"Failed to fetch milk as it does not exist: {milk}")
                return None  
            
        except Exception as e:
            logger.error(f"Error fetching milk: {e}")
            return None

# Returns a list of all the unverified milk for the nurses 
def fetch_unverified_milk():
    with get_db_cursor() as cur:
        try:
            cur.execute("SELECT * FROM unverified_milk;")  
            unverified_data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            unverified_list = [dict(zip(columns, row)) for row in unverified_data]
            logger.info(f"Fetched unverified milk list: {unverified_list}")
            return unverified_list
        
        except Exception as e:
            logger.error(f"Error fetching unverified milk: {e}")
            return None
    
# Creates a new milk record in the database
def create_milk(mother_id, baby_id, expressionDate, frozen):
    with get_db_cursor() as cur:
        try:
            expressionDate = datetime.fromisoformat(expressionDate)
            expiry = calculate_expiry_timestamp(expressionDate, frozen, False)
            uuid = str(uuid.uuid4())

            if expiry:
                cur.execute(
                    """
                    INSERT INTO Milk (id, expiry, expressed, frozen, defrosted, modified)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (uuid, expiry, expressionDate, frozen, False, False)
                )
            else:
                cur.execute(
                    """
                    INSERT INTO Milk (id, expressed, frozen, defrosted, modified)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (uuid, expressionDate, frozen, False, False)
                )
            
            # Get the milk_id of the new milk record
            milk_id = cur.fetchone()[0]

            # Link the new milk record with the mother
            cur.execute(
                """
                INSERT INTO ExpressedBy (milk_id, mother_id)
                VALUES (%s, %s);
                """,
                (milk_id, mother_id)
            )

            # Link the new milk record with the baby
            cur.execute(
                """
                INSERT INTO ExpressedFor (milk_id, baby_id)
                VALUES (%s, %s);
                """,
                (milk_id, baby_id)
            )

            logger.info(f"Created milk: {milk_id}")
            return milk_id
        
        except Exception as e:
            logger.error(f"Error creating milk: {e}")
            return None

# Updates a milk record in the database
def fetch_update_milk(milk_id, verified_by, additives, defrosted): 
    return
