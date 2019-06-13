import unittest
from email_constructor import EmailPatterns

class TestPatterns(unittest.TestCase):
    def setUp(self):
        # Use the dummy file to do
        # all the testing
        test_path='C:\\Users\\Zadigo\\Documents\\Programs\\EmailsApp\\test.csv'
        self.constructor = EmailPatterns(test_path)

    def test_pattern_dot_one(self):
        self.constructor.pattern = 'nom.prenom'
        self.assertListEqual(self.constructor.construct_pattern()[1],
                ['lopez', 'pierre', 'lopez.pierre'])
    
    def test_pattern_dot_two(self):
        self.constructor.pattern = 'prenom.nom'
        self.assertListEqual(self.constructor.construct_pattern()[1],
                ['lopez', 'pierre', 'pierre.lopez'])

    def test_pattern_no_separator(self):
        self.constructor.pattern = 'pnom'
        self.assertListEqual(self.constructor.construct_pattern()[0],
                ['lopez', 'pierre', 'plopez'])


if __name__ == "__main__":
    unittest.main()
