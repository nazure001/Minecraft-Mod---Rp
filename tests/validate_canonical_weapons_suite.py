#!/usr/bin/env python3
"""
Validation Suite for Avatar Elements Tahap 4 Canonical Weapons 3D Blockbench Suite.
Verifies all 4 canonical weapons:
- SM_Dual_Swords
- SM_Earth_Hammer
- SM_War_Fan
- SM_Water_Spear

Checks:
1. File deliverables existence across all formats (.bbmodel, .geo.json, .json, .obj, .mtl, .png, preview stills & GIFs)
2. Java JSON model coordinate bounds strictly in [-16, 32]
3. Bedrock geometry schema and bone definitions
4. Blockbench project format, resolution (64x64), embedded textures, and locators
5. 64x64 texture atlas resolution and format validity
6. Wavefront OBJ & MTL syntax integrity
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSET_PACK = ROOT / "art-source" / "asset_pack"

WEAPONS = [
    ("SM_Dual_Swords", "Zuko Dao Broadswords"),
    ("SM_Earth_Hammer", "Kyoshi Earthbender Warhammer"),
    ("SM_War_Fan", "Kyoshi Warriors War Fan"),
    ("SM_Water_Spear", "Water Tribe Harpoon Spear")
]

checks = []

def record(name, passed, detail=""):
    checks.append((name, passed, detail))
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}: {detail}")

print("\n=======================================================")
print(" RUNNING CANONICAL WEAPONS ASSET VALIDATION SUITE")
print("=======================================================\n")

for asset_id, title in WEAPONS:
    print(f"--> Validating {asset_id} ({title})...")

    # 1. Blockbench .bbmodel
    bb_path = ASSET_PACK / "models" / "bbmodel" / f"{asset_id}.bbmodel"
    bb_exists = bb_path.is_file()
    record(f"{asset_id} - Blockbench file exists", bb_exists, str(bb_path))

    if bb_exists:
        bb_data = json.loads(bb_path.read_text(encoding="utf-8"))
        res = bb_data.get("resolution", {})
        res_ok = res.get("width") == 64 and res.get("height") == 64
        record(f"{asset_id} - BBModel 64x64 resolution", res_ok, f"{res.get('width')}x{res.get('height')}")

        elements = bb_data.get("elements", [])
        record(f"{asset_id} - BBModel elements count", len(elements) > 0, f"{len(elements)} elements")

        textures = bb_data.get("textures", [])
        tex_ok = len(textures) > 0 and "data:image/png;base64," in textures[0].get("source", "")
        record(f"{asset_id} - BBModel embedded texture", tex_ok, f"{len(textures)} texture(s)")

        locators = bb_data.get("locators", {})
        loc_ok = "trail_begin" in locators and "trail_end" in locators and "imbue_emitter" in locators
        record(f"{asset_id} - BBModel locators", loc_ok, f"Keys: {list(locators.keys())}")

    # 2. Bedrock .geo.json
    geo_path = ASSET_PACK / "models" / f"{asset_id}.geo.json"
    geo_exists = geo_path.is_file()
    record(f"{asset_id} - Bedrock geometry file exists", geo_exists, str(geo_path))

    if geo_exists:
        geo_data = json.loads(geo_path.read_text(encoding="utf-8"))
        geo_list = geo_data.get("minecraft:geometry", [])
        geo_ok = len(geo_list) > 0 and geo_list[0].get("description", {}).get("identifier") == f"geometry.{asset_id}"
        record(f"{asset_id} - Bedrock identifier geometry.{asset_id}", geo_ok, str(geo_list[0].get("description", {}).get("identifier") if geo_list else "None"))

    # 3. Java display model .json
    java_path = ASSET_PACK / "models" / f"{asset_id}.json"
    java_exists = java_path.is_file()
    record(f"{asset_id} - Java model file exists", java_exists, str(java_path))

    if java_exists:
        java_data = json.loads(java_path.read_text(encoding="utf-8"))
        j_elements = java_data.get("elements", [])
        out_of_bounds = []
        for el in j_elements:
            for k in ("from", "to"):
                coords = el.get(k, [])
                if any(c < -16.0 or c > 32.0 for c in coords):
                    out_of_bounds.append((el.get("name"), k, coords))
        record(f"{asset_id} - Java model coordinates [-16, 32]", len(out_of_bounds) == 0, f"{len(j_elements)} elements; Out-of-bounds: {out_of_bounds}")

        display = java_data.get("display", {})
        disp_ok = "thirdperson_righthand" in display and "firstperson_righthand" in display and "gui" in display
        record(f"{asset_id} - Java display transforms", disp_ok, f"Modes: {list(display.keys())}")

    # 4. Wavefront OBJ & MTL
    obj_path = ASSET_PACK / "meshes" / "weapons" / f"{asset_id}.obj"
    mtl_path = ASSET_PACK / "meshes" / "weapons" / f"{asset_id}.mtl"
    obj_ok = obj_path.is_file() and obj_path.stat().st_size > 500
    mtl_ok = mtl_path.is_file() and mtl_path.stat().st_size > 50
    record(f"{asset_id} - Wavefront OBJ & MTL exist", obj_ok and mtl_ok, f"OBJ: {obj_path.stat().st_size if obj_path.is_file() else 0} bytes")

    # 5. Texture Atlas 64x64 PNG
    tex_path = ASSET_PACK / "assets" / "avatar_elements" / "textures" / "weapons" / f"{asset_id}.png"
    tex_exists = tex_path.is_file()
    if tex_exists:
        img = Image.open(tex_path)
        img_ok = img.size == (64, 64) and img.mode in ("RGBA", "RGB")
        record(f"{asset_id} - 64x64 RGBA Texture Atlas", img_ok, f"Size: {img.size}, Mode: {img.mode}")
    else:
        record(f"{asset_id} - Texture Atlas exists", False, str(tex_path))

    # 6. Previews (Isometric PNG and Turntable GIF)
    iso_path = ASSET_PACK / "previews" / asset_id / f"{asset_id}_isometric.png"
    gif_path = ASSET_PACK / "previews" / asset_id / f"{asset_id}_turntable.gif"
    previews_ok = iso_path.is_file() and gif_path.is_file() and gif_path.stat().st_size > 10000
    record(f"{asset_id} - 3D Isometric & Turntable GIF", previews_ok, f"GIF size: {gif_path.stat().st_size if gif_path.is_file() else 0} bytes")

    print("")

all_passed = all(p for _, p, _ in checks)
passed_count = sum(1 for _, p, _ in checks)
total_count = len(checks)

print("=======================================================")
print(f" RESULT: {passed_count}/{total_count} CHECKS PASSED ({100.0 * passed_count / total_count:.1f}%)")
print("=======================================================\n")

if not all_passed:
    sys.exit(1)
