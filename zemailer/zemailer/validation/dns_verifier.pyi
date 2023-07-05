from typing import Union

from dns.resolver import Answer

from zemailer.validation.models import EmailAddress


def get_mx_records(
    domain: str,
    timeout: int,
    email_object: EmailAddress
) -> Answer: ...


def clean_mx_records(
    domain: str,
    timeout: int,
    email_object: EmailAddress
) -> set[str]: ...


def verify_dns(
    email: EmailAddress,
    timeout: int = ...
) -> Union[list[str], set[str]]: ...
