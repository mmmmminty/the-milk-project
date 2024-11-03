import uuid
import psycopg2
from contextlib import contextmanager

from utils.constants import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SCHEMA_FILE_PATH, TEST_DATA_FILE_PATH
from utils.logger_config import logger

def initdb():
    logger.info("Initializing the database")
    get_db_connection()

    # Create tables
    execute_sql_file(SCHEMA_FILE_PATH)
    logger.info("Tables created")

    # Do other stuff on startup
    execute_sql_file(TEST_DATA_FILE_PATH)
    logger.info("Test data inserted")
    
    # ...

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
        yield conn
    except psycopg2.DatabaseError as e:
        logger.error(f"Database error: {e}")
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            yield cur
            conn.commit()

def execute_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()

    with get_db_cursor() as cur:
        cur.execute(sql_script)

def generate_unique_id(numeric=False):
    if numeric:
        return uuid.uuid4().int >> 96
    return str(uuid.uuid4())
