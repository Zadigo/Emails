from smtplib import SMTP, SMTPResponseException, SMTPServerDisconnected


class SMTPCheck(SMTP):
    def __init__(self, local_hostname, timeout, debug, sender, recipient):
        super().__init__(local_hostname=local_hostname, timeout=timeout)
        self._sender = sender
        self._recip = recipient
        self.errors = {}
        self.sock = None
        self._command = None
        self._host = None

    def mail(self, sender: str, options: tuple = ()):
        """
        Like `smtplib.SMTP.mail`, but raise an appropriate exception on
        negative SMTP server response.
        A code > 400 is an error here.
        """
        code, message = super().mail(sender=sender, options=options)
        if code >= 400:
            print(code, message)
            raise
        return code, message
    
    def rcpt(self, recip: str, options: tuple = ()):
        """
        Like `smtplib.SMTP.rcpt`, but handle negative SMTP server
        responses directly.
        """
        code, message = super().rcpt(recip=recip, options=options)
        if code >= 500:
            # Address clearly invalid: issue negative result
            print(code, message)
            raise
        elif code >= 400:
            print(code, message)
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

    def check_server(self, host):
        """
        Run the check for one SMTP server.

        Return `True` on positive result.

        Return `False` on ambiguous result (4xx response to `RCPT TO`),
        while collecting the error message for later use.

        Raise `AddressNotDeliverableError`. on negative result.
        """
        try:
            self.connect(host=host)
            self.starttls()
            self.ehlo_or_helo_if_needed()
            self.mail(sender=self._sender.ace)
            code, message = self.rcpt(recip=self._recip.ace)
        except SMTPServerDisconnected as e:
            return False
        except SMTPResponseException as e:
            if e.smtp_code >= 500:
                raise
            else:
                self.__temporary_errors[self._host] = smtp_message
            return False
        finally:
            self.quit()
        return code < 400
