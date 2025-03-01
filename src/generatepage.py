import os
import re
from splitblocks import *

def generate_page(from_path, template_path, dest_path):
    #print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown = md_file.read()
    with open(template_path) as t_file:
        template = t_file.read()
    #print (f"markdown: {markdown} \n template: {template}")
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    #print (f"Html:\n{html}")
    title = extract_title(markdown)
    #print (f"title:\n{title}")
    final_page = populate_template(template, title, html)
    #print (f"Final page:\n{final_page}")
    dest_directory = os.path.dirname(dest_path)
    if dest_directory:
        os.makedirs(dest_directory, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(final_page)



def populate_template(template, title, content):
    result = template.replace("{{ Title }}", title)
    #print (f"After title:\n{result}")
    result = result.replace("{{ Content }}", content)
    return result

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        path = os.path.join(dir_path_content, item)
        if os.path.isfile(path):
            html = re.sub(r'\.md$', '.html', item, flags=re.IGNORECASE)
            generate_page(path, template_path, os.path.join(dest_dir_path, html))
        else:
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, item))