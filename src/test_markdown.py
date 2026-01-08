import unittest
from textnode import TextNode, TextType
from markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_before(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_with_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and link [link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and link [link](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode(
            "This was an image here and a link [link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This was an image here and a link [link](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            new_nodes,
        )

    # def test_split_link(self):
    #     node = TextNode(
    #         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with a link ", TextType.TEXT),
    #             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #             TextNode(" and ", TextType.TEXT),
    #             TextNode(
    #                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #             ),
    #         ],
    #         new_nodes,
    #     )

    # def test_split_link_no_before(self):
    #     node = TextNode(
    #         "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #             TextNode(" and ", TextType.TEXT),
    #             TextNode(
    #                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #             ),
    #         ],
    #         new_nodes,
    #     )

    # def test_split_link_with_image(self):
    #     node = TextNode(
    #         "This is text with a link [to boot dev](https://www.boot.dev) and image ![image](https://i.imgur.com/zjjcJKZ.png)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with a link ", TextType.TEXT),
    #             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #             TextNode(" and image ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
    #         ],
    #         new_nodes,
    #     )

    # def test_split_link_with_no_link(self):
    #     node = TextNode(
    #         "There was a link and image ![image](https://i.imgur.com/zjjcJKZ.png)",
    #         TextType.TEXT,
    #     )
    #     new_nodes = split_nodes_link([node])
    #     self.assertListEqual(
    #         [
    #             TextNode("There was a link and image ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
    #         ],
    #         new_nodes,
    #     )

    def test_text_to_textnodes_full(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()