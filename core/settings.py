import collections
import functools
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FOLDERS = [
    os.path.join(BASE_DIR, 'data')
]

DOCUMENTS_PATH = os.path.join(os.environ.get('HOMEDRIVE'), os.environ.get('HOMEPATH'), 'Documents')

EMAILFILES_DIRS = [
    os.path.join(DOCUMENTS_PATH, 'zemailer')
]

class Configuration:
    def __init__(self, **kwargs):
        self.internal_dict = dict()
        # Root path for the project
        self.internal_dict['BASE_DIR'] = BASE_DIR

        # Path to the data folder. Override this
        # for a custom path to use
        self.internal_dict['DATA_FOLDERS'] = DATA_FOLDERS

        self.internal_dict['EMAILFILES_DIRS'] = EMAILFILES_DIRS

        # Set user and password for
        # the SMTP server
        self.internal_dict['USER'] = None

        self.internal_dict['PASSWORD'] = None

        # IMPORTANT: Modify this with care or
        # the EmailPatterns engine will not work
        self.internal_dict['BASE_REGEX_PATTERNS'] = {
            'with_separator': [
                # nom.prenom <-> prenom.nom
                # nom_prenom <-> prenom_nom
                # nom-prenom <-> prenom-nom
                r'^(?:(?:sur)?name)(\S)(?:(?:sur)?name)$',
                # n.prenom <-> p.nom
                # n-prenom <-> p-nom
                # n_prenom <-> p_nom
                r'^(?:n|s)(\S)(?:(?:sur)?name)$'
            ],
            'without_separator': [
                # pnom <-> nprenom
                r'^(n|s)?((?:sur)?name)$',
                # nomp
                r'^(surname)(n)$',
                # nom or prenom
                r'^((?:sur)?name)$',
            ]
        }

        # Extension to use by default
        # when creating a file
        self['OUTPUT_EXTENSION'] = 'csv'

        # Dictionnary for setting the parameters
        # of the servers
        # Extend the servers by appending a dictionnary
        # to it after importing the configuration file
        self['SERVER_CONFIG'] = {
            'default': {
                'name': 'google',
                'host': 'smtp.gmail.com',
                'port': 587,
                'user': self.internal_dict['USER'],
                'password': self.internal_dict['PASSWORD']
            },
            'outlook': {
                'name': 'outlook',
                'host': 'smtp.gmail.com',
                'port': 587,
                'user': self.internal_dict['USER'],
                'password': self.internal_dict['PASSWORD']
            }
        }

        # Name used by default to create
        # a new file
        self.internal_dict['NEW_FILE_PATTERN_NAME'] = '{month}_{year}_{token}'
        
        # This is a test parameter variable
        # created to test the features of the application
        self.internal_dict['DUMMY_FILE'] = os.path.join(self.internal_dict['DATA_FOLDERS'][0], 'dummy.csv')

    def __getitem__(self, name):
        return self.internal_dict[name]
   
    def __setitem__(self, name, value):
        if name == 'EMAILFILES_DIRS':
            self.internal_dict['EMAILFILES_DIRS'].append(value)

        if name == 'DATA_FOLDERS':
            self.internal_dict['DATA_FOLDERS'].append(value)

        self.internal_dict[name] = value

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.internal_dict)})'

    def __str__(self):
        return str(self.internal_dict)

    def has_key(self, key):
        return key in self.internal_dict.keys()

    @functools.lru_cache
    def update(self, key, value):
        self.internal_dict.update({key: value})
        return self.internal_dict

    @functools.cached_property
    def values(self):
        return self.internal_dict.values()

    def get(self, key):
        return self.internal_dict[key]

    def set_credentials(self, user, password, server='default'):
        server_configs = self.internal_dict['SERVER_CONFIG']

        credentials = {'user': user, 'password': password}

        if server == 'global':
            self.internal_dict['USER'] = user
            self.internal_dict['PASSWORD'] = password
        elif server == 'default':
            server_configs[server].update(**credentials)


configuration = Configuration()
