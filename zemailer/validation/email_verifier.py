from ipaddress import IPv4Address, IPv6Address

from zemailer.validation.constants import LITERAL_REGEX, USER_REGEX, HOST_REGEX


def validate_ipv4_address(value):
    try:
        IPv4Address(value)
    except:
        return False
    else:
        return True


def validate_ipv6_address(value):
    try:
        IPv6Address(value)
    except:
        return False
    else:
        return True


def validate_address(value):
    return validate_ipv4_address(value) or validate_ipv6_address(value)


def validate_email(email):
    from zemailer.validation.models import EmailAddress
    if not isinstance(email, EmailAddress):
        raise ValueError("'email' should be an instance of EmailAddress")

    if not USER_REGEX.match(email.user):
        raise ValueError(f'Invalid email address. Got: {email}')

    if email.get_literal_ip is not None:
        result = LITERAL_REGEX.match(email.ace_formatted_domain)
        if result is None:
            raise ValueError(f'Invalid email address. Got: {email}')

        if not validate_ipv6_address(result[1]):
            raise ValueError(f'Invalid email address. Got: {email}')
    else:
        if HOST_REGEX.match(email.ace_formatted_domain) is None:
            raise ValueError(f'Invalid email address. Got: {email}')

    return True
