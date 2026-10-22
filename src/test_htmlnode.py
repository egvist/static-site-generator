import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
            node = HTMLNode()
            self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode(props={"class": "container"})
        self.assertEqual(
            node.props_to_html(),
            ' class="container"'
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(
            node.to_html(),
            "<b>Bold text</b>"
        )

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])

        self.assertEqual(
            parent.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])

        self.assertEqual(
            parent.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_multiple_children(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " normal "),
                LeafNode("i", "Italic")
            ]
        )

        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> normal <i>Italic</i></p>"
        )

    def test_props(self):
        parent = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container"}
        )

        self.assertEqual(
            parent.to_html(),
            '<div class="container"><p>Hello</p></div>'
        )

    def test_no_tag(self):
        parent = ParentNode(None, [LeafNode("p", "Hello")])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_no_children(self):
        parent = ParentNode("div", [])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_none_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()

if __name__ == "__main__":
    unittest.main()