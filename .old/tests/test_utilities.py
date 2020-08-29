import unittest

from app.mixins.utils import UtilitiesMixin


class TestPatterns(unittest.TestCase):
    def setUp(self):
        self.utils = UtilitiesMixin()

    def test_flatten_names(self):
        self.assertEqual(self.utils.flatten_name('Eugénie Bouchard'), 'eugenie bouchard')

    def test_normalize_name(self):
        self.assertEqual(self.utils.normalize_name(' Eugénie Bouchard'), 'eugénie bouchard')
        self.assertEqual(self.utils.normalize_name(' Eugénie BOUCHARD'), 'eugénie bouchard')
        self.assertEqual(self.utils.normalize_name(' Eugénie BOUCHARD   '), 'eugénie bouchard')

    def test_splitter(self):
        self.assertListEqual(self.utils.splitter('Eugénie Bouchard'), ['Eugénie', 'Bouchard'])
        self.assertListEqual(self.utils.splitter('Eugénie Pauline-Bouchard'), ['Eugénie', 'Pauline-Bouchard'])

    def test_reverse(self):
        self.assertListEqual(self.utils.reverse('Eugénie Bouchard'), ['Bouchard', 'Eugénie'])

    def test_decompose(self):
        self.assertListEqual(self.utils.decompose('Eugenie Pauline Bouchard'), ['Eugenie', 'Pauline Bouchard'])


if __name__ == "__main__":
    unittest.main()
