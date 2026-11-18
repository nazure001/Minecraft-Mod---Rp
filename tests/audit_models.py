import json
import os

valid_angles = {-45.0, -22.5, 0.0, 22.5, 45.0}

dirs_to_check = [
    r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets",
    r"d:\repo\Minecraft Mod & Rp\mod\src\client\resources\assets",
]

print("=== CHECKING ALL MODEL ROTATIONS ===")
for base in dirs_to_check:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith(".json"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                    if isinstance(data, dict) and "elements" in data:
                        for i, el in enumerate(data["elements"]):
                            if "rotation" in el:
                                rot = el["rotation"]
                                ang = float(rot.get("angle", 0))
                                if ang not in valid_angles:
                                    print(f"[{f}] elem {i} ({el.get('name', 'unnamed')}): angle={ang}")
                except Exception as e:
                    pass

print("\n=== CHECKING OVERRIDES EXISTENCE ===")
main_assets = r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets"
items_dir = os.path.join(main_assets, "minecraft", "models", "item")
if os.path.exists(items_dir):
    for f in os.listdir(items_dir):
        if f.endswith(".json"):
            path = os.path.join(items_dir, f)
            with open(path, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            for ov in data.get("overrides", []):
                model_ref = ov.get("model", "")
                if ":" in model_ref:
                    ns, mpath = model_ref.split(":", 1)
                    target = os.path.join(main_assets, ns, "models", mpath + ".json")
                    if not os.path.exists(target):
                        print(f"{f}: missing {model_ref} -> {target}")

print("\n=== CHECKING TEXTURES EXISTENCE ===")
for root, dirs, files in os.walk(main_assets):
    for f in files:
        if f.endswith(".json"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                if isinstance(data, dict) and "textures" in data:
                    for k, tex in data["textures"].items():
                        if isinstance(tex, str) and not tex.startswith("#"):
                            if ":" in tex:
                                ns, tpath = tex.split(":", 1)
                                if ns == "minecraft":
                                    continue
                                ttarget = os.path.join(main_assets, ns, "textures", tpath + ".png")
                                if not os.path.exists(ttarget):
                                    print(f"{f}: texture missing! {tex} -> {ttarget}")
            except Exception as e:
                pass
print("=== DONE ===")
