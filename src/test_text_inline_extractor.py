import unittest

from text_node import TextNode, TextType
from text_inline_extractor import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


    def test_nested_inline_to_node_text(self):
        node = TextNode("This is text `with two `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            self.fail("Exception expected for nested inlines")


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(actual, expected)


    def test_extract_markdown_images_plain_text(self):
        text = "This is text with a plain text"
        actual = extract_markdown_images(text)
        expected = []
        self.assertListEqual(actual, expected)


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(actual, expected)
       
        
    def test_extract_markdown_links_plain_text(self):
        text = "This is text with a plain text"
        actual = extract_markdown_links(text)
        expected = []
        self.assertListEqual(actual, expected)


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
