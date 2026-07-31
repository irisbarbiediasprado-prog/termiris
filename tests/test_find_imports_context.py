from analysis.context import AnalysisContext
from analysis import ImportInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.location import wrap, get_positions
from drivers.libcst.find_imports import FindImportsVisitor


def test_find_imports_with_context():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
import os
import sys as system
from pathlib import Path
"""
    )

    wrapper = wrap(tree)

    context = AnalysisContext(
        tree=tree,
        positions=get_positions(wrapper),
    )

    visitor = FindImportsVisitor(context)

    driver.visit(tree, visitor)

    assert visitor.imports == [
        ImportInfo(module="os"),
        ImportInfo(module="sys", alias="system"),
        ImportInfo(module="pathlib"),
    ]
