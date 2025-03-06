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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_basic(self):
        # Test a single image in the middle of text
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        # Test text with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_non_text_node(self):
        # Test that non-TEXT nodes are left unchanged
        node = TextNode("existing image", TextType.IMAGE, "https://example.com/img.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_images_multiple(self):
        # Test text with multiple images
        node = TextNode(
            "Here's ![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.png) for testing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here's ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://example.com/img2.png"),
                TextNode(" for testing", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        # Test image at the beginning of text
        node = TextNode(
            "![first image](https://example.com/first.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first image", TextType.IMAGE, "https://example.com/first.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        # Test image at the end of text
        node = TextNode(
            "Text followed by ![last image](https://example.com/last.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("last image", TextType.IMAGE, "https://example.com/last.png"),
            ],
            new_nodes,
        )
    
    def test_split_links_basic(self):
        # Test a single link in text
        node = TextNode(
            "Check out [this site](https://example.com) for more info",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("this site", TextType.LINK, "https://example.com"),
                TextNode(" for more info", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        # Test multiple links in text
        node = TextNode(
            "Visit [example1](https://example1.com) or [example2](https://example2.com) today",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("example1", TextType.LINK, "https://example1.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("example2", TextType.LINK, "https://example2.com"),
                TextNode(" today", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        # Test text with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_links_at_beginning(self):
        # Test link at beginning of text
        node = TextNode(
            "[Start here](https://start.com) and continue reading",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start here", TextType.LINK, "https://start.com"),
                TextNode(" and continue reading", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        # Test link at end of text
        node = TextNode(
            "Read to the end and [click here](https://end.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Read to the end and ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "https://end.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        # Test text that is only a link
        node = TextNode(
            "[standalone link](https://alone.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("standalone link", TextType.LINK, "https://alone.com"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        # Test consecutive links without text between them
        node = TextNode(
            "[first link](https://first.com)[second link](https://second.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://first.com"),
                TextNode("second link", TextType.LINK, "https://second.com"),
            ],
            new_nodes,
        )
        
    def test_split_links_with_empty_text(self):
        # Test links with empty text
        node = TextNode(
            "Before [](https://empty.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://empty.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_markdown_in_text(self):
        # Test links that contain markdown syntax in their text
        node = TextNode(
            "Check [**bold link**](https://bold.com) and [*italic link*](https://italic.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("**bold link**", TextType.LINK, "https://bold.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("*italic link*", TextType.LINK, "https://italic.com"),
            ],
            new_nodes,
        )

    def test_split_images_with_links_text(self):
        # Test images with link-like text that shouldn't be parsed as links
        node = TextNode(
            "Image with link-like alt text: ![Here's a [link]](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with link-like alt text: ", TextType.TEXT),
                TextNode("Here's a [link]", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_multiple_node_processing(self):
        # Test that the function correctly processes multiple nodes
        node1 = TextNode(
            "First node with [a link](https://first.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Second node with no links",
            TextType.TEXT,
        )
        node3 = TextNode(
            "Third node with [another link](https://third.com)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node1, node2, node3])
        
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://first.com"),
                TextNode("Second node with no links", TextType.TEXT),
                TextNode("Third node with ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://third.com"),
            ],
            new_nodes,
        )
    def test_split_images_with_special_characters(self):
        # Test images with special characters in alt text
        node = TextNode(
            "Image with special chars: ![Alt & text with: semicolons](https://example.com/special.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with special chars: ", TextType.TEXT),
                TextNode("Alt & text with: semicolons", TextType.IMAGE, "https://example.com/special.png"),
            ],
            new_nodes,
        )


    def test_split_images_at_beginning(self):
        # Test image at beginning of text
        node = TextNode(
            "![First image](https://example.com/first.png)Followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First image", TextType.IMAGE, "https://example.com/first.png"),
                TextNode("Followed by text", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_plain_text(self):
        # Test with plain text only
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is plain text", TextType.TEXT)],
            nodes
        )

    def test_text_to_textnodes_bold(self):
        # Test with bold text
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_mixed_content(self):
        text = "This is **bold** and _italic_ text with `code`"
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
    
        self.assertListEqual(expected_nodes, nodes)

    def test_text_to_textnodes_code(self):
        # Test with code
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ],
            nodes
        )
    
    def test_text_to_textnodes_italic(self):
        # Test with italic text
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ],
            nodes
        )
    
    def test_text_to_textnodes_link_with_nested_parentheses(self):
        # Test with a link that contains nested parentheses in the URL
        text = "Check out this [link](https://example.com/path(nested)/more)"
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/path(nested)/more")
        ]
        
        self.assertListEqual(expected_nodes, nodes)
    
    def test_consecutive_links(self):
        text = "Visit [first](https://first.com) and [second](https://second.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("first", TextType.LINK, "https://first.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "https://second.com")
        ]
        self.assertEqual(expected, nodes)
        
    def test_links_with_special_chars(self):
        text = "See [example](https://example.com/path?query=value&other=123)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("example", TextType.LINK, "https://example.com/path?query=value&other=123")
        ]
        self.assertEqual(expected, nodes)

    def test_links_with_special_chars(self):
        text = "See [example](https://example.com/path?query=value&other=123)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("example", TextType.LINK, "https://example.com/path?query=value&other=123")
        ]
        self.assertEqual(expected, nodes)

    def test_empty_link_parts(self):
        text = "Empty text [](https://example.com) and empty URL [text]()"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Empty text ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" and empty URL ", TextType.TEXT),
            TextNode("text", TextType.LINK, "")
        ]
        self.assertEqual(expected, nodes)


class TestBlockToHTML(unittest.TestCase) :   
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
if __name__ == "__main__":
    unittest.main()