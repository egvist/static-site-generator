import unittest
from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()