from .diff_types import ASTChange


from .diff_types import ASTChange


def diff_nodes(original, fixed, path=""):
    changes = []

    if original is None and fixed is None:
        return []

    if original is None:
        return [ASTChange("node_added", path, None, fixed.tag)]

    if fixed is None:
        return [ASTChange("node_removed", path, original.tag, None)]

    # TAG CHANGE (root or direct mismatch, or original_tag mismatch)
    orig_tag = getattr(original, 'original_tag', original.tag)
    fixed_tag = getattr(fixed, 'original_tag', fixed.tag)
    orig_close = getattr(original, 'close_tag', None)
    fixed_close = getattr(fixed, 'close_tag', None)
    # Detect tag name or closing tag mismatch
    if orig_tag != fixed_tag or (orig_close and fixed_close and orig_close != fixed_close):
        changes.append(ASTChange(
            type="tag_change",
            path=path,
            before=f"{orig_tag} (close: {orig_close})",
            after=f"{fixed_tag} (close: {fixed_close})"
        ))

    # TEXT CHANGE
    if original.text != fixed.text:
        changes.append(ASTChange(
            type="text_change",
            path=path,
            before=original.text,
            after=fixed.text
        ))

    orig_children = original.children or []
    fixed_children = fixed.children or []

    used_fixed = set()

    for i, oc in enumerate(orig_children):
        match_index = None
        for j, fc in enumerate(fixed_children):
            if j in used_fixed:
                continue
            oc_tag = getattr(oc, 'original_tag', oc.tag)
            fc_tag = getattr(fc, 'original_tag', fc.tag)
            # Handle None tags (e.g., text nodes)
            if oc_tag is None or fc_tag is None:
                if oc_tag == fc_tag:
                    match_index = j
                    break
                continue
            if oc_tag.lower() == fc_tag.lower():
                match_index = j
                break
        if match_index is not None:
            used_fixed.add(match_index)
            fc = fixed_children[match_index]
            # CASE CHANGE DETECTION
            if oc_tag != fc_tag:
                changes.append(ASTChange(
                    type="tag_change",
                    path=f"{path}/{oc_tag}",
                    before=oc_tag,
                    after=fc_tag
                ))
            changes.extend(diff_nodes(oc, fc, f"{path}/{oc_tag}[{i}]"))
        else:
            changes.extend(diff_nodes(oc, None, f"{path}/{getattr(oc, 'original_tag', oc.tag)}[{i}]"))

    # added nodes
    for j, fc in enumerate(fixed_children):
        if j not in used_fixed:
            changes.extend(diff_nodes(None, fc, f"{path}/{fc.tag}[{j}]"))

    return changes

