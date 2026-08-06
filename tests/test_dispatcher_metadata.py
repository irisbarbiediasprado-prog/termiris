import pytest
from unittest.mock import MagicMock, patch
from protocol.dispatcher import ProtocolDispatcher, ProtocolRuntime
from protocol.isa import Operation, PrimitiveISA
from cli.metadata import extract_metadata

class TestDispatcherMetadata:
    def test_dispatch_injects_metadata(self):
        """Verifica se o dispatcher injeta metadados na Operation."""
        mock_kernel = MagicMock()
        mock_op = Operation(instruction=PrimitiveISA.RETRIEVE, payload={"target": "foo"})
        mock_kernel.compile.return_value = [mock_op]

        dispatcher = ProtocolDispatcher(kernel=mock_kernel, engine=None)
        raw = ".file foo --hash=abc123 --origin=test"
        ops = dispatcher.dispatch(raw)

        assert len(ops) == 1
        assert ops[0].metadata == {"hash": "abc123", "origin": "test"}

    def test_dispatch_without_metadata(self):
        """Quando não há metadados, a Operation não deve ter metadata."""
        mock_kernel = MagicMock()
        mock_op = Operation(instruction=PrimitiveISA.RETRIEVE, payload={"target": "foo"})
        mock_kernel.compile.return_value = [mock_op]

        dispatcher = ProtocolDispatcher(kernel=mock_kernel, engine=None)
        raw = ".file foo"
        ops = dispatcher.dispatch(raw)

        assert len(ops) == 1
        assert ops[0].metadata == {}

    def test_dispatch_preserves_other_fields(self):
        """Verifica se outros campos da Operation são preservados ao adicionar metadata."""
        mock_kernel = MagicMock()
        mock_op = Operation(
            instruction=PrimitiveISA.RETRIEVE,
            payload={"target": "foo", "extra": "bar"}
        )
        mock_kernel.compile.return_value = [mock_op]

        dispatcher = ProtocolDispatcher(kernel=mock_kernel, engine=None)
        raw = ".file foo --hash=abc123"
        ops = dispatcher.dispatch(raw)

        assert ops[0].instruction == PrimitiveISA.RETRIEVE
        assert ops[0].payload == {"target": "foo", "extra": "bar"}
        assert ops[0].metadata == {"hash": "abc123"}

    def test_protocol_runtime_returns_operations_with_metadata(self):
        """ProtocolRuntime com engine=None deve retornar Operations com metadata."""
        mock_kernel = MagicMock()
        mock_op = Operation(instruction=PrimitiveISA.RETRIEVE, payload={"target": "foo"})
        mock_kernel.compile.return_value = [mock_op]

        dispatcher = ProtocolDispatcher(kernel=mock_kernel, engine=None)
        runtime = ProtocolRuntime(dispatcher=dispatcher)

        raw = ".file foo --hash=abc123"
        ops = runtime.handle(raw)

        assert len(ops) == 1
        assert ops[0].metadata == {"hash": "abc123"}
