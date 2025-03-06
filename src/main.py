import os
from textnode import *

def path_to_victory(src, target):
    static_path = "../static"
    public_path = "../public"
    if os.path.exists(static_path):
        static_files = os.listdir(static_path)
        for static_entries in static_files:
            if os.path.isfile(f"{public_path}/{static_entries}"):
                continue 
    if os.path.exists(public_path):
        path_files = os.listdir(public_path)
        for public_entries in path_files:
            if os.path.isfile(f"{public_path}/{public_entries}"):
                continue
    
def main():
    test_node = TextNode("Hello, WwwwwwaWORLD ol son", TextType.BOLD)
    print(test_node)
    return test_node

if __name__ == "__main__":
    main()