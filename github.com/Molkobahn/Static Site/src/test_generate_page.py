import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_files(self):
        markdown = "# Header\nThis is some text.\nThe end!"
        self.assertEqual(extract_title(markdown), "Header")

    def test_extract_files_exception(self):
        markdown2 = "## Header\nThis is some text.\nThe end!"
        with self.assertRaises(Exception):
            extract_title(markdown2)