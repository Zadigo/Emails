from dns import resolver
from dns.rdatatype import MX as rdtype_mx
from dns.rdtypes.ANY.MX import MX

from zemailer.validation.constants import HOST_REGEX



def get_mx_records(domain, timeout, email_object):
    """Returns the DNS records for the given domain

    >>> get_mx_records("example.com", 10)"""
    try:
        return resolver.resolve(
            qname=domain,
            rdtype=rdtype_mx,
            lifetime=timeout
        )
    except resolver.NXDOMAIN:
        email_object.add_error('domain_error')
        raise Exception('Domain not found')
    except resolver.NoNameservers:
        raise resolver.NoNameservers
    except resolver.Timeout:
        email_object.add_error('timeout')
        raise Exception('Domain lookup timed out')
    except resolver.YXDOMAIN:
        email_object.add_error('dns_error')
        raise Exception('Misconfigurated DNS entries for domain')
    except resolver.NoAnswer:
        email_object.add_error('dead_server')
        raise Exception('No MX record for domain found')
    

def clean_mx_records(domain, timeout, email_object):
    """
    Returns a list of hostnames in the MX record
    """
    answer = get_mx_records(domain, timeout, email_object)

    result = set()
    for record in answer.rrset.processing_order():
        dns_string = record.exchange.to_text().rstrip('.')
        result.add(dns_string)
    
    # Check that each record follows RFC 
    values = list(map(lambda x: HOST_REGEX.search(string=x), result))
    if not values:
        email_object.add_error('domain_error')
        raise ValueError('No MX records found')
    email_object.add_mx_records(result)
    # print('Found mx records', result)
    return result


def verify_dns(email, timeout=10):
    """
    Check whether there are any responsible SMTP servers for the email
    address by looking up the DNS MX records.

    In case no responsible SMTP servers can be determined, a variety of
    exceptions is raised depending on the exact issue, all derived from
    `MXError`. Otherwise, return the list of MX hostnames.

    >>> verify_dns('email@gmail.com')
    ... ['smtp.1.2.3.4]
    """
    # from zemailer.validation.validators import EmailAddress

    # if not isinstance(email, EmailAddress):
    #     raise

    if email.get_literal_ip:
        return [email.get_literal_ip]
    else:
        return clean_mx_records(email.domain, timeout, email)
