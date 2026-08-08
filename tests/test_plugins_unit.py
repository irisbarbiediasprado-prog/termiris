import pytest
from protocol.ir import IntentKind, Intent
from protocol.compiler import ProtocolCompiler
from protocol.isa import PrimitiveISA, Operation
from protocol.plugins.retrieve import RetrievePlugin, ResourceType
from protocol.plugins.bootstrap import BootstrapPlugin


class TestRetrievePlugin:
    """Testes unitários isolados do RetrievePlugin."""

    @pytest.fixture
    def plugin(self):
        return RetrievePlugin()

    def test_parse_ast_valid_file(self, plugin):
        tokens = ["FILE", "main.py"]
        ast = plugin.parse_ast(tokens)
        
        assert ast.resource_type == ResourceType.FILE
        assert ast.targets[0] == "main.py"

    def test_parse_ast_invalid_args_raises_value_error(self, plugin):
        """Garante que o parser falhe cedo ao receber argumentos insuficientes."""
        with pytest.raises(ValueError, match="RETRIEVE vazio"):
            plugin.parse_ast([])

    def test_lower_to_intent(self, plugin):
        ast = plugin.parse_ast(["FILE", "config.json"])
        intent = plugin.lower_to_intent(ast)

        assert isinstance(intent, Intent)
        assert intent.kind == IntentKind.READ_RESOURCE
        assert intent.target == "config.json"

    def test_lower_to_operations(self, plugin):
        ast = plugin.parse_ast(["FILE", "script.py"])
        intent = plugin.lower_to_intent(ast)
        compiler = ProtocolCompiler()
        operations = compiler.compile(intent)

        assert len(operations) == 1
        assert operations[0].instruction == PrimitiveISA.RETRIEVE
        assert operations[0].payload["resource_type"] == "FILE"
        assert operations[0].payload["target"] == "script.py"


class TestBootstrapPlugin:
    """Testes unitários isolados do BootstrapPlugin."""

    @pytest.fixture
    def plugin(self):
        return BootstrapPlugin()

    def test_command_name(self, plugin):
        assert plugin.command == "BOOTSTRAP"

    def test_full_pipeline(self, plugin):
        ast = plugin.parse_ast([])
        intent = plugin.lower_to_intent(ast)
        compiler = ProtocolCompiler()
        operations = compiler.compile(intent)

        assert intent.kind == IntentKind.BOOTSTRAP_GENESIS
        # Em tests/test_plugins_unit.py:
        assert intent.target == "bootstrap_plugin"  # Era "bootstrap_repository"

        # Em tests/test_plugins_unit.py:
        assert "source_file" in intent.metadata
        assert intent.metadata["source_file"].endswith("000-bootstrap.card")

        assert len(operations) == 1
        assert operations[0].instruction == PrimitiveISA.SNAPSHOT
