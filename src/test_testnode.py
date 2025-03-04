import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()