import unittest
from database.tables.family import create_mother_and_baby, fetch_baby
from tests.database_test import setup_test_env
from utils.qr_code import qr_code_maker
from utils.label_maker import label_maker
from pathlib import Path
from pyzbar.pyzbar import decode
from PIL import Image

class utils_tests(unittest.TestCase):
    def test_create_qrcode(self):
        setup_test_env(False)

        link = "https://www.google.com/"
        file_name1 = "./backend/images/test_qr_code1.png"

        qr_code_maker(link, file_name1)
        self.assertTrue(Path(file_name1).is_file())
        decoded_data = decode(Image.open(file_name1))

        file_name2 = "./backend/images/test_qr_code2.png"
        embedded_image_name = "./backend/images/colours.png"
        qr_code_maker(link, file_name2, embedded_image_name)
        self.assertTrue(Path(file_name2).is_file())
        decoded_data = decode(Image.open(file_name2))

        Path(file_name1).unlink()
        Path(file_name2).unlink()


    def test_create_label(self):
        setup_test_env(False)

        mother_id, baby_id = create_mother_and_baby(1323, 'Japo Braun', 'Mel Braun')
        self.assertIsNotNone(mother_id)
        self.assertIsNotNone(baby_id)

        embedded_image_path = "./backend/images/colours.png"

        label_maker(mother_id)
        file_name = f"./backend/images/a4_label_page_{mother_id}.png"
        self.assertTrue(Path(file_name).is_file())
        Path(file_name).unlink()

        label_maker(mother_id, embedded_image_path = embedded_image_path)
        file_name = f"./backend/images/a4_label_page_{mother_id}.png"
        self.assertTrue(Path(file_name).is_file())
        Path(file_name).unlink()

        baby = fetch_baby(baby_id)
        self.assertEqual(baby.get('id'), baby_id)
        self.assertEqual(baby.get('name'), 'Mel Braun')