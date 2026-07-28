import sys, os, json

INDEX_FILE = os.path.expanduser("~/.termiris/runtime/cache/artifacts/index.json")

def main():
    if sys.stdin.isatty():
        return

    try:
        evt = json.load(sys.stdin)
        art_id = evt.get("artifact_id")
        if not art_id:
            return

        index_data = {"entries": {}}
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index_data = json.load(f)

        evt_type = evt.get("type", "CONTEXT_CREATED")
        if evt_type in ["CONTEXT_CREATED", "CONTEXT_UPDATED"]:
            index_data["entries"][art_id] = {
                "type": evt.get("artifact_type", "default"),
                "state": evt.get("state", "ACTIVE"),
                "priority": int(evt.get("priority", 0)),
                "resource": evt.get("resource", "")
            }
        elif evt_type == "CONTEXT_DELETED":
            if art_id in index_data["entries"]:
                index_data["entries"][art_id]["state"] = "DELETED"

        os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
        tmp = INDEX_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2)
        os.rename(tmp, INDEX_FILE)
    except Exception as e:
        sys.stderr.write(f"[indexer] Erro: {e}\n")

