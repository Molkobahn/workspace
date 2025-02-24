from textnode import TextNode, TextType
from copy_static import copy_static
from generate_page import generate_page, generate_pages_recursive
import os
import shutil

def main():
    src = "/home/molkobahn/workspace/github.com/Molkobahn/Static Site/static"
    dst = "/home/molkobahn/workspace/github.com/Molkobahn/Static Site/public"

    
    if os.path.exists(dst):
        shutil.rmtree(dst)

    copy_static(src, dst)
    from_path = "/home/molkobahn/workspace/github.com/Molkobahn/Static Site/content"
    template_path = "/home/molkobahn/workspace/github.com/Molkobahn/Static Site/template.html"
    dest_path = "/home/molkobahn/workspace/github.com/Molkobahn/Static Site/public"
    generate_pages_recursive(from_path, template_path, dest_path)

main()