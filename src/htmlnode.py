

class HTMLNode():
    def __init__(self, tag = None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self ):
        props = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        children_str = "".join(child.to_html() if isinstance(child, HTMLNode) else str(child) for child in self.children)
        if props:
            return f"<{self.tag} {props}>{children_str}</{self.tag}"
        else:
            return f"<{self.tag}>{children_str}</{self.tag}>"

    def props_to_html(self):
        props_list = []

        for k, v in self.props.items():
            str = f' {k}="{v}"'
            props_list.append(str)

        return "".join(props_list)


    def __repr__(self):
        props = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        children_str = "".join(str(child) for child in self.children)
        return f"<{self.tag}{props}>{children_str}</{self.tag}>"


    # For unit testing
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.props == other.props and
                self.children == other.children)
