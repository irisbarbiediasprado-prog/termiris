from refactor.operations import ReplaceImportOperation

def test_replace_import_has_reference():
    op = ReplaceImportOperation(
        kind="replace_import",
        reference="legacy_import",
        old_module="optparse",
        new_module="argparse",
    )
    assert op.reference == "legacy_import"
