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
        node = TextNode("This is a text node", TextType.LINKS, "http://www.boot.dev")
        self.assertEqual(node.text_node_to_html_node(), '<a href="http://www.boot.dev">This is a text node</a>')
        node = TextNode("This is a text node", TextType.IMAGES, "http://www.boot.dev")
        self.assertEqual(node.text_node_to_html_node(), '<img src="http://www.boot.dev" alt="This is a text node">')

    def test_split_nodes_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_split_nodes_italic_delimiter(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)

        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_split_nodes_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_split_nodes_delimiter_at_start(self):
        node = TextNode("**This** is text with a **Bolded** word at start", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)

        expected_nodes = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("Bolded", TextType.BOLD),
            TextNode(" word at start", TextType.TEXT),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("This is text with a **Bolded** word at **end**", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
        # self.assertEqual(len(new_nodes), 4)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("Bolded", TextType.BOLD),
            TextNode(" word at ", TextType.TEXT),
             TextNode("end", TextType.BOLD),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and `another code block` word", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])


    def test_invalid_markdown(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            utils.split_nodes_delimiter([node], "`", TextType.CODE)




if __name__ == "__main__":
    unittest.main()

# hen the url property is None,
# or when the text_type property is different.
# You'll want to make sure that when properties  are different, the TextNode objects are not equal.