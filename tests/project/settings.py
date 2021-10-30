import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')


EMAILFILES_DIRS = []


BASE_REGEX_PATTERNS = []


SERVER_CONFIG = {
    'default': {
        'name': 'google',
        'host': 'smtp.gmail.com',
        'port': 587,
        'user': None,
        'password': None
    }
}


BACKEND = 'Gmail'


BACKENDS = [
    'zemailer.core.Gmail',
    'zemailer.core.Outlook'
]


BUILDERS = [
    'project.builders'
]
