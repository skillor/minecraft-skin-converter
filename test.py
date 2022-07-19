import unittest
import os

from minecraft_skin_converter import SkinConverter


class Tests(unittest.IsolatedAsyncioTestCase):
    def test_convert_steve_to_alex(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        sc = SkinConverter()
        sc.load_from_file(os.path.join(working_dir, 'images/steve.png'))
        self.assertTrue(sc.is_steve())
        sc.convert()
        self.assertFalse(sc.is_steve())

    def test_convert_alex_to_steve(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        sc = SkinConverter()
        sc.load_from_file(os.path.join(working_dir, 'images/alex.png'))
        self.assertFalse(sc.is_steve())
        sc.convert()
        self.assertTrue(sc.is_steve())


if __name__ == '__main__':
    unittest.main()
