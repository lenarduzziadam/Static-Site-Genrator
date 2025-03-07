import os
import shutil
from textnode import *

def path_to_victory(src, target):
    # First, clean the target directory if it exists
    if os.path.exists(target):
        shutil.rmtree(target)
    
    # Create a fresh target directory
    os.mkdir(target)
    
   # Get a list of all items in the source directory
    items = os.listdir(src)
    
    # Now, for each item in the source directory
    for item in items:
        # Create full paths for source and destination
        src_path = os.path.join(src, item)
        target_path = os.path.join(target, item)
        
        # If it's a file, copy it
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} to {target_path}")
            shutil.copy(src_path, target_path)
        # If it's a directory, create it in the target and recurse
        else:
            print(f"Processing directory: {src_path}")
            # What should we do with directories?
            # Hint: You'll need to:
            os.mkdir(target)
            # 1. Create the directory in the target
            # 2. Recursively call this function
            path_to_victory(src_path, target_path)
    
def main():
    test_node = TextNode("Hello, WwwwwwaWORLD ol son", TextType.BOLD)
    print(test_node)
    return test_node

if __name__ == "__main__":
    main()