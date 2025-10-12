import re
from text_node import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_node_list.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        delimited_words = get_delimited_words(old_node.text, delimiter)
        for block in split_text:
            if not block:
                continue
            if block in delimited_words:
                new_node = TextNode(block, text_type)
            else:
                new_node = TextNode(block, TextType.TEXT)
            new_node_list.append(new_node)

    return new_node_list
    

def get_delimited_words(text, delimiter):
    delimiter_count = text.count(delimiter)
    if delimiter_count % 2 != 0:
        raise ValueError(f"Invalid Node Text: delimiter {delimiter} not closed. \nString passed: {text}")

    indexes_list = []
    last_index = -1
    start_index = None
    for i in range(delimiter_count):
        last_index = text.index(delimiter, last_index+1)
        if start_index is None:
            start_index = last_index + len(delimiter)
        else:
            indexes_list.append((start_index, last_index))
            start_index = None
    
    delimited_words = [] 
    for indexes in indexes_list:
        delimited_words.append(text[indexes[0]:indexes[1]])
   
    return delimited_words


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_node_list.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_node_list.append(old_node)
            continue
        
        text_to_split = old_node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            
            sections = text_to_split.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                new_node_list.append(TextNode(sections[0], TextType.TEXT))
            new_node_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_to_split = sections[1]
        if sections[1]:
            new_node_list.append(TextNode(sections[1], TextType.TEXT))

    return new_node_list


def split_nodes_link(old_nodes):
    new_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_node_list.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_node_list.append(old_node)
            continue
        
        text_to_split = old_node.text
        for link in links:
            link_anchor = link[0]
            link_url = link[1]
            
            sections = text_to_split.split(f"[{link_anchor}]({link_url})", 1)
            if sections[0]:
                new_node_list.append(TextNode(sections[0], TextType.TEXT))
            new_node_list.append(TextNode(link_anchor, TextType.LINK, link_url))
            text_to_split = sections[1]
        if sections[1]:
            new_node_list.append(TextNode(sections[1], TextType.TEXT))

    return new_node_list
