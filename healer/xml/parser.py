import re
from .types import Token
from .fuzzy import normalize_tag

XML_DECLARATION_RE = re.compile(r"<\?xml[^>]*\?>")
TAG_RE = re.compile(r"</?[^>]+>")


def tokenize(xml: str):
    tokens = []

    # 1. extract XML declaration
    decl_match = XML_DECLARATION_RE.search(xml)
    if decl_match:
        tokens.append(Token("declaration", decl_match.group()))
        xml = xml.replace(decl_match.group(), "")

    pos = 0

    for match in TAG_RE.finditer(xml):
        start, end = match.span()

        if start > pos:
            text = xml[pos:start]
            if text.strip():
                tokens.append(Token("text", text))

        tag = match.group()

        if tag.startswith("</"):
            tokens.append(Token("close", tag[2:-1].strip()))
        else:
            tokens.append(Token("open", tag[1:-1].split()[0].strip()))

        pos = end

    if pos < len(xml):
        tail = xml[pos:]
        if tail.strip():
            tokens.append(Token("text", tail))

    return tokens

def parse_and_fix(tokens):
    stack = []
    output = []

    for t in tokens:

        if t.type == "declaration":
            output.append(t.value)

        elif t.type == "text":
            output.append(t.value)

        elif t.type == "open":
            tag = t.value.lower()
            output.append(f"<{tag}>")
            stack.append(tag)

        elif t.type == "close":
            tag = normalize_tag(t.value, stack)

            if stack and stack[-1] == tag:
                output.append(f"</{tag}>")
                stack.pop()
            else:
                # fuzzy fix: try to close something valid
                if tag in stack:
                    # pop until we find it
                    while stack:
                        top = stack.pop()
                        output.append(f"</{top}>")
                        if top == tag:
                            break
                else:
                    # ignore bad closing
                    continue

    # close remaining
    while stack:
        output.append(f"</{stack.pop()}>")

    return "".join(output)
