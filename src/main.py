from textnode import TextNode, TextType
import os
import shutil


def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    src_dir = os.path.join(root_dir, "static")
    src_paths = get_source_paths(src_dir)
    print(' contents of src  ----> ', src_paths)


# Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
# It should first delete all the contents of the destination directory to ensure that the copy is clean.

# It should copy all files and subdirectories, nested files, etc.

# I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.

# Here are some of the standard library docs that might be helpful:
# os.path.exists
# os.listdir
# os.path.join
# os.path.isfile
# os.mkdir
# shutil.copy
# shutil.rmtree

# [ ] Hook the function up to your main function and test it out. I didn't use a unit test for this one because it interacts with the file system: I just tested it manually.
# [ ] Add the public/ directory to your .gitignore file. This is where the generated site will live. As a general rule, it's bad to commit generated stuff, especially if it can be regenerated easily.
# [ ] Ensure that running main.sh generates the public directory and all the copied content correctly.

def copy_contents_to_dir(src, dest):
    pass
    # get a list of all the files and dirs from source

    # for path in source_paths:
        # new_path = "root/distination/"

        # a

def get_source_paths(src):
    src_paths = []
    dir_paths = os.listdir(src)
    print('--------')
    print('dir paths list', dir_paths)
    print(' ')
    for path in dir_paths:
        full_path = os.path.join(src, path)
        if os.path.isfile(full_path):
            src_paths.append(full_path)
        else:
            src_paths.extend(get_source_paths(full_path))

    return src_paths


main()