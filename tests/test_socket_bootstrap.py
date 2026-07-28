import os
import socket
import sys
import time
from pathlib import Path


def test_bootstrap_real_runtime():
  print("==================================================")
  print("   TERMIRIS - TESTE E2E DO RUNTIME (MITL REAL)    ")
  print("==================================================")

  runtime_dir = Path.home() / ".termiris" / "runtime"
  socket_path = runtime_dir / "parser.sock"
  snapshot_path = runtime_dir / "cache" / "state" / "snapshot.ctx"

  # 1. Garante a estrutura e limpa o snapshot para testar escrita do zero
  snapshot_path.parent.mkdir(parents=True, exist_ok=True)
  if snapshot_path.exists():
    snapshot_path.unlink()
    print("🧹 [CLEANUP] Snapshot antigo limpo.")

  # 2. Testa o envio direto ao Protocol Handler (O mesmo fallback do seu script 'ai')
  print("⚡ [DISPATCH] Injetando '<< BOOTSTRAP >>' no protocol-handler...")

  # Executa o comando via subprocess exatamente como o seu bin/ai faz
  cmd = f'echo "<< BOOTSTRAP >>" | {Path.home()}/.termiris/bin/protocol-handler'
  exit_code = os.system(cmd)

  assert exit_code == 0, "Falha ao executar o bin/protocol-handler"

  # 3. Polling para garantir que o snapshot.ctx foi escrito no disco
  print("⏳ [WAIT] Verificando criação atômica do snapshot.ctx...")
  timeout = 3.0
  start_time = time.time()

  while time.time() - start_time < timeout:
    if snapshot_path.exists() and snapshot_path.stat().st_size > 0:
      break
    time.sleep(0.1)

  # 4. Validações
  assert (
      snapshot_path.exists()
  ), f"O snapshot não foi gerado em: {snapshot_path}"

  content = snapshot_path.read_text()
  print("\n✅ [SUCESSO] snapshot.ctx atualizado pelo Runtime!")
  print("--------------------------------------------------")
  print(content[:250] + "\n...")
  print("--------------------------------------------------")

  # Regras do protocolo
  assert (
      "TERMIRIS BOOTSTRAP" in content
      or "state=LEARNING" in content
      or "type=BOOTSTRAP" in content
  )
  assert "<<RETRIEVE FILE protocol/SPEC_PROTOCOL.md>>" in content
  print("\n🎉 TESTE E2E PASSOU COM SUCESSO!")


if __name__ == "__main__":
  test_bootstrap_real_runtime()
