import unittest
from blocks_markdown import BlockType, markdown_to_blocks, block_to_blocktype

class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        actual = markdown_to_blocks(md)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(actual, expected)


    def test_blocks_markdown_heading(self):
        excpected = BlockType.HEADING
        actual = block_to_blocktype("# this is a heading block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("### this is a heading block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("###### this is a heading block")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_not_heading(self):

        excpected = BlockType.PARAGRAPH
        actual = block_to_blocktype("####### this is a PARAGRAPH block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("#this is a PARAGRAPH block")
        self.assertEqual(actual, excpected)
    

    def test_blocks_markdown_code(self):

        excpected = BlockType.CODE
        
        actual = block_to_blocktype("```this is also a CODE block```")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("```this is a \nCODE block```")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("````this is a CODE block with a back-tick in the first and last character````")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_not_code(self):

        excpected = BlockType.PARAGRAPH

        actual = block_to_blocktype("````this is a PARAGRAPH block``")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("``this is a PARAGRAPH block````")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_quote(self):

        excpected = BlockType.QUOTE
        
        actual = block_to_blocktype(">this is a QUOTE block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype(">this is also \n>a QUOTE block")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_not_quote(self):

        excpected = BlockType.PARAGRAPH

        actual = block_to_blocktype(">this is NOT \na QUOTE block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("this is NOT \n>a QUOTE block too")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_unordered_list(self):

        excpected = BlockType.UNORDERED_LIST
        
        actual = block_to_blocktype("- this is an UNORDERED LIST block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("- this is an UNORDERED LIST block\n- Another item in the list\n- A third item in the list")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_not_unordered_list(self):

        excpected = BlockType.PARAGRAPH
        
        actual = block_to_blocktype("- this is a PARAGRAPH block\n Because this middle item doesn't start with -\n- A third item in the list")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("- this is a PARAGRAPH block\n-Because this middle item doesn't have a space after the -\n- A third item in the list")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_ordered_list(self):

        excpected = BlockType.ORDERED_LIST
        
        actual = block_to_blocktype("1. this is an ORDERED LIST block")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("1. this is an ORDERED LIST block\n2. All lines start with a number followed by a . and a space\n3. And the list starts at 1.")
        self.assertEqual(actual, excpected)


    def test_blocks_markdown_not_ordered_list(self):

        excpected = BlockType.PARAGRAPH

        actual = block_to_blocktype("2. this is an PARAGRAPH block\n3. Because the list starts on 2 instead of 1")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("1. this is an PARAGRAPH block\n3. Because the increment is not of 1")
        self.assertEqual(actual, excpected)

        actual = block_to_blocktype("1. this is an PARAGRAPH block\n2.Because there is not a space after the dot in this item")
        self.assertEqual(actual, excpected)
