import re

def extract_markdown_images(text):
    image_tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_tuples

def extract_markdown_links(text):
    link_tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_tuples 

# def extract_markdown_images(text):
#     image_tuples = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
#     return image_tuples 

# def extract_markdown_links(text):
#     link_tuples = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
#     return link_tuples 

