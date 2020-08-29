import csv
import pandas
from io import FileIO, StringIO

from zemailer.core import errors


class FileOpener:
    """
    Open a file that can be used to construct a list of emails

    Parameters
    ----------

        file_path: path of the file to open
    """

    opened_file = None

    def __init__(self, file_path, normalize=False, columns:list=[]):
        if not file_path.endswith('csv'):
            raise errors.FileTypeError(('Your file should be a csv file '
                            'in order to improve file handling'))

        dataframe  = pandas.read_csv(file_path)

        self.dataframe = dataframe
        self.names = []
        self.emails = []

        columns = self.dataframe.columns

        if 'names' in columns:
            self.names = self.dataframe['names']

        if 'surnames' in columns:
            self.surnames = self.dataframe['surnames']          

        if 'emails' in columns:
            self.emails = self.dataframe['emails']

        if 'fullname' not in columns:
            fullnames = []
            for i, name in enumerate(self.dataframe['names']):
                fullnames.append(name + ' ' + self.dataframe['surnames'][i])
            self.dataframe['fullnames'] = fullnames
        
        if normalize and self.emails:
            self.emails = self.emails.apply(self.simple_normalization)

        if normalize and self.names:
            self.names = self.names.apply(self.simple_normalization)

        self.number_of_items = self.dataframe['names'].count()

    @staticmethod
    def simple_normalization(value):
        return value.lower().strip()
