import csv
import re

test_path='C:\\Users\\Zadigo\\Documents\\Programs\\EmailsApp\\test.csv'

class EmailConstructor:
    def __init__(self, file_path=None):
        """Open a file to construct a list of emails.
        """

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

class PatternsMixin:
    def name_dot_surname(self, name):
        """`name.surname@domain.fr`
        """
        # for content in self.csv_content:
        #     structure = f'{content[0]}.{content[1]}'
        #     content.append(structure)
        # return self.csv_content
        pass

class EmailPatterns(EmailConstructor, PatternsMixin):
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
                        pass

            else:
                raise TypeError()
        else:
            raise TypeError()

    def append_domain(self, name):
        return name + '@' + self.domain  

# test=EmailPatterns(test_path)
# test.pattern='nom.prenom'
# print(test.construct_pattern())