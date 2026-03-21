from dataclasses import dataclass
from typing import Optional


@dataclass
class ASTChange:
    type: str
    path: str
    before: Optional[str]
    after: Optional[str]
