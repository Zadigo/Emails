from functools import cached_property

import idna


class EmailEvaluationMixin:
    evaluation = set()
    mx_records = None
    messages = []
    errors = {}

    @property
    def is_risky(self):
        return any([
            'protected' in self.evaluation
        ])
    
    def get_json_response(self):
        return {
            'risky': self.is_risky,
            'email': self.email,
            'evaluation': self.evaluation
        }

    def add_error(self, error):
        self.evaluation.add(error)

    def add_mx_records(self, records):
        self.mx_records = records
        for record in records:
            if 'protection' in record:
                self.add_error('protected')

    def add_message(self, host, code, message):
        message = message.decode('utf-8')
        self.messages.append([host, code, message])


class EmailAddress(EmailEvaluationMixin):
    """Represents the raw email object"""

    def __init__(self, email):
        self.email = email

        try:
            self.user, self.domain = self.email.rsplit('@', 1)
        except Exception:
            raise ValueError(f'Email is not valid. Got: {email}')

        if self.get_literal_ip is None:
            self.ace_formatted_domain = self.domain
        else:
            try:
                self.ace_formatted_domain = idna.encode(
                    self.domain).decode('ascii')
            except idna.IDNAError:
                raise

    def __repr__(self):
        return f'<EmailAddress: {self.email}>'

    def __str__(self):
        return self.email

    @cached_property
    def get_literal_ip(self):
        logic = [
            self.domain.startswith('['),
            self.domain.endswith(']')
        ]
        return self.domain[1:-1] if all(logic) else None

    @cached_property
    def restructure(self):
        """The ASCII-compatible encoding for the email address"""
        return '@'.join((self.user, self.ace_formatted_domain))
