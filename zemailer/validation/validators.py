import idna
from functools import cached_property
from zemailer.validation.dns_verifier import verify_dns
from zemailer.validation.smtp_verifier import smtp_check


class EmailAddress:
    """Represents the raw email object"""
    
    def __init__(self, email):
        self.email = email

        try:
            self.user, self.domain = self.email.rsplit('@', 1)
        except ValueError:
            raise

        if self.get_literal_ip is None:
            self.ace_formatted_domain = self.domain
        else:
            try:
                self.ace_formatted_domain = idna.encode(self.domain).decode('ascii')
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


def validate_or_fail(email, *, check_format=True, check_blacklist=True, check_dns=True, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False):
    """
    Return `True` if the email address validation is successful, `None`
    if the validation result is ambigious, and raise an exception if the
    validation fails
    """
    email = EmailAddress(email)

    if check_format:
        pass

    if check_blacklist:
        pass

    mx_records = verify_dns(email, timeout=dns_timeout)

    if not check_smtp:
        return True
    
    if smtp_from_address is not None:
        pass

    return smtp_check(
        email=email,
        mx_records=mx_records,
        timeout=smtp_timeout,
        helo_host=smtp_helo_host,
        from_address=smtp_from_address,
        debug=smtp_debug
    )


def validate(email, **kwargs):
    """
    Return `True` or `False` depending if the email 
    address exists or/and can be delivered. Returns `None` 
    if the result is ambigious
    """
    try:
        validation_results = validate_or_fail(email, **kwargs)
    except Exception:
        return False
    else:
        return any(validation_results)
        # return False


print(validate('hugorombouts@malongo.fr'))
# print(validate('xavier.royaux@mcdonalds.com'))
# validate('jortypoazfina@lesburgersdepapa.fr')
# validate('cedric@lesburgersdepapa.fr')
# validate('kylie@california-bliss.fr')
