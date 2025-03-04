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