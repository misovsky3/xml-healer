import re
from .types import Token


TAG_RE = re.compile(r"</?[^>]+>")


def tokenize(xml: str):
    """
    Converts raw XML into structured tokens.
    """

    pos = 0
    tokens = []

    for match in TAG_RE.finditer(xml):
        start, end = match.span()

        # text before tag
        if start > pos:
            text = xml[pos:start]
            if text.strip():
                tokens.append(Token("text", text))

        tag = match.group()

        if tag.startswith("</"):
            tokens.append(Token("close", tag[2:-1]))
        else:
            tokens.append(Token("open", tag[1:-1].split()[0]))

        pos = end

    # remaining text
    if pos < len(xml):
        text = xml[pos:]
        if text.strip():
            tokens.append(Token("text", text))

    return tokens


def parse_and_fix(tokens):
    stack = []
    output = []

    for t in tokens:
        if t.type == "text":
            output.append(t.value)

        elif t.type == "open":
            output.append(f"<{t.value}>")
            stack.append(t.value)

        elif t.type == "close":
            if stack and stack[-1] == t.value:
                output.append(f"</{t.value}>")
                stack.pop()
            else:
                # invalid closing tag → ignore
                continue

    # close remaining
    while stack:
        tag = stack.pop()
        output.append(f"</{tag}>")

    return "".join(output)
