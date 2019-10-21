# Emails
|The Emails application regroups a series of functions and classes that can be used to construct mass email patterns off names that would be provided.

In order to perform requests to web, you need to set the configuration dictionnary that will be used by these classes in order to perform the different actions.

These email classes require authentication such as email and password in order to perform.

```
from zemailer import configuration

configuration.set_credentials(user, password)
...
```

NOTE: When using .set_credentials(), you are setting the credentials for the default server which is Gmail.

Once you've set the credentials, you are now ready to call the email classes.

## Sending emails

Sending an email is as simple as calling `SendEmail()` or `SendEmailWithAttachment()`.

You must provide a __sender__, a __receiver__ (which are email addresses), the __subject__ of the email and other additional pieces of information that you wish to attach to the email.

```
from zemailer import configuration
from zemailer import SendEmail

configuration.set_crendentials(user, password)

subject = 'My first email'

SendEmail(email@gmail.com, email@gmail.com, subject)
```

By executing the class, the .\_\_init\_\_(sender, receiver, subject, **kwargs) is called automatically, such as the server backend to perform the request.

However, the main reason zemailer was created was to simplify and accelerate the construction of email addresses out of anybody's names.

# Constructing emails

There are many ways to construct an email with the application. The first easiest way is to import the numerous preset patters from the mixins:

```
from zemailer.app.mixins.schools import  EDHEC

EDHEC(file_path=None)
```

From there, you need to provide a file path containing a list of names in order to create a list of emails using the specific preset.

You can easily override a preset by subclassing it:

```
class AnotherSchool(EDHEC):
    pass
```

You can then override the `pattern` and the `domain` attributes.

The pattern, is the style around which you wish to construct the email. For example __eugenie.bouchard__ or __eugenie-bouchard__ while the domain is self explanatory e.g. google.com.
    