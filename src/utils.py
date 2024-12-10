from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re



def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return text_node.text
    elif text_node.text_type == TextType.BOLD:
        return f"<b>{text_node.text}</b>"
    elif text_node.text_type == TextType.ITALIC:
        return f"<i>{text_node.text}</i>"
    elif text_node.text_type == TextType.CODE:
        return f"<code>{text_node.text}</code>"
    elif text_node.text_type == TextType.LINK:
        return f'<a href="{text_node.url}">{text_node.text}</a>'
    elif text_node.text_type == TextType.IMAGE:
        return f'<img src="{text_node.url}" alt="{text_node.text}">'
    else:
        raise ValueError("Invalid text type")


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

                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
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

                    new_nodes.append(TextNode(link_text, TextType.LINK, link))
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



def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()

        if block:
            # handle list blocks
            if block.startswith('* ') or block.startswith('- '):
                #remove leading spaces from each line in unordered list
                lines = block.split("\n")
                lines = [line.lstrip() for line in lines]
                block = "\n".join(lines)

            blocks.append(block)
    return blocks



def block_to_block_type(block_text):
    if block_text.startswith("# "):
        return "heading"
    elif block_text.startswith("```") and block_text.endswith("```"):
        return "code"
    elif block_text.startswith(">"):
        return "quote"
    elif block_text.startswith("* ") or block_text.startswith("- "):
        lines = block_text.split("\n")
        for line in lines:
            line.strip()
            if not line.startswith(block_text[:2]):
                return "paragraph"
        return "unordered_list"

    elif block_text.startswith("1. "):
        lines = block_text.split("\n")
        line_num = 1
        for line in lines:
            line = line.strip()
            if not line.startswith(f"{line_num}. "):
                return "paragraph"
            line_num += 1
        return "ordered_list"
    else:
        return "paragraph"


# [] converts a full markdown document into a single parent HTMLNode.
# That one parent HTMLNode should of course contain many child HTMLNode objects representing the nested elements.

# I created an additional 8 helper functions to keep my code neat and easy to understand,
# because there's a lot of logic necessary for the markdown_to_html_node.
# I don't want to give you my exact functions because I want you to do this from scratch.
# However, I'll give you the basic order of operations:

# [ ] Split the markdown into blocks (you already have a function for this)

# [ ] Loop over each block:
    # [x] Determine the type of block (you already have a function for this)
    # [ ] Based on the type of block, create a new HTMLNode with the proper data
# [ ] Assign the proper child HTMLNode objects to the block node.
    # I created a shared text_to_children(text) function that works for all block types.
    # It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using
    # previously created functions (think TextNode -> HTMLNode).

# [ ] Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.


def markdown_to_html_node(markdown):
    pass

    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        new_node = block_to_html_node(block, type)
        nodes.append(new_node)
    return nodes

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    child_nodes = []
    for node in textnodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

def block_to_paragraph_node(text):
    children = text_to_children(text)
    return HTMLNode("p", None, children)

def block_to_heading_node(text):
    children = text_to_children(text[2:])
    return HTMLNode("h", None, children)

def block_to_code_node(text):
    children = text_to_children(text[3:-3])
    return HTMLNode("code", None, children)

def block_to_quote_node(text):
    children = text_to_children(text[1:])
    return HTMLNode("q", None, children)


def block_to_unordered_list_node(text):
    list_item_nodes = []
    sections = text.split("\n")
    for section in sections:
        children = text_to_children(section[2:])
        list_item_node = HTMLNode("li", None, children)
        list_item_nodes.append(list_item_node)

    return HTMLNode("ul", None, list_item_nodes)

def block_to_ordered_list_node(text):
    list_item_nodes = []
    sections = text.split("\n")
    for section in sections:
        section = section.strip()
        children = text_to_children(section[3:])
        list_item_node = HTMLNode("li", None, children)
        list_item_nodes.append(list_item_node)

    return HTMLNode("ol", None, list_item_nodes)

def block_to_html_node(block_text, type):
    map = {
        "paragraph": block_to_paragraph_node,
        "heading": block_to_heading_node,
        "code": block_to_code_node,
        "quote": block_to_quote_node,
        "unordered_list": block_to_unordered_list_node,
        "ordered_list": block_to_ordered_list_node
    }

    return map[type](block_text)


