import libcst as cst
from refactor.operations import ReplaceImportOperation
from refactor.executors.libcst import LibCSTExecutor
from refactor.context import RefactorContext
from drivers.libcst import LibCSTDriver

def test_libcst_executor_replace_import():
    code = "import optparse\n"
    tree = cst.parse_module(code)
    op = ReplaceImportOperation(
        kind="replace_import",
        reference="legacy_import",
        old_module="optparse",
        new_module="argparse",
    )
    driver = LibCSTDriver()
    executor = LibCSTExecutor(driver)
    context = RefactorContext(tree=tree)
    new_tree = executor.execute(context, op)
    assert new_tree.code == "import argparse\n"
