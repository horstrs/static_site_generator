import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_no_param(self):
        node = HTMLNode()
        
        self.assertIsInstance(node, HTMLNode)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)


    def test_repr(self):
        prop_link = {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    }
        
        node = HTMLNode(tag="a", value="link", props=prop_link)
        actual = repr(node)
        expected = "HTMLNode(a, link, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(actual, expected, "string representation incorrect")


    def test_init(self):        
        node = HTMLNode(tag="a", value="b", props="c", children="d")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "b")
        self.assertEqual(node.props, "c")
        self.assertEqual(node.children, "d")


    def test_props_to_html(self):
        prop_link = {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    }
        node = HTMLNode(props=prop_link)
        actual = node.props_to_html()
        expected = " href='https://www.google.com' target='_blank'"

        self.assertEqual(actual, expected, "props_to_html method didn't converted dictionary correcty")


class TestLeafNode(unittest.TestCase):
    def test_no_param(self):
        try:
            LeafNode()
            self.fail("Exception expected")
        except TypeError:
            pass


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        actual = node.to_html()
        expected = "<p>Hello, world!</p>"
        self.assertEqual(actual, expected)


    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
 