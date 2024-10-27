from datetime import datetime
import unittest
import uuid
from database.tables.staff import create_nurse, delete_nurse, fetch_nurse, link_nurse_to_baby
from database.tables.family import create_baby, create_mother_and_baby, delete_family, fetch_all_babies, fetch_babies, fetch_baby, fetch_mother, fetch_mothers
from database.tables.additives import add_additive_to_milk, create_additive, fetch_additive_by_name, fetch_additives, fetch_all_additives, update_additive_expiry_modifier
from database.database import execute_sql_file
from database.tables.milk import create_milk, delete_milk, fetch_milk, fetch_milks, fetch_milks_by_baby, fetch_milks_by_mother, update_milk

# WHEN TESTING, YOU MUST CHANGE THE DB_PASSWORD CONSTANT IN THE CONSTANTS.PY FILE TO THE PASSWORD OF YOUR DATABASE

class milk_tests(unittest.TestCase):
    def test_create_and_fetch_milk(self):
        # Setup
        setup_test_env(True)
        milk_id = create_milk(1, '7e66e1bd-22d3-45f1-9d87-d32fa40dc36e', "2021-01-01T00:00:00", False)

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

    def test_fetch_milk_with_additives(self):
        setup_test_env(True)
        milk_id = create_milk(1, '7e66e1bd-22d3-45f1-9d87-d32fa40dc36e', "2021-01-01T00:00:00", False)
        self.assertIsNotNone(milk_id)

        add_additive_to_milk('Vitamin D', 100, milk_id)

        milk = fetch_milk(milk_id)

        expected_additives = {
            'VITAMIN D': (100, 0)
        }
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('modified'), False)
        self.assertEqual(milk.get('verified_id'), None)
        self.assertEqual(milk.get('additives'), expected_additives)

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

    def test_fetch_by_mother(self):
        setup_test_env(False)
        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')

        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id1 = create_milk(mother_id, baby_id, "2021-01-01T00:00:00", False)
        milk_id2 = create_milk(mother_id, baby_id, "2021-01-02T00:00:00", False)
        milk_id3 = create_milk(mother_id, baby_id, "2021-01-03T00:00:00", False)
        milk_id4 = create_milk(mother_id, baby_id, "2021-01-04T00:00:00", False)       

        self.assertIsNotNone(milk_id1)
        self.assertIsNotNone(milk_id2)
        self.assertIsNotNone(milk_id3)
        self.assertIsNotNone(milk_id4)

        milks = fetch_milks_by_mother(mother_id)
        self.assertEqual(milks, [milk_id1, milk_id2, milk_id3, milk_id4])

    def test_fetch_by_baby(self):
        setup_test_env(False)
        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        twin_id = create_baby(mother_id, 'Poe Braun')

        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)
        self.assertIsNotNone(twin_id)

        milk_id1 = create_milk(mother_id, baby_id, "2021-01-01T00:00:00", False)
        milk_id2 = create_milk(mother_id, baby_id, "2021-01-02T00:00:00", False)
        milk_id3 = create_milk(mother_id, twin_id, "2021-01-03T00:00:00", False)
        milk_id4 = create_milk(mother_id, twin_id, "2021-01-04T00:00:00", False)       

        self.assertIsNotNone(milk_id1)
        self.assertIsNotNone(milk_id2)
        self.assertIsNotNone(milk_id3)
        self.assertIsNotNone(milk_id4)

        milks = fetch_milks_by_baby(baby_id)
        self.assertEqual(milks, [milk_id1, milk_id2])

    def test_update_milk(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id = create_milk(mother_id, baby_id, "2021-01-01T00:00:00", False)
        self.assertIsNotNone(milk_id)

        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('modified'), False)
        self.assertEqual(milk.get('verified_id'), None)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        self.assertTrue(update_milk(milk_id, verified_by=nurse_id))
        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('modified'), False)
        self.assertEqual(milk.get('verified_id'), nurse_id)

    def test_delete_milk(self):
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

        self.assertTrue(delete_milk('f1ea645f-4efa-4612-889c-0f271548bd83'))
        expected_uuids = [
            '60253dad-74e8-4ec7-abb7-ec91bc7d39f7',
            'f67ea1e4-4aea-496b-b30b-41a76ba1394f',
            'be7e2418-37d4-42f3-bdb0-3fa3e7c95a84',
            '7301d088-aed2-4810-9412-4389a3965f44',
            '05ce303e-a473-4ef7-906a-ba6471f5a880',
            'c749124d-cbb6-423e-a354-df6cc92786ae'
        ]
        self.assertEqual(fetch_milks(), expected_uuids)        
        
class additive_tests(unittest.TestCase):
    def test_fetch_addititves(self):
        setup_test_env(True)

        milk = fetch_milk('f1ea645f-4efa-4612-889c-0f271548bd83')
        self.assertIsNotNone(milk)

        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (100, 0)
        }
        self.assertEqual(additives, expected_additives)

    def test_create_additives(self):
        setup_test_env(True)

        milk = fetch_milk('f1ea645f-4efa-4612-889c-0f271548bd83')
        self.assertIsNotNone(milk)

        # Add a new additive
        self.assertTrue(add_additive_to_milk('Vitamin C', 300, milk.get('id')))

        # Fetch the additives
        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (100, 0),
            'VITAMIN C': (300, 0)
        }
        self.assertEqual(additives, expected_additives)
    
    def test_increase_quantity(self):     
        setup_test_env(True)

        milk = fetch_milk('f1ea645f-4efa-4612-889c-0f271548bd83')
        self.assertIsNotNone(milk)

        # Fetch the additives
        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (100, 0)
        }
        self.assertEqual(additives, expected_additives)

        # Add more of the same additive
        self.assertTrue(add_additive_to_milk('Vitamin D', 200, milk.get('id')))

        # Fetch the additives
        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (300, 0)
        }
        self.assertEqual(additives, expected_additives)
    
    def test_increase_expiry_modifier(self):
        setup_test_env(True)

        milk = fetch_milk('f1ea645f-4efa-4612-889c-0f271548bd83')
        self.assertIsNotNone(milk)

        # Fetch the additives
        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (100, 0)
        }
        self.assertEqual(additives, expected_additives)

        self.assertTrue(update_additive_expiry_modifier('Vitamin D', 24))

        # Fetch the additives
        additives = fetch_additives(milk.get('id'))
        expected_additives = {
            'VITAMIN D': (100, 24)
        }
        self.assertEqual(additives, expected_additives)

    def test_create_and_fetch_additives(self):
        setup_test_env(False)

        additives = fetch_all_additives()
        self.assertIsNone(additives)

        additive = create_additive('viTAmIn a', 48)
        self.assertEqual(additive, 'VITAMIN A')
        
        create_additive('viTAmIn e', 48)
        create_additive('viTAmIn d', 48)

        self.assertIsNone(create_additive('viTAmIn a', 24))
        additives = fetch_all_additives()
        expected_additives = ['VITAMIN A', 'VITAMIN E', 'VITAMIN D']
        self.assertEqual(additives, expected_additives)
    
    def test_fetch_additive_by_name(self):
        setup_test_env(False)

        additive = create_additive('viTAmIn a', 48)
        self.assertEqual(additive, 'VITAMIN A')

        additive = fetch_additive_by_name(additive)
        expected = {
            'name': 'VITAMIN A',
            'custom_expiry_modifier': 48
        }
        self.assertEqual(additive, expected)

class family_tests(unittest.TestCase):
    def test_create_mother_and_baby(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        mother = fetch_mother(mother_id)
        self.assertEqual(mother.get('id'), mother_id)
        self.assertEqual(mother.get('name'), 'Japo Braun')

        baby = fetch_baby(baby_id)
        self.assertEqual(baby.get('id'), baby_id)
        self.assertEqual(baby.get('name'), 'Mel Braun')

    def test_create_baby_on_mother(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        twin_id = create_baby(mother_id, 'Poe Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)
        self.assertIsNotNone(twin_id)

        baby = fetch_baby(baby_id)
        self.assertEqual(baby.get('name'), 'Mel Braun')
        twin = fetch_baby(twin_id)
        self.assertEqual(twin.get('name'), 'Poe Braun')

        self.assertEqual(fetch_babies(mother_id), [(baby_id,), (twin_id,)])

    def test_fetch_babies(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        twin_id = create_baby(mother_id, 'Poe Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)
        self.assertIsNotNone(twin_id)

        self.assertEqual(fetch_babies(mother_id), [(baby_id,), (twin_id,)])

    def test_delete_family(self):
        setup_test_env(False)

        _, baby_id1 = create_mother_and_baby(5323, 'Sol Hicko', 'Bob Hicko')
        _, baby_id2 = create_mother_and_baby(6432, 'Fiona Spades', 'Jack Spades')

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        twin_id = create_baby(mother_id, 'Poe Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)
        self.assertIsNotNone(twin_id)

        self.assertTrue(delete_family(mother_id))
        self.assertIsNone(fetch_mother(mother_id))
        self.assertIsNone(fetch_baby(baby_id))
        self.assertIsNone(fetch_baby(twin_id))

        expected_mothers = [5323, 6432]
        self.assertEqual(fetch_mothers(), expected_mothers)

        expected_babies = [baby_id1, baby_id2]
        self.assertEqual(fetch_all_babies(), expected_babies)

class staff_tests(unittest.TestCase):
    def test_create_nurse(self):
        setup_test_env(False)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        nurse = fetch_nurse(nurse_id)
        self.assertEqual(nurse.get('id'), 1342)
        self.assertEqual(nurse.get('name'), 'Joy Mackenzie')

    def test_link_nurse_to_baby(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        self.assertTrue(link_nurse_to_baby(nurse_id, baby_id))
    
    def test_delete_nurse(self):
        setup_test_env(False)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        self.assertTrue(delete_nurse(1342))
        self.assertIsNone(fetch_nurse(1342))

    def test_delete_nurse_linked_to_milk(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id = create_milk(mother_id, baby_id, "2021-01-01T00:00:00", False)
        self.assertIsNotNone(milk_id)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)
        self.assertTrue(update_milk(milk_id, verified_by=nurse_id))
        
        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('verified_id'), nurse_id)

        self.assertTrue(delete_nurse(1342))
        self.assertIsNone(fetch_nurse(1342))

        milk = fetch_milk(milk_id)
        self.assertIsNone(milk.get('verified_id'))

def setup_test_env(defaultData):
    execute_sql_file("backend/database/psql/restart.sql")
    execute_sql_file("backend/database/psql/schema.sql")

    if defaultData:
        execute_sql_file("backend/database/psql/test_data.sql")