import unittest
from zemailer.validation.dns_verifier import get_mx_records, clean_mx_records


class TestDNSVerifier(unittest.TestCase):
    def test_get_mx_records(self):
        answer = get_mx_records('example.com', 10)
        mx_records = answer.rrset.processing_order()
        self.assertTrue(len(mx_records) > 0)

    def test_clean_mx_records(self):
        result = clean_mx_records('example.fr', 10)
        self.assertListEqual(list(result), [''])


if __name__ == '__main__':
    unittest.main()
