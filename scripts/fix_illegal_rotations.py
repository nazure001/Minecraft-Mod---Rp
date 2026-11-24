import os
import json
import uuid

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
VALID_ANGLES = {-45.0, -22.5, 0.0, 22.5, 45.0}

def snap_to_valid_angle(angle):
    # Find nearest valid Minecraft angle
    return min(VALID_ANGLES, key=lambda x: abs(x - angle))

def fix_rotations_and_uuids():
    print("="*70)
    print("SNAPPING ILLEGAL ROTATION ANGLES & INJECTING REMAINING UUIDS")
    print("="*70)

    # 1. Snap illegal rotation angles in all JSON models
    fixed_rot_files = 0
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip git, reference, etc.
        if any(ig in root for ig in [".git", "reference", ".claude", ".gradle", "build", "bin"]):
            continue
            
        for f in files:
            if f.endswith(".json"):
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                    if isinstance(data, dict) and "elements" in data:
                        modified = False
                        for el in data["elements"]:
                            if "rotation" in el and isinstance(el["rotation"], dict):
                                rot = el["rotation"]
                                ang = float(rot.get("angle", 0))
                                if ang not in VALID_ANGLES:
                                    snapped = snap_to_valid_angle(ang)
                                    rot["angle"] = snapped
                                    modified = True
                        if modified:
                            with open(p, "w", encoding="utf-8") as jf:
                                json.dump(data, jf, indent=2)
                            fixed_rot_files += 1
                            print(f"  -> Snapped rotation angles in: {os.path.relpath(p, REPO_ROOT)}")
                except Exception as e:
                    pass

    print(f"\nFixed illegal rotation angles in {fixed_rot_files} JSON files.")

    # 2. Inject UUIDs into avatar-verify bbmodels
    fixed_bb_count = 0
    verify_dir = os.path.join(REPO_ROOT, "avatar-verify")
    if os.path.exists(verify_dir):
        for root, dirs, files in os.walk(verify_dir):
            for f in files:
                if f.endswith(".bbmodel"):
                    bbp = os.path.join(root, f)
                    try:
                        with open(bbp, "r", encoding="utf-8") as bf:
                            bb = json.load(bf)
                        elements = bb.get("elements", [])
                        outliner = bb.get("outliner", [])
                        modified = False
                        for el in elements:
                            if isinstance(el, dict) and "uuid" not in el:
                                el["uuid"] = str(uuid.uuid4())
                                modified = True
                        if modified:
                            if isinstance(outliner, list):
                                elem_uuids = [el["uuid"] for el in elements if isinstance(el, dict) and "uuid" in el]
                                bb["outliner"] = elem_uuids
                            with open(bbp, "w", encoding="utf-8") as bf:
                                json.dump(bb, bf, indent=2)
                            fixed_bb_count += 1
                            print(f"  -> Injected UUIDs into verify model: {os.path.relpath(bbp, REPO_ROOT)}")
                    except Exception as e:
                        pass
    print(f"Fixed UUIDs in {fixed_bb_count} bbmodels in avatar-verify.")

    print("\n" + "="*70)
    print("ROTATION & UUID REMEDIATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    fix_rotations_and_uuids()
