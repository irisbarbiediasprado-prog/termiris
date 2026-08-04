from pathlib import Path
from refactor.target_resolver import AnalysisIndexTargetResolver
from refactor.executor import OperationExecutor
from refactor.models import Target, Transformation, Code, Function
from refactor.operations import UpdateOperation

def test_resolver_handles_broken_files(tmp_path):
    good = tmp_path/"good.py"
    good.write_text("def ok(): pass")
    bad = tmp_path/"bad.py"
    bad.write_text("def =!!! syntax error (((")
    AnalysisIndexTargetResolver.clear_cache()
    r_fast = AnalysisIndexTargetResolver(root=tmp_path, mode="fast")
    assert r_fast.resolve("ok") is not None
    AnalysisIndexTargetResolver.clear_cache()
    r_full = AnalysisIndexTargetResolver(root=tmp_path, mode="full")
    assert r_full.resolve("ok") is not None
    AnalysisIndexTargetResolver.clear_cache()

def _ws(tmp_path):
    class W:
        def resolve(self, p):
            pp = Path(p)
            return pp if pp.is_absolute() else tmp_path/pp
    return W()

def test_replace_body_else_branch(tmp_path):
    f = tmp_path/"g.py"
    f.write_text("def other():\n    x=1\n\ndef myfunc():\n    old=1\n")
    ws = _ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f), symbol="myfunc"), transformation=Transformation(kind="replace_body", value=Code("python","new=2")))
    ex.execute(op)
    txt = f.read_text()
    assert "new=2" in txt and "other" in txt

def test_replace_import_else_branch(tmp_path):
    f = tmp_path/"h.py"
    f.write_text("import os, json\n")
    ws = _ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f)), transformation=Transformation(kind="replace_import", value={"old":"os","new":"sys"}))
    ex.execute(op)
    txt = f.read_text()
    assert "sys" in txt and "json" in txt

def test_add_method_else_branch(tmp_path):
    f = tmp_path/"i.py"
    f.write_text("class Real:\n    pass\n")
    ws = _ws(tmp_path)
    ex = OperationExecutor(workspace=ws)
    meth = Function(name="m", signature="(self)", body=Code("python","return 1"))
    op = UpdateOperation(kind="update", reference="r", target=Target(path=str(f), symbol="FakeClass"), transformation=Transformation(kind="add_method", value=meth))
    ex.execute(op)
    assert "def m" not in f.read_text()

def test_runtime_base_not_implemented():
    from runtime.executors import OperationExecutor as RuntimeOpEx
    from unittest.mock import Mock
    class NoOverride(RuntimeOpEx):
        def __init__(self):
            self.repository = Mock(); self.emitter = Mock(); self.state = {}
    inst = NoOverride()
    try:
        inst.execute(Mock()); assert False
    except NotImplementedError:
        pass

def test_list_executor_candidate_branch(tmp_path, monkeypatch):
    from runtime.executors import ListExecutor
    from protocol.isa import Operation, PrimitiveISA
    from unittest.mock import Mock
    # isola o home pra não conflitar com cwd = ~/.termiris
    fake_home = tmp_path/"fakehome"
    fake_home.mkdir()
    fallback = fake_home/".termiris"/"cov_final_test_123"
    fallback.mkdir(parents=True)
    (fallback/"x.txt").write_text("a")
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # garante que relativo não existe no cwd real
    ex = ListExecutor(Mock(), Mock(), {})
    res = ex.execute(Operation(instruction=PrimitiveISA.LIST, payload={"path":"cov_final_test_123"}))
    assert res.success
