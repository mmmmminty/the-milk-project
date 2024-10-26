import unittest
from backend.database.database import execute_sql_file
from backend.database.milk.milk import create_milk, fetch_milk, fetch_milks

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
        self.assertEqual(milk.get('expiry'), "2021-01-03T00:00:00")
        self.assertEqual(milk.get('expressed'), "2021-01-01T00:00:00")
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('modified'), False)

        # Test relations
        # TODO

    def test_fetch_milks(self):
        setup_test_env(True)
        self.assertEqual(fetch_milks(), [1, 2, 3, 4, 5, 6, 7])

def setup_test_env(defaultData):
    execute_sql_file("backend/database/psql/restart.sql")
    execute_sql_file("backend/database/psql/schema.sql")

    if defaultData:
        execute_sql_file("backend/database/psql/test_data.sql")