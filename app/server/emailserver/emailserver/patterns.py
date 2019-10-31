"""A utilities class for various tasks on names such as
reversing or splitting names

author: pendenquejohn@gmail.com
"""

import collections
import re


class BaseMessages:
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}: message={self.message}"

class Info(BaseMessages):
    def __init__(self, message):
        super().__init__(message)

class UtilitiesMixin:
    """A mixin is used to extend classes with various definitions on 
    repetitive tasks on names such as normalizing them etc.
    """
    def splitter(self, name):
        """Create an array with a single name by splitting it.

        Result
        ------
        
        `Eugénie Bouchard` becomes `[Eugénie, Bouchard]`.
        """
        return name.split(' ')

    def split_multiple(self, names):
        """Split multiple names into arrays
        """
        if not isinstance(names, (list, tuple)):
            raise TypeError('Names should be a list or a tuple')

        for name in names:
            yield name.split(' ')

    def normalize_name(self, name):
        """A helper function that normalizes a name to lowercase
        and strips any whitespaces

        Example
        -------

            "Eugenie Bouchard " becomes "eugenie bouchard"
        """
        return name.lower().strip()

    def flatten_name(self, name):
        """Replace all accents from a name and
        normalize it.
        
        Example
        ------

            "Eugénie Bouchard" or "Eugénie Bouchard\\s?"
            becomes `eugenie bouchard`.

            NOTE - This method will also normalize the name
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
        """Reverse an array with names.

        Example
        -------
        
            [Eugenie, Bouchard] to [Bouchard, Eugenie]
        """
        return list(reversed(self.splitter(name)))

    def decompose(self, name, change_position=False):
        """Structures composed names into two unique names

        Example
        -------
        
            "Eugenie Pauline Bouchard" becomes "Eugenie" "Pauline Bouchard"

            [Eugenie, Pauline Bouchard] or [Eugenie Pauline, Bouchard]

        Parameters
        ----------

            change_position - changes the direction in which the composed name
                              should appear. The default position is on the left.
        """
        # [Eugenie, Pauline, Bouchard]
        splitted_name = self.splitter(name)
        # Test if list = 3
        if len(splitted_name) != 3:
            print(Info('Cannot perform operation. Your name seems to be a '
                    'non composed name: %s') % name)
            return None
        # Pop middle name
        middle_name = splitted_name.pop(1)
        # Create composed name by joining parts
        if change_position:
            # .. Eugenie and Pauline
            composed_name = ' '.join([splitted_name[0], middle_name])
            splitted_name[0] = composed_name
        else:
            # .. Pauline and Bouchard
            composed_name = ' '.join([middle_name, splitted_name[1]])
            # ..
            splitted_name[1] = composed_name
        # [Eugenie, Pauline Bouchard] or
        # [Eugenie Pauline, Bouchard]
        return splitted_name

utilities = UtilitiesMixin()

def construct_emails(func):
    """A decorator function that can be used to construct
    a list of emails from  a list of names.

    Example
    -------

    Suppose you have a function that returns a list or a tuple
    and from these returned values (which are names) you wish
    to construct a list of emails:

        @construct_emails
        def test_function():
            names = [Eugenie Bouchard, Maria Sharapova]
            return names

        constructor(., gmail.com)

        You can pass one domain or multiple domains.

        In which case, an email will be constructed for each
        domains that were provided.

        You will then get a list of constructed emails using the
        separator and the domain that you provided:

        [eugenie.bouchard@google.com, maria.sharapova@google.com]

        Finally, if you wish to reverse the position of the name and
        the surname, use the `reverse = True` parameter.

    This decorator is an alternative to utilizing the email construction 
    classes.
    """
    def constructor(separator, domains=['gmail.com'], reverse_names=False):
        names = func()
        if not isinstance(names, (list, tuple)):
            raise TypeError("Names should be a list"
                "or a tuple of names. Received '%s'" % type(names))

        new_names = []
        new_name = ''

        for name in names:
            # Take out all the accents, spaces and
            # lowercase the names
            new_name = utilities.flatten_name(name)
            splitted_name = new_name.split(' ')

            # In case we want bouchard.eugenie
            # instead of eugenie.bouchard
            # if reverse_names:
            #     splitted_name.reverse()

            # Create the new name using the separator
            constructed_name = separator.join(splitted_name)

            for domain in domains:
                # TODO: Maybe yield the names as a generator
                # as opposed to the list below
                new_names.append(constructed_name + '@' + domain)

        return new_names
    return constructor
