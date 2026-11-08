import urllib.request
import json
import numpy as np

def call_bb(action, params={}):
    req = urllib.request.Request(
        "http://127.0.0.1:8787/command",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"id": "req-diag", "action": action, "params": params}).encode("utf-8")
    )
    resp = urllib.request.urlopen(req, timeout=5)
    return json.loads(resp.read().decode())

out = call_bb("list_outliner")
elements = out.get("result", [])
print(f"Total elements returned: {len(elements)}")
for el in elements:
    name = el.get("name")
    parent = el.get("parent")
    origin = el.get("origin")
    rot = el.get("rotation")
    f = el.get("from")
    t = el.get("to")
    print(f"[{el.get('type')}] {name} (parent: {parent}) origin={origin} rot={rot} from={f} to={t}")
