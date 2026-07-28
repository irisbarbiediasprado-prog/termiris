import pytest
from pathlib import Path
from protocol.isa import PrimitiveISA, Operation
from protocol.ir import IntentKind, Intent
from protocol.kernel import Tokenizer, CommandRouter, ProtocolKernel
from protocol.plugins.retrieve import RetrievePlugin
from protocol.plugins.bootstrap import BootstrapPlugin


class TestVPMProtocolFramework:
    """Testes unitários e de integração para a Virtual Protocol Machine (VPM)."""

    @pytest.fixture
    def router_with_plugins(self):
        """Monta um CommandRouter e registra os plugins padrão."""
        router = CommandRouter()
        router.register(RetrievePlugin())
        router.register(BootstrapPlugin())
        return router

    @pytest.fixture
    def kernel(self, router_with_plugins):
        return ProtocolKernel(router_with_plugins)

    # -------------------------------------------------------------------------
    # 1. Testes do Tokenizer
    # -------------------------------------------------------------------------

    def test_tokenizer_valid_tag(self):
        tokens = Tokenizer.tokenize("Texto livre << RETRIEVE FILE main.py >> mais texto")
        assert tokens == ["RETRIEVE", "FILE", "main.py"]

    def test_tokenizer_no_tag_returns_empty(self):
        tokens = Tokenizer.tokenize("Apenas um texto qualquer sem protocolo")
        assert tokens == []

    # -------------------------------------------------------------------------
    # 2. Testes do Kernel e Pipeline (Tokens -> AST -> IR -> ISA)
    # -------------------------------------------------------------------------

    def test_kernel_compiles_retrieve_file(self, kernel):
        raw_input = "<< RETRIEVE FILE main.py >>"
        operations = kernel.compile(raw_input)

        assert len(operations) == 1
        op = operations[0]
        assert isinstance(op, Operation)
        assert op.instruction == PrimitiveISA.READ
        assert op.payload["target"] == "main.py"

    def test_kernel_compiles_bootstrap(self, kernel):
        raw_input = "<< BOOTSTRAP >>"
        operations = kernel.compile(raw_input)

        assert len(operations) == 1
        op = operations[0]
        assert op.instruction == PrimitiveISA.SNAPSHOT
        # Em tests/test_protocol.py:
        assert op.payload["action"] == "BOOTSTRAP_GENESIS"
        assert (
                    op.payload["file_path"]
                        == f"{Path.home()}/.termiris/tp/bootstrap/000-bootstrap.card"
                        )



    def test_kernel_unregistered_command_raises_error(self, kernel):
        with pytest.raises(ValueError, match="Comando do protocolo não reconhecido: UNKNOWN"):
            kernel.compile("<< UNKNOWN COMMAND >>")

    def test_kernel_empty_input_returns_empty_list(self, kernel):
        assert kernel.compile("") == []

    # -------------------------------------------------------------------------
    # 3. Testes do Auto-Discovery do CommandRouter
    # -------------------------------------------------------------------------

    def test_router_auto_discovery(self):
        router = CommandRouter()
        router.auto_discover()

        # Garante que os plugins da pasta plugins/ foram descobertos
        assert router.route("RETRIEVE") is not None
        assert router.route("BOOTSTRAP") is not None
