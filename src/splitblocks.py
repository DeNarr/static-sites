from enum import Enum
import re
from splitnodes import *
from htmlnode import *

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
    elif markdown.startswith("```") and markdown.endswith("```"):
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
    
def markdown_to_html_node(markdown):
    new_nodes = []
    split_blocks = markdown_to_blocks(markdown)
    for block in split_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            # Remove the leading #s and space
            content = re.sub(r'^#+\s+', '', block)
            children = text_to_children(content)
            tag = block_type_to_html_tag(block_type, block)
            new_nodes.append(ParentNode(tag, children))
            continue
        if block_type in [BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST]:
            items = split_list_items(block)
            list_items = []
            for item in items:
                # Clean the item based on list type
                cleaned_item = clean_list_item(item, block_type == BlockType.ORDERED_LIST)
                if cleaned_item:  # Only add non-empty items
                    list_items.append(ParentNode("li", text_to_children(cleaned_item)))
            
            tag = "ol" if block_type == BlockType.ORDERED_LIST else "ul"
            new_nodes.append(ParentNode(tag, list_items))
            continue     
        if block_type == BlockType.CODE:
            # Strip triple backticks and clean the block
            clean_block = block.strip()
            if clean_block.startswith('```'):
                clean_block = clean_block[3:]
            if clean_block.endswith('```'):
                clean_block = clean_block[:-3]
            clean_block = clean_block.strip()

            # Ensure the block ends with a newline
            if not clean_block.endswith('\n'):
                clean_block += '\n'
            
            # Create a code node inside a pre node
            code_node = ParentNode("code", [text_node_to_html_node(TextNode(clean_block, TextType.TEXT))])
            new_nodes.append(ParentNode("pre", [code_node]))
            continue  # Skip the rest of the loop  
        elif block_type == BlockType.QUOTE:
            # Your existing quote handling code
            lines = block.split('\n')
            clean_lines = [line.lstrip('>').strip() for line in lines]
            clean_block = ' '.join(clean_lines)
            children = text_to_children(clean_block)
        else:
            children = text_to_children(block)

        new_nodes.append(ParentNode(block_type_to_html_tag(block_type, block), children))

    return ParentNode("div", new_nodes)


def block_type_to_html_tag(block_type, block):
    if block_type == BlockType.HEADING:
        # Safely find the first space or assume invalid structure
        space_index = block.find(" ")
        heading_level = block.count("#", 0, space_index if space_index > 0 else len(block))
        return f"h{min(heading_level, 6)}"  # Cap the level at 6
    else:
        # Map other block types
        tag_map = {
            BlockType.PARAGRAPH: "p",
            BlockType.UNORDERED_LIST: "ul",
            BlockType.CODE: "pre",
            BlockType.QUOTE: "blockquote",
            BlockType.ORDERED_LIST: "ol"
        }
        return tag_map[block_type]

def text_to_children(text):
    # First, replace newlines with spaces
    text = ' '.join(text.split('\n'))
    
    children = []
    while text:
        # Look for the first matching pattern
        bold_match = re.search(r"\*\*(.*?)\*\*", text)
        italic_match = re.search(r"_(.*?)_", text)
        code_match = re.search(r"`(.*?)`", text)
        
        # Find the earliest match
        matches = [m for m in [bold_match, italic_match, code_match] if m is not None]
        if not matches:
            # No matches found, add remaining text
            children.append(text_node_to_html_node(TextNode(text, TextType.TEXT)))
            break
            
        # Get the earliest match
        match = min(matches, key=lambda m: m.start())
        start = match.start()
        
        # Add text before the match
        if start > 0:
            children.append(text_node_to_html_node(TextNode(text[:start], TextType.TEXT)))
            
        # Determine the type and add the formatted text
        if text[start:].startswith("**"):
            children.append(text_node_to_html_node(TextNode(match.group(1), TextType.BOLD)))
        elif text[start:].startswith("_"):
            children.append(text_node_to_html_node(TextNode(match.group(1), TextType.ITALIC)))
        elif text[start:].startswith("`"):
            children.append(text_node_to_html_node(TextNode(match.group(1), TextType.CODE)))
            
        text = text[match.end():]
    
    return children

def split_list_items(block):
    # Split into lines and remove empty ones
    items = [line.strip() for line in block.split('\n') if line.strip()]
    return items

def clean_list_item(item, is_ordered=False):
    if is_ordered:
        # Remove "1." or any number followed by period
        return re.sub(r'^\d+\.\s*', '', item)
    else:
        # Remove "- " or "* "
        return re.sub(r'^[-*]\s*', '', item)