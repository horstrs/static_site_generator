class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children and type(children) is not list:
            raise TypeError
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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    

    def to_html(self):
        if self.value is None:
            raise ValueError(f"Invalid HTML: leaf nodes must have a value! Node: {self}")
        if not self.tag or self.tag == "":
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    
    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Invalid HTML: tag missing in parent node. Node: {self}")
        if self.children is None:
            raise ValueError(f"Invalid HTML: children missing in parent node. Node: {self}")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html_string += node.to_html()
        html_string += f"</{self.tag}>"
        return html_string