from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(value, tag, props)
    

    def to_html(self):
        if not self.value:
            raise ValueError("Invalid HTML: Leaf nodes must have a value!")
        if not self.tag or self.tag == "":
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"