from analysis.context import AnalysisContext
from analysis import ClassInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.location import wrap, get_positions
from drivers.libcst.find_classes import FindClassesVisitor


def test_find_classes_with_context():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
class A:
    pass

class B:
    pass
"""
    )

    wrapper = wrap(tree)

    context = AnalysisContext(
        tree=tree,
        positions=get_positions(wrapper),
    )

    visitor = FindClassesVisitor(context)

    driver.visit(tree, visitor)

    assert visitor.classes == [
        ClassInfo(name="A"),
        ClassInfo(name="B"),
    ]
