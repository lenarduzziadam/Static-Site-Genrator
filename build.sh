#!/bin/bash

# Define the repo name (update this to your actual GitHub repository name)
REPO_NAME="Static-Site-Genrator"

# Run the Python script with the basepath set for GitHub Pages
python3 src/main.py "/$REPO_NAME/"

# Print success message
echo "Build completed! Files are now in the /docs directory."

cd docs && python3 -m http.server 8000
