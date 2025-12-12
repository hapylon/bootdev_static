import unittest

from unittest import TestCase
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(TestCase):

    def test_text_to_textnodes_complex(self):
        text = (
            "This is **bold** and _italic_ with `code`, "
            "an ![image](https://img.com/a.png) and a "
            "[link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITAL),
                TextNode(" with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://img.com/a.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_lesson(self):
        markdown_text = (
            "This is **text** with an _italic_ word and a `code block` and "
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and "
            "a [link](https://boot.dev)"
            )
        
        nodes = text_to_textnodes(markdown_text)

        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITAL),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()