from enum import Enum

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
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
    
def block_to_block_type(block_text):
    match block_text.text_type:
            case BlockType.HEADING:
                pass #1-6 '#' characters
            case BlockType.CODE:
                pass #must start with ``` and end with ``` backticks
            case BlockType.QUOTE:
                pass #every line in a quote block must start with '>'
            case BlockType.UNORDERED_LIST:
                pass #every line in unordered lists must start with - followed by a space (- list_item_one) 
            case BlockType.ORDERED_LIST:
                pass #every line in an ordered list must begin with a number then have a . and space (7. lucky)
            case _:
                pass #block is normal paragrpah if this is case <p> </p>