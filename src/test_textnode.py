import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
