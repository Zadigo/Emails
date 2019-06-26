class EmailerError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self, text=None):
        return text or 'Error'
        
class NoServerError(EmailerError):
    def __init__(self, error_message):
        self.error_message = error_message

    def __unicode__(self):
        return super().__unicode__(self.error_message)

class NoPatternError(TypeError):
    def __unicode__(self):
        return 'A pattern was not provided. Did you forget to provide one? (ex. name.surname)'

    def __str__(self, text=None):
        return self.__unicode__()

class ImproperlyConfiguredError(EmailerError):
    """Error that can be raised when setting is not correct
    in the configuration class
    """
    def __init__(self, message, **params):
        self.message = message
        self.params = params

    def __unicode__(self):
        return super().__unicode__(text=self.message)
