import unittest
import utils
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node1", TextType.BOLD)
        node2 = TextNode("This is text node2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node_no_url = TextNode("Has no url, should be None", TextType.BOLD)
        node_with_url = TextNode("has url", TextType.BOLD, "http://www.boot.dev")
        self.assertEqual(node_no_url.url, None)
        self.assertEqual(node_with_url.url, "http://www.boot.dev" )

    def test_text_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_node_to_html_node(), "<b>This is a text node</b>")
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_node_to_html_node(), "<i>This is a text node</i>")
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text_node_to_html_node(), "<code>This is a text node</code>")
        node = TextNode("This is a text node", TextType.LINK, "http://www.boot.dev")
        self.assertEqual(node.text_node_to_html_node(), '<a href="http://www.boot.dev">This is a text node</a>')
        node = TextNode("This is a text node", TextType.IMAGE, "http://www.boot.dev")
        self.assertEqual(node.text_node_to_html_node(), '<img src="http://www.boot.dev" alt="This is a text node">')




if __name__ == "__main__":
    unittest.main()

# hen the url property is None,
# or when the text_type property is different.
# You'll want to make sure that when properties  are different, the TextNode objects are not equal.