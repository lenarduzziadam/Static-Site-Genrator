import re
from enum import Enum

from htmlnode import *


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
    #grabs nodes within old_nodes list one by one
    for node in old_nodes:
        #chekcs if nodes text_type is not TEXT if so will simply append the result and continue to next iteration (node)
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue 
        
        #assigns text of current node to text
        text = node.text
        
        #locates the first occurence of the dilimeter in the text
        start_index = text.find(delimiter)
        
        #if the dilimeter is not found then there is nothing to split,
        #so thus we simply add to the result and move to next iteration
        if start_index == -1:
            result.append(node)
            continue
        
        #looks for closing dilimiter which would be after the starting dilimiter searching till the end of the list start_index + (len(delimiter))
        end_index = text.find(delimiter, start_index + len(delimiter))
        
        #if no end_index then raises exception in terminal making note that no delimiter was found, making note of Error in markdown
        if end_index == -1:
            raise Exception(f"No matching delimiter found for {delimiter}")
        
        #splitting text in three parts :
        #   -before_text: text prior to opening dilimiter
        #   -delimited_text: text between dilimiters (which will also get text type)
        #   -after_text: text after closing delimiter
        before_text = text[:start_index]  
        delimited_text = text[start_index + len(delimiter) :end_index]
        after_text = text[end_index + len(delimiter):]
        
        #creates new text node for each part if not empty
        if before_text:
            result.append(TextNode(before_text, TextType.TEXT))
        if delimited_text:
            result.append(TextNode(delimited_text, text_type))
        if after_text:
            result.append(TextNode(after_text, TextType.TEXT))
        
    return result


#classless function again, regex guide below for referece:

# Regex Quick Reference:
# .        - any character except newline
# \w       - word character [a-zA-Z0-9_]
# \d       - digit [0-9]
# \s       - whitespace (space, tab, newline)
# [abc]    - character class (matches a, b, or c)
# [^abc]   - negated character class (matches anything except a, b, or c)
# ^        - start of string
# $        - end of string
# *        - zero or more repetitions
# +        - one or more repetitions
# ?        - zero or one repetition
# {n}      - exactly n repetitions
# {n,}     - n or more repetitions
# {n,m}    - between n and m repetitions
# (...)    - capturing group
# (?:...)  - non-capturing group
# a|b      - match a or b
#  |       NOTE: the above seperator for match is | specificlaly 
# \        - escape special characters

def extract_markdown_images(text):
    ## pattern for image alt text and url extraction:
    # !            - literal exclamation mark that indicates a markdown image
    # \[           - literal opening square bracket (escaped with \)
    # ([^\[\]]*)   - capture group 1: any characters except square brackets, * means zero or more
    # \]           - literal closing square bracket (escaped with \)
    # \(           - literal opening parenthesis (escaped with \)
    # ([^\(\)]*)   - capture group 2: any characters except parentheses, * means zero or more
    # \)           - literal closing parenthesis (escaped with \)
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    # Updated regex to handle nested parentheses in URLs
    # We use negative lookbehind (?<!) to ensure we don't match image markdown
    pattern = r"(?<!!)\[(.*?)\]\(((?:[^()]*|\([^()]*\))*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    #grabs nodes within old_nodes list one by one
    for node in old_nodes:
        #chekcs if nodes text_type is not TEXT if so will simply append the result and continue to next iteration (node)
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue 
        
        images = extract_markdown_images(node.text)
        
        if not images:
            result.append(node)
            continue
            
        current_text = node.text
        
        for alt_text, url, in images:
            # The full markdown for this image looks like: ![alt_text](url)
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the current_text at the image markdown
            # This gives us the text before the image and the text after
            parts = current_text.split(image_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0],TextType.TEXT))
            
            result.append(TextNode(alt_text,TextType.IMAGE, url))
            
            # Update current_text to be whatever remains after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
                
        # Don't forget to add any remaining text after processing all images
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
    
    return result

def split_nodes_link(old_nodes):
    result = []
    #grabs nodes within old_nodes list one by one
    for node in old_nodes:
        #chekcs if nodes text_type is not TEXT if so will simply append the result and continue to next iteration (node)
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        
        if not links:
            result.append(node)
            continue
            
        current_text = node.text
        
        for link_text, url, in links:
            # The full markdown for this image looks like: ![alt_text](url)
            link_markdown = f"[{link_text}]({url})"
            
            # Split the current_text at the image markdown
            # This gives us the text before the image and the text after
            parts = current_text.split(link_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0],TextType.TEXT))
            
            result.append(TextNode(link_text,TextType.LINK, url))
            
            # Update current_text to be whatever remains after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
                
        # Don't forget to add any remaining text after processing all images
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT)) 
    
    return result

#combining function time classless again CHAMP
def text_to_textnodes(text):
    #single text node defined with text value
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    #calling existing node image and node line split function
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes


def handle_code_block(block):
    # Remove the ``` markers
    lines = block.strip().split('\n')
    # Skip the first and last lines that contain ```
    code_content = '\n'.join(lines[1:-1])
    
    # Ensure the content ends with a newline
    if not code_content.endswith('\n'):
        code_content += '\n'
        
    # Create the nested structure - code inside pre
    code_node = LeafNode("code", code_content)
    pre_node = ParentNode("pre", [code_node])
    
    return pre_node

def text_to_children(text):
    # Convert the text to a TextNode
    text_node = TextNode(text, TextType.TEXT)
    
    # Split the node to process inline markdown
    inline_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    inline_nodes = split_nodes_delimiter(inline_nodes, "_", TextType.ITALIC)
    inline_nodes = split_nodes_delimiter(inline_nodes, "`", TextType.CODE)
    # Add other delimiters if needed
    
    # Convert each TextNode to HTMLNode
    html_nodes = []
    for node in inline_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

def parse_quote_block(markdown_text):
    """
    Parses a markdown block containing a quote into a nested `blockquote` HTML structure.
    
    Args:
        markdown_text (str): The raw text of the quote block, including any `>` characters.

    Returns:
        ParentNode: The parsed `blockquote` node with children appropriately structured.
    """
    lines = markdown_text.split("\n")
    root_node = ParentNode("blockquote")
    current_node = root_node
    for line in lines:
        if line.strip():  # Skip completely empty lines
            depth = len(line) - len(line.lstrip('>'))  # Count the `>` for nesting
            content = line.lstrip('>').strip()  # Remove `>` and whitespace
            while depth > 1:  # Handle nested blockquotes if depth > 1
                # Create a child blockquote node if not present
                child = ParentNode("blockquote")
                if not current_node.has_children():
                    current_node.add_child(child)
                current_node = current_node.children[-1]  # Dive into the child node
                depth -= 1
            current_node.add_child(TextNode(content))  # Add the inner text as a child
        else:
            current_node.add_child(TextNode(""))  # Add empty lines as text nodes

    return root_node

def markdown_to_html_node(markdown):
    blocked_markdown = markdown_to_blocks(markdown)
    child_node = None
    parent_node = ParentNode("div", [])
    
    # For debugging
    with open("debug.txt", "w") as f:
        f.write(f"Number of blocks: {len(blocked_markdown)}\n")
    
    #processes each block in markdown    
    for block in blocked_markdown:
        if not block.strip():  # Skip completely empty blocks
            continue
        
        #determines what type of block we are dealing with and sets said value to block)type
        block_type = block_to_block_type(block)
        child_node = None #reset child node at the start of each iteration (but after the skip 'if not' above)
        
             
        match block_type:
            # Check if this block is actually a list (even if block_to_block_type doesn't recognize it)
                
            case BlockType.PARAGRAPH:
                 # For paragraphs, join all lines with spaces and remove extra whitespace
                paragraph_text = ' '.join([line.strip() for line in block.split('\n') if line.strip()])
                
                # Process inline markdown (bold, italic, code) within the paragraph text
                children = text_to_children(paragraph_text)
                
                # Create paragraph node with the processed children
                child_node = ParentNode("p", children)
            
            case BlockType.HEADING:
                heading_level = 0
                for char in block:
                    if char == '#':
                        heading_level += 1
                    else:
                        break
                text_content = block[heading_level:].strip()
                
                # Create appropriate h1-h6 node
                child_node = ParentNode(f"h{heading_level}", text_to_children(text_content))
            
            case BlockType.CODE:
                if block_type == BlockType.CODE:
                    child_node = handle_code_block(block)
            
            case BlockType.UNORDERED_LIST:
                    # Create ul node with li children
                    li_nodes = []
                    for item in block.split('\n'):
                        if item.strip():  # Skip empty lines
                            # Strip the '* ' or '- ' prefix
                            if item.strip().startswith('* '):
                                item_text = item.strip()[2:]
                                li_nodes.append(ParentNode("li", text_to_children(item_text)))
                            elif item.strip().startswith('- '):
                                item_text = item.strip()[2:]
                                li_nodes.append(ParentNode("li", text_to_children(item_text)))
                    if li_nodes:  # Only add if we have list items
                        child_node = ParentNode("ul", li_nodes)
            
            case BlockType.ORDERED_LIST:
                # Create ol node with li children
                li_nodes = []
                for item in block.split('\n'):
                    if item.strip():  # Skip empty lines
                        # Find the period after the number
                        text_content = item[item.find('.')+1:].strip()
                        li_nodes.append(ParentNode("li", text_to_children(text_content)))
                child_node = ParentNode("ol", li_nodes)
            
            case BlockType.QUOTE:
                # Strip leading '>' from each line and join them into a single block
                stripped_content = " ".join(line.lstrip("> ") for line in block.split("\n"))
                    
                # Use text_to_children to parse inline markdown within the quote
                child_node = ParentNode("blockquote", text_to_children(stripped_content))
                
        if child_node:
            parent_node.children.append(child_node)
        
        
        for child in parent_node.children:
            f.write(f"Child: {child.to_html()}\n")
    
    return parent_node
            