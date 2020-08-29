import csv
from io import FileIO, StringIO

from zemailer.core import errors
from zemailer.core.mixins.utils import UtilitiesMixin


class FileOpener(UtilitiesMixin):
    """
    Open a file that can be used to construct a list of emails
    """

    opened_file = None

    def __init__(self, file_path):
        if not file_path.endswith('csv'):
            raise errors.FileTypeError(('Your file should be a csv file '
                                    'in order to improve file handling'))

        with open(file_path, 'r', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            csv_content = list(csv_file).copy()

        self.headers = csv_content.pop(0)

        for content in csv_content:
            for i in range(len(content)):
                content[i] = self.normalize_name(content[i])
                
        self.csv_content = csv_content
