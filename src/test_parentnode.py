import unittest
from parentnode import ParentNode

class Test_ParentNode(unittest.TestCase):

    def test_to_html_no_children(self):
        parent = ParentNode("div", [], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"></div>')

    def test_to_html_with_children(self):
        children = [ParentNode("p", [], {"class": "paragraph"}), ParentNode("p", [], {"class": "paragraph"})]
        parent = ParentNode("div", children, {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><p class="paragraph"></p><p class="paragraph"></p></div>')

    def test_to_html_nested_children(self):
        children = [ParentNode("i", [], {"class": "italic"}), ParentNode("i", [], {"class": "italic"})]
        parent = ParentNode("div", children, {"class": "container"})
        grand_parent = ParentNode("h1", [parent], {"class": "header"})

        self.assertEqual(grand_parent.to_html(), '<h1 class="header"><div class="container"><i class="italic"></i><i class="italic"></i></div></h1>')
    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, []).to_html()
