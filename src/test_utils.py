
import unittest
import utils
from textnode import TextNode, TextType
from htmlnode import HTMLNode

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


    # Splitting the nodes with image LINK tests
    # -------------------------------------------

    def test_split_nodes_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,
            )
        result = utils.split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
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
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
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
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2"),
            TextNode(" more text ", TextType.TEXT),
            TextNode("image3", TextType.IMAGE, "url3"),
        ]
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])

    def test_split_nodes_links_no_link(self):
        node = TextNode("This is text with no LINK", TextType.TEXT)
        result = utils.split_nodes_link([node])
        expected_nodes = [TextNode("This is text with no LINK", TextType.TEXT)]
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_links_multiple_links(self):
        node = TextNode("This is a [link1](url1) and another [link2](url2)", TextType.TEXT)
        result = utils.split_nodes_link([node])
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
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
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
        ]
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])

    # TODO: split test case
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = utils.text_to_textnodes(text)
        expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

        self.assertEqual(len(result), len(expected_nodes))

        for i in range(len(result)):
            self.assertEqual(result[i], expected_nodes[i])


    # TODO: split test case
    def test_markdown_to_blocks(self):
        markdown_text = """
            # This is a heading


             This is a paragraph of text. It has some **bold** and *italic* words inside of it.


            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""

        result = utils.markdown_to_blocks(markdown_text)
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]

        self.assertEqual(len(result), len(expected_blocks))

        for i in range(len(result)):
            self.assertEqual(result[i], expected_blocks[i])



    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "heading")

    def test_block_to_block_type_code_block(self):
        block = "```python\nprint('Hello, World!')\n```"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_type_code_block_invalid(self):
        block = "```python\nprint('Hello, World!')"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_quote(self):
        block = "> This is a quote block"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "quote")

    def test_block_to_block_type_unordered_list_star(self):
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_type_unordered_list_invalid_no_space_after_star(self):
        block = "* This is the first list item in a list block\n*This is a list item\n+ This is another list item"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_type_unordered_list_hyphen(self):
        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "ordered_list")

    def test_block_to_block_type_ordered_list_invalid(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n4. This is another list item"
        result = utils.block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    # ---------------------------
    # markdown to html node tests
    # ---------------------------
    def test_markdown_to_html_node_as_div(self):
        markdown_text = """
            This is a paragraph of text.
            """
        result = utils.markdown_to_html_node(markdown_text)
        self.assertEqual(result.tag, "div")

    def test_markdown_to_html_node_paragraph(self):
        markdown_text = """

            This is a paragraph of text.
            """
        result = utils.markdown_to_html_node(markdown_text)
        children = ["This is a paragraph of text."]
        expected = [HTMLNode("p", None, children)]
        self.assertEqual(result.children, expected)

    def test_markdown_to_html_node_heading(self):
        markdown_text = """
            # This is a heading
            """
        result = utils.markdown_to_html_node(markdown_text)
        children = ["This is a heading"]
        expected = [HTMLNode("h1", None, children)]
        self.assertEqual(result.children, expected)

    def test_markdown_to_html_node_heading(self):
        markdown_text = """
            # This is a heading

            ## This is a level 2 heading

            ###### This is a level 6 heading
        """

        result = utils.markdown_to_html_node(markdown_text)
        expected = HTMLNode("div", children=[
            HTMLNode("h1", children=["This is a heading"]),
            HTMLNode("h2", children=["This is a level 2 heading"]),
            HTMLNode("h6", children=["This is a level 6 heading"])
        ])
        self.assertEqual(result, expected)

    def test_markdown_to_html_node_code_block(self):
        markdown_text = """
        ```print('Hello, World!')```
        """
        result = utils.markdown_to_html_node(markdown_text)
        children = ["print('Hello, World!')"]
        expected = [HTMLNode("code", None, children)]
        self.assertEqual(result.children, expected)

    def test_markdown_to_html_node_quote(self):
        markdown_text = """
            >This is a quote block
            """
        result = utils.markdown_to_html_node(markdown_text)
        children = ["This is a quote block"]
        expected = [HTMLNode("q", None, children)]
        self.assertEqual(result.children, expected)

    def test_markdown_to_html_node_unordered_list(self):
        markdown_text = """
        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = utils.markdown_to_html_node(markdown_text)
        children = [
            HTMLNode("li", None, ["This is the first list item in a list block"]),
            HTMLNode("li", None, ["This is a list item"]),
            HTMLNode("li", None, ["This is another list item"]),
        ]
        expected = [HTMLNode("ul", None, children)]
        self.assertEqual(result.children, expected)

    def test_markdown_to_html_node_ordered_list(self):
        markdown_text = """
        1. This is the first list item in a list block
        2. This is a list item
        3. This is another list item
        """
        result = utils.markdown_to_html_node(markdown_text)
        children = [
            HTMLNode("li", None, ["This is the first list item in a list block"]),
            HTMLNode("li", None, ["This is a list item"]),
            HTMLNode("li", None, ["This is another list item"]),
        ]
        expected = [HTMLNode("ol", None, children)]
        self.assertEqual(result.children, expected)


    def test_extract_title(self):
        markdown_text = """
            ###### This is a level 6 heading

            ## This is a level 2 heading

            # This is a heading
        """

        result = utils.extract_title(markdown_text)
        self.assertEqual(result, "This is a heading")


    def test_extract_title_no_title_found(self):
        markdown_text = """
            ###### This is a level 6 heading

            ## This is a level 2 heading
        """
        with self.assertRaises(Exception):
            utils.extract_title(markdown_text)