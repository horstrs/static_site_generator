class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError("children expected to implement")
    

    def props_to_html(self):
        if not self.props:
            return ""
        html_props = ""
        for key, value in self.props.items():
            html_props += f" {key}='{value}'"
        return html_props
    

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {repr(self.props)})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(value, tag, props)
    

    def to_html(self):
        if not self.value:
            raise ValueError("Invalid HTML: Leaf nodes must have a value!")
        if not self.tag or self.tag == "":
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
