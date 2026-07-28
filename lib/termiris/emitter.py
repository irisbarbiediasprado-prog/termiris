import sys, os, json, subprocess
from termiris.resource_manager import fetch_resource

INDEX_FILE = os.path.expanduser("~/.termiris/runtime/cache/artifacts/index.json")
MANIFEST_FILE = os.path.expanduser("~/.termiris/runtime/cache/state/active_manifest.json")
SNAPSHOT_FILE = os.path.expanduser("~/.termiris/runtime/cache/state/snapshot.ctx")
RENDERERS_DIR = os.path.expanduser("~/.termiris/bin/renderers")

MAX_BYTES = 65536  # Cota do MVP

def render(art_type: str, payload: dict) -> str:
    renderer_bin = os.path.join(RENDERERS_DIR, art_type.lower())
    if not (os.path.exists(renderer_bin) and os.access(renderer_bin, os.X_OK)):
        renderer_bin = os.path.join(RENDERERS_DIR, "default")

    try:
        p = subprocess.Popen([renderer_bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, _ = p.communicate(input=json.dumps(payload).encode("utf-8"))
        return out.decode("utf-8").strip()
    except Exception as e:
        return f"[Render Error: {e}]"

def main():
    if not (os.path.exists(MANIFEST_FILE) and os.path.exists(INDEX_FILE)):
        return

    with open(MANIFEST_FILE, "r") as f:
        manifest = json.load(f)
    with open(INDEX_FILE, "r") as f:
        entries = json.load(f).get("entries", {})

    gen = manifest.get("generation", 0)
    lines = [f"<!-- TERMIRIS SNAPSHOT GEN {gen} -->\n"]
    curr_bytes = 0

    for art_id in manifest.get("active", []):
        meta = entries.get(art_id)
        if not meta:
            continue

        res_data = fetch_resource(meta.get("resource", ""))
        rendered = render(meta.get("type", "default"), res_data.get("payload", {}))
        
        block = f'<context id="{art_id}" type="{meta.get("type")}">\n{rendered}\n</context>\n'
        b_len = len(block.encode("utf-8"))

        if curr_bytes + b_len > MAX_BYTES:
            break

        lines.append(block)
        curr_bytes += b_len

    tmp = SNAPSHOT_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    os.rename(tmp, SNAPSHOT_FILE)
