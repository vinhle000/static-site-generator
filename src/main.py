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

    # clean destination path -> Maybe put in outter function use recursion of copy_content inside
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    utils.copy_content(src_dir, dest_dir)

    # utils.generate_page(markdown_dir, template_dir, os.path.join(dest_dir, "index.html"))
    utils.generate_pages_recursive(os.path.join(root_dir, "content"), template_dir, dest_dir)
# Error: failed test 1.10: expected response body to contain '<blockquote>All that is gold does not glitter</blockquote>', but it did not



main()