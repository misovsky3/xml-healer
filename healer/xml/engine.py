from .parser import tokenize, build_ast
from .ast_repair import repair_ast
from .serializer import to_xml
from .classifier import classify
from .scoring import compute_confidence
from .ast_utils import infer_root
from .diff import diff_nodes
from .types import HealResult, FixChange
import copy

def run_healing(xml: str):
    original = xml
    if not xml.strip():
        return HealResult("", 1.0, [], [])
    errors = classify(xml)
    tokens = tokenize(xml)
    original_ast = build_ast(tokens)
    fixed_ast = copy.deepcopy(original_ast)
    fixed_ast = repair_ast(fixed_ast)
    real_root_original = infer_root(original_ast)
    real_root_fixed = infer_root(fixed_ast)
    fixed = to_xml(real_root_fixed)
    diff = diff_nodes(original_ast, fixed_ast) or []
    changes = [
        FixChange(
            type="detected_error",
            value=e,
            severity=0.2,
            error_type=e
        )
        for e in errors
    ]
    confidence = compute_confidence(original, fixed, changes)
    return HealResult(
        fixed_xml=fixed,
        confidence=confidence,
        changes=changes,
        diff=diff
    )
