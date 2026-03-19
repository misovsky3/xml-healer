import difflib


def normalize_tag(tag: str, open_stack: list[str]) -> str:
    """
    Try to match broken tag to closest known open tag.
    """

    if not open_stack:
        return tag

    match = difflib.get_close_matches(tag.lower(), open_stack, n=1, cutoff=0.6)

    if match:
        return match[0]

    return tag.lower()
