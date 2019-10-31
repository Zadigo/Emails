"""This module implements a series of different mixins
that can be used to construct email patterns.

Description
-----------

The mixins are classes that can be subclassed in order
to use their definitions.

John PENDENQUE - pendenquejohn@gmail.com
"""

from app.patterns.constructor import UtilitiesMixin

class PatternsMixin(UtilitiesMixin):
    """A basic helper to construct email
    pattern names quickly.

    In order to use this class, subclass it
    and call any of the definitions that it
    contains.

    Description
    -----------

        class Test(PatternsMixin):
            pass

        Test().name_dot_surname()

    You can also override the definitions if you
    wish to implement additional functionalities.
    """
    def __init__(self, name, reverse=False):
        # ['Eugénie', 'Bouchard'] ->
        # ['eugenie', 'bouchard']
        names = self.splitter(self.flatten_name(name))

        # ['Eugénie', 'Bouchard'] -> 
        # ['Bouchard', 'Eugénie']
        if reverse:
            names.reverse()

        self.names = names

        # Even if he user decides to reverse,
        # we let the variables name and surname 
        # as is
        self.name = names[0]
        self.surname = names[1]

    def name_dot_surname(self):
        """`eugenie.bouchard@domain.fr`
        """
        return f'{self.name}.{self.surname}'

    def name_dash_surname(self):
        """`eugenie-bouchard@domain.fr`
        """
        return f'{self.name}-{self.surname}'

    def name_underscore_surname(self):
        """`eugenie_bouchard@domain.fr`
        """
        return f'{self.name}_{self.surname}'

    def nsurname(self):
        """`ebouchard@domain.fr`
        """
        return f'{self.name[:1]}{self.surname}'

    @property
    def sname(self):
        """`beugenie@domain.fr`
        """
        return f'{self.surname[:1]}{self.name}'

    @property
    def name_s(self):
        """`boucharde@domain.fr`
        """
        return f'{self.name}{self.surname[:1]}'

    @property
    def _name(self):
        """`eugenie@domain.fr`
        """
        return self.name

    @property
    def _surname(self):
        """`bouchard@domain.fr`
        """
        return self.surname

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.names)
