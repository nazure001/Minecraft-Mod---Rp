import os
import json

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"

def build_geo_json(mob_id, cubes, tex_w=128, tex_h=128):
    bones = []
    # Root bone with cubes
    bone_cubes = []
    for c in cubes:
        bone_cubes.append({
            "origin": c["origin"],
            "size": c["size"],
            "uv": [c["uv"][0], c["uv"][1]]
        })
    bones.append({
        "name": "root",
        "pivot": [0, 0, 0],
        "cubes": bone_cubes
    })
    
    geo_data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": f"geometry.{mob_id}",
                    "texture_width": tex_w,
                    "texture_height": tex_h,
                    "visible_bounds_width": 4,
                    "visible_bounds_height": 4,
                    "visible_bounds_offset": [0, 1.5, 0]
                },
                "bones": bones
            }
        ]
    }
    return geo_data

bison_cubes = [
    {"origin": [-12, 10, -18], "size": [24, 16, 36], "uv": [0, 40, 64, 96]}, # body
    {"origin": [-9, 14, -30], "size": [18, 14, 14], "uv": [0, 0, 48, 40]},   # head
    {"origin": [-7, 14, -35], "size": [14, 8, 6], "uv": [48, 0, 80, 24]},     # snout
    {"origin": [9, 23, -24], "size": [4, 4, 6], "uv": [80, 0, 112, 32]},      # horn left base
    {"origin": [11, 27, -27], "size": [3, 9, 4], "uv": [80, 0, 112, 32]},     # horn left tip
    {"origin": [-13, 23, -24], "size": [4, 4, 6], "uv": [80, 0, 112, 32]},    # horn right base
    {"origin": [-14, 27, -27], "size": [3, 9, 4], "uv": [80, 0, 112, 32]},    # horn right tip
    {"origin": [9, 17, -19], "size": [3, 4, 3], "uv": [0, 10, 10, 20]},       # ear left
    {"origin": [-12, 17, -19], "size": [3, 4, 3], "uv": [0, 10, 10, 20]},      # ear right
    {"origin": [8, 0, -15], "size": [5, 10, 6], "uv": [0, 100, 20, 128]},     # leg FL
    {"origin": [-13, 0, -15], "size": [5, 10, 6], "uv": [0, 100, 20, 128]},    # leg FR
    {"origin": [8, 0, -2], "size": [5, 10, 6], "uv": [20, 100, 40, 128]},     # leg ML
    {"origin": [-13, 0, -2], "size": [5, 10, 6], "uv": [20, 100, 40, 128]},    # leg MR
    {"origin": [8, 0, 11], "size": [5, 10, 6], "uv": [40, 100, 60, 128]},     # leg BL
    {"origin": [-13, 0, 11], "size": [5, 10, 6], "uv": [40, 100, 60, 128]},    # leg BR
    {"origin": [-9, 15, 18], "size": [18, 4, 22], "uv": [64, 40, 100, 80]},  # beaver tail
    {"origin": [-11, 26, -6], "size": [22, 5, 20], "uv": [64, 80, 128, 128]} # saddle
]

platypus_cubes = [
    {"origin": [-8, 7, -11], "size": [16, 14, 22], "uv": [0, 40, 64, 95]},   # body
    {"origin": [-9, 14, -12], "size": [18, 8, 14], "uv": [0, 40, 64, 65]},    # shoulder mantle
    {"origin": [-5.5, 14, -19], "size": [11, 10, 9], "uv": [0, 0, 48, 40]},   # bear head
    {"origin": [-5, 14, -26], "size": [10, 3.5, 8], "uv": [48, 0, 88, 32]},   # platypus bill snout
    {"origin": [4, 22, -14], "size": [3, 3, 2], "uv": [6, 2, 14, 10]},       # ear left
    {"origin": [-7, 22, -14], "size": [3, 3, 2], "uv": [34, 2, 42, 10]},      # ear right
    {"origin": [5, 0, -9], "size": [4.5, 8, 5], "uv": [0, 100, 32, 128]},     # leg FL
    {"origin": [-9.5, 0, -9], "size": [4.5, 8, 5], "uv": [0, 100, 32, 128]},  # leg FR
    {"origin": [5, 0, 5], "size": [4.5, 8, 5], "uv": [32, 100, 64, 128]},     # leg BL
    {"origin": [-9.5, 0, 5], "size": [4.5, 8, 5], "uv": [32, 100, 64, 128]},  # leg BR
    {"origin": [-5.5, 10, 11], "size": [11, 3.5, 13], "uv": [64, 40, 104, 80]}# platypus tail
]

ozai_cubes = [
    {"origin": [-3.5, 23, -3.5], "size": [7, 8, 7], "uv": [0, 0, 32, 32]},       # head
    {"origin": [-1.5, 31, -1.5], "size": [3, 3.5, 3], "uv": [32, 0, 64, 32]},    # topknot
    {"origin": [-2, 32, -2.5], "size": [4, 6, 2], "uv": [40, 4, 56, 16]},        # crown crest
    {"origin": [-4, 11, -2.5], "size": [8, 12, 5], "uv": [0, 32, 64, 80]},       # torso upper
    {"origin": [-4.5, 0, -3], "size": [9, 12, 6], "uv": [0, 80, 64, 128]},       # lower imperial robe
    {"origin": [4, 19, -3.5], "size": [4, 4.5, 7], "uv": [64, 32, 96, 64]},      # pauldron left
    {"origin": [-8, 19, -3.5], "size": [4, 4.5, 7], "uv": [64, 32, 96, 64]},     # pauldron right
    {"origin": [4, 10, -2], "size": [3, 11, 4], "uv": [64, 64, 128, 128]},       # arm left + bracer
    {"origin": [-7, 10, -2], "size": [3, 11, 4], "uv": [64, 64, 128, 128]},      # arm right + bracer
    {"origin": [0.5, 0, -2], "size": [3.5, 11, 4], "uv": [0, 80, 32, 128]},      # leg left
    {"origin": [-4, 0, -2], "size": [3.5, 11, 4], "uv": [32, 80, 64, 128]}       # leg right
]

def update_geos():
    targets = [
        ("flying_bison", bison_cubes),
        ("platypus_bear", platypus_cubes),
        ("phoenix_king_ozai", ozai_cubes)
    ]
    
    dirs = [
        os.path.join(REPO_ROOT, "art-source", "Avatar_Elements_Missing_Assets_Staging", "models", "entity"),
        os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "models", "entity")
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        for mob_id, cubes in targets:
            out_p = os.path.join(d, f"{mob_id}.geo.json")
            gdata = build_geo_json(mob_id, cubes)
            with open(out_p, "w", encoding="utf-8") as f:
                json.dump(gdata, f, indent=2)
            print(f"Updated {mob_id}.geo.json at {out_p}")

if __name__ == "__main__":
    update_geos()
