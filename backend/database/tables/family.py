import uuid
from database.database import generate_unique_id, get_db_cursor
from utils.logger_config import logger

def create_mother_and_baby(mother_name, babies):
    with get_db_cursor() as cur:
        try:
            mother_id = generate_unique_id(numeric=True)
            cur.execute('''
                INSERT INTO Mother (id, name)
                VALUES (%s, %s) RETURNING id;
            ''', (mother_id, mother_name))
            mother_id = cur.fetchone()[0]
            
            baby_ids = []
            for id, name in babies:
                cur.execute('''
                    INSERT INTO Baby (id, name)
                    VALUES (%s, %s) RETURNING id;
                ''', (id, name))

                cur.execute('''
                    INSERT INTO MotherOf (baby_id, mother_id)
                    VALUES (%s, %s);
                ''', (id, mother_id))
                baby_ids.append(id)

            logger.info(f"Created Mother ({mother_id}) and Baby(s): {baby_ids}")
            return mother_id, baby_ids
        
        except Exception as e:
            logger.error(f"Error creating mother/baby(s): {e}")
            return None

def create_baby(mother_id, babies):
    with get_db_cursor() as cur:
        try:
            baby_ids = []
            for id, name in babies:
                cur.execute('''
                    INSERT INTO Baby (id, name)
                    VALUES (%s, %s) RETURNING id;
                ''', (id, name))

                cur.execute('''
                    INSERT INTO MotherOf (baby_id, mother_id)
                    VALUES (%s, %s);
                ''', (id, mother_id))
                baby_ids.append(id)

            logger.info(f"Created Mother ({mother_id}) and Baby(s): {baby_ids}")
            return baby_ids
        
        except Exception as e:
            logger.error(f"Error creating babies: {e}")
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
        
def fetch_mother(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT * FROM Mother WHERE id = %s;
            ''', (id,))
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

def fetch_babies(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Baby
                JOIN MotherOf ON Baby.id = MotherOf.baby_id
                WHERE MotherOf.mother_id = %s;
            ''', (id,))
            logger.info(f"Fetched babies for Mother: {id}")
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
        
def delete_family(id):
    with get_db_cursor() as cur:
        try:
            cur.execute('''
                SELECT id FROM Baby
                JOIN MotherOf ON Baby.id = MotherOf.baby_id
                WHERE MotherOf.mother_id = %s;
            ''', (id,))
            babies = cur.fetchall()

            for baby in babies:
                baby_id = baby[0]
                cur.execute('''
                    DELETE FROM Baby WHERE id = %s;
                ''', (baby_id,))
            logger.info(f"Deleted Babies for id: {id}")

            cur.execute('''
                DELETE FROM Mother WHERE id = %s;
            ''', (id,))
            
            logger.info(f"Deleted Mother and associated tables for: {id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting Mother ({id}) and associated tables: {e}")
            return False
