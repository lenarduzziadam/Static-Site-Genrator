from textnode import *

# Test the function directly

test_node = TextNode("... and **Legolas**, ...", TextType.TEXT)
result = split_nodes_delimiter([test_node], "**", TextType.BOLD)
print(result)