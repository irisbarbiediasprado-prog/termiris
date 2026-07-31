import pytest
import libcst as cst
from analysis.context import AnalysisContext
from drivers.libcst.location import wrap, get_positions


def test_analysis_context_creation():
    tree = cst.parse_module("def sample():\n    pass\n")

    wrapper = wrap(tree)
    positions = get_positions(wrapper)

    ctx = AnalysisContext(
        tree=tree,
        positions=positions,
    )

    assert ctx.tree is tree
    assert ctx.positions is positions
    assert ctx.index is None


def test_analysis_context_immutability():
    ctx = AnalysisContext(tree=None)

    with pytest.raises(AttributeError):
        ctx.tree = "new_tree"
