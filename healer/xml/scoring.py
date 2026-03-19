from .types import FixChange


def compute_confidence(original: str, fixed: str, changes: list[FixChange]) -> float:
    """
    Heuristic confidence model.
    """

    score = 1.0

    # 1. structural changes penalty
    for c in changes:
        score -= c.severity

    # 2. length mismatch penalty (basic heuristic)
    if abs(len(original) - len(fixed)) > 50:
        score -= 0.1

    # 3. heavy fuzz penalty
    fuzz_count = sum(1 for c in changes if "fuzzy" in c.type)
    score -= fuzz_count * 0.15

    # clamp
    return max(0.0, min(1.0, score))
