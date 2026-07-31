from drivers.libcst.tree_driver import TreeDriver
from drivers.libcst import parser, walker


class LibCSTDriver(TreeDriver):
    def parse_source(self, source: str):
        return parser.parse_source(source)

    def parse_file(self, path):
        return parser.parse_file(path)

    def visit(self, tree, visitor):
        return walker.visit(tree, visitor)

    def transform(self, tree, transformer):
        return walker.transform(tree, transformer)
