import uuid
from database.database import get_db_cursor
from utils.logger_config import logger

def create_mother_and_baby(mrn, mother_name, baby_name):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                INSERT INTO Mother (id, name)
                VALUES (%s, %s) RETURNING id;
            ''', (mrn, mother_name))
            mother_id = cur.fetchone()[0]
            
            baby_id = str(uuid.uuid4())
            cur.execute('''
                INSERT INTO Baby (id, name)
                VALUES (%s, %s) RETURNING id;
            ''', (baby_id, baby_name))

            cur.execute('''
                INSERT INTO MotherOf (baby_id, mother_id)
                VALUES (%s, %s);
            ''', (baby_id, mrn))

            logger.info(f"Created Mother ({mother_id}) and Baby ({baby_id})")
            return mother_id, baby_id
        
        except Exception as e:
            logger.error(f"Error creating mother/baby: {e}")
            return None

def create_baby(mrn, baby_name):
    with get_db_cursor() as cur:
        try:
            baby_id = str(uuid.uuid4())
            cur.execute('''
                INSERT INTO Baby (id, name)
                VALUES (%s, %s) RETURNING id;
            ''', (baby_id, baby_name))
            baby_id = cur.fetchone()[0]

            cur.execute('''
                INSERT INTO MotherOf (baby_id, mother_id)
                VALUES (%s, %s);
            ''', (baby_id, mrn))

            logger.info(f"Created Baby: {baby_id}")
            return baby_id
        
        except Exception as e:
            logger.error(f"Error creating baby: {e}")
            return None
        
def fetch_mothers():
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Mother;
            ''')
            mothers = cur.fetchall()
            logger.info(f"Fetched mothers")
            return [mother[0] for mother in mothers]
        
        except Exception as e:
            logger.error(f"Error fetching mothers: {e}")
            return None
        
def fetch_mother(mrn):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT * FROM Mother WHERE id = %s;
            ''', (mrn,))
            mother = cur.fetchone()
            columns = [desc[0] for desc in cur.description]
            logger.info(f"Fetched mother: {dict(zip(columns, mother))}")
            return dict(zip(columns, mother))
        
        except Exception as e:
            logger.error(f"Error fetching mother: {e}")
            return None
        
def fetch_all_babies():
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Baby;
            ''')
            babies = cur.fetchall()
            logger.info(f"Fetched babies")
            return [baby[0] for baby in babies]
        
        except Exception as e:
            logger.error(f"Error fetching babies: {e}")
            return None

def fetch_babies(mrn):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Baby
                JOIN MotherOf ON Baby.id = MotherOf.baby_id
                WHERE MotherOf.mother_id = %s;
            ''', (mrn,))
            logger.info(f"Fetched babies for Mother: {mrn}")
            return cur.fetchall()
        
        except Exception as e:
            logger.error(f"Error fetching babies: {e}")
            return None
        
def fetch_baby(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT * FROM Baby WHERE id = %s;
            ''', (id,))
            baby = cur.fetchone()
            columns = [desc[0] for desc in cur.description]
            logger.info(f"Fetched baby: {dict(zip(columns, baby))}")
            return dict(zip(columns, baby))
        
        except Exception as e:
            logger.error(f"Error fetching baby: {e}")
            return None
        
def delete_family(mrn):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Baby
                JOIN MotherOf ON Baby.id = MotherOf.baby_id
                WHERE MotherOf.mother_id = %s;
            ''', (mrn,))
            babies = cur.fetchall()

            for baby in babies:
                baby_id = baby[0]
                cur.execute('''
                    DELETE FROM Baby WHERE id = %s;
                ''', (baby_id,))
            logger.info(f"Deleted Babies for MRN: {mrn}")

            cur.execute('''
                DELETE FROM Mother WHERE id = %s;
            ''', (mrn,))
            
            logger.info(f"Deleted Mother and associated tables: {mrn}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting mother/baby and associated tables: {e}")
            return False
