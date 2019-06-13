import csv
import smtplib
from smtplib import SMTP
from email_app.core.settings import Configuration


class BaseServer:
    """This is the base server used to create a
    an SMTP connection
    """
    def __init__(self, host, port, user, password):
        try:
            # Create SMTP object from host and port
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
                raise
            else:
                print(f'Logged in as {user} to {smtp_connection._host}.')
                # return smtp_connection or None
                self.smtp_connection = smtp_connection

class Gmail(BaseServer):
    def __init__(self, user, password):
        super().__init__('smtp.gmail.com', 587, user, password)

class Outlook(BaseServer):
    def __init__(self, user, password):
        super().__init__('', 587, user, password)
