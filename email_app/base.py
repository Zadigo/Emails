from email_app.mixins.schools import ESCP
from email_app.core.settings import Configuration
from email_app.patterns.patterns import NamePatterns
from email_app.mixins.patterns import PatternsMixin
from email_app.patterns.patterns import BasicNamePatterns
from email_app.mixins.fields import EmailField
# path = Configuration()['DUMMY_FILE']
# print(ESCP(path))
# print(PatternsMixin('Paris Lopez'))

print(ESCP(Configuration()['DUMMY_FILE']))

print(EmailField('test.google@gmail.com', r'^(\w+)\.(\w+)\@(gmail)\.(\w+)'))
