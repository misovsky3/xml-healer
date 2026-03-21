from .ast import Node


def repair_ast(node):
    """
    Structure fix: ensures all children are properly closed. Adds dummy nodes for missing closing tags.
    """
    if node is None:
        return None

    fixed_children = []
    for child in node.children:
        fixed_child = repair_ast(child)
        if fixed_child is not None:
            fixed_children.append(fixed_child)

    # If node is not closed (tag is not empty and children are unbalanced), add a dummy node
    # This is a naive approach: if tag is not empty and children are empty, add a dummy child
    if node.tag and not node.children:
        # Add a dummy node to represent a missing closing tag
        dummy = Node(tag="__missing__" + node.tag)
        fixed_children.append(dummy)

    # If the close_tag does not match the tag, fix it
    if hasattr(node, 'close_tag') and node.close_tag is not None and node.close_tag != node.tag:
        node.close_tag = node.tag

    node.children = fixed_children
    return node

