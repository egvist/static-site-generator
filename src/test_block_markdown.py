
import unittest
from block_markdown import markdown_to_blocks
from block_markdown import BlockType, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):

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

    def test_extra_newlines(self):
        md = "First\n\n\n\nSecond\n\n\n\n\n\nThird"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First", "Second", "Third"]
        )

    def test_whitespace(self):
        md = "  First block  \n\n   Second block   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"]
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])

    def test_single_block(self):
        md = "# Hello World"
        self.assertEqual(
            markdown_to_blocks(md),
            ["# Hello World"]
        )

    def test_list_stays_together(self):
        md = "- Apple\n- Banana\n- Orange"
        self.assertEqual(
            markdown_to_blocks(md),
            ["- Apple\n- Banana\n- Orange"]
        )






class TestBlockToBlockType(unittest.TestCase):

    def test_headings(self):
        for level in range(1, 7):
            block = f"{'#' * level} Heading"
            self.assertEqual(
                block_to_block_type(block),
                BlockType.HEADING,
            )

    def test_invalid_heading(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("#No space"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote(self):
        block = "> Hello\n> World"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        block = "- Apple\n- Banana\n- Orange"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        block = "1. Apple\n2. Banana\n3. Orange"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_list(self):
        block = "1. Apple\n3. Banana"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_invalid_unordered_list(self):
        block = "- Apple\nBanana"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )
