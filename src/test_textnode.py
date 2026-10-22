import unittest
from textnode import TextNode, TextType, text_node_to_html

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_different_text(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_different_type(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        node1 = TextNode("Google", TextType.LINK, "https://google.com" )
        node2 = TextNode("Google", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_none_url(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")

    def test_bold(self):
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.to_html(), "<b>Hello</b>")

    def test_italic(self):
        node = TextNode("Hello", TextType.ITALIC)
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.to_html(), "<i>Hello</i>")

    def test_code(self):
        node = TextNode("x = 5", TextType.CODE)
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.to_html(), "<code>x = 5</code>")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html(node)

        self.assertEqual(
            html_node.to_html(),
            '<a href="https://google.com">Google</a>'
        )

    def test_image(self):
        node = TextNode("Cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/cat.png", "alt": "Cat"}
        )

    def test_invalid_type(self):
        node = TextNode("Hello", "invalid")

        with self.assertRaises(ValueError):
            text_node_to_html(node)

if __name__ == "__main__":
    unittest.main()