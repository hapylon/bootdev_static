import re
from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for i in blocks:
        stripped = i.strip()
        if stripped == "":
            continue
        stripped_blocks.append(stripped)
    return stripped_blocks

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD = "unordered list"
    ORD = "ordered list"

def block_to_block_type(md_block):
    if re.match(r"^#{1,6}\s", md_block):
        return BlockType.HEAD
    elif re.match(r"^\'{3}.*?\'{3}$", md_block, re.DOTALL):
        return BlockType.CODE
    elif all(line.strip().startswith('>') for line in md_block.splitlines()): # if line.strip()):
        return BlockType.QUOTE
    elif all(line.strip().startswith('- ') for line in md_block.splitlines()): # if line.strip()):
        return BlockType.UNORD
    elif is_ordered_list(md_block):
        return BlockType.ORD
    else:
        return BlockType.PARA

def is_ordered_list(md_block):
    lines = md_block.splitlines()
    expected_number = 1
    for line in lines:
        match = re.match(r"^(\d+\.\s)", line.strip())
        if not match:
            return False
        actual_number = int(match.group(1))
        if actual_number == expected_number:
            expected_number +=1
        else:
            return False
    return expected_number > 1
