from email_app.mixins.schools import ESCP
from email_app.core.settings import Configuration

path = Configuration()['DUMMY_FILE']
print(ESCP(path))
