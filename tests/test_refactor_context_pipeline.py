from refactor.context import RefactorContext
from refactor.operations import ReplaceImportOperation
from refactor.executors import LibCSTExecutor
from drivers.libcst import LibCSTDriver


def test_refactor_context_pipeline():
    driver = LibCSTDriver()

    tree = driver.parse_source(
        "import optparse\n"
    )

    context = RefactorContext(
        tree=tree,
    )

    operation = ReplaceImportOperation(
        kind="replace_import",
        reference="optparse",
        old_module="optparse",
        new_module="argparse",
    )

    result = LibCSTExecutor(driver).execute(
        context,
        operation,
    )

    assert result.code == "import argparse\n"
