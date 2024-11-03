import uuid
from database.tables.additives import fetch_additives
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
                columns = [desc[0] for desc in cur.description]
                milk = dict(zip(columns, milk_data))

                additives = fetch_additives(id)
                if additives:
                    milk['additives'] = additives

                logger.info(f"Fetched milk: {milk}")
                return milk
            else:
                logger.info(f"Failed to fetch milk as it does not exist: {milk}")
                return None  
            
        except Exception as e:
            logger.error(f"Error fetching milk: {e}")
            return None

# Returns a list of all the unverified milk for the nurses 
def fetch_unverified_milks(mother_id):
    with get_db_cursor() as cur:
        try:
            cur.execute(
                """
                SELECT Milk.id FROM Milk
                JOIN ExpressedBy ON Milk.id = ExpressedBy.milk_id
                WHERE ExpressedBy.mother_id = %s AND Milk.verified_id IS NULL;
                """,
                (mother_id,)
            )
            milk_data = cur.fetchall()
            milk_list = [milk[0] for milk in milk_data]
            logger.info(f"Fetched unverified milk list for mother {mother_id}: {milk_list}")
            return milk_list
        except Exception as e:
            logger.error(f"Error fetching unverified milks for mother {mother_id}: {e}")
            return None

# Returns a list of all the unverified milk for the nurses 
def fetch_unverified_milks_all(nurse_id):
      with get_db_cursor() as cur:
        try:
            #Check if nurse_id exists
            cur.execute(
                """
                SELECT 1 FROM Nurse WHERE id = %s;
                """,
                (nurse_id,)
            )
            if cur.fetchone() is None:
                logger.info(f"Nurse ID {nurse_id} is invalid.")
                return {"error": "Invalid nurse ID"}

            #Fetch unverified milks from the view
            cur.execute(
                """
                SELECT * FROM unverified_milk;
                """
            )
            milk_data = cur.fetchall()

            milk_list = [milk[0] for milk in milk_data]
            logger.info(f"Fetched unverified milk list for nurse {nurse_id}: {milk_list}")
            return milk_list

        except Exception as e:
            logger.error(f"Error fetching unverified milks for nurse {nurse_id}: {e}")
            return {"error": "Error fetching unverified milk data"}
    
# Creates a new milk record in the database
def create_milk(mother_id, expiry=None, expressed=None, batch=None, volume=None, frozen=False, defrosted=False, fed=False, verified_by=None):
    with get_db_cursor() as cur:
        try:
            milk_id = str(uuid.uuid4())

            if expressed:
                expressed = datetime.fromisoformat(expressed)
                expiry = calculate_expiry_timestamp(expressed, frozen, False)

            cur.execute(
                """
                INSERT INTO Milk (id, expiry, expressed, batch, volume, frozen, defrosted, fed, verified_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (milk_id, expiry, expressed, batch, volume, frozen, defrosted, fed, verified_by)
            )

            # Link the new milk record with the mother
            cur.execute(
                """
                INSERT INTO ExpressedBy (milk_id, mother_id)
                VALUES (%s, %s);
                """,
                (milk_id, mother_id)
            )

            # Find all babies linked to the mother and link the new milk record with them
            cur.execute(
                """
                SELECT baby_id FROM MotherOf WHERE mother_id = %s;
                """,
                (mother_id,)
            )
            for baby_id in cur.fetchall():
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
def update_milk(milk_id, expiry=None, expressed=None, batch=None, volume=None, frozen=False, defrosted=False, fed=False, verified_by=None):
    with get_db_cursor() as cur:
        try:
            if expressed and expiry:
                expressed = datetime.fromisoformat(expressed)
                expiry = datetime.fromisoformat(expiry)
            elif expressed:
                expressed = datetime.fromisoformat(expressed)
                expiry = calculate_expiry_timestamp(expressed, frozen, defrosted)

            cur.execute(
                """
                UPDATE Milk
                SET expiry = COALESCE(%s, expiry),
                    expressed = COALESCE(%s, expressed),
                    batch = COALESCE(%s, batch),
                    volume = COALESCE(%s, volume),
                    frozen = COALESCE(%s, frozen),
                    defrosted = COALESCE(%s, defrosted),
                    fed = COALESCE(%s, fed),
                    verified_id = COALESCE(%s, verified_id)
                WHERE id = %s;
                """,
                (expiry, expressed, batch, volume, frozen, defrosted, fed, verified_by, milk_id)
            )

            updated_fields = [
                field for field in [
                    ('expiry', expiry), ('expressed', expressed), ('batch', batch), ('volume', volume),
                    ('frozen', frozen), ('defrosted', defrosted), ('fed', fed), ('verified_id', verified_by)
                ] if field[1] is not None
            ]
            logger.info(f"Updated milk ({milk_id}) fields: {updated_fields}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating milk: {e}")
            return False
          
# Deletes a milk record and related fields from the database (cascading)
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
