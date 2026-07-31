import pytest
from refactor import Operation


def test_operation_reference_contract():
    op = Operation(
        kind="replace_import",
        reference="optparse",
    )

    assert op.reference == "optparse"

    with pytest.raises(Exception):
        op.reference = "argparse"  # type: ignore
