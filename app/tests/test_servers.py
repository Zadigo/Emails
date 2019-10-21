import os
import unittest

from app.core.servers import BaseServer, Gmail, Outlook


class TestServers(unittest.TestCase):
    def setUp(self):
        user = os.environ.get('EMAIL_USER')
        password = os.environ.get('EMAIL_PASSWORD')
        self.email_server = BaseServer('smtp.gmail.com', 587, user, password)

    def test_connection_successful(self):
        self.assertIsNotNone(self.email_server.smtp_connection)

if __name__ == "__main__":
    unittest.main()
