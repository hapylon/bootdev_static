import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_bold_middle(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_bold_start(self):
        node = TextNode("**Bold** then plain", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " then plain")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_split_multiple_bold_segments(self):
        node = TextNode("A **bold** and **strong** sentence", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        texts = [n.text for n in result]
        types = [n.text_type for n in result]

        self.assertEqual(
            texts, ["A ", "bold", " and ", "strong", " sentence"]
        )
        self.assertEqual(
            types,
            [
                TextType.TEXT, TextType.BOLD,
                TextType.TEXT, TextType.BOLD,
                TextType.TEXT,
            ],
        )

    def test_split_no_delimiter_kept(self):
        node = TextNode("Nothing special here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_split_skips_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_split_raises_on_unclosed_bold(self):
        node = TextNode("This is **broken", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_inline_code(self):
        node = TextNode("Use `print()` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        texts = [n.text for n in result]
        types = [n.text_type for n in result]

        self.assertEqual(texts, ["Use ", "print()", " here"])
        self.assertEqual(
            types,
            [TextType.TEXT, TextType.CODE, TextType.TEXT],
        )

if __name__ == "__main__":
    unittest.main()





# import unittest
# # import pytest

# from textnode import TextNode, TextType
# from split_nodes import split_nodes_delimiter

# class TestTextNode(unittest.TestCase):

#     def test_split_bold_middle(self):
#         node = TextNode("This is **bold** text", TextType.TEXT)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)

#         assert len(result) == 3
#         assert result[0].text == "This is "
#         assert result[0].text_type == TextType.TEXT
#         assert result[1].text == "bold"
#         assert result[1].text_type == TextType.BOLD
#         assert result[2].text == " text"
#         assert result[2].text_type == TextType.TEXT

#     def test_split_bold_start(self):
#         node = TextNode("**Bold** then plain", TextType.TEXT)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)

#         assert len(result) == 2
#         assert result[0].text == "Bold"
#         assert result[0].text_type == TextType.BOLD
#         assert result[1].text == " then plain"
#         assert result[1].text_type == TextType.TEXT

#     def test_split_multiple_bold_segments(self):
#         node = TextNode("A **bold** and **strong** sentence", TextType.TEXT)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)

#         texts = [n.text for n in result]
#         types = [n.text_type for n in result]

#         assert texts == ["A ", "bold", " and ", "strong", " sentence"]
#         assert types == [
#             TextType.TEXT, TextType.BOLD,
#             TextType.TEXT, TextType.BOLD,
#             TextType.TEXT,
#         ]

#     def test_split_no_delimiter_kept(self):
#         node = TextNode("Nothing special here", TextType.TEXT)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)

#         assert result == [node]

#     def test_split_skips_non_text_node(self):
#         node = TextNode("already bold", TextType.BOLD)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)

#         assert result == [node]

#     def test_split_raises_on_unclosed_bold(self):
#         node = TextNode("This is **broken", TextType.TEXT)
#         try:
#             split_nodes_delimiter([node], "**", TextType.BOLD)
#             # If we get here, no exception was raised → fail the test
#             assert False, "Expected an exception for unclosed bold delimiter"
#         except Exception:
#             # Any exception counts as success for this test
#             assert True

#     def test_split_inline_code(self):
#         node = TextNode("Use `print()` here", TextType.TEXT)
#         result = split_nodes_delimiter([node], "`", TextType.CODE)

#         texts = [n.text for n in result]
#         types = [n.text_type for n in result]

#         assert texts == ["Use ", "print()", " here"]
#         assert types == [
#             TextType.TEXT, TextType.CODE, TextType.TEXT
#         ]


