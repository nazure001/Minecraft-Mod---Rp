import urllib.request
import json

def call_bb(action, params={}):
    req = urllib.request.Request(
        "http://127.0.0.1:8787/command",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"id": "req-rig-check", "action": action, "params": params}).encode("utf-8")
    )
    resp = urllib.request.urlopen(req, timeout=5)
    return json.loads(resp.read().decode())

out = call_bb("list_outliner")
for el in out.get("result", []):
    print(f"[{el.get('type')}] {el.get('name')} | origin={el.get('origin')} | parent={el.get('parent')}")
