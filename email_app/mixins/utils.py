import re
import collections

class UtilitiesMixin:
    """A mixin for various tasks on names
    """
    def splitter(self, name):
        """Create an array with the names by seperating
        them. Therefore, `Eugénie Bouchard` becomes `['Eugénie', 'Bouchard']`.
        """
        return name.split(' ')

    def normalize_name(self, name):
        return name.lower().strip()

    def flatten_name(self, name):
        r"""Replace all accents from a name and
        normalize it: `Eugénie Bouchard` or `Eugénie Bouchard\s?`
        becomes `eugenie bouchard`.

        NOTE - This will also normalize the name
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

    def reverse(self, name):
        return list(reversed(self.splitter(name)))

    def decompose(self, name, change_position=False):
        """Work with composed names such as `Eugenie Pauline Bouchard`
        to `Eugenie` - `Pauline Bouchard`. By using `change_position`,
        you can get `Eugenie Pauline` - `Bouchard`
        """
        # [Eugenie, Pauline, Bouchard]
        splitted_name = self.splitter(name)
        # Pop middle name
        middle_name = splitted_name.pop(1)
        # Create composed name
        composed_name = ' '.join([middle_name, splitted_name[1]])
        # ..
        splitted_name[1] = composed_name
        # [Eugenie, Pauline Bouchard] or
        # [Eugenie Pauline, Bouchard]
        return splitted_name
