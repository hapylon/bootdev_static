from typing import List, Dict, Optional

class HTMLNode:
    def __init__(
            self, tag: Optional[str] = None, 
            value: Optional[str] = None, 
            children: Optional[List] = None, 
            props: Optional[Dict] = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        list_props = ""
        if self.props: 
            for i in self.props:
                list_props += (f" {i}={self.props[i]}")
        return list_props
    
    def __repr__(self):
        result = (f"tag: {self.tag} \n" \
        f"value: {self.value}\n" \
        f"children: {self.children}\n" \
        f"props: {self.props}")
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Optional[Dict] = None):
        super().__init__(tag, value, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("no self.value")
        if not self.tag:
            return self.value
        return f'<{self.tag}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List, props: Optional[Dict] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing self.tag")
        if self.children is None:
            raise ValueError("missing self.children")
        children_to_inject = ""
        for child_ in self.children:
            children_to_inject += child_.to_html()
        return f'<{self.tag}>{children_to_inject}</{self.tag}>'
