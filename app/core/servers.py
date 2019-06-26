import csv
import smtplib
from smtplib import SMTP

from app.core.settings import Configuration


class BaseServer:
    """This is the base class used to create a
    an SMTP connection to a server. Subclass it, and
    call its __init__ function.
    """
    def __init__(self, host, port, user, password):
        try:
            # Create an SMTP object from host and port
            # <smtplib.SMTP> object
            smtp_connection = SMTP(host=host, port=port)
        except smtplib.SMTPConnectError:
            raise
        else:
            
            smtp_connection.ehlo()
            # Put connection in TLS mode
            smtp_connection.starttls()

            try:
                # Login user with password
                smtp_connection.login(user, password)
            except smtplib.SMTPAuthenticationError:
                # Provided credentials are not good?
                # Get credentials from configuration
                # Raise an error since there's no purpose
                # using such an app without credentials
                # configuration = Configuration()
                # If user and password are none,
                # raises an ImproperlyConfiguredError()
                # user = configuration['USER']
                # password = configuration['PASSWORD']
                raise
            else:
                print(f'Logged in as {user} to {smtp_connection._host}.')
                # return smtp_connection
                self.smtp_connection = smtp_connection

class Gmail(BaseServer):
    """ A server set to be used with Gmail
    """
    def __init__(self, user, password):
        super().__init__('smtp.gmail.com', 587, user, password)

class Outlook(BaseServer):
    """ A server set to be used with Outlook
    """
    def __init__(self, user, password):
        super().__init__('SMTP.office365.com', 587, user, password)
