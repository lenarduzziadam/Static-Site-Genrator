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
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.listdir(dir_path_content):
        
        source_path = os.path.join(dir_path_content, entry)
        if entry.endswith(".md"):
            # Create destination path (change .md to .html)
                html_filename = entry[:-3] + ".html"  # Remove .md and add .html
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                generate_page(source_path, template_path, dest_path)
                
        elif os.path.isdir(source_path):
            # If it's a directory, make a recursive call
            # Create corresponding destination directory path
            dest_subdir = os.path.join(dest_dir_path, entry)
            
            # Recursive call to process the subdirectory
            generate_pages_recursive(source_path, template_path, dest_subdir)
def main():
    public_dir = "public"
    output_file = os.path.join(public_dir, "index.html")
    content_file = "content/index.md"
    template_file = "template.html"
    
    # Use the actual paths you need for your project
    path_to_victory("static", "public")
    print("Static files copied successfully!")
    
    #generating Page
    generate_page(content_file, template_file, output_file)
    print("page generated in public folder")
    
    blog_dir = "content/blog"
    for blog_name in ["glorfindel", "tom", "majesty"]:
        content_file = os.path.join(blog_dir, blog_name, "index.md")
        # Create the destination directory if it doesn't exist
        output_dir = os.path.join(public_dir, "blog", blog_name)
        os.makedirs(output_dir, exist_ok=True)
        output_group = os.path.join(output_dir, "index.html")
        generate_page(content_file, template_file, output_group)
    
     # Generate contact page
    contact_content_file = "content/contact/index.md"
    contact_output_dir = os.path.join(public_dir, "contact")
    os.makedirs(contact_output_dir, exist_ok=True)
    contact_output_file = os.path.join(contact_output_dir, "index.html")
    generate_page(contact_content_file, template_file, contact_output_file)
    
    print("All pages generated in public folder")

if __name__ == "__main__":
    main()