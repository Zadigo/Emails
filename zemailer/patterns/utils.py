import csv
import unicodedata

EMAIL_PATTERNS = [
    'firstname.lastname',
    'lastname.firstname',
    'firstnamelastname',
    'f1lastname',
    'lastnamef1',
    'firstname',
    'firstnamel1',
    'lastname',
    'f1.lastname',
    'l1.firstname'
]

class Patterns:
    separators = ['.', '-' '_']
    domain = 'gmail'
    particle = 'com'
    seperator = '.'

    def __init__(self, pattern):
        self.pattern = None
        self.pattern_location = None
        pattern = list(filter(lambda x: pattern == x, EMAIL_PATTERNS))
        if not pattern:
            raise ValueError()
        if pattern:
            self.pattern = pattern[-1]
            self.pattern_location = EMAIL_PATTERNS.index(self.pattern)
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
        if self.pattern == 'f1lastname':
            firstname = firstname[0]
            first_value = pattern.replace('f1', firstname)
            second_value = first_value.replace('lastname', lastname)
        elif self.pattern == 'firstnamel1':
            lastname = lastname[0]
            first_value = pattern.replace('firstname', firstname)
            second_value = first_value.replace('l1', lastname)
        elif self.pattern == 'lastnamef1':
            firstname = firstname[0]
            first_value = pattern.replace('lastname', lastname)
            second_value = first_value.replace('f1', firstname)
        elif self.pattern == 'f1.lastname':
            firstname = firstname[0]
            first_value = pattern.replace('lastname', lastname)
            second_value = first_value.replace('f1', firstname)
        elif self.pattern == 'l1.firstname':
            lastname = lastname[0]
            first_value = pattern.replace('firstname', lastname)
            second_value = first_value.replace('l1', firstname)
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


class EmailGenerator:
    emails = []
    def __init__(self, firstname, lastname):
        for pattern in EMAIL_PATTERNS:
            self.emails.append(Email(pattern, firstname, lastname))

    def __iter__(self):
        return iter(self.emails)
    
    def to_file(self, name=None):
        with open('test.csv', mode='w', encoding='utf-8', newline='\n') as f:
            emails = map(lambda x: [x], self.emails)
            writer = csv.writer(f)
            writer.writerows(emails)

# p = Email('lastname', 'John', 'Viré')
# print(p)


e = EmailGenerator('Julie', 'Gar')
e.to_file()
