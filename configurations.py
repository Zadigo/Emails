import os
from datetime import datetime
from secrets import token_hex

class Configuration(dict):
    """This is the base class to configure the
    application. This returns a dictionary object
    that you can use order to update.
    """
    def __init__(self):
        # Root path for the project
        self['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))

        # Path to the data folder
        self['DATA_DIR'] = os.path.join(self['BASE_DIR'], 'data')

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
                    'host': '',
                    'port': '',
                    'user': '',
                    'password': ''
                }
            }
        ]

        # Name used by default to create
        # a new file
        self['NEW_FILE_PATTERN_NAME'] = '{month}_{year}_{token}'