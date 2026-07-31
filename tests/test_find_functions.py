from analysis import FunctionInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.find_functions import FindFunctionsVisitor


def test_find_functions():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
def a():
    pass

def b(x):
    return x
"""
    )

    visitor = FindFunctionsVisitor()
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
