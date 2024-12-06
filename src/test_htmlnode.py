import unittest

from htmlnode import HTMLNode

class TestHTMLnode(unittest.TestCase):
    def test_default_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props={ "href": "https://example.com",
                               "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')


    def test_children_handling(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[1].value, "Child 2")
