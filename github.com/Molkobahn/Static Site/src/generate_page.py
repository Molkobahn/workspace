import os
import pathlib

from blocks import markdown_to_html_node
from htmlnode import HTMLNode


def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""

    if lines[0].startswith("# "):
        title += lines[0].lstrip("# ")
    else:
        raise Exception("No header found")
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:    
        template = file.read()
    
    node = markdown_to_html_node(markdown)
    string = node.to_html()
    title = extract_title(markdown)

    first_replace = template.replace("{{ Title }}", title)
    final_string = first_replace.replace("{{ Content }}", string)

    
    with open(dest_path, 'w') as file:
        file.write(final_string)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    content = os.listdir(dir_path_content)
    for c in content:
        source_path = pathlib.Path(f"{dir_path_content}/{c}")
        if os.path.isfile(source_path):
            if source_path.suffix == '.md':
                dest_path = os.path.join(dest_dir_path, source_path.stem + '.html')
                generate_page(source_path, template_path, dest_path)
        else:
            new_dest_dir = os.path.join(dest_dir_path, c)
            generate_pages_recursive(source_path, template_path, new_dest_dir)