from .ast import Node
import re
from .types import Token

ATTR_RE = re.compile(r'([a-zA-Z_:][a-zA-Z0-9_:.-]*)="([^"]*)"')
XML_DECLARATION_RE = re.compile(r"<\?xml[^>]*\?>")
TAG_RE = re.compile(r"</?[^>]+>")
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
CDATA_RE = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.DOTALL)
PI_RE = re.compile(r"<\?(?!xml)(.*?)\?>", re.DOTALL)
SPECIAL_RE = re.compile(
    r"(<!--.*?-->|<!\[CDATA\[.*?\]\]>|<\?.*?\?>|</?[^>]+>)",
    re.DOTALL
)

def tokenize(xml: str):
    tokens = []

    pos = 0

    for match in SPECIAL_RE.finditer(xml):
        start, end = match.span()

        # text
        if start > pos:
            text = xml[pos:start]
            if text.strip():
                tokens.append(Token("text", text))

        chunk = match.group()

        # XML declaration
        if chunk.startswith("<?xml "):
            tokens.append(Token("declaration", chunk))

        # processing instruction
        elif chunk.startswith("<?"):
            tokens.append(Token("pi", chunk))

        # comment
        elif chunk.startswith("<!--"):
            tokens.append(Token("comment", chunk))

        # CDATA
        elif chunk.startswith("<![CDATA["):
            tokens.append(Token("cdata", chunk))

        # closing tag
        elif chunk.startswith("</"):
            tokens.append(Token("close", chunk[2:-1].strip()))

        # opening / self-closing
        else:
            tag_content = chunk[1:-1].strip()

            is_self_closing = tag_content.endswith("/")
            if is_self_closing:
                tag_content = tag_content[:-1].strip()

            tag_name, attrs = parse_tag(tag_content)

            tokens.append(Token("open", (tag_name, attrs)))

            if is_self_closing:
                tokens.append(Token("close", tag_name))

        pos = end

    # tail
    if pos < len(xml):
        tail = xml[pos:]
        if tail.strip():
            tokens.append(Token("text", tail))

    return tokens






def build_ast(tokens):
    virtual_root = Node("__root__")
    stack = [virtual_root]

    for t in tokens:
        if t.type == "text":
            stack[-1].children.append(Node(tag="", text=t.value))
        elif t.type == "close":
            # Record the actual closing tag as close_tag in the node
            if len(stack) > 1:
                node = stack[-1]
                node.close_tag = t.value
                if node.tag == t.value:
                    stack.pop()
                # If tag does not match, do not pop, but still record close_tag
            else:
                continue
        elif t.type == "open":
            tag_name, attrs = t.value
            node = Node(tag=tag_name, attrs=attrs, original_tag=tag_name)
            stack[-1].children.append(node)
            stack.append(node)
        elif t.type == "comment":
            stack[-1].children.append(Node(tag="__comment__", text=t.value))
        elif t.type == "cdata":
            stack[-1].children.append(Node(tag="__cdata__", text=t.value))
        elif t.type == "pi":
            stack[-1].children.append(Node(tag="__pi__", text=t.value))
    return virtual_root


def parse_tag(tag_str: str):
    """
    Extract tag name + attributes.
    """

    parts = tag_str.strip().split()
    tag = parts[0]

    attrs = dict(ATTR_RE.findall(tag_str))

    return tag, attrs
