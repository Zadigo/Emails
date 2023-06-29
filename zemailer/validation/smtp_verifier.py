from smtplib import SMTP, SMTPResponseException, SMTPServerDisconnected, SMTPNotSupportedError


class SMTPVerifier(SMTP):
    """
    A class that checks an email against a set of MX records
    """
    
    def __init__(self, local_hostname, timeout, debug, sender, recip):
        super().__init__(local_hostname=local_hostname, timeout=timeout)
        debug_level = 2 if debug else False
        self.set_debuglevel(debug_level)

        self._sender = sender
        self._recip = recip
        self._command = None
        self._host = None
        self.errors = {}
        self.sock = None

    def putcmd(self, cmd, args=''):
        self._command = f'{cmd} {args}' if args else cmd
        super().putcmd(cmd, args)

    def mail(self, sender, options=[]):
        """
        Like `smtplib.SMTP.mail`, but raise an appropriate exception on
        negative SMTP server response.
        A code > 400 is an error here.
        """
        code, message = super().mail(sender=sender, options=options)
        if code >= 400:
            print('mail:', code, message)
            raise
        return code, message

    def starttls(self, *args, **kwargs):
        try:
            super().starttls(*args, **kwargs)
        except SMTPNotSupportedError:
            # The server does not support the STARTTLS extension
            pass
        except RuntimeError:
            # SSL/TLS support is not available to your Python interpreter
            pass

    def rcpt(self, recip, options=()):
        """
        Like `smtplib.SMTP.rcpt`, but handle negative SMTP server
        responses directly.
        """
        code, message = super().rcpt(recip=recip, options=options)
        if code >= 500:
            # Address clearly invalid: issue negative result
            print('rcpt', code, message)
            raise
        elif code >= 400:
            print('rcpt', code, message)
            raise
        return code, message

    def quit(self):
        """
        Like `smtplib.SMTP.quit`, but make sure that everything is
        cleaned up properly even if the connection has been lost before.
        """
        try:
            return super().quit()
        except Exception:
            self.ehlo_resp = self.helo_resp = None
            self.esmtp_features = {}
            self.does_esmtp = False
            self.close()

    def connect(self, host='localhost', port=0, source_address=None):
        self._command = 'connect'
        self._host = host
        try:
            code, message = super().connect(
                host=host,
                port=port,
                source_address=source_address
            )
        except OSError as error:
            raise
        else:
            if code >= 400:
                print(code, message)
                raise
        return code, message

    def check(self, record):
        """
        Run the check for one SMTP server.

        Returns `True` on positive result.

        Returns `False` on ambiguous result (4xx response to `RCPT TO`),
        while collecting the error message for later use.
        """
        try:
            self.connect(host=record)
            self.starttls()
            self.ehlo_or_helo_if_needed()
            # Checks the email against the mx record
            self.mail(sender=self._sender.restructure)
            code, message = self.rcpt(recip=self._recip.restructure)
        except SMTPServerDisconnected as e:
            return False
        except SMTPResponseException as e:
            if e.smtp_code >= 500:
                raise Exception(f'Communication error: {self._host} / {message}')
            else:
                self.errors[self._host] = message
            return False
        finally:
            self.quit()
        return code < 400

    def check_multiple(self, records):
        result = [self.check(x) for x in records]
        if self.errors:
            raise Exception(f'Host errors: {self.errors}')
        return result


def smtp_check(email, mx_records, timeout=10, helo_host=None, from_address=None, debug=False):
    """
    Returns `True` as soon as the any of the given server accepts the
    recipient address
    """
    sender = from_address or email
    instance = SMTPVerifier(helo_host, timeout, debug, sender, email)
    return instance.check_multiple(mx_records)
