

from blocks import BlockType, markdown_to_blocks, block_to_block_type, is_ordered_list
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode

def markdown_to_html(markdown_text):
    block_list = markdown_to_blocks(markdown_text)
    gd_children = []
    grandaddy = HTMLNode(tag="div", children=gd_children)
    for block in block_list:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEAD:
            num = 0
            for  i in range(0,7):
                if i == "#":
                    num += 1 
            tag = block_tag(block_type, num)   
        elif block_type == BlockType.CODE:
            # SPECIAL HELPER TO NEST <pre> AND <code> TAGS --- AND WRAP LINES --- AND APPEND TO GD_CHILDREN
            continue
        else:
            tag = block_tag(block_type)
        
        value = None
        children = text_to_children(block)
        props = None
        


        if not value or value == None: 
            html_block = ParentNode(tag, children, props)
        if not children or children == None:
            html_block = LeafNode(tag, value, props)
        
        gd_children.append(html_block)

    return grandaddy




def block_tag(block_type, num=None):
    if block_type == BlockType.HEAD:
        return f"h{num}"
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORD:
        return "ul"                 # NOTE NEED TO ALSO WRAP INDIVIDUAL LINES WITH "li" TAG
    if block_type == BlockType.ORD:
        return "ol"                 # NOTE NEED TO ALSO WRAP INDIVIDUAL LINES WITH "li" TAG
    if block_type == BlockType.PARA:
        return "p"
    if block_type == BlockType.CODE:
        return "code"                 # NOTE NEED TO NEST <code> TAG INSIDE <pre> TAG
    



def text_to_children(markdown_text):
    if markdown_text == "":
        return
    text_nodes = text_to_textnodes(markdown_text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(TextNode.text_node_to_html_node(node))
    return html_nodes
