from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # todo maybe check delimiter char vs a valid TextType
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            text = node.text

            if not text.count(delimiter) % 2 == 0:
                raise Exception("invalid Markdown")

            while delimiter in text:
                chunks = text.split(delimiter, maxsplit = 2)
                if len(chunks[0]) > 0: # Add the text before the delimiter if not empty
                    new_text_node = TextNode(chunks[0], TextType.TEXT)
                    new_nodes.append(new_text_node)
                new_text_type_node = TextNode(chunks[1], text_type)
                new_nodes.append(new_text_type_node)

                text = chunks[2]

            # Add the remaining text as a TextNode
            if text:
                new_text_node = TextNode(text, TextType.TEXT)
                new_nodes.append(new_text_node)


        else:
            new_nodes.append(node)


        return new_nodes
