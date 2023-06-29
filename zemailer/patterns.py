import collections
import csv
import json
import unicodedata
from functools import cached_property, lru_cache
from itertools import chain, permutations

from zemailer.validation.validators import validate

# EMAIL_PATTERNS = [
#     'firstname.lastname',
#     'lastname.firstname',
#     'firstnamelastname',
#     'f1lastname',
#     'lastnamef1',
#     'firstname',
#     'firstnamel1',
#     'lastname',
#     'f1.lastname',
#     'l1.firstname'
# ]


class Patterns:
    """Encapsulates the different types of patterns
    we can get with business emails"""

    separators = ['.', '-', '_']

    def __init__(self, firstname, lastname):
        self._generated_emails = set()

        firstname, lastname = self.clean(firstname, lastname)
        self._firstname = firstname
        self._lastname = lastname

    @staticmethod
    def clean(firstname, lastname):
        lowered_tokens = map(
            lambda x: x.lower().strip(),
            [firstname, lastname]
        )

        def remove_accents(text):
            nfkd_form = unicodedata.normalize('NFKD', text)
            return nfkd_form.encode('ASCII', 'ignore')

        clean_tokens = map(remove_accents, lowered_tokens)
        tokens = map(lambda x: x.decode('utf-8'), clean_tokens)
        return list(tokens)

    @cached_property
    def generate_templates(self):
        results = []
        firstname = self._firstname
        lastname = self._lastname

        tokens = [firstname, lastname]
        truncated_firstname = [firstname[0], lastname]
        truncated_lastname = [firstname, lastname[0]]

        results = []
        results.extend(list(permutations(tokens, 2)))
        results.extend(list(permutations(truncated_firstname, 2)))
        results.extend(list(permutations(truncated_lastname, 2)))
        return results

    def generate_with_separators(self, only=[]):
        """Generate multiple email patterns using a separator"""
        for tokens in self.generate_templates:
            lhv, rhv = tokens
            for seperator in self.separators:
                if only and seperator not in only:
                    continue
                yield ''.join([lhv, seperator, rhv])

    def generate_simple_emails(self):
        for item in self.generate_templates:
            yield ''.join(item)


class Email:
    """Represents an email object

    >>> Email("kendall.jenner", "gmail.com")
    """

    def __init__(self, user, domain):
        self.is_valid = False
        self.user = user
        self.domain = domain
        self.email = ''.join([user, '@', domain])

    def __repr__(self):
        return f'<Email: {self.email} is_valid={self.is_valid}>'

    def __str__(self):
        return self.email

    def __reduce__(self):
        return (self.user, '@', self.domain)

    def __hash__(self):
        return hash([self.user, self.domain, self.email])

    def __eq__(self, obj):
        return str(obj) == self.email

    def test(self, **kwargs):
        """Tests if this is a valid email addresss"""
        self.is_valid = validate(self.email, **kwargs)


class Emails(Patterns):
    """Represents a generated email address using
    a specific pattern"""

    def __init__(self, firstname, lastname, domain='gmail.com', pattern_only=[]):
        super().__init__(firstname, lastname)
        self.pattern_only = pattern_only
        self.domain = domain

    def __repr__(self):
        return f'<Emails: {self.emails}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} {list(self.emails)}>'

    def __iter__(self):
        return iter(list(self.emails))

    def __getitem__(self, index):
        return list(self.emails)[index]

    def __len__(self):
        return len(list(self.emails))

    def __enter__(self, *args, **kwargs):
        return self.emails

    def __exit__(self):
        return False

    @cached_property
    def construct(self):
        """Returns a three-way tuple containing
        the user, @ and the domain"""
        for user in self.users:
            yield user, '@', self.domain

    @cached_property
    def emails(self):
        """Returns Email instances
        """
        for tokens in self.construct:
            user, _, domain = tokens
            yield Email(user, domain)

    @cached_property
    def users(self):
        """Returns the list of patterns for
        the given user"""
        items = [
            list(self.generate_with_separators(only=self.pattern_only)),
            list(self.generate_simple_emails())
        ]
        return chain(*items)

    def to_file(self, name=None):
        """Outputs the results to a csv file"""
        with open('test.csv', mode='w', encoding='utf-8', newline='\n') as f:
            emails = map(lambda x: [x], self)
            writer = csv.writer(f)
            writer.writerows(emails)


class ValidateEmails:
    """Validate a list of email addresses"""
    
    def __init__(self, emails, test_args={}):
        if not isinstance(emails, (tuple, list)):
            raise

        self.results = collections.OrderedDict()

        for item in emails:
            if not isinstance(item, Email):
                raise
            self.results[item.email] = item.test(**test_args)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.results}>'

    def __getitem__(self, index):
        return self.results.get(index, None)

    def to_file(self, filename=None):
        with open('test.json', mode='w') as f:
            json.dump(self.results, f)

