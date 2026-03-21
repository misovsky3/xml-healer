from .ast import Node


def to_xml(node: Node) -> str:
    if node.tag == "":
        return node.text or ""

    if node.tag in ("__comment__", "__cdata__", "__pi__", "__declaration__"):
        return node.text or ""

    # 🔥 wrapper = no tag, just children
    if node.tag == "__wrapper__":
        return "".join(to_xml(c) for c in node.children)

    attrs = serialize_attrs(node.attrs)
    inner = "".join(to_xml(c) for c in node.children)

    return f"<{node.tag}{attrs}>{inner}</{node.tag}>"




def serialize_attrs(attrs: dict) -> str:
    if not attrs:
        return ""
    return " " + " ".join(f'{k}="{v}"' for k, v in attrs.items())
