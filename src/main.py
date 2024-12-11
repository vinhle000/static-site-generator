from textnode import TextNode, TextType
import os
import shutil


def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    src_dir = os.path.join(root_dir, "static")
    dest_dir = os.path.join(root_dir, "public")

    # clean destination path -> Maybe put in outter function use recursion of copy_content inside
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    copy_content(src_dir, dest_dir)


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




main()