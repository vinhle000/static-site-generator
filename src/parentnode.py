from htmlnode import HTMLNode


# If the object doesn't have a tag, raise a ValueError.
# If there are no children, raise a ValueError with a different message.
# Otherwise, return a string representing the HTML tag of the node and
# its children. This should be a recursive method (each recursion being called on a nested child node). I iterated over all the children and called to_html on each, concatenating the results
# and injecting them between the opening and closing tags of the parent.
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if self.tag is None:
           raise ValueError("Parent nodes must have a tag")

        children_html = ''.join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

