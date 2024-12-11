from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re
import os
import shutil
import pathlib


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
    block_text = block_text.strip()
    if block_text.startswith("#"):
        index = 0
        while index < len(block_text) and block_text[index] == "#":
            index += 1
        if index <= 6 and index < len(block_text) and block_text[index] == ' ':
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



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        new_node = block_to_html_node(block, type)
        nodes.append(new_node)
    return HTMLNode("div", None, nodes)


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
    level = len(text.split(' ')[0])
    children = text_to_children(text[level + 1:]) #account for space char after '#'s
    return HTMLNode(f"h{level}", None, children)


def block_to_code_node(text):
    children = text_to_children(text[3:-3])
    return HTMLNode("code", None, children)


def block_to_quote_node(text): #<blockquote> tag for block level, and in-line is <q>
    children = text_to_children(text[1:].strip())
    return HTMLNode("blockquote", None, children)


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


def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")


def copy_content(src, dest):
    if os.path.isfile(src):
        shutil.copy(src, dest)
        return

    if not os.path.exists(dest):
        os.mkdir(dest)

    dir_paths = os.listdir(src)

    for path in dir_paths:
        src_path = os.path.join(src, path)
        dest_path = os.path.join(dest, path)
        copy_content(src_path, dest_path)
    return

def generate_page(from_path, template_path, dest_path):
    print("Generating page from from_path to dest_path using template_path")

    with open(from_path,'r') as file:
        markdown_content = file.read()

    with open(template_path, 'r+') as file:
        template_content = file.read()

    markdown_title = extract_title(markdown_content)
    html_node = markdown_to_html_node(markdown_content)
    html = template_content.replace("{{ Title }}", markdown_title)
    html = html.replace("{{ Content }}", html_node.to_html())


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    def gen_page(curr_path, dest_path):
        print('')

        if os.path.isfile(curr_path):

            if curr_path.endswith('.md'):
                generate_page(curr_path, template_path, os.path.join(os.path.dirname(dest_path), "index.html"))
            return

        paths = os.listdir(curr_path)
        for path in paths:
            curr = os.path.join(curr_path, path)
            dest = os.path.join(dest_path, path)
            gen_page(curr, dest)

    gen_page(dir_path_content, dest_dir_path)