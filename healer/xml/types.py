from dataclasses import dataclass
from typing import List
from enum import Enum


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
    type: FixType
    value: str


@dataclass
class HealResult:
    fixed_xml: str
    confidence: float
    changes: List[FixChange]


@dataclass
class Token:
    type: TokenType
    value: str
