import pytest
from refactor.context import RefactorContext


def test_refactor_context_contract():
    tree = object()

    ctx = RefactorContext(
        tree=tree,
        positions={},
        artifacts={},
    )

    assert ctx.tree is tree
    assert ctx.positions == {}
    assert ctx.artifacts == {}

    with pytest.raises(AttributeError):
        ctx.tree = None  # type: ignore
