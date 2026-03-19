from .types import HealResult, FixChange
from .fixes import fix_unclosed_tags


def run_healing(xml: str) -> HealResult:
    changes = []

    original = xml

    # stage 1: cleanup
    xml = xml.strip()

    # stage 2: repair
    fixed = fix_unclosed_tags(xml)

    # simple heuristic confidence
    confidence = 1.0

    if original != fixed:
        confidence = 0.8
        changes.append(FixChange(type="structure_fix", value="unclosed_tags"))

    return HealResult(
        fixed_xml=fixed,
        confidence=confidence,
        changes=changes
    )
