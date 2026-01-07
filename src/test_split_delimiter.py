import unittest

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


class TestSplit_Delimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("This is ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" here", TextType.TEXT)])

    def test_split_bold(self):
        node = TextNode("This is **bold** here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("This is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" here", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("This is _italic_ here", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode("This is ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" here", TextType.TEXT)])

    def test_unmatched(self):
        node = TextNode("This is **wrong", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)