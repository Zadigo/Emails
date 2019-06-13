import csv
import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type, read_mime_types
from smtplib import SMTP


class BaseServer:
    def create_connection(self, host, port, user, password):
        try:
            smtp_connection = SMTP(host=host, port=port)
        except smtplib.SMTPConnectError:
            raise
        else:
            
            # Ping server
            smtp_connection.ehlo()
            smtp_connection.starttls()

            try:
                smtp_connection.login(user, password)
            except smtplib.SMTPAuthenticationError:
                raise
            else:
                print(f'Logged in as {user} to {smtp_connection._host}.')
                return smtp_connection or None

class Gmail(BaseServer):
    def __init__(self, user, password):
        self.connection = self.create_connection('smtp.gmail.com', 587, user, password)

class SendEmail:
    using_server = Gmail

    def __init__(self):
        if self.using_server:
            if callable(self.using_server):
                Klass = self.using_server('inglish.contact@gmail.com', 'KendallJennerLove97170')

            else:
                raise TypeError()

        else:
            raise ValueError()

        message = MIMEMultipart('alternative')
        message['To'] = ''
        message['From'] = ''
        message['Subject'] = ''
        text = ''
        html = ''
        message.attach(text, 'text')
        message.attach(html, 'html')

        Klass.connection.send_message(message.as_string())
        Klass.connection.close()

class SendEmailWithAttachment(SendEmail):
    def __init__(self, user, password, to_address, file_path, server=None):
        if self.using_server:
            if callable(self.using_server):
                Klass = self.using_server('user', 'password')

            else:
                raise TypeError()

        else:
            if callable(server):
                self.using_server = server
            raise ValueError()

        message = MIMEMultipart('alternative')
        message['To'] = 'contact.kurrikulam@gmail.com'
        message['From'] = user
        message['Subject'] = 'TEST'
        text = MIMEText('TEST')
        # html = MIMEText('test')

        attachment = self.create_attachment(file_path)

        message.attach(text)
        # message.attach(html)
        message.attach(attachment)
        
        Klass.connection.sendmail(user, 'contact.kurrikulam@gmail.com', message.as_string())
        Klass.connection.quit()

    def create_attachment(self, path):
        content = open(path, 'rb')
        # mime_type = guess_type(path)
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(content.read())
        content.close()
        encode_base64(attachment)
        attachment.add_header('Content-Disposition', "attachment; filename= %s" % 'test.txt')
        return attachment
