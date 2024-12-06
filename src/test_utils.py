
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


    # Splitting the nodes with image links tests
    # -------------------------------------------

    def test_split_nodes_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,
            )
        result = utils.split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGES, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])


    def split_nodes_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            )
        result = utils.split_nodes_links([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])

    def test_split_nodes_images_no_image(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        result = utils.split_nodes_image([node])
        expected_nodes = [TextNode("This is text with no images", TextType.TEXT)]
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_images_multiple_images(self):
        node = TextNode("![image1](url1) text ![image2](url2) more text ![image3](url3)", TextType.TEXT)
        result = utils.split_nodes_image([node])
        expected_nodes = [
            TextNode("image1", TextType.IMAGES, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("image2", TextType.IMAGES, "url2"),
            TextNode(" more text ", TextType.TEXT),
            TextNode("image3", TextType.IMAGES, "url3"),
        ]
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])

    def test_split_nodes_links_no_link(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        result = utils.split_nodes_link([node])
        expected_nodes = [TextNode("This is text with no links", TextType.TEXT)]
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_links_multiple_links(self):
        node = TextNode("This is a [link1](url1) and another [link2](url2)", TextType.TEXT)
        result = utils.split_nodes_link([node])
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link1", TextType.LINKS, "url1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINKS, "url2"),
        ]
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])

    def test_split_nodes_links_and_images(self):
        node = TextNode("This is a [link](url) and an image ![image](url)", TextType.TEXT)
        result = utils.split_nodes_link([node])
        result = utils.split_nodes_image(result)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "url"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "url"),
        ]
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])