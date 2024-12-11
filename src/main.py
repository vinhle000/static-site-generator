from textnode import TextNode, TextType
import os
import shutil
import utils

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    src_dir = os.path.join(root_dir, "static")
    dest_dir = os.path.join(root_dir, "public")
    # markdown_dir = os.path.join(root_dir, "content/index.md")
    template_dir = os.path.join(root_dir, "template.html")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    utils.copy_content(src_dir, dest_dir)

    utils.generate_pages_recursive(os.path.join(root_dir, "content"), template_dir, dest_dir)



main()