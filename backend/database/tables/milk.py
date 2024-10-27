import uuid
from database.database import get_db_cursor
from datetime import datetime

from utils.logger_config import logger
from utils.expiry import calculate_expiry_timestamp

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

# Returns a list of all the milk records in the database for a specific baby
def fetch_milks_by_baby(baby_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT Milk.id FROM Milk
                JOIN ExpressedFor ON Milk.id = ExpressedFor.milk_id
                WHERE ExpressedFor.baby_id = %s;
                """,
                (baby_id,)
            )
            milk_data = cur.fetchall()
            milk_list = [milk[0] for milk in milk_data]
            logger.info(f"Fetched milk list for baby {baby_id}: {milk_list}")
            return milk_list
        
        except Exception as e:
            logger.error(f"Error fetching milks for baby {baby_id}: {e}")
            return None

# Returns a list of all the milk records in the database for a specific mother
def fetch_milks_by_mother(mother_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT Milk.id FROM Milk
                JOIN ExpressedBy ON Milk.id = ExpressedBy.milk_id
                WHERE ExpressedBy.mother_id = %s;
                """,
                (mother_id,)
            )
            milk_data = cur.fetchall()
            milk_list = [milk[0] for milk in milk_data]
            logger.info(f"Fetched milk list for mother {mother_id}: {milk_list}")
            return milk_list
        
        except Exception as e:
            logger.error(f"Error fetching milks for mother {mother_id}: {e}")
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
def fetch_unverified_milk(mother_id):
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
            milk_id = str(uuid.uuid4())

            if expiry:
                cur.execute(
                    """
                    INSERT INTO Milk (id, expiry, expressed, frozen, defrosted, modified)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (milk_id, expiry, expressionDate, frozen, False, False)
                )
            else:
                cur.execute(
                    """
                    INSERT INTO Milk (id, expressed, frozen, defrosted, modified)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (milk_id, expressionDate, frozen, False, False)
                )

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

# Updates an existing milk record in the database    
def update_milk(milk_id, expiry=None, expressed=None, frozen=None, defrosted=None, modified=None, verified_by=None):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE Milk
                SET expiry = COALESCE(%s, expiry),
                    expressed = COALESCE(%s, expressed),
                    frozen = COALESCE(%s, frozen),
                    defrosted = COALESCE(%s, defrosted),
                    modified = COALESCE(%s, modified),
                    verified_id = COALESCE(%s, verified_id)
                WHERE id = %s;
                """,
                (expiry, expressed, frozen, defrosted, modified, verified_by, milk_id)
            )

            updated_fields = [field_name for field_name, field_value in zip(
                ['expiry', 'expressed', 'frozen', 'defrosted', 'modified', 'verified_by'],
                [expiry, expressed, frozen, defrosted, modified, verified_by]
            ) if field_value is not None]
            logger.info(f"Updated milk ({milk_id}) fields: {updated_fields}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating milk: {e}")
            return False
        
def delete_milk(milk_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                DELETE FROM Milk
                WHERE id = %s;
                """,
                (milk_id,)
            )
            logger.info(f"Deleted milk: {milk_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting milk: {e}")
            return False