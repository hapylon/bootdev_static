# import re

# from enum import Enum
# from htmlnode import LeafNode
# from typing import List, Dict, Optional
# from extract_links import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


def text_to_textnodes(markdown_text):
    nodes = [TextNode(markdown_text, TextType.TEXT)]
    nodes_b = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes_bi = split_nodes_delimiter(nodes_b, "_", TextType.ITAL)
    nodes_bic = split_nodes_delimiter(nodes_bi, "`", TextType.CODE)
    nodes_bic_img = split_nodes_image(nodes_bic)
    nodes_bic_img_link = split_nodes_link(nodes_bic_img)
    return nodes_bic_img_link

