from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        images = extract_markdown_images(old_node.text)
        if not images:  # If no links were found
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link_text, link_url in images:
            # Split on the current link
            full_link_pattern = f"![{link_text}]({link_url})"
            parts = remaining_text.split(full_link_pattern, 1)
            
            # Add the text before the link (if any)
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link itself
            split_nodes.append(TextNode(link_text, TextType.IMAGE, link_url))
            
            # Update remaining_text for next iteration
            remaining_text = parts[1] if len(parts) > 1 else ""
        # After the for loop ends
        if remaining_text:  # If there's any text left after processing all links
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        links = extract_markdown_links(old_node.text)
        if not links:  # If no links were found
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link_text, link_url in links:
            # Split on the current link
            full_link_pattern = f"[{link_text}]({link_url})"
            parts = remaining_text.split(full_link_pattern, 1)
            
            # Add the text before the link (if any)
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link itself
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Update remaining_text for next iteration
            remaining_text = parts[1] if len(parts) > 1 else ""
        # After the for loop ends
        if remaining_text:  # If there's any text left after processing all links
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Each step uses the results of the previous step
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # Handle delimiters in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def print_nodes(nodes):
    for i, node in enumerate(nodes):
        print(f"{i}. {node.text} ({node.text_type})")