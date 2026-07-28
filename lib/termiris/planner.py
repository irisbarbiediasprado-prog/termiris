import sys, os, json

INDEX_FILE = os.path.expanduser("~/.termiris/runtime/cache/artifacts/index.json")
MANIFEST_FILE = os.path.expanduser("~/.termiris/runtime/cache/state/active_manifest.json")

def main():
    if not os.path.exists(INDEX_FILE):
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f).get("entries", {})

    last_gen = 0
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                last_gen = json.load(f).get("generation", 0)
        except Exception:
            pass

    active = [
        art_id for art_id, meta in entries.items() 
        if meta.get("state") in ["ACTIVE", "NEW"]
    ]

    manifest_data = {
        "generation": last_gen + 1,
        "active": active
    }

    os.makedirs(os.path.dirname(MANIFEST_FILE), exist_ok=True)
    tmp = MANIFEST_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    os.rename(tmp, MANIFEST_FILE)

