from .classifier_utils import error_severity
from .parser import tokenize, parse_and_fix
from .types import HealResult, FixChange
from .scoring import compute_confidence
from .classifier import classify


def run_healing(xml: str):
    original = xml

    errors = classify(xml)

    tokens = tokenize(xml)
    fixed = parse_and_fix(tokens)

    changes: list[FixChange] = []

    for e in errors:
        changes.append(FixChange(
            type="detected_error",
            value=e.value,
            error_type=e,
            severity=error_severity(e)
        ))

    confidence = compute_confidence(original, fixed, changes)

    return HealResult(
        fixed_xml=fixed,
        confidence=confidence,
        changes=changes
    )
