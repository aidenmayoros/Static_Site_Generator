from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINK = "Link"
    IMAGE = "Image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode instance.")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL.")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image TextNode must have a URL.")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    current_node = ""
    for node in old_nodes:
        if node.text == delimiter:
            new_nodes.append(LeafNode(None, current_node))
            new_nodes.append(text_node_to_html_node(TextNode(delimiter, text_type)))
            current_node = ""
        else:
            current_node += node.text
    new_nodes.append(LeafNode(None, current_node))
    return new_nodes
