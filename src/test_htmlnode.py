import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class HTMLNode_test(unittest.TestCase):
    # def test_eq(self):
    #     node = HTMLNode("a", "This is a test paragraph.", None ,{"href": "https://www.google.com"})
    #     node2 = HTMLNode("a", "This is a test paragraph.", None ,{"href": "https://www.google.com"})
    #     self.assertEqual(node, node2)

    def test_props(self):
        node = HTMLNode(tag="a",value="This is a test link.", props={"href": "https://www.google.com"})
        # node2 = HTMLNode("a", "This is a test link.", {"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href=https://www.google.com')

    def test_props2(self):
        node2 = HTMLNode(tag="a", value="This is a test link.", props={"href": "https://www.google.com", "target": "_blank"})
        result = node2.props_to_html()
        self.assertEqual(result, ' href=https://www.google.com target=_blank')

    def test_props3(self):
        node2 = HTMLNode(tag="a", value="This is a test link.", props={"href": "https://www.google.com", "target": "_blank"})
        result = str(node2)
        self.assertNotEqual(result, 'test')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()