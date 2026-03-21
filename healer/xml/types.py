from dataclasses import dataclass
from typing import List
from enum import Enum
from .errors import ErrorType
from .diff_types import ASTChange


class FixType(Enum):
    ADDED_TAG = "added_tag"
    REMOVED_TAG = "removed_tag"
    FIXED_TEXT = "fixed_text"


class TokenType(Enum):
    TEXT = "text"
    OPEN_TAG = "open"
    CLOSE_TAG = "close"

@dataclass
class FixChange:
    type: str
    value: str
    error_type: ErrorType
    severity: float = 0.1

@dataclass
class HealResult:
    fixed_xml: str
    confidence: float
    changes: List[FixChange]
    diff: List[ASTChange]

@dataclass
class Token:
    type: str
    value: str
