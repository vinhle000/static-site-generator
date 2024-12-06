
import unittest
import utils
from textnode import TextNode, TextType

class TestUtils(unittest.TestCase):

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
