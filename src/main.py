import os
import shutil
from textnode import *

def path_to_victory(src, target):
     # Only clean and create the target directory on the initial call
    print(f"Checking if {target} exists...")
    if os.path.exists(target):
        print(f"Cleaning {target} directory...")
        # Remove all contents but keep the directory
        for item in os.listdir(target):
            item_path = os.path.join(target, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)
    else:
        # Create the target directory if it doesn't exist
        print(f"Creating {target} directory...")
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
            os.mkdir(target_path)
            # 1. Create the directory in the target
            # 2. Recursively call this function
            path_to_victory(src_path, target_path)
    
def main():
    # Use the actual paths you need for your project
    path_to_victory("static", "public")
    print("Static files copied successfully!")
    test_node = TextNode("Hello, WwwwwwaWORLD ol son", TextType.BOLD)
    print(test_node)
    
    return test_node

if __name__ == "__main__":
    main()