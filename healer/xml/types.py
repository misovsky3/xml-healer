from dataclasses import dataclass
from typing import List
from enum import Enum


class FixType(Enum):
    ADDED_TAG = "added_tag"
    REMOVED_TAG = "removed_tag"
    FIXED_TEXT = "fixed_text"


@dataclass
class FixChange:
    type: FixType
    value: str


@dataclass
class HealResult:
    fixed_xml: str
    confidence: float
    changes: List[FixChange]
