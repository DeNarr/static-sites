import os
import shutil
import sys
from textnode import *
from htmlnode import *
from copystatic import *
from generatepage import *

def main():
    args = sys.argv
    basepath = "/"
    if len(args) > 1:
        basepath = args[1]

    # Normalize `basepath` to always end with a `/`
    if not basepath.endswith("/"):
        basepath += "/"
    public = "docs"
    if os.path.exists(public):
        print (f"Removing directory {public}")
        shutil.rmtree(public)
    static_to_public("static", public)
    from_path = "content/"
    template_path = "template.html"
    dest_path = f"{public}/"
    generate_pages_recursive(from_path, template_path, dest_path, basepath)



if __name__ == "__main__":
    main()