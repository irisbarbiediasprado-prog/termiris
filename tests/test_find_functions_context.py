from analysis.context import AnalysisContext
from analysis import FunctionInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.location import wrap, get_positions
from drivers.libcst.find_functions import FindFunctionsVisitor


def test_find_functions_with_context():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
def a():
    pass

def b(x):
    return x
"""
    )

    wrapper = wrap(tree)

    context = AnalysisContext(
        tree=tree,
        positions=get_positions(wrapper),
    )

    visitor = FindFunctionsVisitor(context)

    driver.visit(tree, visitor)

    assert visitor.functions == [
        FunctionInfo(
            name="a",
            parameters=(),
        ),
        FunctionInfo(
            name="b",
            parameters=("x",),
        ),
    ]
