import unittest

from textnode import TextNode, TextType
from split_text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT
        )
        result = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode(
            "Hello _world_!",
            TextType.TEXT
        )
        result = split_nodes_delimiter(
            [node], "_", TextType.ITALIC
        )
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code(self):
        node = TextNode(
            "Use `print()` here",
            TextType.TEXT
        )
        result = split_nodes_delimiter(
            [node], "`", TextType.CODE
        )
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        node = TextNode(
            "**Hello** and **world**",
            TextType.TEXT
        )
        result = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )
        expected = [
            TextNode("Hello", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_unclosed_delimiter(self):
        node = TextNode(
            "Hello **world",
            TextType.TEXT
        )
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node], "**", TextType.BOLD
            )

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )
        self.assertEqual(result, [node])







class TestExtractMarkdown(unittest.TestCase):

    def test_single_image(self):
        text = "An ![image](https://example.com/a.png)"
        expected = [("image", "https://example.com/a.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_multiple_images(self):
        text = "![cat](cat.png) and ![dog](dog.png)"
        expected = [
            ("cat", "cat.png"),
            ("dog", "dog.png"),
        ]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_single_link(self):
        text = "Visit [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_no_matches(self):
        text = "Just regular text."
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_links_ignore_images(self):
        text = "![cat](cat.png) and [Google](https://google.com)"
        self.assertListEqual(
            [("Google", "https://google.com")],
            extract_markdown_links(text),
        )
        self.assertListEqual(
            [("cat", "cat.png")],
            extract_markdown_images(text),
        )


class TestSplitImagesAndLinks(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "Hello ![cat](cat.png) and ![dog](dog.png)",
            TextType.TEXT,
        )
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
        ]
        self.assertListEqual(expected, split_nodes_image([node]))

    def test_split_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [GitHub](https://github.com)",
            TextType.TEXT,
        )
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]
        self.assertListEqual(expected, split_nodes_link([node]))

    def test_no_images(self):
        node = TextNode("Hello world", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_no_links(self):
        node = TextNode("Hello world", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_nodes(self):
        node = TextNode("Already bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))

    def test_repeated_images(self):
        node = TextNode(
            "![cat](cat.png) and ![cat](cat.png)",
            TextType.TEXT,
        )
        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]
        self.assertListEqual(expected, split_nodes_image([node]))

    def test_mixed_images_and_links(self):
        node = TextNode(
            "See ![cat](cat.png) and [Google](https://google.com)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)

        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]
        self.assertListEqual(expected, nodes)



class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word "
            "and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(expected, text_to_textnodes(text))

    def test_plain_text(self):
        text = "Hello world"
        expected = [TextNode("Hello world", TextType.TEXT)]

        self.assertListEqual(expected, text_to_textnodes(text))

    def test_multiple_bold(self):
        text = "**Hello** and **world**"
        expected = [
            TextNode("Hello", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]

        self.assertListEqual(expected, text_to_textnodes(text))

    def test_invalid_markdown(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("Hello **world")
