import csv
import re
import os

test_path='C:\\Users\\Zadigo\\Documents\\Programs\\EmailsApp\\test.csv'

class UtilitiesMixin:
    def splitter(self, name):
        """Create an array with the name. `Eugénie Bouchard`
        becomes `['Eugénie', 'Bouchard']`.
        """
        return name.split(' ')

    def normalize_name(self, name):
        return name.lower().strip()

    def flatten_name(self, name):
        r"""Replace all accents from a name and
        normalize it: `Eugénie Bouchard` or `Eugénie Bouchard\s?`
        becomes `eugenie bouchard`.
        """
        new_name=''
        accents = {
            'é': 'e',
            'è': 'e',
            'ê': 'e',
            'ë': 'e',
            'ï': 'i',
            'î': 'i',
            'ü': 'u',
            'ù': 'u',
            'à': 'a',
        }
        for letter in name:
            for key, value in accents.items():
                if letter == key:
                    letter = value
            new_name += letter
        return self.normalize_name(new_name)

class EmailConstructor:
    """Open a file to construct a list of emails.
    The file path can be a url or a path on your
    computer.
    """
    def __init__(self, file_path=None):
        file_path = test_path

        with open(file_path, 'r', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            csv_content = list(csv_file).copy()

        # Pop the headers but keep
        # them for later usage
        self.headers = csv_content.pop(0)
        for content in csv_content:
            for i in range(len(content)):
                content[i] = self.normalize_names(content[i])
        # Store the csv's content
        self.csv_content = csv_content

    @staticmethod
    def normalize_names(name):
        """Normalize a name for example 
        from `Pierre LOPEZ` to `Pierre Lopez`.
        """
        return name.lower().strip()

    @property
    def get_content(self):
        """Get the raw csv content
        """
        return self.csv_content

class EmailPatterns(EmailConstructor):
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
                        # We have to try and get
                        # the type of separator
                        # used in the pattern
                        # TODO: Factorize this section
                        # into a function
                        for base_regex_pattern in base_regex_patterns['with_separator']:
                            pattern_separator = re.search(base_regex_pattern, self.pattern)
                            # Break on first match
                            if pattern_separator:
                                break
                        
                        # ex. ['nom', 'prenom'] using matched separator
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
            raise TypeError()

    def append_domain(self, name):
        return name + '@' + self.domain

class EmailPatternRepr(EmailPatterns):
    """This is the basic class used to return the list
    of emails that were created.

    By subclassing this class you get a list of values
    such as `[[headers], [..., ...]]`.
    """
    def __str__(self):
        return str(self.construct_pattern())

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.construct_pattern()))

    def __getitem__(self, index):
        # Add one in order to return
        # a list not being the headers
        if index == 0:
            index = index + 1
        return str(self.construct_pattern()[index])

class BasicPatterns:
    """Use this class to construct a list of
    emails from scratch providing a `name` or
    a `filepath`. This will take a name and create
    patterns with all provided domains.

    Ex. with `Aurélie Konaté`: __['aurelie.konate@gmail.com', 'aurelie.konate@outlook.com', 
    'aurelie-konate@gmail.com', 'aurelie-konate@outlook.com', 'aurelie_konate@gmail.com', 
    'aurelie_konate@outlook.com']__

    You use this class directly as iterable to output the values to a given file:
    > with open(file_path, 'w') as f:

    >> f.writelines(BasicPatterns('Aurélie Konaté'))
    """
    def __init__(self, name_or_filepath, separators=['.', '-', '_'], 
                    domains=['gmail', 'outlook']):
        patterns = []

        name = self.splitter(self.flatten_name(name_or_filepath))

        # Create occurences
        for separator in separators:
            for domain in domains:
                pattern = f'{name[0]}{separator}{name[1]}@{domain}.com'
                patterns.append(pattern)
        self.patterns = patterns

    def __str__(self):
        return str(self.patterns)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.patterns))

    def __getitem__(self, index):
        return str(self.patterns[index])

    def append(self, value):
        self.patterns.append(value)
        return self.__str__()
