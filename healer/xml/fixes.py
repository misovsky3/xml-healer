import re


TAG_REGEX = re.compile(r"<(/?)([a-zA-Z0-9_:-]+)([^>]*)>")


def fix_unclosed_tags(xml: str) -> str:
    """
    Naive stack-based XML fixer.
    """

    stack = []
    output = []

    tokens = TAG_REGEX.split(xml)

    for i in range(0, len(tokens), 4):
        text = tokens[i]

        if text:
            output.append(text)

        if i + 3 < len(tokens):
            slash = tokens[i + 1]
            tag = tokens[i + 2]

            if slash == "":
                # opening tag
                output.append(f"<{tag}>")
                stack.append(tag)

            else:
                # closing tag
                if stack and stack[-1] == tag:
                    output.append(f"</{tag}>")
                    stack.pop()
                else:
                    # ignore broken closing
                    continue

    # close remaining tags
    while stack:
        tag = stack.pop()
        output.append(f"</{tag}>")

    return "".join(output)
