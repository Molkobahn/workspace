import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Process special nodes first (images and links)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # Then process text styling
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)    
        if len(split_node) % 2 == 0:
            raise Exception("Missing closing delimiter")   
        for i, text in enumerate(split_node):
            if text== "":
                continue
            current_type = text_type if i % 2 == 1 else TextType.TEXT
            if current_type in (TextType.LINK, TextType.IMAGE):
                new_nodes.append(TextNode(text, current_type, node.url))
            else:
                new_nodes.append(TextNode(text, current_type))     
    return new_nodes
    

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        while extract_markdown_images(node.text):
            images = extract_markdown_images(node.text)
            image = images[0]
            sections = node.text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node.text = sections[1]
        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If it's not a text node, preserve it as-is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Process only text nodes for links
        while extract_markdown_links(node.text):
            links = extract_markdown_links(node.text)
            link = links[0]
            sections = node.text.split(f"[{link[0]}]({link[1]})", 1)   
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node.text = sections[1]
        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    image = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image


def extract_markdown_links(text):
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link