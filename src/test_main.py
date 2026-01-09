import unittest
from main import markdown_to_html_node, extract_title

class Testmain(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## This is a text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a text</h2></div>")

    def test_quote(self):
        md = """
    > This is a quote
    >This is also a quote
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nThis is also a quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    - Item one
    - Item two
    - Item three
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        )


    def test_ordered_list(self):
        md = """
    1. First
    2. Second
    3. Third
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_extract_title(self):
        md = "# This is a title"
        node = extract_title(md)
        self.assertEqual("This is a title", node)

    def test_extract_title_few_lines(self):
        md = """
# This is a title
## some text
# some text
"""
        node =extract_title(md)
        self.assertEqual("This is a title", node)

    def test_extract_title_wrong_order(self):
        md = """
## Some line
# This is a title
### some line
"""
        node = extract_title(md)
        self.assertEqual("This is a title", node)

    def test_extract_title_no_heading(self):
        md = "This is a title"
        with self.assertRaises(Exception):
            extract_title(md)