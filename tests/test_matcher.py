import pytest

from analysis.matcher import Matcher


class AlwaysMatcher(Matcher):
    def matches(self, item):
        return True


class NeverMatcher(Matcher):
    def matches(self, item):
        return False


def test_matcher_contract():
    assert AlwaysMatcher().matches("anything") is True
    assert NeverMatcher().matches("anything") is False

    with pytest.raises(TypeError):
        Matcher()
