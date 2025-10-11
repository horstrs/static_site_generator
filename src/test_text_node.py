import unittest

from text_node import TextNode, TextType

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


    def test_plain_text_to_html_node(self):
        text_node = TextNode("This is a plain text node", TextType.TEXT)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")


    def test_bold_text_to_html_node(self):
        text_node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")


    def test_italic_text_to_html_node(self):
        text_node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")


    def test_code_text_to_html_node(self):
        text_node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")


    def test_link_text_to_html_node(self):
        text_node = TextNode("This is a link text node", TextType.LINK, "www.google.com")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})


    def test_image_text_to_html_node(self):
        text_node = TextNode("This is an image node", TextType.IMAGE, "img.src")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "img.src",
                                           "alt": "This is an image node"})


    def test_invalid_text_type(self):
        text_node = TextNode("This is an invalid text type", "Invalid")
        with self.assertRaises(ValueError):
            text_node.text_node_to_html_node()


    def test_link_missing_url(self):
        text_node = TextNode("This is an invalid link text type", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node.text_node_to_html_node()


    def test_image_missing_url(self):
        text_node = TextNode("This is an invalid image text type", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node.text_node_to_html_node()
    

if __name__ == "__main__":
    unittest.main()
 