from database.database import get_db_cursor
from utils.logger_config import logger

def create_nurse(id, name):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                INSERT INTO Nurse (id, name)
                VALUES (%s, %s) RETURNING id;
            ''', (id, name))
            nurse_id = cur.fetchone()[0]
        
            logger.info(f"Created Nurse: {nurse_id}")
            return nurse_id
        
        except Exception as e:
            logger.error(f"Error creating nurse: {e}")
            return None
        
def fetch_nurse(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT * FROM Nurse WHERE id = %s;
            ''', (id,))
            nurse = cur.fetchone()
            columns = [desc[0] for desc in cur.description]
            logger.info(f"Fetched Nurse: {dict(zip(columns, nurse))}")
            return dict(zip(columns, nurse))
        
        except Exception as e:
            logger.error(f"Error fetching nurse: {e}")
            return None
        
def link_nurse_to_baby(nurse_id, baby_id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                INSERT INTO AssignedTo (baby_id, nurse_id)
                VALUES (%s, %s);
            ''', (baby_id, nurse_id))
        
            logger.info(f"Linked Nurse ({nurse_id}) to Baby ({baby_id})")
            return True
        
        except Exception as e:
            logger.error(f"Error linking nurse to baby: {e}")
            return False
        
def delete_nurse(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                DELETE FROM Nurse WHERE id = %s;
            ''', (id,))
        
            logger.info(f"Deleted Nurse: {id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting nurse: {e}")
            return False
        