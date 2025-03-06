import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_node_with_tag_and_value(self):
        node = HTMLNode(tag="p", value="Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a", props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="div", value="Test", props={"class": "container"})
        expected_repr = (
            "HTMLNode(tag=div, value=Test, children=[], props={'class': 'container'})"
        )
        self.assertEqual(repr(node), expected_repr)


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)


class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First child")
        child2 = LeafNode("p", "Second child")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(), "<div><p>First child</p><p>Second child</p></div>"
        )

    def test_to_html_with_nested_parents(self):
        inner_child = LeafNode("em", "Nested child")
        inner_parent = ParentNode("span", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(
            outer_parent.to_html(), "<div><span><em>Nested child</em></span></div>"
        )

    def test_to_html_raises_value_error_for_missing_tag(self):
        child = LeafNode("span", "Child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])

    def test_to_html_raises_value_error_for_missing_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_to_html_raises_value_error_for_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])


if __name__ == "__main__":
    unittest.main()
