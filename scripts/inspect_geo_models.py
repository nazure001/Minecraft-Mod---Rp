import json
import os

geo_dir = r"d:\repo\Minecraft Mod & Rp\art-source\Avatar_Elements_Missing_Assets_Staging\models\entity"

for mob in ["flying_bison", "platypus_bear", "phoenix_king_ozai"]:
    path = os.path.join(geo_dir, f"{mob}.geo.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        geos = data.get("minecraft:geometry", [])
        if geos:
            g = geos[0]
            desc = g.get("description", {})
            tex_w = desc.get("texture_width")
            tex_h = desc.get("texture_height")
            bones = g.get("bones", [])
            print(f"=== {mob} ===")
            print(f"Texture dimensions: {tex_w}x{tex_h}")
            print(f"Bones count: {len(bones)}")
            for b in bones:
                cubes = b.get("cubes", [])
                print(f"  Bone: {b.get('name')}, parent={b.get('parent')}, cubes={len(cubes)}")
                for c in cubes[:3]:
                    print(f"    Cube: origin={c.get('origin')}, size={c.get('size')}, uv={c.get('uv')}")
    else:
        print(f"Not found: {path}")
