from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from markdown import text_to_textnodes
from textnode import text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
import re
import shutil
import os
import sys

def main():
    # node = TextNode(
    #     text="This is some anchor text",
    #     text_type=TextType.LINK,
    #     url="https://www.boot.dev"
    # )

    # print(node)

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    if os.path.exists('./public'):
        shutil.rmtree('./public')

    copy_static('./static', './public')

    # generate_page(
    #     from_path="content/index.md",
    #     template_path="template.html",
    #     dest_path="public/index.html"
    # )

    generate_pages_recursive(
        dir_path_content="./content",
        template_path="./template.html",
        dest_dir_path="./docs",
        basepath = basepath
    )


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
            # inner = [line.lstrip() for line in inner]
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
            quote_children = []

            first_line = True
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

                # add newline between lines (except before the first)
                if not first_line:
                    quote_children.append(LeafNode(None, "\n"))
                first_line = False

                inline_children = text_to_children(text)
                quote_children.extend(inline_children)

            if quote_children:  # only create if we actually have content
                q_node = ParentNode("blockquote", children=quote_children)
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
            if all:
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
            if all:
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



def copy_static(src, dest):
    ### shutil.copytree version (not in assignment)
    # if os.path.exists('./public'):
    #     shutil.rmtree('./public')
    # shutil.copytree('./static', './public', dirs_exist_ok=True)

    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)
    

def extract_title(markdown):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line
            title = title[2:].strip()
            break
    if title is None:
        raise Exception("No title in markdown")
    else:
        return title
    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_file = f.read()

    with open(template_path, "r") as f:
        template_file = f.read()

    node = markdown_to_html_node(markdown_file)
    html = node.to_html()

    title = extract_title(markdown_file)


    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html)
    template_file = template_file.replace('href="/', f'href="{basepath}')
    template_file = template_file.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        new_path = os.path.join(dir_path_content, item)
        # dest_path = new_path.replace("content", "public")
        dest_path = new_path.replace("content", "docs")
        if dest_path.endswith(".md"):
            dest_path = dest_path[:-3] + ".html"
        if os.path.isfile(new_path) and new_path.endswith(".md"):
            generate_page(new_path, template_path, dest_path, basepath)
        elif os.path.isdir(new_path):
            generate_pages_recursive(new_path, template_path, dest_dir_path, basepath)




if __name__ == "__main__":
    main()