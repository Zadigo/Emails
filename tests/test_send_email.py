# from core.senders import SendEmailFromTemplate
# from zemailer.core.senders import SendEmail


# # sender = SendEmail('inglish.contact@gmail.com', 'rogox24197@cyadp.com', 'Some subject')
# sender = SendEmailFromTemplate(
#     'inglish.contact@gmail.com',
#     'science.gooda@yopmail.com',
#     'Some subject',
#     'subject.txt',
#     'test.html', {
#         'sender': 'Google', 
#         'current_date': '1-1-2016'
#     }
# )


import unittest
from zemailer.core.senders import SendEmail


sender = SendEmail

class TestCanSendEmail(unittest.TestCase):
    def setUp(self):
        return super().setUp()
