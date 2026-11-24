import os
import json

ref_dir = r"d:\repo\Minecraft Mod & Rp\reference"
found = []
for root, dirs, files in os.walk(ref_dir):
    for f in files:
        if f.endswith((".geo.json", ".animation.json", ".bbmodel")):
            found.append(os.path.join(root, f))
            if len(found) >= 15:
                break
    if len(found) >= 15:
        break

print(f"Found {len(found)} model/anim files in reference:")
for p in found:
    rel = os.path.relpath(p, ref_dir)
    print(" ", rel)

# Inspect one geo.json if found
for p in found:
    if p.endswith(".geo.json"):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        geos = data.get("minecraft:geometry", [])
        if geos:
            g = geos[0]
            bones = g.get("bones", [])
            print(f"\nStructure of {os.path.basename(p)}:")
            print(f"  Texture: {g.get('description', {}).get('texture_width')}x{g.get('description', {}).get('texture_height')}")
            print(f"  Bones count: {len(bones)}")
            for b in bones[:8]:
                print(f"    - {b.get('name')} (parent: {b.get('parent')}, pivot: {b.get('pivot')}, rot: {b.get('rotation')}, cubes: {len(b.get('cubes', []))})")
        break
