from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
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

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    expected_num = 1
    if re.match(r"#{1,6} .*", markdown):
        return BlockType.HEADING
    elif re.search(r"^```.*```$", markdown, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^>", markdown):
        for line in lines:
            if not re.match(r"^>", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif re.match(r"^[*-] ", markdown):
        for line in lines:
            if not re.match(r"^[*-] ", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1. ", markdown):
        for line in lines:
            if not re.match(f"{expected_num}. ", line):
                return BlockType.PARAGRAPH
            expected_num += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH