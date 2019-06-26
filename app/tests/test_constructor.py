import unittest

from email_app.core.settings import Configuration
from email_app.patterns.constructor import NameConstructor


class TestConstructor(unittest.TestCase):
    def setUp(self):
        test_path = Configuration()['DUMMY_FILE']
        self.constructor = NameConstructor(test_path)

    def test_content_is_list(self):
        self.assertEqual(self.constructor.csv_content.__class__, list)

    def test_normalized_names(self):
        self.assertEqual(self.constructor.normalize_name('Pierre'), 'pierre')
        self.assertEqual(self.constructor.normalize_name('Pierre '), 'pierre')
        self.assertEqual(self.constructor.normalize_name(' pierre '), 'pierre')

if __name__ == "__main__":
    unittest.main()
