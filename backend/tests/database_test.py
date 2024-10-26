from datetime import datetime
import unittest
from database.database import execute_sql_file
from database.tables.milk import create_milk, fetch_milk, fetch_milks

# WHEN TESTING, YOU MUST CHANGE THE DB_PASSWORD CONSTANT IN THE CONSTANTS.PY FILE TO THE PASSWORD OF YOUR DATABASE

class database_tests(unittest.TestCase):
    def test_fetch_milk(self):
        # Setup
        setup_test_env(True)
        milk_id = create_milk(1, 1, "2021-01-01T00:00:00", False)

        # Make sure the milk was created
        self.assertIsNotNone(milk_id)

        # Test the fetch function
        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('modified'), False)

        # Test relations
        # TODO

    def test_fetch_milks(self):
        setup_test_env(True)
        expected_uuids = [
            'f1ea645f-4efa-4612-889c-0f271548bd83',
            '60253dad-74e8-4ec7-abb7-ec91bc7d39f7',
            'f67ea1e4-4aea-496b-b30b-41a76ba1394f',
            'be7e2418-37d4-42f3-bdb0-3fa3e7c95a84',
            '7301d088-aed2-4810-9412-4389a3965f44',
            '05ce303e-a473-4ef7-906a-ba6471f5a880',
            'c749124d-cbb6-423e-a354-df6cc92786ae'
        ]
        self.assertEqual(fetch_milks(), expected_uuids)

def setup_test_env(defaultData):
    execute_sql_file("backend/database/psql/restart.sql")
    execute_sql_file("backend/database/psql/schema.sql")

    if defaultData:
        execute_sql_file("backend/database/psql/test_data.sql")