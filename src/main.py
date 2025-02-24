from textnode import *
from htmlnode import *

def main():
    test_obj = TextNode("This is a text node", TextType.BOLD, "www.google.com")
    print (test_obj)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props="href")
        case TextType.IMAGE:
            return LeafNode("img", "", props=("src", "alt"))
        case _:
            raise Exception ("Not a valid TextType")

if __name__ == "__main__":
    main()