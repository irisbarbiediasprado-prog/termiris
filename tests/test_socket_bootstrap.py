import os
import sys
from pathlib import Path

LIB_DIR = Path.home() / ".termiris" / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from protocol.dispatcher import ProtocolRuntime

def test_bootstrap_real_runtime():
    print("==================================================")
    print("   TERMIRIS - TESTE E2E DO RUNTIME (FACHADA MEM)   ")
    print("==================================================")

    runtime_dir = Path.home() / ".termiris" / "runtime"
    snapshot_path = runtime_dir / "cache" / "state" / "snapshot.ctx"

    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    if snapshot_path.exists():
        snapshot_path.unlink()
        print("🧹 [CLEANUP] Snapshot antigo limpo.")

    print("⚡ [DISPATCH] Processando '<< BOOTSTRAP >>' via ProtocolRuntime...")
    runtime = ProtocolRuntime()
    results = runtime.handle("<< BOOTSTRAP >>")

    assert len(results) > 0, "Nenhum resultado retornado pelo ProtocolRuntime"
    assert results[0].success, "A operação de SNAPSHOT falhou"
    assert snapshot_path.exists(), "O arquivo snapshot.ctx não foi criado no disco!"
    assert snapshot_path.stat().st_size > 0, "O snapshot.ctx foi criado mas está vazio"
    
    print("✅ [SUCESSO] snapshot.ctx gerado com sucesso via fachada!")
