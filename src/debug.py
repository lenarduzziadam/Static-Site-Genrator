from textnode import *

# Test the function directly

test_node = TextNode("**Frodo** and **Legolas**, ... and **Sauron** to a __HIT DATAING SHOW__ at a **Shire new YOU NOWW!!!**", TextType.TEXT)
result = split_nodes_delimiter([test_node], "**", TextType.BOLD)
print(result)
test_node2 = TextNode("Test if _Italics work_ here is the second _italic set_", TextType.TEXT)
result2 = split_nodes_delimiter([test_node2], "_", TextType.ITALIC)
print(result2)
test_node3 = TextNode("Test if **Bold works for more than first entry** here is the second **Bold entry 2** , and finally **bold entry 3**", TextType.TEXT)
result3 = split_nodes_delimiter([test_node3], "**", TextType.BOLD)
print(result3)