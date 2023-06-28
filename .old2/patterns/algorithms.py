import csv
import datetime
import os
import re
import secrets
import threading
from contextlib import contextmanager
from functools import cached_property
from io import FileIO, StringIO

import numpy
from zemailer.patterns.fields import EmailField
from zemailer.settings import configuration
from zemailer.utils.loaders import FileLoader


class NamesMixin(FileLoader):
    """
    Subclass this class and build basic email patterns such 
    as `name.surname`.

    Send a `pattern` as a string, ex. `name.surname`, that
    will be used to construct the email. You can explicitly
    set the separator to be used or rely on the engine 
    presets for that.

    These presets are '.' or '-' or '_'.

    If provided, the `domain` will be appended, otherwise
    the structure will be returned as set by your pattern.

    The `particle` variable can be used to construct emails
    such as `nom.prenom-bba`. It must be a tuple or a list
    containing the string to append and the separator:

        (bba, -)
    """
    pattern = 'surname.name'
    domain = 'gmail'
    separator = None
    particle = 'com'

    inmemory_emails = StringIO()

    def __enter__(self):
        emails = self.construct_pattern['emails']
        return numpy.asarray(emails)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.inmemory_emails.flush()
        return False

    @cached_property
    def build_emails_from_pattern(self):
        separator = self.get_separator()

        # When the separator is not provided,
        # we'll just suppose that the name
        # and the surname are 
        if separator is None:
            separator = ''

        structure = self.pattern.split(separator, 1)
        # Get the position of name and surname in the list
        # so that we can later replace these items
        # by the real name and surname
        index_of_surname = structure.index('surname')
        index_of_name = structure.index('name')

        # We have to create a reusable
        # canvas to prevent changing
        # the names[...] data on each
        # iteration
        template = structure.copy()

        # Replace [name, surname] by the
        # respective names in the file
        # according to the index of name
        # and surname in the array
        # ex. [name, surname] -> [pauline, lopez]
        results = []

        for i in range(self.number_of_items):
            template[index_of_name] = self.get_names[i]
            template[index_of_surname] = self.get_surnames[i]

            mailbox = separator.join(template)
            attrs = [self.normalize_value(mailbox), '@', self.domain, '.', self.particle]
            results.append(EmailField(attrs, pattern=self.pattern))
            template = structure
        return results

    @cached_property
    def build_email_from_regex(self):
        # if not isinstance(self.pattern, list):
        #     pattern = [self.pattern]
        pattern = self.get_regex_pattern()
        if pattern is not None:
            self.pattern = pattern

        return self.build_emails_from_names

    def save(self, filename: str=None):
        structure = [['emails'], self.build_emails_from_names]
        filename = f'{secrets.token_hex(5)}.csv'
        with open(os.path.join(configuration.MEDIA_PATH, filename), mode='w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)

    def finalize_email(self, name):
        """
        Append a domain such as `@example.fr`
        """
        return name + '@' + self.domain

    def get_separator(self):
        """Guesses the separator from the pattern 
        one is not provided"""
        if self.separator is not None:
            return self.separator

        usual_separators = ['.', '-', '_']
        for separator in usual_separators:
            if separator in self.pattern:
                break
        return separator or None

    def get_regex_pattern(self, as_string=False):
        """
        Returns the pattern as an array after having regexed it

        Returns
        -------

            name.surname -> [name, surname]
        """
        for pattern in configuration.BASE_REGEX_PATTERNS:
            pattern_separator = re.search(pattern, self.pattern)

            if pattern_separator:
                break
        
        if as_string and pattern_separator:
            return pattern_separator.group(1)
        
        return pattern_separator if pattern_separator else None
