import libcst

from drivers.tree_visitor import TreeVisitor


class LibCSTVisitor(libcst.CSTVisitor, TreeVisitor):
    """Adapter entre o contrato do Termiris e o LibCST."""
    pass
