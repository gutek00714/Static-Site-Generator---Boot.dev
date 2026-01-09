from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from markdown import text_to_textnodes
from textnode import text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
import re

def main():
    node = TextNode(
        text="This is some anchor text",
        text_type=TextType.LINK,
        url="https://www.boot.dev"
    )

    print(node)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []   # will hold block-level ParentNodes

    for block in blocks:
        if not block.strip():
            continue
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            normalized = block.replace("\n", " ")
            normalized = re.sub(r"\s+", " ", normalized).strip()
            # 1. make inline children from the block text
            inline_children = text_to_children(normalized)
            # 2. make a <p> node with those children
            p_node = ParentNode("p", children=inline_children)
            # 3. add it to the list
            children.append(p_node)
        
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner = lines[1:-1]
            inner = [line.lstrip() for line in inner]
            code_text = "\n".join(inner) + "\n"
            code_text_node = TextNode(code_text, TextType.CODE)
            code_node = text_node_to_html_node(code_text_node)
            pre_node = ParentNode("pre", children=[code_node])
            children.append(pre_node)

        elif block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break
            text = block[count:].lstrip()
            inline_children = text_to_children(text)
            tag = f"h{count}"
            h_node = ParentNode(tag, children=inline_children)
            children.append(h_node)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            first_quote = True
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("> "):
                    text = line[2:]
                elif line.startswith(">"):
                    text = line[1:]
                else:
                    text = line

                # add newline between blockquotes (but not before the first)
                if not first_quote:
                    children.append(LeafNode(None, "\n"))
                first_quote = False

                inline_children = text_to_children(text)
                q_node = ParentNode("blockquote", children=inline_children)
                children.append(q_node)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            all = []
            for line in lines:
                stripped = line.lstrip()
                if stripped.startswith("- "):
                    item_text = stripped[2:]
                elif stripped.startswith("* "):
                    item_text = stripped[2:]
                else:
                    continue
                inline_children = text_to_children(item_text)
                li_node = ParentNode("li", children=inline_children)
                all.append(li_node)
            ul_node = ParentNode("ul", children=all)
            children.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            all = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                dot_index = line.find(". ")
                if dot_index == -1:
                    continue
                item_text = line[dot_index + 2:]
                inline_children = text_to_children(item_text)
                li_node = ParentNode("li", children=inline_children)
                all.append(li_node)
            ol_node = ParentNode("ol", children=all)
            children.append(ol_node)


    parent = ParentNode("div", children=children)
    return parent



def text_to_children(text):
    htmlnode_list = []
    textnodes = text_to_textnodes(text)
    for tn in textnodes:
        htmlnode_list.append(text_node_to_html_node(tn))
    return htmlnode_list








if __name__ == "__main__":
    main()