from enum import Enum
class ErrorType(Enum):
    MISSING_CLOSING_TAG = "missing_closing_tag"
    UNEXPECTED_CLOSING_TAG = "unexpected_closing_tag"
    BROKEN_TAG = "broken_tag"
    MALFORMED_STRUCTURE = "malformed_structure"
    TEXT_NOISE = "text_noise"
    ENCODING_ISSUE = "encoding_issue"
