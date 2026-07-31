import pytest

from analysis.models import (
    FunctionInfo,
    ClassInfo,
    ImportInfo,
    CallInfo,
)


def test_models_immutability_and_defaults():
    func = FunctionInfo(name="foo", parameters=("a", "b"))
    assert func.name == "foo"
    assert func.parameters == ("a", "b")
    assert func.line is None
    with pytest.raises(Exception):
        func.name = "bar"  # type: ignore

    cls = ClassInfo(name="MyClass", line=10)
    assert cls.name == "MyClass"
    assert cls.line == 10
    with pytest.raises(Exception):
        cls.name = "OtherClass"  # type: ignore

    imp = ImportInfo(module="os", alias="system_os")
    assert imp.module == "os"
    assert imp.alias == "system_os"
    with pytest.raises(Exception):
        imp.module = "sys"  # type: ignore

    call = CallInfo(function="print", line=42)
    assert call.function == "print"
    assert call.line == 42
    with pytest.raises(Exception):
        call.function = "exec"  # type: ignore
