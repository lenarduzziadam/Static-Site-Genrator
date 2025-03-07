import os
import shutil
from textnode import *

def path_to_victory(src, target):
    # First, clean the target directory if it exists
    if os.path.exists(target):
        shutil.rmtree(target)
    
    # Create a fresh target directory
    os.mkdir(target)
    
    if os.path.exists(src):
        pass
    
def main():
    test_node = TextNode("Hello, WwwwwwaWORLD ol son", TextType.BOLD)
    print(test_node)
    return test_node

if __name__ == "__main__":
    main()