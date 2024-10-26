import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
# from database.milk import milk
from logger_config import logger
import sys

DB_NAME = "milkdb"
DB_USER = "postgres"
DB_PASSWORD = sys.argv[1]
DB_HOST = "localhost"
DB_PORT = "5432"

SCHEMA_FILE_PATH = "database/psql/schema.sql"
TEST_DATA_FILE_PATH = "database/psql/test_data.sql"

def initdb():
    logger.info("Initializing the database")
    get_db_connection()

    # Create tables
    execute_sql_file("database/psql/schema.sql")
    logger.info("Tables created")

    # Do other stuff on startup
    # execute_sql_file("database/psql/test_data.sql")
    # logger.info("Test data inserted")
    
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
