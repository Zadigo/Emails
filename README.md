# Emails
|The Emails application regroups a series of functions and classes that can be used to construct mass email patterns off names that would be provided.

Constructing emails

There are many ways to construct an email with the application. First, you can import the preset patterns:

```
from app.mixins.schools import  EDHEC

EDHEC()
```

This class would then search for a file that you would have provided and use the names that it contains to create a list of emails for this school.

    