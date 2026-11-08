import urllib.request
import json

def call_bb(action, params={}):
    req = urllib.request.Request(
        "http://127.0.0.1:8787/command",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"id": "req-tree", "action": action, "params": params}).encode("utf-8")
    )
    resp = urllib.request.urlopen(req, timeout=5)
    return json.loads(resp.read().decode())

res = call_bb("list_outliner")
tree = res.get("result", [])

def print_node(n, indent=0):
    pref = "  " * indent
    t = n.get("type")
    name = n.get("name")
    origin = n.get("origin")
    rot = n.get("rotation")
    f = n.get("from")
    to = n.get("to")
    if t == "group":
        print(f"{pref}+ [GROUP] {name} (origin: {origin}, rot: {rot})")
        for c in n.get("children", []):
            print_node(c, indent + 1)
    else:
        print(f"{pref}- [CUBE] {name} from={f} to={to} origin={origin} rot={rot}")

print("=== ACTUAL BLOCKBENCH OUTLINER TREE ===")
for root_node in tree:
    print_node(root_node)
