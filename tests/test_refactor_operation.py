from refactor.operations import ReplaceImportOperation

def test_replace_import_operation_creation():
    op = ReplaceImportOperation(
        kind="replace_import",
        reference="legacy_import",
        old_module="optparse",
        new_module="argparse",
    )
    assert op.reference == "legacy_import"
    assert op.old_module == "optparse"
    assert op.new_module == "argparse"
