class EmailerError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self, text=None):
        return 'Error' or text
        
class NoServerError(EmailerError):
    def __init__(self, error_message):
        self.error_message = error_message

    def __unicode__(self):
        return super().__unicode__(self.error_message)