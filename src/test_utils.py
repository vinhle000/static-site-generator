
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


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = utils.extract_markdown_images(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(result[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = utils.extract_markdown_links(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(result[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))

       # missing ']' in the first link and '!' in the second image
    def test_extract_markdown_images(self):
        # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = utils.extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    # First is image link and second is text link
    def test_invalid_markdown_links(self):
        # text = "This is text with a  image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and link [to youtube](https://www.youtube.com/@bootdotdev"
        text = "This is text with a IMAGE ![rick roll](https://i.imgur.com/aKaOqIh.gif) and LINK [to youtube](https://www.youtube.com/@bootdotdev)"
        result = utils.extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("to youtube", "https://www.youtube.com/@bootdotdev"))