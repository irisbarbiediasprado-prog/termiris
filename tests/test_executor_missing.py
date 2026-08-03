import pytest
from refactor.executor import OperationExecutor
from refactor.operations import CreateFileOperation, CreateSourceFileOperation, UpdateOperation
from refactor.models import SourceFile, Target, Transformation, Function, Class, Code

def test_create_file(tmp_path):
    ws = type("W", (), {"resolve": lambda self, p: tmp_path / p})()
    ex = OperationExecutor(workspace=ws)
    op = CreateFileOperation(kind="create_file", reference="x", path="a.txt", content="hi")
    p = ex.execute(op)
    assert p.read_text() == "hi"

def test_create_source_file(tmp_path):
    ws = type("W", (), {"resolve": lambda self, p: tmp_path / p})()
    ex = OperationExecutor(workspace=ws)
    sf = SourceFile(path="b.py", language="python", declarations=())
    op = CreateSourceFileOperation(kind="create_source", reference="y", source_file=sf)
    p = ex.execute(op)
    assert p.exists()

def test_execute_not_implemented(tmp_path):
    ws = type("W", (), {"resolve": lambda self, p: tmp_path / p})()
    ex = OperationExecutor(workspace=ws)
    class Dummy: pass
    with pytest.raises(NotImplementedError):
        ex.execute(Dummy())

def test_file_not_found(tmp_path):
    ws = type("W", (), {"resolve": lambda self, p: tmp_path / p})()
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="z", target=Target(path="no.py", symbol="x"), transformation=Transformation(kind="replace_body", value=Code("python","pass")))
    with pytest.raises(FileNotFoundError):
        ex._apply_update(op)

def test_unknown_kind(tmp_path):
    f = tmp_path / "c.py"; f.write_text("x=1")
    ws = type("W", (), {"resolve": lambda self, p: f})()
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="x"), transformation=Transformation(kind="unknown_kind", value="x"))
    with pytest.raises(NotImplementedError):
        ex._apply_update(op)

def test_replace_body_class_method(tmp_path):
    f = tmp_path / "e.py"; f.write_text("class OperationExecutor:\n    def execute(self):\n        old=1\n")
    ws = type("W", (), {"resolve": lambda self, p: f})()
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="OperationExecutor.execute"), transformation=Transformation(kind="replace_body", value=Code("python","        return 42")))
    ex._apply_update(op)
    assert "return 42" in f.read_text()

def test_replace_body_simple(tmp_path):
    f = tmp_path / "d.py"; f.write_text("def myfunc():\n    old=1\n")
    ws = type("W", (), {"resolve": lambda self, p: f})()
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="myfunc"), transformation=Transformation(kind="replace_body", value=Code("python","    return 2")))
    ex._apply_update(op)
    assert "return 2" in f.read_text()

def test_replace_import_and_add_import(tmp_path):
    f = tmp_path / "f.py"; f.write_text("import os\n")
    ws = type("W", (), {"resolve": lambda self, p: f})()
    ex = OperationExecutor(workspace=ws)
    op1 = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="x"), transformation=Transformation(kind="replace_import", value={"old":"os","new":"pathlib"}))
    ex._apply_update(op1)
    assert "pathlib" in f.read_text()
    op2 = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="x"), transformation=Transformation(kind="add_import", value="import sys"))
    ex._apply_update(op2)
    assert "sys" in f.read_text()
    ex._apply_update(op2)
    assert f.read_text().count("import sys")==1

def test_add_declaration_and_method(tmp_path):
    f = tmp_path / "h.py"; f.write_text("x=1\n")
    ws = type("W", (), {"resolve": lambda self, p: f})()
    ex = OperationExecutor(workspace=ws)
    func = Function(name="new_func", signature="()", body=Code("python","    return 1"))
    op = UpdateOperation(kind="update", reference="z", target=Target(path=str(f), symbol="x"), transformation=Transformation(kind="add_declaration", value=func))
    ex._apply_update(op)
    assert "new_func" in f.read_text()
    f2 = tmp_path / "i.py"; f2.write_text("class MyClass:\n    pass\n")
    ws2 = type("W", (), {"resolve": lambda self, p: f2})()
    ex2 = OperationExecutor(workspace=ws2)
    func2 = Function(name="my_method", signature="(self)", body=Code("python","    return 1"))
    op2 = UpdateOperation(kind="update", reference="z", target=Target(path=str(f2), symbol="MyClass"), transformation=Transformation(kind="add_method", value=func2))
    ex2._apply_update(op2)
    assert "my_method" in f2.read_text()
