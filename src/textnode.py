from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITAL = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode_2):
        if (
            self.text == TextNode_2.text and
            self.text_type == TextNode_2.text_type and
            self.url == TextNode_2.url
            ):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        if self.text_type not in TextType:
            raise Exception("text type not in TextType enum")
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=self.text, props=None)
            case TextType.BOLD:
                return LeafNode(tag="b", value=self.text, props=None)
            case TextType.ITAL:
                return LeafNode(tag="i", value=self.text, props=None)
            case TextType.CODE:
                return LeafNode(tag="code", value=self.text, props=None)
            case TextType.LINK:
                return LeafNode(tag="a", value=self.text, props={"url": self.url})
            case TextType.IMAGE:
                return LeafNode(tag="img", value="", props={"url": self.url, "alt": self.text})
            