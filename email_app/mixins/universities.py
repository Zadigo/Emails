from email_app.patterns.patterns import NamePatterns
from email_app.mixins.fields import EmailField
from email_app.core.settings import Configuration

class Universities(NamePatterns):
    pattern = None

Universities(Configuration()['DUMMY_FILE']).construct_pattern()