import os
import shutil, sys
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
        
        tempstring = """""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for entry in os.listdir(dir_path_content):
        
        print(f"Entry: {entry}") 
        source_path = os.path.join(dir_path_content, entry)
        print(f" source path{source_path}")
        if entry.endswith(".md"):
            # Create destination path (change .md to .html)
                html_filename = entry[:-3] + ".html"  # Remove .md and add .html
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                generate_page(source_path, template_path, dest_path, basepath)
                
                print("generated singualar page")
                
        elif os.path.isdir(source_path):
            # If directory, make recursive call
            # Create corresponding destination directory path
            dest_subdir = os.path.join(dest_dir_path, entry)
            print(f" post loop Recursing into: {source_path} -> {dest_subdir}")
            print("recursive call utilized")
            # Recursive call to process the subdirectory
            generate_pages_recursive(source_path, template_path, dest_subdir, basepath)
            """
            
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.listdir(dir_path_content):
        
        source_path = os.path.join(dir_path_content, entry)
        if entry.endswith(".md"):
            # Create destination path (change .md to .html)
                html_filename = entry[:-3] + ".html"  # Remove .md and add .html
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                generate_page(source_path, template_path, dest_path, basepath)
                
                print("generated singualar page")
                
        elif os.path.isdir(source_path):
            # If directory, make recursive call
            # Create corresponding destination directory path
            dest_subdir = os.path.join(dest_dir_path, entry)
            
            print("recursive call utilized")
            print(f"Recursing into: {source_path} -> {dest_subdir}")
            generate_pages_recursive(source_path, template_path, dest_subdir, basepath)
            
def main():
    public_dir = "docs"
    content_file = 'content'
    template_file = "template.html"
    
    
    
    # Use the actual paths you need for your project
    path_to_victory("static", public_dir)
    print("Static files copied successfully!")
    
    #generating Page
    generate_pages_recursive(content_file, template_file, public_dir, basepath)
    #print(f"Replacing href/src with basepath: {basepath}")
    print("page generated in docs folder")

    
    print("All pages generated in docs folder")

if __name__ == "__main__":
    # Get the basepath from command line arguments or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    main()