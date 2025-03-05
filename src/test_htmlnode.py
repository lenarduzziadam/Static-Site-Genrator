import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        # Note: The order of attributes might vary, so we need to check for both possibilities
        result = node.props_to_html()
        self.assertTrue(
            result == ' href="https://www.google.com" target="_blank"' or 
            result == ' target="_blank" href="https://www.google.com"'
        )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_html_h1(self):
        node = LeafNode("h1", "Hi")
        self.assertEqual(node.to_html(), "<h1>Hi</h1>")
    def test_leaf_html_title(self):
        node = LeafNode("Title", "Suh Dude!")
        self.assertEqual(node.to_html(), "<Title>Suh Dude!</Title>")
    def test_leaf_html_body(self):
        node = LeafNode("body", "Curls for the Girls, More Plates, More Dates!")
        self.assertEqual(node.to_html(), "<body>Curls for the Girls, More Plates, More Dates!</body>")
    def test_leaf_html_ineq_headers(self):
        node = LeafNode("h2", "Hi")
        self.assertNotEqual(node.to_html(), "<h2>Hi</h1>")
        
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_node_with_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()
    def test_parent_node_with_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )
    def test_parent_node_with_props(self):
        child = LeafNode("span", "Child text")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>Child text</span></div>'
        )
    
    def test_deep_nesting(self):
        leaf = LeafNode("span", "Deep text")
        level3 = ParentNode("div", [leaf])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("article", [level2])
        
        self.assertEqual(
            level1.to_html(),
            "<article><section><div><span>Deep text</span></div></section></article>"
        )
    
    def test_parent_no_tag_but_chidren(self):
        with self.assertRaises(ValueError):
            child = LeafNode("p","CHild o Mine")
            node = ParentNode(None, [child])
            node.to_html()
    
    def test_parent_with_mixed_content_types(self):
        text_node1 = LeafNode(None, "Some text")
        span_node = LeafNode("span", "more text")
        text_node2 = LeafNode(None, "and more text")
        parent = ParentNode("div", [text_node1, span_node, text_node2])
        self.assertEqual(
            parent.to_html(),
            "<div>Some text<span>more text</span>and more text</div>"
        )

    def test_content_with_special_characters(self):
        # Test HTML special characters in content
        node = LeafNode("p", "Text with <brackets> & ampersand")
        # Note: In a real-world scenario, you might want to escape these characters
        # This test is checking if your current implementation handles them as-is
        self.assertEqual(
            node.to_html(),
            "<p>Text with <brackets> & ampersand</p>"
        )

    def test_props_with_special_characters(self):
        node = ParentNode(
            "div", 
            [LeafNode("span", "text")], 
            {"data-test": "value & symbols", "class": "item-1 item-2"}
        )
        # The order of attributes might vary, so check the important parts
        html = node.to_html()
        self.assertTrue('<div' in html)
        self.assertTrue('data-test="value & symbols"' in html)
        self.assertTrue('class="item-1 item-2"' in html)
        self.assertTrue('<span>text</span>' in html)

    def test_realistic_html_structure(self):
        # Create a simplified HTML document structure
        title = LeafNode("title", "My Page")
        head = ParentNode("head", [title])
        
        header = ParentNode("header", [LeafNode("h1", "Website Title")])
        paragraph = LeafNode("p", "Welcome to my site")
        main = ParentNode("main", [paragraph])
        footer = ParentNode("footer", [LeafNode("small", "Copyright 2023")])
        
        body = ParentNode("body", [header, main, footer])
        html = ParentNode("html", [head, body])
        
        expected = (
            "<html><head><title>My Page</title></head>"
            "<body><header><h1>Website Title</h1></header>"
            "<main><p>Welcome to my site</p></main>"
            "<footer><small>Copyright 2023</small></footer></body></html>"
        )
        self.assertEqual(html.to_html(), expected)
        
    def test_extremely_deep_nesting(self):
        # Create a deeply nested structure (7 levels)
        content = LeafNode("span", "Deep content")
        level7 = ParentNode("div", [content])
        level6 = ParentNode("div", [level7])
        level5 = ParentNode("div", [level6])
        level4 = ParentNode("div", [level5])
        level3 = ParentNode("div", [level4])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("div", [level2])
        
        expected = "<div><div><div><div><div><div><div><span>Deep content</span></div></div></div></div></div></div></div>"
        self.assertEqual(level1.to_html(), expected)
        
    def test_markdown_to_blocks(self):
            md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
            
    def test_single_block_multiple_lines_md(self):
            md = """
                This is a paragraph.
                It continues on a second line.
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is a paragraph.\nIt continues on a second line."
                ]
            )
            
    def test_edge_case_block_trailing_newline(self):
            md = """
                
                # Heading

                Some text with **bold** markdown.

                - Item 1
                - Item 2
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "# Heading",
                    "Some text with **bold** markdown.",
                    "- Item 1\n- Item 2"

                ]
            )
                   
    def test_empty_block_multiple_lines_md(self):
            md = """
                
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    ""
                ]
            )
    def test_irregular_lines_md(self):
            md = """
                # Heading



                This is a paragraph.


                - Item 1

                - Item 2
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    
                    "# Heading",
                    "This is a paragraph.",
                    "- Item 1",
                    "- Item 2"
                    
                ]
            )
        
    def test_mixed_spaced_lines_md(self):
        md = """
            Paragraph with multiple lines
                indented on the second line

            Final block
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                    
                
            "Paragraph with multiple lines\nindented on the second line",
            "Final block"

                    
            ]
        )    
    def test_single_block_no_newlines_md(self):
            md = """
                This is a single block without any extra spacing.
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                "This is a single block without any extra spacing."
                ]
            ) 
    
class TestBlockTypeDetection(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
        # Test invalid heading (too many #)
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nSome code\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nMultiple\nLines\nOf Code\n```"), BlockType.CODE)
        
        # Test incomplete code block
        self.assertEqual(block_to_block_type("```\nUnclosed code block"), BlockType.PARAGRAPH)
    
    def test_quote_block(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2\n>Line 3"), BlockType.QUOTE)
        
        # Test invalid quote (missing > on some lines)
        self.assertEqual(block_to_block_type(">Line 1\nLine 2 without >"), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        # Basic unordered list
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
        
        # Test with invalid format (missing space)
        self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)
        
        # Test with mixed format (some lines don't start with -)
        self.assertEqual(block_to_block_type("- Item 1\nNot an item\n- Item 3"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Basic ordered list
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), BlockType.ORDERED_LIST)
        
        # Test with incorrect numbering
        self.assertEqual(block_to_block_type("1. First item\n3. Third item"), BlockType.PARAGRAPH)
        
        # Test with non-sequential numbering
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n4. Fourth item"), BlockType.PARAGRAPH)
        
        # Test with invalid format (missing space)
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        # Empty block
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        
        # Just whitespace
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        
        # Block with just a newline
        self.assertEqual(block_to_block_type("\n"), BlockType.PARAGRAPH)
        
        # Mixed content that doesn't match any specific type
        self.assertEqual(block_to_block_type("Some text\n```code```\n> quote"), BlockType.PARAGRAPH)
    
    def test_ordered_list_detailed(self):
        # Basic ordered list with three items
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n3. Third item"), 
            BlockType.ORDERED_LIST
        )
        
        # Long ordered list
        self.assertEqual(
            block_to_block_type("1. Item\n2. Item\n3. Item\n4. Item\n5. Item\n6. Item\n7. Item"), 
            BlockType.ORDERED_LIST
        )
        
        # Ordered list with content after the number
        self.assertEqual(
            block_to_block_type("1. Item with longer text\n2. Another longer item text"), 
            BlockType.ORDERED_LIST
        )
        
        # Test with incorrect starting number (should be 1)
        self.assertEqual(
            block_to_block_type("2. Starting with two\n3. Then three"), 
            BlockType.PARAGRAPH
        )
        
        # Test with non-sequential numbering
        self.assertEqual(
            block_to_block_type("1. First\n3. Third\n4. Fourth"), 
            BlockType.PARAGRAPH
        )
        
        # Test with missing period
        self.assertEqual(
            block_to_block_type("1 Item one\n2 Item two"), 
            BlockType.PARAGRAPH
        )
        
        # Test with missing space after period
        self.assertEqual(
            block_to_block_type("1.First\n2.Second"), 
            BlockType.PARAGRAPH
        )
        
        # Test with correct start but wrong format later
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\nNot part of list"), 
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_detailed(self):
        # Basic unordered list
        self.assertEqual(
            block_to_block_type("- Item one\n- Item two\n- Item three"), 
            BlockType.UNORDERED_LIST
        )
        
        # Single item unordered list
        self.assertEqual(
            block_to_block_type("- Just one item"), 
            BlockType.UNORDERED_LIST
        )
        
        # Long unordered list
        self.assertEqual(
            block_to_block_type("- Item\n- Item\n- Item\n- Item\n- Item\n- Item"), 
            BlockType.UNORDERED_LIST
        )
        
        # Unordered list with longer content
        self.assertEqual(
            block_to_block_type("- This is a longer item with more text\n- Another longer item"), 
            BlockType.UNORDERED_LIST
        )
        
        # Test with missing space after dash
        self.assertEqual(
            block_to_block_type("-No space\n-Still no space"), 
            BlockType.PARAGRAPH
        )
        
        # Test with mixed format (some lines don't start with -)
        self.assertEqual(
            block_to_block_type("- First item\nNot a list item\n- Third item"), 
            BlockType.PARAGRAPH
        )
        
        # Test with different dash character (should fail)
        self.assertEqual(
            block_to_block_type("— Item one\n— Item two"), 
            BlockType.PARAGRAPH
        )
        
        # Test with extra space before dash (should fail)
        self.assertEqual(
            block_to_block_type(" - Item one\n - Item two"), 
            BlockType.PARAGRAPH
        )
    
    def test_heading_detailed(self):
        # Test all valid heading levels
        self.assertEqual(block_to_block_type("# Heading level 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading level 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading level 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading level 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading level 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading level 6"), BlockType.HEADING)
        
        # Test with different content after the heading marker
        self.assertEqual(block_to_block_type("# 123"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# !@#$%^&*()"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# Heading with multiple words"), BlockType.HEADING)
        
        # Test with no space after # (should be paragraph)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
        # Test with too many # characters (should be paragraph)
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        
        # Test with space before # (should be paragraph)
        self.assertEqual(block_to_block_type(" # Space before"), BlockType.PARAGRAPH)
        
        # Test with multiple lines (should be paragraph)
        self.assertEqual(block_to_block_type("# Heading\nSecond line"), BlockType.PARAGRAPH)
        
        # Test with empty content after #
        self.assertEqual(block_to_block_type("# "), BlockType.HEADING)
        
    
    def test_heading_edge_cases(self):
        # Valid headings with different content
        self.assertEqual(block_to_block_type("# Single hash"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Six hashes"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# "), BlockType.HEADING)  # Empty content is still valid
        self.assertEqual(block_to_block_type("###### "), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# 12345"), BlockType.HEADING)  # Numbers
        self.assertEqual(block_to_block_type("# !@#$%^"), BlockType.HEADING)  # Symbols
        
        # Invalid headings - should be paragraphs
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(" # Space before hash"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# \nMulti-line"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# First line\nSecond line"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)  # Just a hash, no space
        self.assertEqual(block_to_block_type("# First\n# Second"), BlockType.PARAGRAPH)  # Multiple headings
        
        # Tricky cases
        self.assertEqual(block_to_block_type("## Heading with # in the middle"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# Heading ending with #"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# Heading with space at end "), BlockType.HEADING)
    
    
    def test_quote_detailed(self):
        # Basic quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        
        # Multi-line quote
        self.assertEqual(
            block_to_block_type("> Line one\n> Line two\n> Line three"), 
            BlockType.QUOTE
        )
        
        # Quote with empty lines (still valid as long as '>' is present)
        self.assertEqual(
            block_to_block_type("> Line one\n> \n> Line three"), 
            BlockType.QUOTE
        )
        
        # Quote with different content types
        self.assertEqual(
            block_to_block_type("> Normal text\n> # Heading style\n> - List item style"), 
            BlockType.QUOTE
        )
        
        # Quote without space after '>' (still valid)
        self.assertEqual(
            block_to_block_type(">No space\n>Still a quote"), 
            BlockType.QUOTE
        )
        
        # Invalid quote - missing '>' on one line
        self.assertEqual(
            block_to_block_type("> First line\nMissing quote marker\n> Third line"), 
            BlockType.PARAGRAPH
        )
        
        # Invalid quote - spaces before '>'
        self.assertEqual(
            block_to_block_type(" > Space before"), 
            BlockType.PARAGRAPH
        )
        
        # Single character quote
        self.assertEqual(
            block_to_block_type("> a"), 
            BlockType.QUOTE
        )
        
        # Empty quote (just the marker)
        self.assertEqual(
            block_to_block_type(">"), 
            BlockType.QUOTE
        )
        
        # Multiple '>' characters (still valid)
        self.assertEqual(
            block_to_block_type(">> Nested quote style"), 
            BlockType.QUOTE
        )
    
    def test_block_edge_cases(self):
        # Heading edge cases
        self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)  # Just a hash, no space
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# \t"), BlockType.HEADING)  # Tab after space
        self.assertEqual(block_to_block_type("# Heading with #s inside # # #"), BlockType.HEADING)
        
        # Quote edge cases
        self.assertEqual(block_to_block_type(">\n>\n>"), BlockType.QUOTE)  # Empty lines but all have >
        self.assertEqual(block_to_block_type("> Line 1\n > Line 2"), BlockType.PARAGRAPH)  # Space before > on line 2
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2"), BlockType.QUOTE)  # No space after > is still valid
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)  # Just a >
        
        # Code block edge cases
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)  # Empty code block
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)  # Single line code
        self.assertEqual(block_to_block_type("``code``"), BlockType.PARAGRAPH)  # Only 2 backticks
        self.assertEqual(block_to_block_type("```code"), BlockType.PARAGRAPH)  # Missing closing backticks
        self.assertEqual(block_to_block_type("code```"), BlockType.PARAGRAPH)  # Missing opening backticks
