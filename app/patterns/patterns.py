from app.patterns.constructor import NameConstructor
from app.mixins.utils import UtilitiesMixin
from zemailer.app.patterns.constructor import FileOpener
import os
import re

class NamePatterns(NameConstructor):
    """This is the base class used to represent the list
    of emails that were created by the NameConstructor superclass.

    Example
    -------

        class MyClass(NamePatters):
            pattern = 'nom.prenom'

    Description
    -----------

    By subclassing this class you will get a list of values
    such as :
        [
            [ headers ],
            [ name, email ],
            ...
        ]
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

class BasicNamePatterns(UtilitiesMixin):
    """Use this class to construct a list of of multiple emails 
    from scratch providing a person's `name` or a `filepath` 
    containing people's names.

    Contrarily to the other classes, this class in particular does
    not need to be subclassed to be used.
    
    Description
    -----------

    This will take a name and create patterns with all provided domains.

    Ex. with `Aurélie Konaté`
        [
            'aurelie.konate@gmail.com', 'aurelie.konate@outlook.com', 
            'aurelie-konate@gmail.com', 'aurelie-konate@outlook.com', 
            'aurelie_konate@gmail.com', 'aurelie_konate@outlook.com'
        ]

    You can use this class directly as an iterable to output the values to a given file:
        with open(file_path, 'w') as f:
            f.writelines(BasicPatterns('Aurélie Konaté'))

    Parameters
    ----------

    `name_or_filepath` is a single string name or a file path containing a list of names
    
    `separators` contains a list of separators to use in order to create the email patterns

    `domains` is the list of all the domains that you wish to use to construct the emails
    """
    def __init__(self, name_or_filepath, separators=['.', '-', '_'], 
                    domains=['gmail', 'outlook']):
        patterns = []

        # Check if the provided element is a path
        # is_path = re.match(r'[\w+\:\w+\\+]+(\.\w+)', name_or_filepath)
        # if is_path:
        #     # Open the file
        #     obj = FileOpener(name_or_filepath).csv_content
        #     names = self.split_multiple(obj)

        # Split names
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
