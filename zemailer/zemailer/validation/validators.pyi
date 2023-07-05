from typing import Literal, Union

from zemailer.validation.models import EmailAddress


def validate_or_fail(
    email,
    *,
    check_format: bool = ...,
    check_blacklist: bool = ...,
    check_dns: bool = ...,
    dns_timeout: Literal[10] = ...,
    check_smtp: bool = True,
    smtp_timeout=Literal[10],
    smtp_helo_host: str = None,
    smtp_from_address: str = None,
    smtp_debug: bool = False
) -> tuple[EmailAddress, bool]: ...


def validate(
    email: str,
    **kwargs
) -> Union[bool, tuple[bool, EmailAddress]]: ...
