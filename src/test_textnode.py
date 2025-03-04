import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node3, node4)
        
        node3 = TextNode("This is a text node", TextType.NORMAL, None)
        node4 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node3, node4)

    def test_ineq(self):
        node = TextNode("This Text node BRO:", TextType.ITALIC)
        node2 = TextNode("This is a DIFFERENT NODE CHAMP:", TextType.NORMAL)
        self.assertNotEqual(node, node2)
    
    def test_url_ineq(self):    
        node = TextNode("This Text node BRO:", TextType.NORMAL, None)
        node2 = TextNode("This Text node BRO:", TextType.NORMAL, "dkfj")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("Boot.dev logo", TextType.IMAGE, "https://boot.dev/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/logo.png", "alt": "Boot.dev logo"})
    
    def test_basic_delimiter_splitting(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_no_delimiters(self):
        node = TextNode("This is regular text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is regular text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_non_text_nodes(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_missing_closing_delimiter(self):
        node = TextNode("This text has an opening delimiter ` but no closing one", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "No matching delimiter found for `")

    
    
    def test_different_delimiters(self):
        # Test bold syntax
        node = TextNode("This is **bold text** for sure", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " for sure")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
        # Test italic syntax
        node = TextNode("This is _italic text_ for sure", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " for sure")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_delimiters_at_start_or_end(self):
        # Delimiters at the start of the text
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " at the start")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        
        # Delimiters at the end of the text
        node = TextNode("at the end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "at the end ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "Here are multiple images: ![first](https://example.com/1.jpg) and ![second](https://example.com/2.jpg)"
        )
        self.assertListEqual([
            ("first", "https://example.com/1.jpg"),
            ("second", "https://example.com/2.jpg")
        ], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Check out [Boot.dev](https://boot.dev) for coding courses"
        )
        self.assertListEqual([("Boot.dev", "https://boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Here are multiple links: [first link](https://example.com) and [second link](https://another-example.com)"
        )
        self.assertListEqual([
            ("first link", "https://example.com"),
            ("second link", "https://another-example.com")
        ], matches)

    def test_extract_markdown_links_with_images(self):
        # Test that the function correctly distinguishes between images and links
        matches = extract_markdown_links(
            "This has both a ![image](https://image.com) and a [link](https://link.com)"
        )
        self.assertListEqual([("link", "https://link.com")], matches)

    def test_extract_markdown_links_special_characters(self):
        # Test links with special characters in the text portion
        matches = extract_markdown_links(
            "Link with [special characters: @#$%](https://special.com)"
        )
        self.assertListEqual([("special characters: @#$%", "https://special.com")], matches)
        
if __name__ == "__main__":
    unittest.main()