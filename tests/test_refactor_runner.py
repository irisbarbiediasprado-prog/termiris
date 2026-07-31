from drivers.libcst import LibCSTDriver
from refactor.context import RefactorContext
from refactor.executors import LibCSTExecutor
from refactor.operations import ReplaceImportOperation
from refactor.runner import RefactorRunner

def test_refactor_runner():
    driver = LibCSTDriver()
    context = RefactorContext(
        tree=driver.parse_source("import optparse\n")
    )
    operations = [
        ReplaceImportOperation(
            kind="replace_import",
            reference="legacy_import",
            old_module="optparse",
            new_module="argparse",
        )
    ]
    result = RefactorRunner(
        LibCSTExecutor(driver)
    ).run(context, operations)
    assert result.tree.code == "import argparse\n"
