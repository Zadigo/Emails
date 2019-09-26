import os
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type, read_mime_types

from app.core.errors import NoServerError
from app.core.servers import Gmail
from zemailer.app.core.settings import configuration

class SendEmail:
    """Send an email using a server

    Parameters
    ----------

    `sender` the email sending the message

    `receiver` the email or emails receiving the message

    `subject` of the message that you are sending 

    `server` is the backend used to send the email(s)

    Optional: `attachment` corresponds to the path of the object
    that you want to attach to the email
    """
    server = Gmail
    config = configuration['SERVER_CONFIG']

    def __init__(self, sender, receiver, subject, **kwargs):
        if self.server:
            if callable(self.server):
                # Create a new server instance
                # to be used - The default server
                # is the Gmail one
                # .. Klass = self.server('', '')
                user = self.config['default']['user']
                password = self.config['default']['password']
                Klass = self.server(user, password)
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

        # Attachment - attach if any
        if 'attachment' in kwargs:
            message.attach(kwargs['attachment'])

        # ..Send email
        Klass.smtp_connection.sendmail(sender, receiver, message.as_string())
        Klass.smtp_connection.close()

class SendEmailWithAttachment(SendEmail):
    def __init__(self, sender, receiver, subject, file_path, **kwargs):
        attachment = self.create_attachment(file_path)
        super().__init__(sender, receiver, subject, attachment=attachment)

    def create_attachment(self, path):
        """Create an attachment using a local path
        """
        content = open(path, 'rb')
        # mime_type = guess_type(path)
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(content.read())
        content.close()
        # Encode in Base64
        encode_base64(attachment)
        # Get the file's name
        filename = os.path.basename(path)
        attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        return attachment

    def create_attachments(self, paths):
        if not isinstance(paths, (list, tuple)):
            raise TypeError()

        attachments = []

        for path in paths:
            attachments.append(self.create_attachment(path))

        return attachments
