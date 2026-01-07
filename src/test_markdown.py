import unittest
from markdown import extract_markdown_images, extract_markdown_links

class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images("This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_images_none(self):
        matches = extract_markdown_images("no images")
        self.assertListEqual([], matches)

    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is [a link](https://www.boot.dev)")
        self.assertListEqual([("a link", "https://www.boot.dev")], matches)

    def test_links_none(self):
        matches = extract_markdown_links("no links")
        self.assertListEqual([], matches)

    def test_links_no_images(self):
        matches = extract_markdown_links("![img](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)")
        self.assertListEqual([("link", "https://www.boot.dev")], matches)