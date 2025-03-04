from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
        
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and self.text_type == other.text_type and
                    self.url == other.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

#classless function meant to work with both classes
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception(f"Invalid text type: {text_node.text_type}")

#new code function (classless)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue 
        text = node.text
        
        start_index = text.find(delimiter)
        if start_index == -1:
            result.append(node)
            continue
            
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            raise Exception(f"No matching delimiter found for {delimiter}")
        
        before_text = text[:start_index]
        delimited_text = text[start_index + len(delimiter) :end_index]
        after_text = text[end_index + len(delimiter):]
        
        if before_text:
            result.append(TextNode(before_text, TextType.TEXT))
        if delimited_text:
            result.append(TextNode(delimited_text, text_type))
        if after_text:
            result.append(TextNode(after_text, TextType.TEXT))
    return result