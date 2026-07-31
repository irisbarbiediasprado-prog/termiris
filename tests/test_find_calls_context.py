from analysis.context import AnalysisContext
from analysis import CallInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.location import wrap, get_positions
from drivers.libcst.find_calls import FindCallsVisitor


def test_find_calls_with_context():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
print("hello")
len([])
"""
    )

    wrapper = wrap(tree)

    context = AnalysisContext(
        tree=tree,
        positions=get_positions(wrapper),
    )

    visitor = FindCallsVisitor(context)

    driver.visit(tree, visitor)

    assert visitor.calls == [
        CallInfo(function="print"),
        CallInfo(function="len"),
    ]
