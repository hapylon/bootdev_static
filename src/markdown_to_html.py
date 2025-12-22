

from blocks import BlockType, markdown_to_blocks, block_to_block_type, strip_unord_list_lines, strip_ord_list_lines, strip_quote_lines
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode
from blocks import (
    BlockType, 
    markdown_to_blocks, 
    block_to_block_type, 
    strip_unord_list_lines,
    strip_ord_list_lines, 
    strip_quote_lines
)

def markdown_to_html(markdown_text):
    block_list = markdown_to_blocks(markdown_text)
    gd_children = []
    
    for block in block_list:
        block_type = block_to_block_type(block)
        
        # # if block_type == BlockType.HEAD:
        # #     num = 0
        # #     adjust = False
        # #     for  i in range(0,7):
        # #         if i >= len(block):
        # #             break
        # #         if block[i] == "#":
        # #             num += 1 
        # #         elif block[i] != " ":
        # #             adjust = True
        # #             break
                
        #     tag = block_tag(block_type, num)   
        #     # header_child = LeafNode(tag="p", value=block[i:])
        #     # html_block = ParentNode(tag=tag, children=header_child).to_html()
        #     if adjust == True:
        #         html_block = LeafNode(tag=tag, value=block[num:])
        #     elif adjust == False:
        #         html_block = LeafNode(tag=tag, value=block[num+1:])
        #     gd_children.append(html_block)
        #     continue
        if block_type == BlockType.HEAD:
            num = 0
            for ch in block:
                if ch == "#":
                    num += 1
                else:
                    break
            tag = block_tag(block_type, num)
            text = block[num+1:]  # skip hashes and the required space
            html_block = LeafNode(tag=tag, value=text)
            gd_children.append(html_block)
            continue

        elif block_type == BlockType.CODE:
            tag = block_tag(block_type)
            strip_block = block.splitlines()
            if len(strip_block) <= 2:
                clean_block = "\n".join(strip_block[1:-1])  # will be "" anyway
                # clean_block = ""
            else:
                clean_block = "\n".join(strip_block[1:-1])
            code_child = [LeafNode(tag, clean_block)]
            html_block = ParentNode(tag="pre", children=code_child)
            gd_children.append(html_block)
            continue

        elif block_type == BlockType.UNORD:
            tag = block_tag(block_type)
            list_nodes = strip_unord_list_lines(block)
            
            list_children = []
            for item in list_nodes:
                item_nodes = text_to_children(item)
                list_child = ParentNode(tag="li", children=item_nodes)
                list_children.append(list_child)
            html_block = ParentNode(tag=tag, children = list_children)
            gd_children.append(html_block)
            continue

        elif block_type == BlockType.ORD:
            tag = block_tag(block_type)
            list_nodes = strip_ord_list_lines(block)
            list_children = []
            for item in list_nodes:
                item_nodes = text_to_children(item)
                list_child = ParentNode(tag="li", children=item_nodes)
                list_children.append(list_child)
            html_block = ParentNode(tag=tag, children = list_children)
            gd_children.append(html_block)
            continue
        
        elif block_type == BlockType.QUOTE:
            tag = block_tag(block_type)
            list_nodes = strip_quote_lines(block)
            list_children = []
            for item in list_nodes:
                item_nodes = text_to_children(item)
                list_children.extend(item_nodes)
            html_block = ParentNode(tag=tag, children = list_children)
            gd_children.append(html_block)
            continue

        else:
            tag = block_tag(block_type)
            list_children = text_to_children(block)
            html_block = ParentNode(tag=tag, children=list_children)
            gd_children.append(html_block)
            continue
        
    # TEMP TEST
    gd_children.append(
        LeafNode("img", "", {"src": "images/tolkien.png", "alt": "Test"})
    )   
    grandaddy = ParentNode(tag="div", children=gd_children)
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
    
    text_nodes = text_to_textnodes(markdown_text)
    return [node.text_node_to_html_node() for node in text_nodes]
    # if markdown_text == "":
    #     return
    # html_nodes = []
    # text_nodes = text_to_textnodes(markdown_text)
    # for node in text_nodes:
    #     html_nodes.append(TextNode.text_node_to_html_node(node))
    # return html_nodes
