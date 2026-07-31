from refactor.context import RefactorContext
from refactor.operations import ReplaceImportOperation
from refactor.transformers import ReplaceImportTransformer
import libcst as cst

def test_transformer_uses_context():
    tree = cst.parse_module("import optparse\n")
    context = RefactorContext(tree=tree)
    operation = ReplaceImportOperation(
        kind="replace_import",
        reference="legacy_import",
        old_module="optparse",
        new_module="argparse",
    )
    result = tree.visit(
        ReplaceImportTransformer(context, operation)
    )
    assert result.code == "import argparse\n"
