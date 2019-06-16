import unittest
from email_app.core.settings import Configuration
from email_app.patterns.constructor import NamePatterns

class TestPatterns(unittest.TestCase):
    def setUp(self):
        # Use the dummy file to do
        # all the testing
        test_path = Configuration()['DUMMY_FILE']
        self.constructor = NamePatterns(test_path)

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
