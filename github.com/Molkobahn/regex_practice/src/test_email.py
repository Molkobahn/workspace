# test_email.py
import unittest
from regex_practice import extract_email  # make sure this matches your file name

class TestEmailExtractor(unittest.TestCase):
    def test_basic_emails(self):
        text = "Contact us at hello.world@example.com or support@university.edu"
        result = extract_email(text)
        expected = ["hello.world@example.com", "support@university.edu"]
        self.assertEqual(result, expected)
    
    def test_no_emails(self):
        text = "This text has no emails"
        result = extract_email(text)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()