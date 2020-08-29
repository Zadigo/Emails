import os
import unittest

from zemailer.app.core._settings import Settings, deserialize

PATH = 'C:\\Users\\Zadigo\\Documents\\Apps\\zemailer\\app\\core\\settings.json'

def get(self, name):
    return name

settings = Settings(name_or_path=PATH)
data_path = os.path.join(settings.get('settings__data_path'), 'dummy_settings.json')

class TestSettings(unittest.TestCase):
    def test_populate(self):
        populated_data = settings.populate(open(data_path, 'w', encoding='utf-8'))
        self.assertIsInstance(populated_data, dict)

    def test_handler(self):
        # Check whether we are opening the file
        # correctly
        handle = settings.handler()
        self.assertIsInstance(handle, handle.__class__)
        handle.close()

    def test_cache(self):
        self.assertIsInstance(settings.cache, dict)
        self.assertIsNotNone(settings.cache)
        # Check that we can correctly access an
        # item -; required item
        self.assertTrue('_id' in settings.cache)

class TestDeserializer(unittest.TestCase):
    def test_deserializer(self):
        self.assertTrue(callable(deserialize(get)))
        self.assertIsInstance(deserialize(get)(settings, 'settings__base_path'), str)

if __name__ == "__main__":
    unittest.main()
