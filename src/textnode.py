from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return text_node.text
        elif text_node.text_type == TextType.BOLD:
            return f"<b>{text_node.text}</b>"
        elif text_node.text_type == TextType.ITALIC:
            return f"<i>{text_node.text}</i>"
        elif text_node.text_type == TextType.CODE:
            return f"<code>{text_node.text}</code>"
        elif text_node.text_type == TextType.LINKS:
            return f'<a href="{text_node.url}">{text_node.text}</a>'
        elif text_node.text_type == TextType.IMAGES:
            return f'<img src="{text_node.url}" alt="{text_node.text}">'
        else:
            raise ValueError("Invalid text type")