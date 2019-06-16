import os
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type, read_mime_types

from email_app.core.errors import NoServerError
from email_app.core.servers import Gmail, Outlook


class SendEmail:
    """Send an email using a server
    """
    server = Gmail

    def __init__(self, sender, receiver, subject, **kwargs):
        if self.server:
            if callable(self.server):
                # Create a new server instance
                # to be used
                Klass = self.server('', '')
            else:
                raise NoServerError('Server is not a callable. \
                            Received %s' % type(self.server))
        else:
            raise NoServerError('Server was not provided. \
                        Did you forget to register a server?')

        # Create a MIME object
        message = MIMEMultipart('alternative')
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject
        
        # Create MIME text objects
        text = MIMEText('This is a test', 'plain')
        html = MIMEText('<html><body>This is a test</body></html>', 'html')
        # Attach
        message.attach(text)
        message.attach(html)

        # Attachment
        if 'attachment' in kwargs:
            message.attach(kwargs['attachment'])

        # ..Send email
        Klass.smtp_connection.sendmail(sender, receiver, message.as_string())
        Klass.smtp_connection.close()

class SendEmailWithAttachment(SendEmail):
    def __init__(self, file_path):
        attachment = self.create_attachment(file_path)
        super().__init__('', '', 'Test', attachment=attachment)

    def create_attachment(self, path):
        """Create an attachment
        """
        content = open(path, 'rb')
        # mime_type = guess_type(path)
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(content.read())
        content.close()
        # Encode in Base64
        encode_base64(attachment)
        # Filename
        filename = os.path.basename(path)
        attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        return attachment
        