import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode


# Inputs = (text, text_type, url=None)
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_are_inputs_equal(self):
        node = TextNode("testing", TextType.ITALIC)
        node2 = TextNode("testing", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_is_text_not_equal(self):
        node = TextNode("testing", TextType.ITALIC)
        node2 = TextNode("test", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_defaultURL_value(self):
        node = TextNode("testing", TextType.BOLD)
        self.assertEqual(node.url, None)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link_text(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_link_without_url_raises_error(self):
        node = TextNode("Click here", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_text(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Images don't have inner text
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.jpg", "alt": "An image"}
        )

    def test_image_without_url_raises_error(self):
        node = TextNode("An image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_text_type_raises_error(self):
        node = TextNode("Invalid", "InvalidType")  # Not in TextType enum
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_non_textnode_input_raises_error(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("Not a TextNode")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_node_no_delimiter(self):
        old_nodes = [TextNode("hello", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, ",", TextType.TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertIsInstance(new_nodes[0], LeafNode)
        self.assertEqual(new_nodes[0].value, "hello")

    def test_multiple_nodes_no_delimiter(self):
        old_nodes = [TextNode("hello", TextType.TEXT), TextNode("world", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, ",", TextType.TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertIsInstance(new_nodes[0], LeafNode)
        self.assertEqual(new_nodes[0].value, "helloworld")

    def test_single_node_with_delimiter(self):
        old_nodes = [
            TextNode("hello", TextType.TEXT),
            TextNode(",", TextType.TEXT),
            TextNode("world", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, ",", TextType.TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertIsInstance(new_nodes[0], LeafNode)
        self.assertEqual(new_nodes[0].value, "hello")
        self.assertIsInstance(new_nodes[1], LeafNode)
        self.assertEqual(new_nodes[1].value, ",")
        self.assertIsInstance(new_nodes[2], LeafNode)
        self.assertEqual(new_nodes[2].value, "world")

    def test_multiple_nodes_with_delimiter(self):
        old_nodes = [
            TextNode("hello", TextType.TEXT),
            TextNode(",", TextType.TEXT),
            TextNode("world", TextType.TEXT),
            TextNode(",", TextType.TEXT),
            TextNode("foo", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, ",", TextType.TEXT)
        self.assertEqual(len(new_nodes), 5)
        self.assertIsInstance(new_nodes[0], LeafNode)
        self.assertEqual(new_nodes[0].value, "hello")
        self.assertIsInstance(new_nodes[1], LeafNode)
        self.assertEqual(new_nodes[1].value, ",")
        self.assertIsInstance(new_nodes[2], LeafNode)
        self.assertEqual(new_nodes[2].value, "world")
        self.assertIsInstance(new_nodes[3], LeafNode)
        self.assertEqual(new_nodes[3].value, ",")
        self.assertIsInstance(new_nodes[4], LeafNode)
        self.assertEqual(new_nodes[4].value, "foo")


if __name__ == "__main__":
    unittest.main()
