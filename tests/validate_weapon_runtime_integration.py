#!/usr/bin/env python3
"""Validation gate for Weapon Runtime & Resource Integration (VA-07)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_ROOT = ROOT / "mod" / "src" / "main" / "resources"
MOD_MODELS = RESOURCE_ROOT / "assets" / "avatar_elements" / "models" / "item"
MOD_TEX = RESOURCE_ROOT / "assets" / "avatar_elements" / "textures"
IRON_SWORD_PATH = RESOURCE_ROOT / "assets" / "minecraft" / "models" / "item" / "iron_sword.json"
EN_LANG = RESOURCE_ROOT / "assets" / "avatar_elements" / "lang" / "en_us.json"
ID_LANG = RESOURCE_ROOT / "assets" / "avatar_elements" / "lang" / "id_id.json"
AVATAR_ITEMS_JAVA = ROOT / "mod" / "src" / "main" / "java" / "com" / "avatarmod" / "elements" / "item" / "AvatarItems.java"

checks = []

def record(name, passed, detail):
    checks.append((name, passed, detail))

# 1. Check AvatarItems.java registration
java_code = AVATAR_ITEMS_JAVA.read_text(encoding="utf-8")
for item_name, ident in [
    ("DUAL_SWORDS", "dual_swords"),
    ("EARTH_HAMMER", "earth_hammer"),
    ("WAR_FAN", "war_fan"),
    ("WATER_SPEAR", "water_spear")
]:
    registered = f'"{ident}"), {item_name}' in java_code
    record(f"Java registration: {item_name}", registered, f'Identifier "{ident}"')

# 2. Check Item Models Bounds and Textures
for ident in ["dual_swords", "earth_hammer", "war_fan", "water_spear"]:
    model_path = MOD_MODELS / f"{ident}.json"
    if not model_path.is_file():
        record(f"Model exists: {ident}", False, str(model_path))
        continue
    record(f"Model exists: {ident}", True, str(model_path))
    
    model_data = json.loads(model_path.read_text(encoding="utf-8"))
    out_of_bounds = []
    for elem in model_data.get("elements", []):
        for key in ("from", "to"):
            for v in elem[key]:
                if v < -16.0 or v > 32.0:
                    out_of_bounds.append((elem.get("name"), key, elem[key]))
    record(f"Model bounds [-16, 32]: {ident}", len(out_of_bounds) == 0, f"OOB: {out_of_bounds}")
    
    # Texture check
    tex_ref = model_data.get("textures", {}).get("texture", "")
    ns, rel_path = tex_ref.split(":", 1)
    tex_file = RESOURCE_ROOT / "assets" / ns / "textures" / f"{rel_path}.png"
    record(f"Texture resolves: {ident}", tex_file.is_file(), str(tex_file))

# 3. Check iron_sword.json CMD Overrides
iron_sword = json.loads(IRON_SWORD_PATH.read_text(encoding="utf-8"))
overrides = {ov.get("predicate", {}).get("custom_model_data"): ov.get("model") for ov in iron_sword.get("overrides", [])}
for cmd, expected_model in [
    (2001, "avatar_elements:item/dual_swords"),
    (2002, "avatar_elements:item/earth_hammer"),
    (2003, "avatar_elements:item/war_fan"),
    (2004, "avatar_elements:item/water_spear")
]:
    record(f"CMD {cmd} override", overrides.get(cmd) == expected_model, f"{overrides.get(cmd)} == {expected_model}")

# 4. Check Language entries
en_data = json.loads(EN_LANG.read_text(encoding="utf-8"))
id_data = json.loads(ID_LANG.read_text(encoding="utf-8"))
for ident in ["dual_swords", "earth_hammer", "war_fan", "water_spear"]:
    key = f"item.avatar_elements.{ident}"
    record(f"Lang en_us: {ident}", key in en_data, en_data.get(key))
    record(f"Lang id_id: {ident}", key in id_data, id_data.get(key))

failed = 0
print("=======================================================")
print(" RUNNING WEAPON RUNTIME INTEGRATION VALIDATION")
print("=======================================================")
for name, passed, detail in checks:
    state = "PASS" if passed else "FAIL"
    print(f"[{state}] {name}: {detail}")
    if not passed:
        failed += 1

print(f"\n{len(checks) - failed}/{len(checks)} checks passed.")
sys.exit(1 if failed else 0)
