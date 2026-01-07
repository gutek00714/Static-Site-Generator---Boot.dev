from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new = node.text.split(delimiter)

            if len(new) % 2 == 0:
                raise ValueError("Invalid Markdown syntax")
            

            for i in range(len(new)):
                text = new[i]
                if text == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    
                    
                    new_nodes.append(TextNode(text, text_type))


    return new_nodes