import os
import shutil
from textnode import *
from htmlnode import *

def main():
    test_obj = TextNode("This is a text node", TextType.BOLD, "www.google.com")
    print (test_obj)
    public = "public"
    if os.path.exists(public):
        print (f"Removing directory {public}")
        shutil.rmtree(public)
    print (f"Creating directory {public}")
    os.mkdir(public)
    static_to_public("static", public)

def static_to_public(src_path, dst_path):
    if os.path.exists(src_path):
        files = os.listdir(src_path)
        for file in files:
            spath = os.path.join(src_path, file)
            if os.path.isfile(spath):
                print (f"Copying {spath} to {dst_path}")
                shutil.copy(spath, dst_path)
            else:
                dpath = os.path.join(dst_path, file)
                print (f"Creating directory {dpath}")
                os.mkdir(dpath)
                static_to_public(spath, dpath)

if __name__ == "__main__":
    main()