import unittest
import os

from minecraft_skin_converter import SkinConverter


class Tests(unittest.IsolatedAsyncioTestCase):
    def test_convert_steve_to_alex(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        sc = SkinConverter()
        sc.load_from_file(os.path.join(working_dir, 'images/steve.png'))
        self.assertTrue(sc.is_steve())
        sc.steve_to_alex()
        self.assertFalse(sc.is_steve())

    def test_convert_alex_to_steve(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        sc = SkinConverter()
        sc.load_from_file(os.path.join(working_dir, 'images/alex.png'))
        self.assertFalse(sc.is_steve())
        sc.alex_to_steve()
        self.assertTrue(sc.is_steve())

    def test_convert_half_steve(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        sc = SkinConverter()
        sc.load_from_file(os.path.join(working_dir, 'images/half.png'))
        self.assertTrue(sc.is_half_skin())
        sc.normalize_skin()
        self.assertTrue(sc.is_steve())
        sc.steve_to_alex()
        self.assertFalse(sc.is_steve())

    def test_convert_alex_bytes(self):
        sc = SkinConverter()
        with open('images/alex.png', 'rb') as f:
            sc.load_from_bytes(f.read())
        self.assertFalse(sc.is_steve())
        image_bytes = sc.save_to_bytes()
        sc.load_from_bytes(image_bytes)
        self.assertFalse(sc.is_steve())


if __name__ == '__main__':
    unittest.main()
