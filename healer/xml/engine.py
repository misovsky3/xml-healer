from .parser import tokenize, parse_and_fix
from .types import HealResult, FixChange


def run_healing(xml: str) -> HealResult:
    original = xml

    tokens = tokenize(xml)
    fixed = parse_and_fix(tokens)

    changes = []
    confidence = 1.0

    if original != fixed:
        confidence = 0.85
        changes.append(
            FixChange(type="parser_rewrite", value="token_stack_reconstruction")
        )

    return HealResult(fixed_xml=fixed, confidence=confidence, changes=changes)
