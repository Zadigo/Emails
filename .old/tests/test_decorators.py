import unittest

from zemailer.app.patterns.decorators import construct_emails


def names():
    return ['Eugenie Bouchard']

class TestDecorators(unittest.TestCase):
    def test_construct_emails(self):
        construct = construct_emails(names)

        values = construct('.', domains=['gmail.com'])
        self.assertIsInstance(values, list)
        # Test email and "."
        self.assertEqual('eugenie.bouchard@gmail.com', values[0])
        # .. test "-"
        values = construct('-')
        self.assertEqual('eugenie-bouchard@gmail.com', values[0])


if __name__ == "__main__":
    unittest.TestCase()
