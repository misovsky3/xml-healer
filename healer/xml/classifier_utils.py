from .errors import ErrorType


def error_severity(error: ErrorType | str) -> float:
    error_key = error.value if hasattr(error, "value") else str(error)
    return {
        "missing_closing_tag": 0.2,
        "unexpected_closing_tag": 0.25,
        "broken_tag": 0.4,
        "malformed_structure": 0.3,
        "encoding_issue": 0.5,
        "text_noise": 0.15,
    }.get(error_key, 0.1)
