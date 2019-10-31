import csv

from app.core.errors import FileTypeError
from app.core.mixins.utils import UtilitiesMixin


class FileOpener(UtilitiesMixin):
    """Open a file that can be used to construct a list of emails.

    The file can be a .csv or .txt type.
    """

    def __init__(self, file_path=None):
        if not file_path.endswith('csv'):
            raise FileTypeError('Your file should be a csv file \
                                    in order to improve file handling.')

        with open(file_path, 'r', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            csv_content = list(csv_file).copy()

        # Pop the headers but keep
        # them for later usage
        self.headers = csv_content.pop(0)

        for content in csv_content:
            for i in range(len(content)):
                content[i] = self.normalize_name(content[i])
                
        # Store the csv's content
        self.csv_content = csv_content
