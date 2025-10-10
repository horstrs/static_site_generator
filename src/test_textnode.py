import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_two_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2, "Text Type is different")

        node2 = TextNode("This is a link node", TextType.BOLD)
        self.assertNotEqual(node, node2, "Text is different")

        node2 = TextNode("This is a link node", TextType.BOLD, "test.url")
        self.assertNotEqual(node, node2, "Url is different")


    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertIsInstance(node, TextNode)
        self.assertIsNone(node.url)
        self.assertEqual(node, node2)


    def test_repr(self):
        node = TextNode("This is a link node", TextType.LINK, "test.url")
        
        actual = repr(node)
        expected = "TextNode(This is a link node, link, test.url)"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
 