from blocks_markdown import BlockType, markdown_to_blocks, block_to_blocktype
from text_inline_extractor import (
    text_to_text_nodes,
)
from text_node import TextNode, TextType
from html_node import ParentNode


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    HTML_children = []
    for md_block in md_blocks:
        html_node = block_to_html_node(md_block)
        HTML_children.append(html_node)
    return ParentNode("div", HTML_children)


def block_to_html_node(md_block):
    block_type = block_to_blocktype(md_block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(md_block)
        case BlockType.CODE:
            return code_to_html_node(md_block)
        case BlockType.HEADING:
            return heading_to_html_node(md_block)
        case BlockType.QUOTE:
            return quote_to_html_node(md_block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(md_block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(md_block)
        case _:
            raise ValueError(f"block type '{block_type}' not supported")


def paragraph_to_html_node(md_block):
    cleaned_block = clean_up_text_block(md_block)
    html_nodes = text_to_html_children(cleaned_block)
    return ParentNode("p", html_nodes)


def code_to_html_node(md_block):
    cleaned_block = clean_up_code_block(md_block)
    text_node = TextNode(cleaned_block, TextType.CODE)
    html_nodes = text_node.text_node_to_html_node()
    return ParentNode("pre", [html_nodes])


def heading_to_html_node(md_block):
    level = 0
    for char in md_block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(md_block):
        raise ValueError(
            f"Invalid heading block. Contains only header symbols. MD Block: {md_block}"
        )
    cleaned_block = md_block[level + 1 :]
    children = text_to_html_children(cleaned_block)
    return ParentNode(f"h{level}", children)


def quote_to_html_node(md_block):
    block_split = md_block.split("\n")
    cleaned_block = []
    for line in block_split:
        cleaned_block.append(line.lstrip(">").strip())
    cleaned_text = " ".join(cleaned_block)
    return ParentNode("blockquote", text_to_html_children(cleaned_text))


def unordered_list_to_html_node(md_block):
    items = md_block.split("\n")
    html_nodes = []
    for item in items:
        text = item[2:]
        children = text_to_html_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ul", html_nodes)


def ordered_list_to_html_node(md_block):
    items = md_block.split("\n")
    html_nodes = []
    for item in items:
        text = item[3:]
        children = text_to_html_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", html_nodes)


def text_to_html_children(text):
    text_nodes = text_to_text_nodes(text)
    html_nodes = []
    for text_node in text_nodes:
        single_html_node = text_node.text_node_to_html_node()
        html_nodes.append(single_html_node)
    return html_nodes


def clean_up_text_block(text):
    split_text = text.split("\n")
    return " ".join(split_text)


def clean_up_code_block(text):
    return text[3:-3]
