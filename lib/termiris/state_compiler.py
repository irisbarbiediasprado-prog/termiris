#!/usr/bin/env python3
"""
TERMIRIS STATE COMPILER (Linker)
Compila o estado LOGICO sem cortes de cota/janela física.
Gera a generation do build no active_manifest.json.
"""

import os
import sys
import json
import time

ROOT_DIR = os.environ.get("TERMIRIS_RUNTIME", os.path.expanduser("~/.termiris/runtime"))
ARTIFACT_DIR = os.path.join(ROOT_DIR, "cache", "artifacts")
STATE_DIR = os.path.join(ROOT_DIR, "cache", "state")

INDEX_FILE = os.path.join(ARTIFACT_DIR, "index.json")
MANIFEST_FILE = os.path.join(STATE_DIR, "active_manifest.json")

def compile_state():
    if not os.path.exists(INDEX_FILE):
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_entries = json.load(f).get("entries", {})

    last_gen = 0
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                last_gen = json.load(f).get("generation", 0)
        except Exception:
            pass

    # Mapeamento do ciclo de vida
    active_ids, dormant_ids, invalid_ids, deleted_ids, error_ids = [], [], [], [], []

    for art_id, meta in index_entries.items():
        state = meta.get("state", "NEW")

        if state in ["ACTIVE", "NEW"]:
            active_ids.append(art_id)
        elif state == "DORMANT":
            dormant_ids.append(art_id)
        elif state == "INVALID":
            invalid_ids.append(art_id)
        elif state == "DELETED":
            deleted_ids.append(art_id)
        else:
            error_ids.append(art_id)

    manifest_data = {
        "version": 1,
        "generation": last_gen + 1,
        "generated_at": int(time.time() * 1000),
        "states": {
            "active": active_ids,
            "dormant": dormant_ids,
            "invalid": invalid_ids,
            "deleted": deleted_ids,
            "error": error_ids
        }
    }

    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = MANIFEST_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.rename(tmp, MANIFEST_FILE)

    sys.stderr.write(f"[compiler] Build Gen {last_gen + 1}: {len(active_ids)} ativos.\n")

def main():
        compile_state()



if __name__ == "__main__":
    main()