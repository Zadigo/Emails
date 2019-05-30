import unittest
import os
import configurations

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.config = configurations.Configuration()

    def test_root_path(self):
        self.assertEqual(os.path.basename(self.config['BASE_DIR']), 'EmailsApp')


if __name__ == "__main__":
    unittest.main()
