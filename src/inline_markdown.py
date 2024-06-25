from textnode import (
    TextNode,
    text_type_text,
    # text_type_bold,
    # text_type_italic,
    # text_type_code,
)

# boot.dev
# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != text_type_text:
#             new_nodes.append(old_node)
#             continue
#         split_nodes = []
#         sections = old_node.text.split(delimiter)
#         if len(sections) % 2 == 0:
#             raise ValueError("Invalid markdown, formatted section not closed")
#         for i in range(len(sections)):
#             if sections[i] == "":
#                 continue
#             if i % 2 == 0:
#                 split_nodes.append(TextNode(sections[i], text_type_text))
#             else:
#                 split_nodes.append(TextNode(sections[i], text_type))
#         new_nodes.extend(split_nodes)
#     return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        node_split_list = old_node.text.split(delimiter)
        if len(node_split_list) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for i in range(len(node_split_list)):
            if node_split_list[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(node_split_list[i], text_type_text))
            else:
                new_nodes.append(TextNode(node_split_list[i], text_type))
    return new_nodes
