import datetime
import json
import os
import secrets
from importlib import import_module

# PATH = 'C:\\Users\\Zadigo\\Documents\\Apps\\zemailer\\app\\core\\settings.json'

PATH = os.path.join(os.getcwd(), 'app', 'core', 'conf', 'settings.json')

def deserialize(func):
    """A decorator that deserializes objects stored
    in the file
    """
    def get(self, name):
        class_name = self.__class__.__name__

        # Check if there is a softlink
        try:
            parent, child = name.split('__', 1)
        except ValueError:
            # We have a simple string
            searched_item = func(self, name)
        else:
            # BUG: TypeError: string indices must be integers
            # We have a parent__child link
            searched_item = func(self, parent)[child]

        # Can only work if dictionnary and
        # that the value is not None
        if isinstance(searched_item, (dict, list)) \
                and searched_item is not None:
            # Converts the timestamp in its
            # original datetime class
            if '__class__' in searched_item:
                tag = searched_item['__class__']
                if tag == 'datetime':
                    datetime_class = datetime.date.fromtimestamp(searched_item['access_date'])
                    searched_item.update({'access_date_class': datetime_class})
        # return "%s([%s])" % (class_name, searched_item)
        return searched_item
    return get

class Settings:
    """Construct a simple dictionnary object with all the settings
    to be used with the application
    """
    email_class = None

    def __init__(self, name_or_path=None, **kwargs):
        if not name_or_path:
            # If no custom path has been provided,
            # default to the custom path
            name_or_path = 'settings.json'
        self.name_or_path = name_or_path
        
        settings_file = self.handler()
        settings_dict = json.load(settings_file)
        # If the file does not have the
        # base structure {_id, settings:{}},
        # raise an error
        if not settings_dict:
            raise ValueError('The file is not valid.')

        # Work on a cache version of the
        # different items in the settings file
        self.cache = settings_dict.copy()
        # Checks that the file has an _id and proceeds
        # to populate the settings section of the
        # file with the default values
        self.check_file_id(settings_dict['_id'], settings_file)

    def __repr__(self):
        return f'{self.__class__.__name__}([{self.cache}])'
    
    def handler(self):
        """A handler for opening the settings file
        """
        try:
            settings_file = open(self.name_or_path, 'r+', encoding='utf-8')
        except FileExistsError:
            raise
        return settings_file

    def check_file_id(self, file_id, handle=None, **kwargs):
        if not file_id:
            # Assume the file is a new version and proceed
            # to populate all the required elements
            self.cache['_id'] = secrets.token_hex(nbytes=25)

            if handle:
                # We need the file handle to proceed to
                # the next section of populating the settings
                populated_settings = self.populate(handle)
                return populated_settings
            else:
                # If none, lets just simply change
                # do the file _id and return
                return
        else:
            # The file has already been created and
            # populated so no need to pursue
            handle.close()
            return

    def populate(self, handle):
        """Populates a settings file with the base parameters
        for running the applications
        """
        base_dir = str(os.getcwd())
        base = {
            'base_path': base_dir,
            'data_path': os.path.join(base_dir, 'app\\data'),
            'email_class': 'zemailer.app.core.sender',
            'settings_class': 'zemailer.app.core.settings'
        }
        self.cache['settings'] = base
        self.cache['last_updated'] = self.serialize_date()
        # Empty the file. For whatever
        # reason, json does not do so
        # beforehand resulting
        # in an erroneous file
        handle.writelines('')
        # Populate the settings file
        # with the extra settings
        json.dump(self.cache, handle, indent=4)
        handle.close()
        return self.cache
    
    def serialize_date(self):
        """Serializes the current date in order to be stored
        in the backup file
        """
        return {'__class__': datetime.__name__, 'access_date': self.current_timestamp()}

    @staticmethod
    def current_timestamp():
        """Get the current date as a timestamp
        """
        return datetime.datetime.now().timestamp()

    @deserialize
    def get(self, name):
        try:
            result = self.cache[name]
        except KeyError:
            result = None
        return result

    @staticmethod
    def load_module(dotted_path=None):
        """This loads some required modules in order
        to complete the file settings
        """
        module = import_module('zemailer.app.core.sender')
        senders = []
        for klass, value in module.__dict__.items():
            if isinstance(value, type):
                items = {klass: value}
                senders.append(items)

# This is the constructed initialized settings
# to use within the app or outside
initialized_settings = Settings(name_or_path=PATH)
