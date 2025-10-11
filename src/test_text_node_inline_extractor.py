import unittest

from text_node import TextNode, TextType
from text_node_inline_extractor import split_nodes_delimiter

class Test_Text_Node_Converter(unittest.TestCase):

    def test_run(self):
        node = TextNode("This is a **long** text `with two` `code blocks` and _multiple_ delimiters", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is a **long** text ", TextType.TEXT),
                    TextNode("with two", TextType.CODE),
                    TextNode(" ", TextType.TEXT),
                    TextNode("code blocks", TextType.CODE),
                    TextNode(" and _multiple_ delimiters", TextType.TEXT),
                    ]
        self.assertListEqual(actual, expected)
        
        node = actual
        actual = split_nodes_delimiter(node, "_", TextType.ITALIC)
        expected = [TextNode("This is a **long** text ", TextType.TEXT),
                    TextNode("with two", TextType.CODE),
                    TextNode(" ", TextType.TEXT),
                    TextNode("code blocks", TextType.CODE),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("multiple", TextType.ITALIC),
                    TextNode(" delimiters", TextType.TEXT),
                    ]
        self.assertListEqual(actual, expected)
    
    
    def test_plain_text_to_node_text(self):
        node = TextNode("This is a plain text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertListEqual(actual, expected)

    def test_bold_text_to_node_text(self):
        node = TextNode("**This is** a text with bold inline text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is", TextType.BOLD),
                    TextNode(" a text with bold inline text", TextType.TEXT),
                    ]
        self.assertListEqual(actual, expected)


    def test_italic_text_to_node_text(self):
        node = TextNode("This is a text with _italic_ inline text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [TextNode("This is a text with ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" inline text", TextType.TEXT),
                    ]
        self.assertListEqual(actual, expected)


    def test_code_text_to_node_text(self):
        node = TextNode("At the end: `code block`", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("At the end: ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    ]
        self.assertListEqual(actual, expected)


    def nested_inline_to_node_text(self):
        
        with self.assertRaises(ValueError):
            node = TextNode("This is text `with two `code block` word", TextType.TEXT)
            split_nodes_delimiter([node], "`", TextType.CODE)
            self.fail("Exception expected for nested inlines")

"""
    def test_link_text_to_node_text(self):
        node = TextNode("This is a text with bold inline text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.LINK)
        expected = [node]
        self.assertListEqual(actual, expected)


    def test_images_text_to_node_text(self):
        node = TextNode("This is a text with **bold** inline text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertListEqual(actual, expected)"""
