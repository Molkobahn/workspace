import shutil
import os


def copy_static(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    content = os.listdir(src)    
    for c in content:
        if os.path.isfile(f"{src}/{c}"):
            shutil.copy(f"{src}/{c}", dst)
        else:
            copy_static(f"{src}/{c}", f"{dst}/{c}")

