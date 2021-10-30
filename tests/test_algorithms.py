# from zemailer.patterns.algorithms import NamesMixin


# names = NamesMixin('names.csv')
# names.save()
import unittest

from zemailer.patterns.algorithms import EmailField, NamesMixin


class TestNamesMixin(unittest.TestCase):
    def setUp(self):
        self.algorithm = NamesMixin('names.csv')

    def test_can_build_names(self):
        results = self.algorithm.build_emails_from_names
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertNotIsInstance(results[0], EmailField)


if __name__ == '__main__':
    unittest.main()
