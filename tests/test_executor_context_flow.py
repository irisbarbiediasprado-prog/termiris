from drivers.libcst import LibCSTDriver
from refactor.context import RefactorContext
from refactor.executors import LibCSTExecutor
from refactor.operations import ReplaceImportOperation

def test_executor_context_flow():
    driver = LibCSTDriver()
    context = RefactorContext(
        tree=driver.parse_source("import optparse\n")
    )
    operation = ReplaceImportOperation(
        kind="replace_import",
        reference="legacy_import",
        old_module="optparse",
        new_module="argparse",
    )
    result = LibCSTExecutor(driver).execute(context, operation)
    assert result.code == "import argparse\n"
