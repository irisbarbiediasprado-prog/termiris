from analysis import CallInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.find_calls import FindCallsVisitor


def test_find_calls():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
print("hello")
open("file.txt")
custom()
"""
    )

    visitor = FindCallsVisitor()
    driver.visit(tree, visitor)

    assert visitor.calls == [
        CallInfo(function="print"),
        CallInfo(function="open"),
        CallInfo(function="custom"),
    ]
