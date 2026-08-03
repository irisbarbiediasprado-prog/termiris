import pytest
from pathlib import Path
from runtime.executors import ListExecutor, SnapshotExecutor, OperationExecutor
from models import Artifact
from protocol.isa import Operation, PrimitiveISA
from unittest.mock import Mock
from models import RuntimeResult

def test_abstract_executor_init():
    class Dummy(OperationExecutor):
        def __init__(self, repository, emitter, state):
            super().__init__(repository, emitter, state)
        def execute(self, operation):
            return RuntimeResult(success=True, snapshot=None)
    repo=Mock(); emit=Mock(); state={}
    d=Dummy(repo, emit, state)
    assert d.repository==repo

def test_snapshot_legacy_and_targets(tmp_path):
    f=tmp_path/"a.txt"; f.write_text("hello")
    repo=Mock(); repo.fetch.side_effect=lambda ref: Artifact(uri=ref.uri, content="c", metadata={})
    emitter=Mock(); emitter.emit.return_value="snap"
    ex=SnapshotExecutor(repo, emitter, {})
    assert ex.execute(Operation(instruction=PrimitiveISA.SNAPSHOT, payload={"file_path":str(f)})).success
    ex2=SnapshotExecutor(repo, emitter, {})
    assert ex2.execute(Operation(instruction=PrimitiveISA.SNAPSHOT, payload={"targets":[str(f)]})).success

def test_list_executor_cases(tmp_path):
    (tmp_path/"file1.txt").write_text("a"); (tmp_path/"dir1").mkdir()
    repo=Mock(); emitter=Mock(); emitter.emit.return_value="snap"
    ex=ListExecutor(repo, emitter, {})
    res=ex.execute(Operation(instruction=PrimitiveISA.LIST, payload={"path":str(tmp_path)}))
    assert res.success
    assert not ListExecutor(repo, emitter, {}).execute(Operation(instruction=PrimitiveISA.LIST, payload={"path":"/no_such_xyz"})).success
    f=tmp_path/"file.txt"; f.write_text("x")
    res2=ListExecutor(repo, emitter, {}).execute(Operation(instruction=PrimitiveISA.LIST, payload={"path":str(f)}))
    assert res2.error=="INVALID_ARGUMENT"
    home=Path.home()/".termiris"/"fallback_test"; home.mkdir(parents=True, exist_ok=True)
    (home/"inner.txt").write_text("a")
    res3=ListExecutor(repo, emitter, {}).execute(Operation(instruction=PrimitiveISA.LIST, payload={"path":"fallback_test"}))
    assert res3.success
