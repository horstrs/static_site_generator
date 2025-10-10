import unittest

from leafnode import LeafNode


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
