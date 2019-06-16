import csv
import re
import os
from email_app.core.errors import NoPatternError
from email_app.mixins.utils import UtilitiesMixin
from email_app.core.settings import Configuration

class FileOpener(UtilitiesMixin):
    """Open a file to construct a list of emails.
    The file path can be a url or a path on your
    computer.
    """
    config = Configuration()

    def __init__(self, file_path=None):
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

class NameConstructor(FileOpener):
    """Subclass this class and build basic email
    patterns such as `name.surname`.

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
    ('bba', '-').
    """
    pattern = ''
    domain = ''
    separator = ''
    particle = ''

    def construct_pattern(self):
        # self.config['BASE_REGEX_PATTERNS']
        base_regex_patterns = {
            'with_separator': [
                # nom.prenom // prenom.nom
                # nom_prenom // prenom_nom
                # nom-prenom // prenom-nom
                r'^(?:(?:pre)?nom)(\S)(?:(?:pre)?nom)$',
                # n.prenom // p.nom
                # n-prenom // p-nom
                # n_prenom // p_nom
                r'^(?:n|p)(\S)(?:(?:pre)?nom)$'
            ],
            'without_separator': [
                # pnom
                # nprenom
                r'^(p|n)?((?:pre)?nom)$'
            ]
        }

        if self.pattern:
            if isinstance(self.pattern, str):
                if self.separator:
                    # If the user provided us
                    # with a separator, just use it
                    names = self.pattern.split(self.separator)

                else:
                    # Make sure there is a separator in there
                    # otherwise we have to use another logic
                    if '.' in self.pattern or '-' in self.pattern or \
                        '_' in self.pattern:
                        pattern_separator = ''
                        # We have to try and identify
                        # the type of separator used in the pattern
                        # TODO: Factorize this section
                        # into a function
                        for base_regex_pattern in base_regex_patterns['with_separator']:
                            pattern_separator = re.search(base_regex_pattern, self.pattern)
                            # Break on first match
                            if pattern_separator:
                                break
                        
                        # We can split the names once the separator has
                        # been correctly identified
                        # ex. ['nom', 'prenom']
                        separator_object = pattern_separator.group(1)
                        names = self.pattern.split(separator_object, 1)
                        
                        index_of_surname = names.index('nom')
                        index_of_name = names.index('prenom')

                        # We have to create a blank
                        # canvas to prevent changing
                        # the names[...] data on each
                        # iteration
                        template_names = names.copy()

                        for items in self.csv_content:
                            # names[index_of_name] = 'test'
                            # names[index_of_surname] = 'testa'
                            template_names[index_of_surname] = items[0]
                            template_names[index_of_name] = items[1]
                            final_pattern = separator_object.join(template_names)
                            # If a domain was provided,
                            # append it to the names
                            if self.domain:
                                items.append(self.append_domain(final_pattern))
                            else:
                                items.append(final_pattern)
                            # Reset the template
                            template_names = names

                        # Update & reinsert headers
                        self.headers.append('email')
                        self.csv_content.insert(0, self.headers)

                        return self.csv_content

                    else:
                        # TODO: Factorize this section
                        # into a function
                        for base_regex_pattern in base_regex_patterns['without_separator']:
                            captured_elements = re.search(base_regex_pattern, self.pattern)
                            # Break on first match
                            if captured_elements:
                                break
                        
                        # Get group(1) & group(2)
                        # ex. p, nom, n, prenom
                        first_captured_element = captured_elements.group(1)
                        second_captured_element = captured_elements.group(2)

                        truncated_name = truncated_surname = ''

                        for items in self.csv_content:
                            if first_captured_element == 'n':
                                # TODO: Factorize
                                truncated_surname = items[0][:1]
                            elif first_captured_element == 'p':
                                # TODO: Factorize
                                truncated_name = items[1][:1]

                            if second_captured_element == 'nom':
                                name_to_append = items[0]
                            elif second_captured_element == 'prenom':
                                name_to_append = items[1]

                            final_pattern = truncated_name + name_to_append or \
                                             truncated_surname + name_to_append
                                             
                            # If a domain was provided,
                            # append it to the names
                            if self.domain:
                                items.append(self.append_domain(final_pattern))
                            else:
                                items.append(final_pattern)

                        return self.csv_content

            else:
                raise TypeError()
        else:
            raise NoPatternError()

    def append_domain(self, name):
        return name + '@' + self.domain

    def search_separator(self, name, with_separator=True):
        """Get a regex match using the REGEX email
        engine. The `with_separator` parameter helps you match
        a pattern that has a separator or that has none
        """
        if with_separator:
            for base_regex_pattern in self.config['BASE_REGEX_PATTERNS']['with_separator']:
                captured_elements = re.search(base_regex_pattern, self.pattern)
                # Break on first match
                if captured_elements:
                    break
            return captured_elements.group(1)
        else:
            for base_regex_pattern in self.config['BASE_REGEX_PATTERNS']['without_separator']:
                captured_elements = re.search(base_regex_pattern, self.pattern)
                # Break on first match
                if captured_elements:
                    break

            # Get group(1) & group(2)
            # ex. p, nom; n, prenom...
            first_captured_element = captured_elements.group(1)
            second_captured_element = captured_elements.group(2)
            return first_captured_element, second_captured_element

# s = NameConstructor(Configuration()['DUMMY_FILE'])
# s.pattern = 'nom.prenom'
# print(s.construct_pattern())
