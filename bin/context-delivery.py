#!/usr/bin/env python3
import time
import subprocess
import sys
from pathlib import Path

lib_path = Path.home() / ".termiris/lib"
sys.path.insert(0, str(lib_path))

from termiris.context_policy import ContextPolicy

STATE_DIR = Path.home() / ".termiris/runtime/cache/state"
SNAPSHOT = STATE_DIR / "snapshot.ctx"
META = STATE_DIR / "snapshot.meta"
SESSION_STATE = Path.home() / ".termiris/runtime/cache/sessions/state"

SESSION = "ia_chat"
TARGET = "ia_chat:Chat*"

policy = ContextPolicy(state_dir=STATE_DIR)

def should_deliver(new_hash, last_success):
    return new_hash is not None and new_hash != last_success
def get_snapshot_hash():
    if not META.exists():
        return None
    for line in META.read_text().splitlines():
        if line.startswith("snapshot_hash="):
            return line.split("=", 1)[1].strip()
    return None

def deliver(hash_val):
    # ContextPolicy decide se deve enviar ou não
    decision = policy.check(hash_val)
    print(f"[policy] {decision}")
    if decision["mode"] == "PG":
        print(f"⏳ Política: modo PG, aguardando {decision['delay']}s")
        time.sleep(decision["delay"])
    # Envia .file puro, SEM hash
    subprocess.run([
        "tmux", "send-keys", "-t", TARGET, "C-u",
        f".file {SNAPSHOT}", "Enter"
    ], check=True)
    print(f"🟢 .file enviado (hash={hash_val})")

def read_session_state():
    if not SESSION_STATE.exists():
        return None
    state = {}
    for line in SESSION_STATE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            state[k.strip()] = v.strip()
    return state

def main():
    print("👁️ context-delivery (Python) iniciado")
    last_success = ""
    last_success_file = STATE_DIR / "last_success"
    if last_success_file.exists():
        last_success = last_success_file.read_text().strip()

    while True:
        new_hash = get_snapshot_hash()
        if new_hash and new_hash != last_success:
            deliver(new_hash)
            # Aguarda confirmação do estado
            for _ in range(120):
                state = read_session_state()
                if state and state.get("hash") == new_hash:
                    status = state.get("status", "")
                    if status in ("PASS", "SUCCESS", "OK"):
                        last_success_file.write_text(new_hash)
                        print("✅ Sucesso")
                        break
                    elif status in ("TEMP_ERROR", "RETRY"):
                        print("⚠️ Erro temporário, reenviando...")
                        break
                    elif status in ("FAIL", "ERROR", "PERM_ERROR"):
                        print("❌ Erro permanente")
                        break
                time.sleep(1)
            else:
                print("⏰ Timeout")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
