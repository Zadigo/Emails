import re

# class EmailField(UtilitiesMixin):
#     """Email object field
#     """
#     def __init__(self, nom, prenom, domaine, separator='.', regex=None):
#         self.nom = nom
#         self.prenom = prenom
#         self.domaine = domaine
#         self.separator = separator
#         email = separator.join([self.nom, self.prenom])
#         self.email = email + '@' + self.domaine

#     def __setattr__(self, name, value):
#         if name == 'nom' or name == 'prenom':
#             value = self.flatten_name(value)
#         return super().__setattr__(name, value)

#     def __str__(self):
#         return '%s(%s)' % (
#             self.__class__.__name__,
#             [self.nom, self.prenom, '@' + self.domaine]
#         )

#     def __repr__(self):
#         return self.email

class EmailField:
    """To create more complexe patterns, use this field
    with a regex pattern that will parse the given email.
    """
    def __init__(self, email, pattern):
        is_match = re.search(pattern, email)
        if is_match:
            # Get the tuple of 
            # the matching value
            self.groups = is_match.groups()

    def __str__(self):
        return str(self.groups)
