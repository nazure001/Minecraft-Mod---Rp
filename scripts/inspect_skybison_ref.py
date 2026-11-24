import os
import json

base_ref = r"d:\repo\Minecraft Mod & Rp\reference\avatar-legend-reforged-1.3.0\assets\av3"
geo_path = os.path.join(base_ref, "geo", "entity", "skybison.geo.json")
anim_path = os.path.join(base_ref, "animations", "entity", "skybison.animation.json")

print("=== SKYBISON.GEO.JSON ===")
if os.path.exists(geo_path):
    with open(geo_path, "r", encoding="utf-8") as f:
        gdata = json.load(f)
    geom = gdata.get("minecraft:geometry", [{}])[0]
    desc = geom.get("description", {})
    print(f"Texture: {desc.get('texture_width')}x{desc.get('texture_height')}")
    bones = geom.get("bones", [])
    print(f"Total bones: {len(bones)}")
    for b in bones:
        cubes = b.get("cubes", [])
        print(f"  Bone: {b.get('name')}, parent={b.get('parent')}, pivot={b.get('pivot')}, rot={b.get('rotation')}, cubes={len(cubes)}")
        for c in cubes[:1]:
            print(f"    sample cube: size={c.get('size')}, inflate={c.get('inflate')}")

print("\n=== SKYBISON.ANIMATION.JSON ===")
if os.path.exists(anim_path):
    with open(anim_path, "r", encoding="utf-8") as f:
        adata = json.load(f)
    anims = adata.get("animations", {})
    print(f"Animations: {list(anims.keys())}")
    for aname, acontent in anims.items():
        print(f"  Anim: {aname}, loop={acontent.get('loop')}, length={acontent.get('animation_length')}")
        bone_keys = list(acontent.get("bones", {}).keys())
        print(f"    animated bones ({len(bone_keys)}): {bone_keys[:6]}...")
