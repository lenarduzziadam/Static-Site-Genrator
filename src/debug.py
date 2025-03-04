from textnode import extract_markdown_images

# Test the function directly
result = extract_markdown_images("Image with link-like alt text: ![Here's a [link]](https://example.com/img.png)")
print(result)