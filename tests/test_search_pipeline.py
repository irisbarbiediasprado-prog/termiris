import pytest
import uuid
from protocol.isa import PrimitiveISA, Operation
from runtime.search_executor import SearchExecutor
from models import Artifact, RuntimeResult


class TestSearchExecutor:
    def test_execute_returns_runtime_result(self):
        s = SearchExecutor(emitter=_fake_emitter())
        op = Operation(PrimitiveISA.SEARCH, {"pattern": "IntentKind", "root": "."})
        res = s.execute(op)
        assert isinstance(res, RuntimeResult)
        assert res.success
        assert res.snapshot is not None
        art = res.snapshot.artifacts[0]
        assert isinstance(art, Artifact)
        assert art.uri.startswith("search://")
        assert isinstance(art.content, str)
        assert isinstance(art.metadata, dict)
        assert "count" in art.metadata
        assert "matches" in art.metadata

    def test_execute_with_results(self):
        s = SearchExecutor(emitter=_fake_emitter())
        op = Operation(PrimitiveISA.SEARCH, {"pattern": "IntentKind", "root": "."})
        res = s.execute(op)
        art = res.snapshot.artifacts[0]
        assert art.metadata["count"] > 0
        assert len(art.metadata["matches"]) == art.metadata["count"]

    def test_execute_no_results(self):
        s = SearchExecutor(emitter=_fake_emitter())
        pattern = f"NO_MATCH_{uuid.uuid4().hex}"
        op = Operation(PrimitiveISA.SEARCH, {"pattern": pattern, "root": "."})
        res = s.execute(op)
        art = res.snapshot.artifacts[0]
        assert art.metadata["count"] == 0
        assert art.metadata["matches"] == []
        assert art.content == ""

    def test_execute_parser_robustness(self):
        s = SearchExecutor(emitter=_fake_emitter())
        op = Operation(PrimitiveISA.SEARCH, {"pattern": "class", "root": "."})
        res = s.execute(op)
        for m in res.snapshot.artifacts[0].metadata["matches"]:
            assert isinstance(m, dict)
            assert "file" in m and "line" in m and "text" in m
            assert isinstance(m["line"], int)
            assert ":" not in m["file"]


def _fake_emitter():
    """Emissor mínimo para testes unitários do SearchExecutor."""
    class FakeEmitter:
        def emit(self, generation, artifacts):
            from models import ContextSnapshot
            import time, hashlib
            return ContextSnapshot(
                generation=generation,
                snapshot_hash=hashlib.sha256(str(artifacts).encode()).hexdigest()[:16],
                artifacts=artifacts,
                size_bytes=sum(len(a.content) for a in artifacts),
                timestamp=time.time(),
            )
    return FakeEmitter()


@pytest.fixture
def kernel():
    from protocol.kernel import ProtocolKernel, CommandRouter
    router = CommandRouter()
    router.auto_discover()
    return ProtocolKernel(router)


@pytest.fixture
def engine():
    from runtime.engine import RuntimeEngine
    return RuntimeEngine()


class TestSearchPipeline:
    def test_compile_produces_search_operation(self, kernel):
        ops = kernel.compile("<< RETRIEVE SEARCH IntentKind >>")
        assert len(ops) == 1
        assert ops[0].instruction == PrimitiveISA.SEARCH
        assert ops[0].payload["pattern"] == "IntentKind"

    def test_pipeline_execution(self, kernel, engine):
        ops = kernel.compile("<< RETRIEVE SEARCH IntentKind >>")
        for op in ops:
            res = engine.apply(op)
            assert res.success
            assert res.snapshot is not None
            artifacts = res.snapshot.artifacts
            assert len(artifacts) == 1
            art = artifacts[0]
            assert isinstance(art, Artifact)
            assert art.metadata["count"] > 0
