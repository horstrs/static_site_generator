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
    

def get_delimited_words(text_node, delimiter):
    delimiter_count = text_node.count(delimiter)
    if delimiter_count % 2 != 0:
        raise ValueError(f"Invalid Node Text: delimiter {delimiter} not closed. \nString passed: {text_node.text}")

    indexes_list = []
    last_index = -1
    start_index = None
    for i in range(delimiter_count):
        last_index = text_node.index(delimiter, last_index+1)
        if start_index is None:
            start_index = last_index + len(delimiter)
        else:
            indexes_list.append((start_index, last_index))
            start_index = None
    
    delimited_words = [] 
    for indexes in indexes_list:
        delimited_words.append(text_node[indexes[0]:indexes[1]])
   
    return delimited_words
