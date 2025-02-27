import os
import shutil

def static_to_public(src_path, dst_path):
    if not os.path.exists(dst_path):
        print (f"Creating directory {dst_path}")
        os.mkdir(dst_path)
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