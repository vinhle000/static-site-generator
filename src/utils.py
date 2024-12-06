from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # todo maybe check delimiter char vs a valid TextType
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            text = node.text

            if not text.count(delimiter) % 2 == 0:
                raise Exception("invalid Markdown")

            while delimiter in text:
                chunks = text.split(delimiter, maxsplit = 2)
                if len(chunks[0]) > 0: # Add the text before the delimiter if not empty
                    new_text_node = TextNode(chunks[0], TextType.TEXT)
                    new_nodes.append(new_text_node)
                new_text_type_node = TextNode(chunks[1], text_type)
                new_nodes.append(new_text_type_node)

                text = chunks[2]

            # Add the remaining text as a TextNode
            if text:
                new_text_node = TextNode(text, TextType.TEXT)
                new_nodes.append(new_text_node)


        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(?P<text>[^\[\]]+)\]\((?P<url>[^\(\)]+)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"(?<!\!)\[(?P<text>[^\[\]]+)\]\((?P<url>[^\(\)]+)\)"
    matches = re.findall(regex, text)
    return matches


def split_nodes_image(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            curr_text = node.text
            matches = extract_markdown_images(node.text)

            if not matches:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
            else:
                for image_alt, image_link in matches:
                    sections = curr_text.split(f"![{image_alt}]({image_link})", 1)


                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))

                    new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_link))
                    curr_text = sections[1]

                if curr_text:
                    new_nodes.append(TextNode(curr_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            curr_text = node.text
            matches = extract_markdown_links(node.text)

            if not matches:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
            else:
                for link_text, link in matches:
                    sections = curr_text.split(f"[{link_text}]({link})", 1)

                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))

                    new_nodes.append(TextNode(link_text, TextType.LINKS, link))
                    curr_text = sections[1]

                if curr_text:
                    new_nodes.append(TextNode(curr_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes