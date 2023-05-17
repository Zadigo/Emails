import unicodedata


class Patterns:
    patterns = [
        'firstname.lastname',
        'lastname.firstname',
        'firstnamelastname',
        'flastname',
        'lastname',
        'firstname',
        'firstnamel'
    ]
    separators = ['.', '-' '_']
    domain = 'gmail'
    particle = 'com'
    seperator = '.'

    def __init__(self, pattern):
        self.pattern = None
        self.pattern_location = None
        pattern = list(filter(lambda x: pattern == x, self.patterns))
        if not pattern:
            raise ValueError()
        if pattern:
            self.pattern = pattern[-1]
            self.pattern_location = self.patterns.index(self.pattern)
        self._items = []
        self._firstname = None
        self._lastname = None

    def __repr__(self):
        return f'<Pattern: {self.pattern}>'
    
    @staticmethod
    def clean(firstname, lastname):
        lowered_tokens = map(lambda x: x.lower().strip(), [firstname, lastname])

        def remove_accents(text):
            nfkd_form = unicodedata.normalize('NFKD', text)
            return nfkd_form.encode('ASCII', 'ignore')
        clean_tokens = map(remove_accents, lowered_tokens)
        tokens = map(lambda x: x.decode('utf-8'), clean_tokens)
        return list(tokens)
    
    @property
    def guess_separator(self):
        for separator in self.separators:
            if separator in self.pattern:
                yield separator

    def _substitute(self, firstname, lastname):
        firstname, lastname = self.clean(firstname, lastname)
        pattern = self.pattern
        if self.pattern == 'flastname':
            firstname = firstname[0]
            first_value = pattern.replace('f', firstname)
            second_value = first_value.replace('lastname', lastname)
        elif self.pattern == 'firstnamel':
            lastname = lastname[0]
            first_value = pattern.replace('firstname', firstname)
            second_value = first_value.replace('l', lastname)
        else:
            first_value = pattern.replace('firstname', firstname)
            second_value = first_value.replace('lastname', lastname)
        return second_value
    
    def as_email(self, firstname, lastname):
        self._firstname = firstname
        self._lastname = lastname
        self._items = [
            self._substitute(firstname, lastname),
            '@',
            self.domain,
            '.',
            self.particle
        ]
        return ''.join(self._items)


class Email(Patterns):
    def __init__(self, pattern, firstname, lastname):
        super().__init__(pattern)
        self.email = self.as_email(firstname, lastname)

    def __repr__(self):
        return f'<Email: {self.email}>'
    
    def __str__(self):
        return self.email
    
    def __hash__(self):
        return hash([self.email, self.pattern, self.pattern_location])
    
    def __eq__(self, obj):
        return self.email == str(obj)
    
    def __contains__(self, obj):
        return str(obj) in self.email


p = Email('firstname.lastname', 'John', 'Viré')
print(p)
