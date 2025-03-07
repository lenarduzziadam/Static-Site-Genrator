from enum import Enum
from conversion import *
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
        
    def props_to_html(self):
        if not self.props:
            return ""
        
        props_list = []
        for key, value in self.props.items():
            props_list.append(f' {key}="{value}"')
        return "".join(props_list)
    
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        else:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All Parent Nodes must have tag")
        if self.children is None:
            raise ValueError("All Parents Need a Child Ol, Son!!!")
        
        parent_node_children = "" 
        for child in self.children:
            parent_node_children += child.to_html()
            
        props_html = self.props_to_html() 
        return f"<{self.tag}{props_html}>{parent_node_children}</{self.tag}>"



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if not block:
            continue
        
        
        if "\n" in block:
            strings = stripped_block.split("\n")
            fixed_block = []
            for string in strings:
                stripped_string = string.strip()
                fixed_block.append(stripped_string)
            stripped_block ="\n".join(fixed_block)
            
        
        new_blocks.append(stripped_block)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(block_text):
    # Check if Heading
    if block_text.startswith('#'):
        # Check if there are no newlines in the text (must be a single line)
        if '\n' not in block_text:
            # Check if it follows heading format (# followed by space)
            parts = block_text.split(' ', 1)
            if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(char == '#' for char in parts[0]):
                return BlockType.HEADING
    
    # Check if Code block
    elif block_text.startswith('```') and block_text.endswith('```'):
        return BlockType.CODE
    
    # Check if Quote block
    lines = block_text.split('\n')
    is_quote = True
    for line in lines:
        if not line.startswith('>'):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
   
    #check if unordered
    is_unordered = True
    #iterates line by line checking for proper start breaks out if condition not there
    for line in lines:
        if not line.startswith('- '):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    #checks if ordered
    is_ordered = True
    
    #enumerates line by line
    for i, line in enumerate(lines):
        #checks if line has proper start of not breaks out if not utilizing i and enumeration to get the proper number
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST #returns only if is_ordered true


    #if nothing else returns as paragraph type 
    return BlockType.PARAGRAPH


#new function
def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("string cannot be empty") 
    if not markdown.startswith("#"):
        raise Exception("ivalid markdown title format, Ol son")
    
    sliced_markdown = markdown[1:].strip()
    
    if len(sliced_markdown) == 0:
        raise Exception("string cannot be blank")
    
    return sliced_markdown