from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING ="heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")

    # Heading
    if markdown.startswith("#"):
        count = 0
        for char in markdown:
            if char == "#":
                count += 1
            else: 
                break

        if 1 <= count <= 6 and markdown[count] == " ":
            return BlockType.HEADING
        
    # Code
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    
    # Quote
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    is_ordered = True
    for i, line in enumerate(lines):
        expected = f"{i+1}. "
        if not line.startswith(expected):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    # Paragraph
    return BlockType.PARAGRAPH