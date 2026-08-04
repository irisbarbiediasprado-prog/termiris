from pathlib import Path
from refactor.executor import OperationExecutor
from refactor.models import Target, Transformation, Class, Function, Code, SourceFile
from refactor.operations import CreateFileOperation, CreateSourceFileOperation, UpdateOperation

def make_ws(tmp_path):
    class W:
        def resolve(self, p):
            pp = Path(p)
            return pp if pp.is_absolute() else tmp_path / pp
    return W()

def test_create_file(tmp_path):
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = CreateFileOperation(kind="create_file", reference="r", path="a.py", content="x=1")
    ex.execute(op)
    assert (tmp_path / "a.py").read_text() == "x=1"

def test_create_source_file(tmp_path):
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    cls = Class(name="C", methods=())
    sf = SourceFile(path="b.py", language="python", declarations=(cls,))
    op = CreateSourceFileOperation(kind="create_source_file", reference="r", source_file=sf)
    ex.execute(op)
    assert "class C" in (tmp_path / "b.py").read_text()

def test_execute_not_implemented(tmp_path):
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    try:
        ex.execute(object())
        assert False
    except NotImplementedError:
        pass

def test_file_not_found(tmp_path):
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(tmp_path / "nope.py")), transformation=Transformation(kind="replace_body", value=Code("python","x=1")))
    try:
        ex.execute(op)
        assert False
    except FileNotFoundError:
        pass

def test_unknown_kind(tmp_path):
    f = tmp_path / "c.py"; f.write_text("x=1")
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f)), transformation=Transformation(kind="unknown_kind", value="v"))
    try:
        ex.execute(op)
        assert False
    except NotImplementedError:
        pass

def test_replace_body_class_method(tmp_path):
    f = tmp_path / "e.py"; f.write_text("class OperationExecutor:\n    def execute(self):\n        old=1\n")
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f), symbol="OperationExecutor.execute"), transformation=Transformation(kind="replace_body", value=Code("python","new=2")))
    ex.execute(op)
    assert "new=2" in f.read_text()

def test_replace_body_simple(tmp_path):
    f = tmp_path / "d.py"; f.write_text("def myfunc():\n    old=1\n")
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f), symbol="myfunc"), transformation=Transformation(kind="replace_body", value=Code("python","new=2")))
    ex.execute(op)
    assert "new=2" in f.read_text()

def test_replace_import_and_add_import(tmp_path):
    f = tmp_path / "f.py"; f.write_text("import os\n")
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op1 = UpdateOperation(kind="update", reference="r", target=Target(path=str(f)), transformation=Transformation(kind="replace_import", value={"old":"os","new":"sys"}))
    ex.execute(op1)
    op2 = UpdateOperation(kind="update", reference="r", target=Target(path=str(f)), transformation=Transformation(kind="add_import", value="from pathlib import Path"))
    ex.execute(op2)
    txt = f.read_text()
    assert "sys" in txt and "Path" in txt

def test_add_declaration_and_method(tmp_path):
    f = tmp_path / "h.py"; f.write_text("x=1\n")
    ws = make_ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    cls = Class(name="C", methods=())
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f)), transformation=Transformation(kind="add_declaration", value=cls))
    ex.execute(op)
    meth = Function(name="m", signature="(self)", body=Code("python","return 1"))
    op2 = UpdateOperation(kind="update", reference="r", target=Target(path=str(f), symbol="C"), transformation=Transformation(kind="add_method", value=meth))
    ex.execute(op2)
    assert "class C" in f.read_text()
