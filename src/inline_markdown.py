import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
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


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


# boot.dev
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


# def split_nodes_image(old_nodes):
#     new_nodes = []
#     for old_node in old_nodes:
#         textSplit = re.split(r"!\[(.*?)\]\((.*?)\)", old_node.text)
#         textMatched = extract_markdown_images(old_node.text)
#
#         i = 0
#         j = 0
#         while i < len(textSplit):
#
#             if old_node.text_type != text_type_text:
#                 new_nodes.append(old_node)
#                 i += 1
#                 continue
#             if textSplit[i] == "":
#                 i += 1
#                 continue
#             imgTuple = textMatched[j]
#             if imgTuple[0] == textSplit[i] and imgTuple[1] == textSplit[i + 1]:
#                 new_nodes.append(TextNode(imgTuple[0], text_type_image, imgTuple[1]))
#                 j += 1
#                 i += 2
#             else:
#                 new_nodes.append(TextNode(textSplit[i], text_type_text))
#                 i += 1
#
#     return new_nodes
#
#
# def split_nodes_link(old_nodes):
#     new_nodes = []
#     for old_node in old_nodes:
#         textSplit = re.split(r"\[(.*?)\]\((.*?)\)", old_node.text)
#         textMatched = extract_markdown_links(old_node.text)
#
#         i = 0
#         j = 0
#         while i < len(textSplit):
#
#             if old_node.text_type != text_type_text:
#                 new_nodes.append(old_node)
#                 i += 1
#                 continue
#             if textSplit[i] == "":
#                 i += 1
#                 continue
#             imgTuple = textMatched[j]
#             if imgTuple[0] == textSplit[i] and imgTuple[1] == textSplit[i + 1]:
#                 new_nodes.append(TextNode(imgTuple[0], text_type_link, imgTuple[1]))
#                 j += 1
#                 i += 2
#             else:
#                 new_nodes.append(TextNode(textSplit[i], text_type_text))
#                 i += 1
#
#     return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
