class UtilitiesMixin:
    """A mixin for various tasks on names
    """
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