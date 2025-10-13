import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if not block:
            continue
        cleaned_blocks.append(block.strip())
    return cleaned_blocks


def block_to_blocktype(markdown_block):
    is_heading_block = re.findall(r"^(#{1,6} )", markdown_block)
    if is_heading_block:
        return BlockType.HEADING

    is_code_block = re.findall(r"^`{3}.*`{3}$", markdown_block, re.S)
    if is_code_block:
        return BlockType.CODE

    block_split_by_lines = markdown_block.split("\n")
    if is_regex_true_for_all_lines(block_split_by_lines, r"^>"):
        return BlockType.QUOTE

    if is_regex_true_for_all_lines(block_split_by_lines, r"^- "):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i in range(len(block_split_by_lines)):
        is_ordered_list = re.match(rf"^{i + 1}. ", block_split_by_lines[i])
        if not is_ordered_list:
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_regex_true_for_all_lines(block_lines, regex):
    for line in block_lines:
        is_regex_true = re.match(regex, line)
        if not is_regex_true:
            return False
    return True
