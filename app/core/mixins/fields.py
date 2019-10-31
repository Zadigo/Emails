import re

class EmailField:
    """To create more complexe patterns, use this field
    with a regex pattern that will parse the given email.

    Example
    -------

    To parse `test.google@gmail.com`, the regex
    would be `^(\\w+)(\\.)(\\w+)\\@(gmail)\\.(\\w+)` with the captured
    groups beeing `('test', '.', 'google', 'gmail', 'com')`.

    This helper function is useful for parsing and creating patterns
    off more complexe email patterns.
    """
    def __init__(self, email, pattern):
        is_match = re.search(pattern, email)
        if is_match:
            # Get the tuple of 
            # the matching value
            self.groups = is_match.groups()

    def __str__(self):
        return str(self.groups)
