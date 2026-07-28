from pathlib import Path
from protocol.plugins.bootstrap import BootstrapPlugin
from protocol.isa import PrimitiveISA

def test_bootstrap_e2e_integration():
    """Testa a integração E2E do BootstrapPlugin do carregamento ao disco."""
    # 1. Instancia o plugin
    plugin = BootstrapPlugin()
    assert plugin.command == "BOOTSTRAP"

    # 2. Roda a pipeline de compilação interna
    ast = plugin.parse_ast([])
    intent = plugin.lower_to_intent(ast)
    operations = plugin.lower_to_operations(intent)

    # 3. Valida a instrução ISA gerada
    op = operations[0]
    assert op.instruction == PrimitiveISA.SNAPSHOT
    assert op.payload["action"] == "BOOTSTRAP_GENESIS"

    # 4. Valida a integração com o sistema de arquivos (I/O)
    card_path = Path(op.payload["file_path"])
    assert card_path.exists(), f"Arquivo não encontrado em: {card_path}"

    content = card_path.read_text()
    assert "TERMIRIS BOOTSTRAP" in content
    assert "<<RETRIEVE FILE protocol/SPEC_PROTOCOL.md>>" in content

