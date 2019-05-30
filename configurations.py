import os
from datetime import datetime
from secrets import token_hex

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')

SERVER_CONFIG = [
    {
        'default': {
            'host': '',
            'port': '',
            'user': '',
            'password': ''
        }
    }
]


# These are the base regex patterns
# used in order parse the pattern
# sent by the user to construct an email.

# IMPORTANT: Modify this with care or
# the EmailPatterns engine will not work

BASE_REGEX_PATTERNS = {
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


# Name used by default to create
# a new file

NEW_FILE_PATTERN_NAME = '{month}_{year}_{token}'


# Extension to use by default
# when creating a file

OUTPUT_EXTENSION = 'csv'
