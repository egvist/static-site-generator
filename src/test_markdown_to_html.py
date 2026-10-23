
import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

    def test_heading(self):
        md = "## Hello **world**"

        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h2>Hello <b>world</b></h2></div>"
        )

    def test_quote(self):
        md = "> Hello\n> **world**"

        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><blockquote>Hello <b>world</b></blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- Apple\n- **Banana**"

        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ul><li>Apple</li><li><b>Banana</b></li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. Apple\n2. Banana"

        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ol><li>Apple</li><li>Banana</li></ol></div>"
        )

