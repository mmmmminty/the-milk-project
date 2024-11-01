# Database constants
import sys

DB_NAME = "milkdb"
DB_USER = "postgres"
DB_PASSWORD = sys.argv[1]
DB_HOST = "localhost"
DB_PORT = "5432"

SCHEMA_FILE_PATH = "database/psql/schema.sql"
TEST_DATA_FILE_PATH = "database/psql/test_data.sql"

# Additive expiry modifier
ADDITIVE_DEFAULT_EXPIRY_MODIFIER = 0

# Backend Server constants
BACKEND_SERVER_PORT = 5010
