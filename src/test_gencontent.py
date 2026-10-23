
import unittest
import os
import tempfile
from gencontent import extract_title, generate_pages_recursive


class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_spaces(self):
        self.assertEqual(
            extract_title("#   Tolkien Fan Club   "),
            "Tolkien Fan Club"
        )

    def test_title_after_other_content(self):
        markdown = "Some paragraph\n\n## Subtitle\n\n# Main Title"
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_no_h1(self):
        markdown = "## Subtitle\n\nSome text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_document(self):
        with self.assertRaises(ValueError):
            extract_title("")



class TestGeneratePagesRecursive(unittest.TestCase):

    def test_recursive_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            content = os.path.join(temp, "content")
            public = os.path.join(temp, "public")
            template = os.path.join(temp, "template.html")

            os.makedirs(os.path.join(content, "blog"))

            with open(template, "w") as f:
                f.write("<html><title>{{ Title }}</title>{{ Content }}</html>")

            with open(os.path.join(content, "index.md"), "w") as f:
                f.write("# Home\n\nHello!")

            with open(os.path.join(content, "blog", "index.md"), "w") as f:
                f.write("# Blog\n\n**Welcome**")

            generate_pages_recursive(content, template, public)

            home_path = os.path.join(public, "index.html")
            blog_path = os.path.join(public, "blog", "index.html")

            self.assertTrue(os.path.isfile(home_path))
            self.assertTrue(os.path.isfile(blog_path))

            with open(home_path) as f:
                home_html = f.read()

            with open(blog_path) as f:
                blog_html = f.read()

            self.assertIn("<title>Home</title>", home_html)
            self.assertIn("<p>Hello!</p>", home_html)
            self.assertIn("<title>Blog</title>", blog_html)
            self.assertIn("<b>Welcome</b>", blog_html)
