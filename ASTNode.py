# AST Construction
# One single class for all AST nodes to simplify the tree traversing
from simple_colors import *

class ASTNode:
    def __init__(self, value, children=None, leaf=None, line=None):
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.line = line

    def add_siblings(self, siblings):
        self.children.extend(siblings)

    def __repr__(self):
        return self.pretty_print()

    def pretty_print(self, prefix="", is_last=True):

        connector = "└─ " if is_last else "├─ "
        node_repr = f"{connector}{self.value}"
        if self.leaf is not None:
            node_repr += ": " + green(f" {self.leaf} ", ['bold'])
        if self.line is not None:
            node_repr += blue(f" (line {self.line})")
        result = [prefix + node_repr]

        # Update prefix for the next level
        prefix += "   " if is_last else "│  "

        # Recursively print children
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            result.append(child.pretty_print(prefix, is_last_child))

        return "\n".join(result)

