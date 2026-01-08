import re
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        # 1. Non-text nodes: keep them as-is and skip further work
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # 2. Get all (alt, url) pairs
        images = extract_markdown_images(node.text)

        # 3. If there are none, just keep the node
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        # 4. Otherwise, work with a temporary text variable
        text = node.text

        # 5. Loop through each (alt, url) from images:
        for alt, url in images:
            # build the exact markdown snippet
            image_md = f"![{alt}]({url})"
            # split the CURRENT text around this image, once
            sections = text.split(image_md, 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""

            # if before isn't empty, add a TEXT node for it
            if len(before) != 0:
                text_node = TextNode(before, TextType.TEXT)
                new_nodes.append(text_node)

             # add an IMAGE node for this image (alt, url)
            image_node = TextNode(alt, TextType.IMAGE, url)
            new_nodes.append(image_node)

            # update text to the remaining part
            text = after

        # after the for alt, url in images loop
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        # 1. Non-text nodes: keep them as-is and skip further work
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # 2. Get all (alt, url) pairs
        links = extract_markdown_links(node.text)

        # 3. If there are none, just keep the node
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        # 4. Otherwise, work with a temporary text variable
        text = node.text

        # 5. Loop through each (alt, url) from links:
        for alt, url in links:
            # build the exact markdown snippet
            link_md = f"[{alt}]({url})"
            # split the CURRENT text around this link, once
            sections = text.split(link_md, 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""

            # if before isn't empty, add a TEXT node for it
            if len(before) != 0:
                text_node = TextNode(before, TextType.TEXT)
                new_nodes.append(text_node)

             # add an LINK node for this link (alt, url)
            link_node = TextNode(alt, TextType.LINK, url)
            new_nodes.append(link_node)

            # update text to the remaining part
            text = after

        # after the for alt, url in links loop
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    old_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    old_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
    return old_nodes