from drivers.libcst import LibCSTDriver
from drivers.libcst.visitor import LibCSTVisitor


class DummyVisitor(LibCSTVisitor):
    def __init__(self):
        self.visited = False

    def visit_Module(self, node):
        self.visited = True


def test_driver_visit():
    driver = LibCSTDriver()
    tree = driver.parse_source("def hello():\n    pass\n")

    visitor = DummyVisitor()
    driver.visit(tree, visitor)

    assert visitor.visited
