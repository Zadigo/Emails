from functools import cached_property

import idna

from zemailer.validation.blacklist import blacklist
from zemailer.validation.dns_verifier import verify_dns
from zemailer.validation.email_verifier import validate_email
from zemailer.validation.models import EmailAddress
from zemailer.validation.smtp_verifier import smtp_check


def validate_or_fail(email, *, check_format=True, check_blacklist=True, check_dns=True, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False):
    """
    Return `True` if the email address validation is successful, `None`
    if the validation result is ambigious, and raise an exception if the
    validation fails
    """
    email_object = EmailAddress(email)

    if check_format:
        validate_email(email_object)

    if check_blacklist:
        pass

    mx_records = verify_dns(email_object, timeout=dns_timeout)

    if not check_smtp:
        return True
    
    if smtp_from_address is not None:
        pass

    return email_object, smtp_check(
        email=email_object,
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
        email_object, validation_results = validate_or_fail(email, **kwargs)
    except Exception:
        return False
    else:
        return any(validation_results), email_object


# validate('romain.gallon@yopmail.com')
validate('chassan_s@subway.fr')
