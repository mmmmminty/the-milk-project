from datetime import datetime
import unittest
from database.validation import ValidationType, validate
from database.tables.staff import create_nurse, delete_nurse, fetch_nurse, link_nurse_to_baby
from database.tables.family import create_baby, create_mother_and_baby, delete_family, fetch_all_babies, fetch_babies, fetch_baby, fetch_mother, fetch_mothers
from database.tables.additives import add_additive_to_milk, create_additive, fetch_additive_by_name, fetch_additives, fetch_all_additives, update_additive_expiry_modifier
from database.database import execute_sql_file, generate_unique_id
from database.tables.milk import create_milk, delete_milk, fetch_milk, fetch_milks, fetch_milks_by_baby, fetch_milks_by_mother, fetch_unverified_milks, update_milk

# WHEN TESTING, YOU MUST CHANGE THE DB_PASSWORD CONSTANT IN THE CONSTANTS.PY FILE TO THE PASSWORD OF YOUR DATABASE

class milk_tests(unittest.TestCase):
    def test_create_and_fetch_milk(self):
        # Setup
        setup_test_env(True)
        milk_id = create_milk(1, expressed="2021-01-01T00:00:00")

        # Make sure the milk was created
        self.assertIsNotNone(milk_id)

        # Test the fetch function
        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('volume'), None)
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        self.assertEqual(milk.get('fed'), False)
        self.assertEqual(milk.get('verified_id'), None)

    def test_fetch_milk_with_additives(self):
        setup_test_env(True)
        milk_id = create_milk(1, expressed="2021-01-01T00:00:00")
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

    def test_fetch_unverified_milks(self):
        setup_test_env(True)
        all_milk = fetch_milks_by_mother(1)
        self.assertEqual(all_milk, ['f1ea645f-4efa-4612-889c-0f271548bd83', 'c749124d-cbb6-423e-a354-df6cc92786ae'])

        unverified_milk = fetch_unverified_milks(1)
        self.assertEqual(unverified_milk, ['c749124d-cbb6-423e-a354-df6cc92786ae'])

    def test_fetch_by_mother(self):
        setup_test_env(False)
        mother_id, baby_id = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])

        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id1 = create_milk(mother_id, expressed="2021-01-01T00:00:00")
        milk_id2 = create_milk(mother_id, expressed="2021-01-02T00:00:00")
        milk_id3 = create_milk(mother_id, expressed="2021-01-03T00:00:00")
        milk_id4 = create_milk(mother_id, expressed="2021-01-04T00:00:00")       

        self.assertIsNotNone(milk_id1)
        self.assertIsNotNone(milk_id2)
        self.assertIsNotNone(milk_id3)
        self.assertIsNotNone(milk_id4)

        milks = fetch_milks_by_mother(mother_id)
        self.assertEqual(milks, [milk_id1, milk_id2, milk_id3, milk_id4])

    def test_fetch_by_baby(self):
        setup_test_env(True)
        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        twin_ids = create_baby(mother_id, [(generate_unique_id(numeric=True), 'Poe Braun')])

        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)
        self.assertIsNotNone(twin_ids)

        milk_id1 = create_milk(mother_id, expressed="2021-01-01T00:00:00")
        milk_id2 = create_milk(mother_id, expressed="2021-01-02T00:00:00")
        milk_id3 = create_milk(mother_id, expressed="2021-01-03T00:00:00")
        milk_id4 = create_milk(mother_id, expressed="2021-01-04T00:00:00")   

        self.assertIsNotNone(milk_id1)
        self.assertIsNotNone(milk_id2)
        self.assertIsNotNone(milk_id3)
        self.assertIsNotNone(milk_id4)

        milks = fetch_milks_by_baby(baby_ids[0])
        self.assertEqual(milks, [milk_id1, milk_id2, milk_id3, milk_id4])

    def test_update_milk(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id = create_milk(mother_id, expressed="2021-01-01T00:00:00")
        self.assertIsNotNone(milk_id)

        milk = fetch_milk(milk_id)
        self.assertEqual(milk.get('id'), milk_id)
        self.assertEqual(milk.get('expiry'), datetime.fromisoformat("2021-01-03T00:00:00"))
        self.assertEqual(milk.get('expressed'), datetime.fromisoformat("2021-01-01T00:00:00"))
        self.assertEqual(milk.get('frozen'), False)
        self.assertEqual(milk.get('defrosted'), False)
        
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

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        mother = fetch_mother(mother_id)
        self.assertEqual(mother.get('id'), mother_id)
        self.assertEqual(mother.get('name'), 'Japo Braun')

        baby = fetch_baby(baby_ids[0])
        self.assertEqual(baby.get('id'), baby_ids[0])
        self.assertEqual(baby.get('name'), 'Mel Braun')

    def test_create_babies_on_mother(self):
        setup_test_env(False)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun'), (generate_unique_id(numeric=True), 'Poe Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        baby = fetch_baby(baby_ids[0])
        self.assertEqual(baby.get('name'), 'Mel Braun')
        twin = fetch_baby(baby_ids[1])
        self.assertEqual(twin.get('name'), 'Poe Braun')

        self.assertEqual(fetch_babies(mother_id), [(baby_ids[0],), (baby_ids[1],)])

    def test_create_many_babies_on_mother(self):
        setup_test_env(False)
        mother_id, baby_id = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        twin_ids = create_baby(mother_id, [(generate_unique_id(numeric=True), 'Poe Braun'), (generate_unique_id(numeric=True), 'Finn Braun'), (generate_unique_id(numeric=True), 'Jasper Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)
        self.assertIsNotNone(twin_ids)

        baby = fetch_baby(baby_id[0])
        self.assertEqual(baby.get('name'), 'Mel Braun')

        for twin_id in twin_ids:
            twin = fetch_baby(twin_id)
            self.assertIsNotNone(twin)
            self.assertTrue((twin_id,) in fetch_babies(mother_id))


    def test_fetch_babies(self):
        setup_test_env(False)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        twin_ids = create_baby(mother_id, [(generate_unique_id(numeric=True), 'Poe Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)
        self.assertIsNotNone(twin_ids)

        self.assertEqual(fetch_babies(mother_id), [(baby_ids[0],), (twin_ids[0],)])

    def test_delete_family(self):
        setup_test_env(False)

        mother_id1, baby_ids1 = create_mother_and_baby('Sol Hicko', [(generate_unique_id(numeric=True), 'Bob Hicko')])
        mother_id2, baby_ids2 = create_mother_and_baby('Fiona Spades', [(generate_unique_id(numeric=True), 'Jack Spades')])

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        twin_ids = create_baby(mother_id, [(generate_unique_id(numeric=True), 'Poe Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)
        self.assertIsNotNone(twin_ids)

        self.assertTrue(delete_family(mother_id))
        self.assertIsNone(fetch_mother(mother_id))
        self.assertIsNone(fetch_baby(baby_ids[0]))
        self.assertIsNone(fetch_baby(twin_ids[0]))

        expected_mothers = [mother_id1, mother_id2]
        self.assertEqual(fetch_mothers(), expected_mothers)

        expected_babies = [baby_ids1[0], baby_ids2[0]]
        self.assertEqual(fetch_all_babies(), expected_babies)

class staff_tests(unittest.TestCase):
    def test_create_nurse(self):
        setup_test_env(False)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertTrue(nurse_id)

        nurse = fetch_nurse(nurse_id)
        self.assertEqual(nurse.get('id'), 1342)
        self.assertEqual(nurse.get('name'), 'Joy Mackenzie')

    def test_link_nurse_to_baby(self):
        setup_test_env(False)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        self.assertTrue(link_nurse_to_baby(nurse_id, baby_ids[0]))
    
    def test_delete_nurse(self):
        setup_test_env(False)

        nurse_id = create_nurse(1342, 'Joy Mackenzie')
        self.assertIsNotNone(nurse_id)

        self.assertTrue(delete_nurse(1342))
        self.assertIsNone(fetch_nurse(1342))

    def test_delete_nurse_linked_to_milk(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        milk_id = create_milk(mother_id, expressed="2021-01-01T00:00:00")
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

class validation_tests(unittest.TestCase):
    def test_validate_ok(self):
        setup_test_env(True)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        milk_id = create_milk(mother_id, expressed="2025-01-01T00:00:00")
        self.assertIsNotNone(milk_id)

        # Test the milk is safe for baby
        validation = validate(milk_id, baby_ids[0])
        self.assertEqual(validation[0], ValidationType.OK_VALID_FEED)

    def test_validate_not_expressed_for(self):
        setup_test_env(True)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        milk_id = create_milk(mother_id, expressed="2025-01-01T00:00:00")
        self.assertIsNotNone(milk_id)

        # Test the milk is not expressed for the baby
        validation = validate(milk_id, 4)
        self.assertEqual(validation[0], ValidationType.ERR_NOT_EXPRESSED_FOR)

    def test_validate_expired(self):
        setup_test_env(True)

        mother_id, baby_ids = create_mother_and_baby('Japo Braun', [(generate_unique_id(numeric=True), 'Mel Braun')])
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_ids)

        milk_id = create_milk(mother_id, expressed="2021-01-01T00:00:00")
        self.assertIsNotNone(milk_id)

        # Test the milk has expired
        validation = validate(milk_id, baby_ids[0])
        self.assertEqual(validation[0], ValidationType.ERR_EXPIRED)

# NOTE: Remove 'backend/' from the path when running coverage
def setup_test_env(defaultData):
    execute_sql_file("./backend/database/psql/restart.sql")
    execute_sql_file("./backend/database/psql/schema.sql")

    if defaultData:
        execute_sql_file("./backend/database/psql/test_data.sql")
