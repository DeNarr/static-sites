import unittest
from splitblocks import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_heading(self):
        block = "#heading"  # missing space
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "####### heading"  # too many #s
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_code(self):
        block = "```\ncode"  # missing closing backticks
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_quote(self):
        block = "> quote\nnot a quote"  # second line missing >
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_lists(self):
        block = "* item\nno item"  # second line missing *
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. item\n3. item"  # wrong number sequence
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_complex_valid_blocks(self):
        block = "### My Heading, with punctuation! (2023)"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "* Item 1, with punctuation!\n* Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. Complex item!\n2. Another, with dots..."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)



if __name__ == "__main__":
    unittest.main()