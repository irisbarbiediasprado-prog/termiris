import libcst
from libcst.metadata import MetadataWrapper


def visit(tree, visitor):
    return MetadataWrapper(tree).visit(visitor)


def transform(tree, transformer):
    return tree.visit(transformer)
