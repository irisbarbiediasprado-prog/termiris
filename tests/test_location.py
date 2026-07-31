import libcst
from drivers.libcst.parser import parse_source
from drivers.libcst.location import wrap, get_positions


def test_location_provider():
    tree = parse_source(
        "def hello():\n    pass\n"
    )

    wrapper = wrap(tree)
    positions = get_positions(wrapper)

    assert positions

    assert any(
        position.start.line == 1
        for position in positions.values()
    )
