#!/usr/bin/env python3
"""Read-only release gate for the Earth Pillar asset/runtime contract."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "art-source" / "asset_pack"
RESOURCE_ROOT = ROOT / "mod" / "src" / "main" / "resources"
MODEL_PATH = (
    RESOURCE_ROOT
    / "assets"
    / "avatar_elements"
    / "models"
    / "vfx"
    / "earth_pillar.json"
)
BBMODEL_PATH = ASSET_ROOT / "models" / "bbmodel" / "earth_pillar.bbmodel"
GEO_PATH = ASSET_ROOT / "models" / "earth_pillar.geo.json"
ANIMATION_PATH = ASSET_ROOT / "animations" / "earth_pillar.animation.json"
SKILL_PATH = (
    ROOT
    / "mod"
    / "src"
    / "main"
    / "java"
    / "com"
    / "avatarmod"
    / "elements"
    / "skill"
    / "impl"
    / "EarthPillarSkill.java"
)
CLIENT_VFX_ROOT = (
    ROOT
    / "mod"
    / "src"
    / "client"
    / "java"
    / "com"
    / "avatarmod"
    / "elements"
    / "client"
    / "vfx"
)
CONTROLLER_PATH = CLIENT_VFX_ROOT / "CinematicVfxController.java"
VFX_TYPE_PATH = CLIENT_VFX_ROOT / "VfxType.java"
TRANSFORM_UTIL_PATH = CLIENT_VFX_ROOT / "VfxTransformUtil.java"
DEEPSLATE_MODEL_PATH = (
    RESOURCE_ROOT / "assets" / "minecraft" / "models" / "item" / "deepslate.json"
)

checks = []


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record(name, passed, detail):
    checks.append((name, passed, detail))


model = load_json(MODEL_PATH)
elements = model.get("elements", [])
out_of_range = []
for element in elements:
    for key in ("from", "to"):
        coords = element[key]
        if any(value < -16 or value > 32 for value in coords):
            out_of_range.append((element.get("name"), key, coords))
record(
    "Minecraft Java model bounds [-16, 32]",
    not out_of_range,
    f"{len(elements)} elements; out-of-range: {out_of_range}",
)

texture_id = model["textures"]["pillar"]
namespace, texture_path = texture_id.split(":", 1)
texture_file = RESOURCE_ROOT / "assets" / namespace / "textures" / f"{texture_path}.png"
record("Runtime texture resolves", texture_file.is_file(), str(texture_file))

deepslate_model = load_json(DEEPSLATE_MODEL_PATH)
dispatch = [
    override
    for override in deepslate_model.get("overrides", [])
    if override.get("predicate", {}).get("custom_model_data") == 1005
]
dispatch_ok = len(dispatch) == 1 and dispatch[0].get("model") == "avatar_elements:vfx/earth_pillar"
record("Deepslate CustomModelData 1005 dispatch", dispatch_ok, str(dispatch))

bbmodel = load_json(BBMODEL_PATH)


def group_names(nodes):
    names = set()
    for node in nodes:
        if isinstance(node, dict):
            if node.get("name"):
                names.add(node["name"])
            names.update(group_names(node.get("children", [])))
    return names


groups = group_names(bbmodel.get("outliner", []))
missing_bb_bones = []
for animation in bbmodel.get("animations", []):
    for key, animator in animation.get("animators", {}).items():
        if animator.get("type") == "bone":
            bone_name = animator.get("name", key)
            if bone_name not in groups:
                missing_bb_bones.append((animation.get("name"), bone_name))
record(
    "Blockbench animation bones exist in outliner",
    not missing_bb_bones,
    f"groups={sorted(groups)}; missing={missing_bb_bones}",
)

geometry = load_json(GEO_PATH)["minecraft:geometry"][0]
geo_bones = {bone["name"] for bone in geometry.get("bones", [])}
animation = load_json(ANIMATION_PATH)
missing_geo_bones = []
for clip_name, clip in animation.get("animations", {}).items():
    for bone_name in clip.get("bones", {}):
        if bone_name not in geo_bones:
            missing_geo_bones.append((clip_name, bone_name))
record(
    "Bedrock animation bones exist in geometry",
    not missing_geo_bones,
    f"geometry bones={sorted(geo_bones)}; missing={missing_geo_bones}",
)

boxes = [
    cube
    for bone in geometry.get("bones", [])
    for cube in bone.get("cubes", [])
]
top_y = max(cube["origin"][1] + cube["size"][1] for cube in boxes) / 16
skill_source = SKILL_PATH.read_text(encoding="utf-8")
height_match = re.search(r"PILLAR_HEIGHT\s*=\s*([0-9.]+)f", skill_source)
if height_match is None:
    raise ValueError(f"Could not find PILLAR_HEIGHT in {SKILL_PATH}")
runtime_height = float(height_match.group(1))
height_ok = abs(top_y - runtime_height) <= 1 / 16
record(
    "Bedrock asset height matches runtime PILLAR_HEIGHT",
    height_ok,
    f"asset={top_y:.5f} blocks; runtime={runtime_height:.5f} blocks",
)

java_top_y = max(element["to"][1] for element in elements) / 16
controller_source = CONTROLLER_PATH.read_text(encoding="utf-8")
vfx_type_source = VFX_TYPE_PATH.read_text(encoding="utf-8")
transform_source = TRANSFORM_UTIL_PATH.read_text(encoding="utf-8")
base_scale_match = re.search(
    r"EARTH_PILLAR\s*\(.*?new Vector3f\(\s*([0-9.]+)f\s*,",
    vfx_type_source,
    re.DOTALL,
)
y_scale_match = re.search(
    r"createPillarTransform\(\s*type\.baseScale\(\)\.x\(\)\s*,\s*"
    r"type\.baseScale\(\)\.x\(\)\s*\*\s*([0-9.]+)f\s*\)",
    controller_source,
)
helper_match = re.search(
    r"createPillarTransform\(float xzScale, float yScale\)\s*\{\s*"
    r"return new AffineTransformation\(\s*"
    r"new Vector3f\(0\.0f,\s*0\.0f,\s*0\.0f\),\s*"
    r"new Quaternionf\(\),\s*"
    r"new Vector3f\(xzScale,\s*yScale,\s*xzScale\)",
    transform_source,
    re.DOTALL,
)
transform_details_available = (
    base_scale_match is not None
    and y_scale_match is not None
    and helper_match is not None
)
if transform_details_available:
    base_scale = float(base_scale_match.group(1))
    y_scale_multiplier = float(y_scale_match.group(1))
    runtime_java_top_y = java_top_y * base_scale * y_scale_multiplier
    java_height_ok = abs(runtime_java_top_y - runtime_height) <= 1 / 16
    transform_detail = (
        f"model={java_top_y:.5f} blocks; base scale={base_scale:.3f}; "
        f"Y multiplier={y_scale_multiplier:.3f}; transformed={runtime_java_top_y:.5f}; "
        f"runtime={runtime_height:.5f} blocks"
    )
else:
    java_height_ok = False
    transform_detail = (
        "could not verify Earth Pillar base scale, controller multiplier, "
        "and zero-offset Y transform"
    )
record(
    "Runtime Java model top matches PILLAR_HEIGHT after VFX transform",
    java_height_ok,
    transform_detail,
)

failed = 0
for name, passed, detail in checks:
    state = "PASS" if passed else "FAIL"
    print(f"[{state}] {name}: {detail}")
    if not passed:
        failed += 1

print(f"\n{len(checks) - failed}/{len(checks)} checks passed.")
sys.exit(1 if failed else 0)
