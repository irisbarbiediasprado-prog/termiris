import sys, os, json, subprocess

BACKENDS_DIR = os.path.expanduser("~/.termiris/bin/resource_backends")

def fetch_resource(resource_uri: str) -> dict:
    provider = resource_uri.split("://")[0] if "://" in resource_uri else "filesystem"
    backend_bin = os.path.join(BACKENDS_DIR, provider)

    if not (os.path.exists(backend_bin) and os.access(backend_bin, os.X_OK)):
        backend_bin = os.path.join(BACKENDS_DIR, "filesystem")

    try:
        p = subprocess.Popen([backend_bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate(input=json.dumps({"resource": resource_uri}).encode("utf-8"))
        return json.loads(out.decode("utf-8"))
    except Exception as e:
        return {"payload": {"error": str(e)}}

def main():
    if not sys.stdin.isatty():
        req = json.load(sys.stdin)
        res = fetch_resource(req.get("resource", ""))
        print(json.dumps(res))

