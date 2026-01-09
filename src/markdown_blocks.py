from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING ="heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


# def block_to_block_type(markdown):
#     lines = markdown.split("\n")

#     # Heading
#     if markdown.startswith("#"):
#         count = 0
#         for char in markdown:
#             if char == "#":
#                 count += 1
#             else: 
#                 break

#         if 1 <= count <= 6 and markdown[count] == " ":
#             return BlockType.HEADING
        
#     # Code
#     if markdown.startswith("```\n") and markdown.endswith("```"):
#         return BlockType.CODE
    
#     # Quote
#     if all(line.startswith("> ") for line in lines):
#         return BlockType.QUOTE

#     # Unordered list
#     if all(line.startswith("- ") for line in lines):
#         return BlockType.UNORDERED_LIST

#     # Ordered list
#     is_ordered = True
#     for i, line in enumerate(lines):
#         expected = f"{i+1}. "
#         if not line.startswith(expected):
#             is_ordered = False
#             break
#     if is_ordered:
#         return BlockType.ORDERED_LIST
    
#     # Paragraph
#     return BlockType.PARAGRAPH

def block_to_block_type(block):
    lines = block.split("\n")
    stripped_lines = [line.strip() for line in lines if line.strip()]

    first = stripped_lines[0]

    # 1. CODE
    if first.startswith("```"):
        return BlockType.CODE

    # 2. HEADING
    if first.startswith("#"):
        # count hashes
        count = 0
        for ch in first:
            if ch == "#":
                count += 1
            else:
                break
        # require a space after the hashes
        if count > 0 and len(first) > count and first[count] == " ":
            return BlockType.HEADING

    # 3. QUOTE: every non-empty line starts with ">"
    if all(line.startswith(">") for line in stripped_lines):
        return BlockType.QUOTE

    # 4. UNORDERED LIST: every non-empty line starts with "- " or "* "
    if all(line.startswith("- ") or line.startswith("* ") for line in stripped_lines):
        return BlockType.UNORDERED_LIST

    # 5. ORDERED LIST: every non-empty line starts with "<digits>. "
    def is_ordered(line):
        i = 0
        while i < len(line) and line[i].isdigit():
            i += 1
        return i > 0 and i + 1 < len(line) and line[i] == "." and line[i+1] == " "

    if all(is_ordered(line) for line in stripped_lines):
        return BlockType.ORDERED_LIST

    # 6. Otherwise: PARAGRAPH
    return BlockType.PARAGRAPH