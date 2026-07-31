import pytest
from refactor.result import RefactorResult


def test_refactor_result_contract():
    result = RefactorResult(
        tree=None,
        applied=("op",),
    )

    assert result.applied == ("op",)

    with pytest.raises(AttributeError):
        result.tree = "new"  # type: ignore
