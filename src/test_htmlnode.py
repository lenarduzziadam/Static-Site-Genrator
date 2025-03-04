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