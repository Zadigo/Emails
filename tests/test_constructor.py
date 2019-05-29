import unittest
from email_constructor import EmailConstructor

class TestConstructor(unittest.TestCase):
    def setUp(self):
        test_path='C:\\Users\\Zadigo\\Documents\\Programs\\EmailsApp\\test.csv'
        self.constructor = EmailConstructor(test_path)

    def test_content_is_list(self):
        self.assertEqual(self.constructor.csv_content.__class__, list)

    def test_normalized_names(self):
        self.assertEqual(self.constructor.normalize_names('Pierre'), 'pierre')
        self.assertEqual(self.constructor.normalize_names('Pierre '), 'pierre')
        self.assertEqual(self.constructor.normalize_names(' pierre '), 'pierre')

if __name__ == "__main__":
    unittest.main()
