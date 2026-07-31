from analysis import ImportInfo
from drivers.libcst import LibCSTDriver
from drivers.libcst.find_imports import FindImportsVisitor


def test_find_imports():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        """
import os
import sys as system

from pathlib import Path
"""
    )

    visitor = FindImportsVisitor()
    driver.visit(tree, visitor)

    assert visitor.imports == [
        ImportInfo(
            module="os",
        ),
        ImportInfo(
            module="sys",
            alias="system",
        ),
        ImportInfo(
            module="pathlib",
        ),
    ]
