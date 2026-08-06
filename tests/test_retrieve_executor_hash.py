import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from protocol.isa import Operation, PrimitiveISA
from runtime.retrieve_executor import RetrieveExecutor
from models import Artifact

class TestRetrieveExecutorHash:
    @patch("runtime.retrieve_executor.Path.home")
    def test_execute_attaches_hash_to_artifact(self, mock_home, tmp_path):
        """Verifica se o hash é extraído de op.metadata e anexado ao artifact.metadata."""
        # Cria diretório fake para o trace
        fake_home = tmp_path / "fake-home"
        fake_runtime = fake_home / ".termiris" / "runtime"
        fake_runtime.mkdir(parents=True, exist_ok=True)
        mock_home.return_value = fake_home

        # Mock do emitter
        mock_emitter = MagicMock()
        mock_emitter.emit.return_value = MagicMock()

        # Mock do _file para retornar um artifact
        with patch("runtime.retrieve_executor._file") as mock_file:
            mock_file.return_value = Artifact(
                uri="file:///tmp/foo",
                content="conteudo",
                metadata={"kind": "file"}
            )
            executor = RetrieveExecutor(emitter=mock_emitter)
            op = Operation(
                instruction=PrimitiveISA.RETRIEVE,
                payload={"resource_type": "FILE", "target": "/tmp/foo"},
                metadata={"hash": "abc123"}
            )
            result = executor.execute(op)

            assert result.success is True
            # Verifica se o emitter recebeu um snapshot com artifact contendo hash
            call_args = mock_emitter.emit.call_args
            artifacts = call_args[0][1]  # segundo argumento é lista de artifacts
            assert len(artifacts) == 1
            assert artifacts[0].metadata.get("hash") == "abc123"

    def test_execute_without_hash(self, tmp_path):
        """Quando não há hash, o artifact não deve receber campo hash."""
        # Cria diretório fake
        fake_home = tmp_path / "fake-home"
        fake_runtime = fake_home / ".termiris" / "runtime"
        fake_runtime.mkdir(parents=True, exist_ok=True)

        mock_emitter = MagicMock()
        mock_emitter.emit.return_value = MagicMock()

        with patch("runtime.retrieve_executor.Path.home") as mock_home:
            mock_home.return_value = fake_home
            with patch("runtime.retrieve_executor._file") as mock_file:
                mock_file.return_value = Artifact(
                    uri="file:///tmp/foo",
                    content="conteudo",
                    metadata={"kind": "file"}
                )
                executor = RetrieveExecutor(emitter=mock_emitter)
                op = Operation(
                    instruction=PrimitiveISA.RETRIEVE,
                    payload={"resource_type": "FILE", "target": "/tmp/foo"},
                    metadata={}  # sem hash
                )
                result = executor.execute(op)

                call_args = mock_emitter.emit.call_args
                artifacts = call_args[0][1]
                assert len(artifacts) == 1
                assert "hash" not in artifacts[0].metadata
