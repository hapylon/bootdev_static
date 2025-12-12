from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        # If this node doesn't contain the delimiter, keep as-is
        if delimiter not in text:
            new_nodes.append(node)
            continue

        sections = text.split(delimiter)

        # If len is even, there's an unclosed delimiter
        if len(sections) % 2 == 0:
            raise Exception("invalid markdown, formatted section not closed")

        # Build new nodes: even indexes = outside, odd indexes = inside
        split_nodes = []
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_to_append = []
        img_node_text = node.text
        img_tuples = extract_markdown_images(img_node_text)
        remaining_text = img_node_text
        if len(img_tuples) == 0:
            node_to_append.append(node)

        for i, img_tuple in enumerate(img_tuples):
            per_tuple = []
            anchor_txt = img_tuple[0]
            url_txt = img_tuple[1]
            chopping_block = remaining_text.split("![" + anchor_txt + "](" + url_txt + ")", maxsplit=1)
            
            if chopping_block[0] != "":
                per_tuple.append(TextNode(chopping_block[0], TextType.TEXT))
            per_tuple.append(TextNode(anchor_txt, TextType.IMAGE, url_txt))
            
            if i == len(img_tuples) -1 and chopping_block[1] != "":
                per_tuple.append(TextNode(chopping_block[1], TextType.TEXT))
            
            remaining_text = chopping_block[1]
            
            node_to_append.extend(per_tuple)

        new_nodes.extend(node_to_append)
    
    return new_nodes
            
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_to_append = []
        node_text = node.text
        link_tuples = extract_markdown_links(node_text)
        remaining_text = node_text
        if len(link_tuples) == 0:
            node_to_append.append(node)

        for i, link_tuple in enumerate(link_tuples):
            per_tuple = []
            link_txt = link_tuple[0]
            url_txt = link_tuple[1]
            chopping_block = remaining_text.split("[" + link_txt + "](" + url_txt + ")", maxsplit=1)
            
            if chopping_block[0] != "":
                per_tuple.append(TextNode(chopping_block[0], TextType.TEXT))
            per_tuple.append(TextNode(link_txt, TextType.LINK, url_txt))
            
            if i == len(link_tuples) -1 and chopping_block[1] != "":
                per_tuple.append(TextNode(chopping_block[1], TextType.TEXT))
            
            remaining_text = chopping_block[1]
            
            node_to_append.extend(per_tuple)

        new_nodes.extend(node_to_append)
    
    return new_nodes




# def split_nodes_image(old_nodes):
#     new_nodes = []
#     for node in old_nodes:
#         node_to_append = []
#         img_node_text = node.text
#         img_tuples = extract_links.extract_markdown_images(img_node_text)
        
#         for tuple in img_tuples:
#             node_to_append.extend(split_image_helper(tuple, img_node_text))
        
#         new_nodes.extend(node_to_append)
    
#     return new_nodes
            
# def split_image_helper(img_tuple, img_node_text):
#     per_tuple = []
#     anchor_txt = img_tuple[0]
#     url_txt = img_tuple[1]
#     img_split_node = img_node_text.split("![" + anchor_txt + "](" + url_txt + ")")
    
#     if len(img_split_node) == 1:
#         per_tuple.append(TextNode(img_split_node, TextType.TEXT))
    
#     for i in range(len(img_split_node)):
#         per_tuple.append((TextNode(img_split_node[i], TextType.TEXT)))
#         if i-1 < len(img_split_node):
#             per_tuple.append(TextNode(anchor_txt, TextType.IMAGE, url_txt))
    
#     return per_tuple

# from typing import List, Dict, Optional
# from textnode import TextNode, TextType
# from htmlnode import HTMLNode, LeafNode, ParentNode

# def split_nodes_delimiter(old_nodes: List, delimiter, text_type):
#     new_nodes = []
    
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.extend(node)    
        
#         if delimiter not in node.text:
#             new_nodes.extend(node)
#             continue
        
#         if (node.text[0] != delimiter and
#             node.text[-1] != delimiter and
#             len(node.split(delimiter)) % 2 != 1):
#             raise Exception("invalid markdown syntax (no closing delimiter case A")
        
#         if ((node.text[0] != delimiter ^
#             node.text[-1] != delimiter) and
#             len(node.split(delimiter)) % 2 != 0):
#             raise Exception("invalid markdown syntax (no closing delimiter case B)")

#         if node.text[0] != delimiter:       # and node.text[-1] != delimiter:
#             splits = node.text.split(delimiter)
#             nodes_to_append = []
#             for i in range(0, len(splits)): #need to adjust this?
#                 if i % 2 == 0:
#                     nodes_to_append.extend(TextNode(splits[i], TextType.TEXT))
#                 if i % 2 == 1:                       
#                     nodes_to_append.extend(TextNode(splits[i], delimiter_dict[delimiter]))
#             new_nodes.extend(nodes_to_append)
        
#   return new_nodes