import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        child_node = LeafNode("span", "child")
        node = HTMLNode(tag=None, value="link", children=[child_node], props=prop_link)
        actual = repr(node)
        expected = "HTMLNode(None, link, [HTMLNode(span, child, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(actual, expected, "string representation incorrect")


    def test_child_not_list(self):
        with self.assertRaises(TypeError):
            HTMLNode(children="a")


    def test_init(self):        
        node = HTMLNode(tag="a", value="b", props="c", children=["d"])
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "b")
        self.assertEqual(node.props, "c")
        self.assertEqual(node.children, ["d"])


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
        with self.assertRaises(TypeError):
            LeafNode()
            self.fail("Exception expected")


    def test_init(self):
        actual = LeafNode("tag", "value", "props")
        self.assertEqual(actual.tag, "tag")
        self.assertEqual(actual.value, "value")
        self.assertEqual(actual.props, "props")


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        actual = node.to_html()
        expected = "<p>Hello, world!</p>"
        self.assertEqual(actual, expected)


    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_init(self):
        actual = ParentNode("tag", ["children"], "props")
        self.assertEqual(actual.tag, "tag")
        self.assertEqual(actual.children, ["children"])
        self.assertEqual(actual.props, "props")


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


    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
             parent_node.to_html()
             self.fail("Exception expected")

    
    def test_to_html_no_child(self):
        parent_node = ParentNode("a", None)
        with self.assertRaises(ValueError):
             parent_node.to_html()
             self.fail("Exception expected")
    
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
 