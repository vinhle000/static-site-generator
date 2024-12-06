import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_to_html_with_value(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "intro"})
        self.assertEqual(node.to_html(), '<p class="intro"> Hello, world!</p>')

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError) as context:
            LeafNode("h1", None).to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!", props={"class": "intro"})
        self.assertEqual(node.to_html(), 'Hello, world!')
