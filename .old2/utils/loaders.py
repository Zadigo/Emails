import csv
import os
from functools import cached_property
from zemailer.core.exceptions import FileTypeError
from zemailer.patterns.mixins import UtilitiesMixin
from zemailer.settings import configuration


def load_file(file_name: str):
    """Gets and returns the data of a given file within
    the `media` folder of the project"""
    if not file_name.endswith('csv'):
        raise FileTypeError('Your file should be a csv file in order to improve file handling')
    full_path = os.path.join(configuration.MEDIA_PATH, file_name)
    with open(full_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        list_copy = list(reader).copy()
    return list_copy


class FileLoader(UtilitiesMixin):
    """
    Parametes
    ---------

        - file_path ([type]): [description]
        - normalize (bool, optional): [description]. Defaults to False.
        - columns (list, optional): [description]. Defaults to [].
        - has_headers (bool, optional): [description]. Defaults to True.
    """

    def __init__(self, file_name: str, columns: list = [], has_headers: bool = True):
        self._data = load_file(file_name)

        self.columns = []
        if has_headers:
            self.columns = self._data.pop(0)

        # self.names = []
        # self.surnames = []
        # self.emails = []


        # Try to collect the default fields
        # from the CSV file
        # default_columns = ['names', 'surnames', 'emails']
        # for column in default_columns:
        #     values = self.collect_column_values(column, self.columns, self._data)
        #     setattr(self, column, values)

        # if 'names' in self.columns:
        #     emails = list(self.collect_column_values('names', self.columns, self._data))
        #     self.emails = self.multi_normalization(emails)

        # if 'emails' in self.columns:
        #     emails = list(self.collect_column_values('emails', self.columns, self._data))
        #     self.emails = self.multi_normalization(emails)

        # columns = self.dataframe.columns

        # if 'names' in columns:
        #     self.names = self.dataframe['names']

        # if 'surnames' in columns:
        #     self.surnames = self.dataframe['surnames']

        # if 'emails' in columns:
        #     self.emails = self.dataframe['emails']

        # if 'fullname' not in columns:
        #     fullnames = []
        #     for i, name in enumerate(self.dataframe['names']):
        #         fullnames.append(name + ' ' + self.dataframe['surnames'][i])
        #     self.dataframe['fullnames'] = fullnames

        # if normalize and self.emails:
        #     self.emails = self.emails.apply(self.simple_normalization)

        # if normalize and self.names:
        #     self.names = self.names.apply(self.simple_normalization)

        # self.number_of_items = self.dataframe['names'].count()

        # if normalize and self.emails:
        #     self.emails = list(map(lambda x: self.simple_normalization(x), self.emails))

    def __repr__(self):
        return f"{self.__class__.__name__}(count={len(self.get_names)})"

    @staticmethod
    def collect_column_values(column_name: str, columns: list, data: list):
        """Return all the values from a specific columns"""
        if column_name not in columns:
            return []
            
        position = columns.index(column_name)
        return list(map(lambda x: x[position], data))

    @cached_property
    def get_emails(self):
        return self.collect_column_values('emails', self.columns, self._data)

    @cached_property
    def get_names(self):
        return self.collect_column_values('names', self.columns, self._data)

    @cached_property
    def get_surnames(self):
        return self.collect_column_values('surnames', self.columns, self._data)

    @cached_property
    def number_of_items(self):
        if self.get_names:
            return len(self.get_names)
        if self.get_surnames:
            return len(self.get_surnames)
        return len(self.get_emails)

    def get_column_index(self, name: str):
        return self.columns.index(name)
