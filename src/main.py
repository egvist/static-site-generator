from textnode import TextNode, TextType
import os
import shutil
import sys
from gencontent import generate_page, generate_pages_recursive


def copy_directory(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied: {source_path} -> {destination_path}")

        else:
            copy_directory(source_path, destination_path)


def copy_static_to_public():
    source = "static"
    destination = "docs"

    if os.path.exists(destination):
        shutil.rmtree(destination)

    copy_directory(source, destination)

def main():

    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public()

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath
    )
if __name__ == "__main__":
    main()