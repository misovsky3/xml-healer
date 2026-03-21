from .ast import Node


def infer_root(node: Node) -> Node:
    children = [c for c in node.children if c.tag or c.text]

    if not children:
        return Node("", text="")

    # split prefix vs real elements
    prefix = []
    elements = []

    for c in children:
        if c.tag in ("__pi__", "__comment__", "__cdata__"):
            prefix.append(c)
        elif c.tag == "":
            prefix.append(c)  # text before root
        else:
            elements.append(c)

    # 1. single root element
    if len(elements) == 1:
        root = elements[0]

        # attach prefix BEFORE root
        return Node("__wrapper__", children=prefix + [root])

    # 2. multiple roots → wrap
    return Node("root", children=children)

