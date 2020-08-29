import functools
import re
import threading
from contextlib import contextmanager
from io import StringIO

import numpy

from zemailer.core.files import FileOpener
from zemailer.core.settings import configuration
from zemailer.mixins.base import UtilitiesMixin


class Names(FileOpener):
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
    pattern = ''
    domain = ''
    separator = ''
    particle = ''

    inmemory_emails = StringIO()

    @functools.cached_property
    def construct_pattern(self):
        regex_patterns = configuration.get('BASE_REGEX_PATTERNS')

        if self.pattern:
            if isinstance(self.pattern, str):
                if self.separator:
                    # If the user provides us with
                    # a separator, we can just use it
                    names = self.pattern.split(self.separator)
                else:
                    has_separator = self._get_separator()
                    if has_separator:
                        # We can split the names once the separator has
                        # been correctly identified ex. ['nom', 'prenom']
                        regex_pattern = self._get_regex_pattern(regex_patterns, 'with_separator', as_string=True)

                        structure = self.pattern.split(has_separator, 1)
                        # Get the index of name and surname in the list
                        # so that we can later replace these items
                        # by the real name and surname
                        index_of_surname = structure.index('surname')
                        index_of_name = structure.index('name')

                        # We have to create a reusable
                        # canvas to prevent changing
                        # the names[...] data on each
                        # iteration
                        template_names = structure.copy()
                        # Replace [name, surname] by the
                        # respective names in the file
                        # according to the index of name
                        # and surname in the array
                        # ex. [name, surname] => [pauline, lopez]
                        emails = []
                        
                        for i in range(self.number_of_items):
                            template_names[index_of_surname] = self.names[i]
                            template_names[index_of_name] = self.surnames[i]

                            final_pattern = has_separator.join(template_names)

                            if self.domain:
                                emails.append(self._append_domain(final_pattern))
                            else:
                                emails.append(final_pattern)
                            template_names = structure

                    for email in emails:
                        self.inmemory_emails.write(email)
                        # self.emails.seek(0)

                    self.dataframe['emails'] = emails
                return self.dataframe
            elif isinstance(self.pattern, (list, tuple)):
                pass

    def _get_separator(self):
        usual_separators = ['.', '-', '_']
        for separator in usual_separators:
            if separator in self.pattern:
                break
        return separator or None

    def _get_regex_pattern(self, patterns, pattern_name, as_string=False):
        """
        Returns the pattern as an array after having regexed it

            name.surname -> [name, surname]
        """
        for base_regex_pattern in patterns[pattern_name]:
            pattern_separator = re.search(base_regex_pattern, self.pattern)
            if pattern_separator:
                break
        if as_string and pattern_separator:
            return pattern_separator.group(1)
        return pattern_separator if pattern_separator else None

    def _append_domain(self, name):
        """
        Append a domain such as `@example.fr`
        """
        return name + '@' + self.domain

    def __enter__(self):
        emails = self.construct_pattern['emails']
        return numpy.asarray(emails)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.inmemory_emails.flush()
        return False




class Test(Names):
    pattern = 'name.surname'
    domain = 'gmail.com'

names = Test('C:\\Users\\Pende\\Documents\\myapps\\zemailer\\data\\dummy.csv')

with names as e:
    print(e)
