"""Core configuration for the application
"""

import os
from datetime import datetime
from secrets import token_hex
from email_app.core.errors import ImproperlyConfiguredError

class Configuration(dict):
    """This is the base class to configure the
    application. This returns a dictionary object
    that you can use order to update.
    """
    def __init__(self):
        # Root path for the project
        self['BASE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Path to the data folder
        self['DATA_DIR'] = os.path.join(self['BASE_DIR'], 'data')
        
        # Set user and password for
        # the SMTP server
        self['USER'] = None
        
        self['PASSWORD'] = None

        # These are the base regex patterns
        # used in order parse the pattern
        # sent by the user to construct an email.

        # IMPORTANT: Modify this with care or
        # the EmailPatterns engine will not work
        self['BASE_REGEX_PATTERNS'] = {
            'with_separator': [
                # nom.prenom <-> prenom.nom
                # nom_prenom <-> prenom_nom
                # nom-prenom <-> prenom-nom
                r'^(?:(?:pre)?nom)(\S)(?:(?:pre)?nom)$',
                # n.prenom <-> p.nom
                # n-prenom <-> p-nom
                # n_prenom <-> p_nom
                r'^(?:n|p)(\S)(?:(?:pre)?nom)$'
            ],
            'without_separator': [
                # pnom <-> nprenom
                r'^(p|n)?((?:pre)?nom)$',
                # nomp
                r'^(nom)(p)$',
                # nom or prenom
                r'^((?:pre)?nom)$',
            ]
        }

        # Extension to use by default
        # when creating a file
        self['OUTPUT_EXTENSION'] = 'csv'

        self['SERVER_CONFIG'] = [
            {
                'default': {
                    'host': 'smtp.gmail.com',
                    'port': 597,
                    'user': self.get('USER'),
                    'password': self.get('PASSWORD')
                }
            }
        ]

        # Name used by default to create
        # a new file
        self['NEW_FILE_PATTERN_NAME'] = '{month}_{year}_{token}'

        # This is a test parameter variable
        # created to test the features of the application
        self['DUMMY_FILE'] = os.path.join(self['DATA_DIR'], 'dummy.csv')

    def __getitem__(self, obj):
        # Make sure user and password are set
        if obj == 'USER' or obj == 'PASSWORD':
            if self.get(obj) is None:
                raise ImproperlyConfiguredError('The %s setting was not configured properly.'
                    ' Did you forget to set it before calling %s()?' % (obj, self.__class__.__name__))
        return super().__getitem__(obj)
