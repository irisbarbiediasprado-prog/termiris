from analysis import ClassInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.find_classes import FindClassesVisitor


def test_find_classes():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
class A:
    pass

class B:
    pass
"""
    )

    visitor = FindClassesVisitor()
    driver.visit(tree, visitor)

    assert visitor.classes == [
        ClassInfo(name="A"),
        ClassInfo(name="B"),
    ]
