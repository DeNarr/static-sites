import os
import shutil
from textnode import *
from htmlnode import *
from copystatic import *
from generatepage import *

def main():
    test_obj = TextNode("This is a text node", TextType.BOLD, "www.google.com")
    print (test_obj)
    public = "public"
    if os.path.exists(public):
        print (f"Removing directory {public}")
        shutil.rmtree(public)
    static_to_public("static", public)
    from_path = "content/"
    template_path = "template.html"
    dest_path = "public/"
    generate_pages_recursive(from_path, template_path, dest_path)



if __name__ == "__main__":
    main()