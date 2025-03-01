import unittest
from generatepage import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_generate_page(self):
        from_path = "content/index.md"
        template_path = "template.html"
        dest_path = "public/index.html"
        generate_page(from_path, template_path, dest_path)