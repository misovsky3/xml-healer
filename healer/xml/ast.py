from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Node:
    tag: str
    children: List["Node"] = field(default_factory=list)
    text: Optional[str] = None
    attrs: Dict[str, str] = field(default_factory=dict)
    original_tag: Optional[str] = None  # preserves original tag name/case
    close_tag: Optional[str] = None     # preserves the actual closing tag as seen in the input
