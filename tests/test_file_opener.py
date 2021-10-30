# from zemailer.patterns.algorithms import FileLoader

# opener = FileLoader('dummy.csv')
# print(opener.emails)
import unittest

from zemailer.utils.loaders import FileLoader


class TestFileLoader(unittest.TestCase):
    def setUp(self):
        self.loader = FileLoader('names.csv')

    def test_can_parse_files(self):
        self.assertIsInstance(self.loader.get_emails, list)
        self.assertIsInstance(self.loader.get_names, list)
        self.assertIsInstance(self.loader.get_surnames, list)
        self.assertEqual(self.loader.number_of_items, 1)


if __name__ == '__main__':
    unittest.main()


