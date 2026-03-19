import re
from .errors import ErrorType


def classify(xml: str) -> list[ErrorType]:
    errors: list[ErrorType] = []

    # 1. missing closing tags (very naive heuristic)
    open_tags = len(re.findall(r"<[a-zA-Z0-9_]+>", xml))
    close_tags = len(re.findall(r"</[a-zA-Z0-9_]+>", xml))

    if open_tags > close_tags:
        errors.append(ErrorType.MISSING_CLOSING_TAG)

    # 2. unexpected closing
    if close_tags > open_tags:
        errors.append(ErrorType.UNEXPECTED_CLOSING_TAG)

    # 3. broken tags
    if re.search(r"<[^>]*<", xml):
        errors.append(ErrorType.BROKEN_TAG)

    # 4. encoding issues (very simple heuristic)
    if "�" in xml:
        errors.append(ErrorType.ENCODING_ISSUE)

    # 5. malformed structure (very simple heuristic)
    if re.search(r"[a-z]</[a-z]", xml):
        errors.append(ErrorType.MALFORMED_STRUCTURE)

    return errors
