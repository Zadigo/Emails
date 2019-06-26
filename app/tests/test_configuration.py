import unittest
import os
from email_app.core.settings import Configuration

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.config = Configuration()

    def test_root_path(self):
        self.assertEqual(os.path.basename(self.config['BASE_DIR']), 'email_app')

if __name__ == "__main__":
    unittest.main()
