import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        assert block_to_block_type("# Heading") == BlockType.HEADING

    def test_heading_levels(self):
        assert block_to_block_type("###### Heading") == BlockType.HEADING
        assert block_to_block_type("#H") == BlockType.PARAGRAPH

    def test_code_block(self):
        markdown = "```\ncode here\n```"
        assert block_to_block_type(markdown) == BlockType.CODE

    def test_quote_block(self):
        markdown = "> quote line\n> another quote"
        assert block_to_block_type(markdown) == BlockType.QUOTE

    def test_unordered_list(self):
        markdown = "- item one\n- item two"
        assert block_to_block_type(markdown) == BlockType.UNORDERED_LIST

    def test_ordered_list(self):
        markdown = "1. first\n2. second\n3. third"
        assert block_to_block_type(markdown) == BlockType.ORDERED_LIST

    def test_paragraph(self):
        assert block_to_block_type("just normal text") == BlockType.PARAGRAPH



if __name__ == "__main__":
    unittest.main()