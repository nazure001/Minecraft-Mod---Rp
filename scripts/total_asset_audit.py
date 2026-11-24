import os
import json
import struct
from PIL import Image

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"

results = {
    "scanned_files": 0,
    "json_errors": [],
    "zero_byte_files": [],
    "png_errors": [],
    "missing_textures": [],
    "illegal_rotations": [],
    "out_of_bounds_elements": [],
    "uv_errors": [],
    "bbmodel_errors": [],
    "cmd_conflicts": [],
    "missing_model_references": [],
    "mcmeta_issues": [],
    "sounds_issues": []
}

VALID_ANGLES = {-45.0, -22.5, 0.0, 22.5, 45.0}

IGNORE_DIRS = {".git", "reference", ".claude", ".gradle", "build", "bin", ".idea", "__pycache__"}

def audit_repo():
    print(f"Starting total asset audit on: {REPO_ROOT}")
    
    # First pass: collect all textures and verify file readability
    for root, dirs, files in os.walk(REPO_ROOT):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
        for f in files:
            results["scanned_files"] += 1
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
            except Exception as e:
                continue
            
            if size == 0:
                results["zero_byte_files"].append(path)
                continue
                
            # Verify PNGs
            if f.lower().endswith(".png"):
                try:
                    with Image.open(path) as img:
                        img.verify()
                except Exception as e:
                    results["png_errors"].append((path, str(e)))
                    
            # Verify JSONs
            if f.lower().endswith(".json") or f.lower().endswith(".mcmeta"):
                try:
                    with open(path, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                except Exception as e:
                    results["json_errors"].append((path, str(e)))

    print(f"Pass 1 complete. Scanned {results['scanned_files']} files.")
    print(f"Zero-byte files: {len(results['zero_byte_files'])}")
    print(f"JSON syntax errors: {len(results['json_errors'])}")
    print(f"PNG corruptions: {len(results['png_errors'])}")

    # Second pass: Model and Texture references, BBModels, Sounds, Pack.mcmeta
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for f in files:
            path = os.path.join(root, f)
            lower_f = f.lower()

            # Audit pack.mcmeta
            if lower_f == "pack.mcmeta":
                try:
                    with open(path, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                    pack_info = data.get("pack", {})
                    fmt = pack_info.get("pack_format")
                    # Check folder path to determine if datapack (48) or resourcepack (34)
                    is_datapack = "datapack" in root.lower() or "data" in root.lower()
                    is_resourcepack = "resourcepack" in root.lower() or "asset" in root.lower()
                    if is_datapack and fmt != 48:
                        results["mcmeta_issues"].append((path, f"Datapack pack_format is {fmt}, expected 48 for 1.21.1"))
                    elif is_resourcepack and fmt != 34:
                        results["mcmeta_issues"].append((path, f"Resourcepack pack_format is {fmt}, expected 34 for 1.21.1"))
                except Exception as e:
                    pass

            # Audit .bbmodel files
            if lower_f.endswith(".bbmodel"):
                try:
                    with open(path, "r", encoding="utf-8") as bf:
                        bb = json.load(bf)
                    elements = bb.get("elements", [])
                    outliner = bb.get("outliner", [])
                    uuids = set()
                    for el in elements:
                        u = el.get("uuid")
                        if not u:
                            results["bbmodel_errors"].append((path, f"Element '{el.get('name')}' missing UUID"))
                        elif u in uuids:
                            results["bbmodel_errors"].append((path, f"Duplicate UUID '{u}'"))
                        else:
                            uuids.add(u)
                except Exception as e:
                    results["bbmodel_errors"].append((path, str(e)))

            # Audit Java JSON Models
            if lower_f.endswith(".json") and ("models" in root.lower() or "elements" in root.lower()):
                try:
                    with open(path, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                    if isinstance(data, dict):
                        # Elements check
                        if "elements" in data:
                            for idx, el in enumerate(data["elements"]):
                                el_name = el.get("name", f"elem_{idx}")
                                # Check bounds [-16, 32]
                                f_pos = el.get("from", [])
                                t_pos = el.get("to", [])
                                if len(f_pos) == 3 and len(t_pos) == 3:
                                    for c in f_pos + t_pos:
                                        if c < -16.0 or c > 32.0:
                                            results["out_of_bounds_elements"].append((path, el_name, f_pos, t_pos))
                                            break
                                # Check rotations
                                if "rotation" in el:
                                    rot = el["rotation"]
                                    angle = float(rot.get("angle", 0))
                                    if angle not in VALID_ANGLES:
                                        results["illegal_rotations"].append((path, el_name, angle))
                                # Check UVs
                                faces = el.get("faces", {})
                                for fname, fdata in faces.items():
                                    uv = fdata.get("uv", [])
                                    if len(uv) == 4:
                                        # UV in Java models is usually [0, 16]
                                        if any(c < -16.0 or c > 32.0 for c in uv):
                                            results["uv_errors"].append((path, el_name, fname, uv))
                        
                        # Overrides check in item root models
                        if "overrides" in data:
                            cmd_seen = {}
                            for ov in data["overrides"]:
                                predicate = ov.get("predicate", {})
                                cmd = predicate.get("custom_model_data")
                                model_ref = ov.get("model", "")
                                if cmd is not None:
                                    if cmd in cmd_seen:
                                        results["cmd_conflicts"].append((path, cmd, model_ref, cmd_seen[cmd]))
                                    else:
                                        cmd_seen[cmd] = model_ref
                                        
                                # Check if target model exists
                                if ":" in model_ref:
                                    ns, mpath = model_ref.split(":", 1)
                                    # Search in asset roots
                                    candidate1 = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", ns, "models", mpath + ".json")
                                    candidate2 = os.path.join(REPO_ROOT, "avatar-skill-resourcepack", "assets", ns, "models", mpath + ".json")
                                    candidate3 = os.path.join(REPO_ROOT, "avatar-armor-resourcepack", "assets", ns, "models", mpath + ".json")
                                    candidate4 = os.path.join(REPO_ROOT, "Avatar_Elements_Production_Bundle_v3", "assets", ns, "models", mpath + ".json")
                                    candidate5 = os.path.join(REPO_ROOT, "art-source", "asset_pack", "assets", ns, "models", mpath + ".json")
                                    if not any(os.path.exists(c) for c in [candidate1, candidate2, candidate3, candidate4, candidate5]):
                                        results["missing_model_references"].append((path, model_ref))

                        # Texture existence check
                        if "textures" in data and isinstance(data["textures"], dict):
                            for tkey, tval in data["textures"].items():
                                if isinstance(tval, str) and not tval.startswith("#"):
                                    if ":" in tval:
                                        ns, tpath = tval.split(":", 1)
                                        if ns == "minecraft":
                                            continue
                                        c1 = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", ns, "textures", tpath + ".png")
                                        c2 = os.path.join(REPO_ROOT, "avatar-skill-resourcepack", "assets", ns, "textures", tpath + ".png")
                                        c3 = os.path.join(REPO_ROOT, "avatar-armor-resourcepack", "assets", ns, "textures", tpath + ".png")
                                        c4 = os.path.join(REPO_ROOT, "Avatar_Elements_Production_Bundle_v3", "assets", ns, "textures", tpath + ".png")
                                        c5 = os.path.join(REPO_ROOT, "art-source", "asset_pack", "assets", ns, "textures", tpath + ".png")
                                        if not any(os.path.exists(c) for c in [c1, c2, c3, c4, c5]):
                                            results["missing_textures"].append((path, tval))
                except Exception as e:
                    pass

    # Audit sounds.json
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        if "sounds.json" in files:
            spath = os.path.join(root, "sounds.json")
            try:
                with open(spath, "r", encoding="utf-8") as sf:
                    sdata = json.load(sf)
                # Check sound file existence
                # Sounds are located relative to assets/<namespace>/sounds/
                base_sounds_dir = os.path.join(os.path.dirname(spath), "sounds")
                for event_name, event_data in sdata.items():
                    for snd in event_data.get("sounds", []):
                        # Skip delegated sound events (type == 'event')
                        if isinstance(snd, dict) and snd.get("type") == "event":
                            continue
                        sname = snd if isinstance(snd, str) else snd.get("name", "")
                        if ":" in sname:
                            _, subname = sname.split(":", 1)
                        else:
                            subname = sname
                        ogg_path = os.path.join(base_sounds_dir, subname + ".ogg")
                        if not os.path.exists(ogg_path):
                            results["sounds_issues"].append((spath, event_name, sname, ogg_path))
            except Exception as e:
                results["sounds_issues"].append((spath, "JSON_SYNTAX_ERROR", str(e), ""))

    # Output detailed report
    report_json_path = os.path.join(REPO_ROOT, "scripts", "audit_report.json")
    with open(report_json_path, "w", encoding="utf-8") as rf:
        json.dump(results, rf, indent=2)
    print(f"\n[INFO] Full audit report saved to: {report_json_path}")

    print("\n" + "="*80)
    print("TOTAL ASSET AUDIT REPORT")
    print("="*80)
    
    print(f"\n1. ZERO-BYTE FILES ({len(results['zero_byte_files'])}):")
    for f in results['zero_byte_files']:
        print(f"  - {f}")
        
    print(f"\n2. JSON SYNTAX ERRORS ({len(results['json_errors'])}):")
    for p, err in results['json_errors']:
        print(f"  - {p}: {err}")
        
    print(f"\n3. CORRUPT / UNREADABLE PNGs ({len(results['png_errors'])}):")
    for p, err in results['png_errors']:
        print(f"  - {p}: {err}")
        
    print(f"\n4. PACK.MCMETA FORMAT ISSUES ({len(results['mcmeta_issues'])}):")
    for p, issue in results['mcmeta_issues']:
        print(f"  - {p}: {issue}")
        
    print(f"\n5. BLOCKBENCH MODEL ISSUES ({len(results['bbmodel_errors'])}):")
    for p, err in results['bbmodel_errors']:
        print(f"  - {p}: {err}")
        
    print(f"\n6. ILLEGAL ROTATION ANGLES ({len(results['illegal_rotations'])}):")
    for p, el, ang in results['illegal_rotations']:
        print(f"  - {p} [{el}]: angle={ang}")
        
    print(f"\n7. OUT OF BOUNDS ELEMENTS [-16, 32] ({len(results['out_of_bounds_elements'])}):")
    for p, el, f_pos, t_pos in results['out_of_bounds_elements']:
        print(f"  - {p} [{el}]: from={f_pos}, to={t_pos}")
        
    print(f"\n8. CUSTOM MODEL DATA (CMD) CONFLICTS ({len(results['cmd_conflicts'])}):")
    for p, cmd, m1, m2 in results['cmd_conflicts']:
        print(f"  - {p} CMD {cmd}: {m1} vs {m2}")
        
    print(f"\n9. MISSING MODEL REFERENCES ({len(results['missing_model_references'])}):")
    for p, mref in results['missing_model_references']:
        print(f"  - {p}: missing model '{mref}'")
        
    print(f"\n10. MISSING TEXTURES ({len(results['missing_textures'])}):")
    for p, tex in results['missing_textures']:
        print(f"  - {p}: missing texture '{tex}'")
        
    print(f"\n11. SOUNDS.JSON ISSUES ({len(results['sounds_issues'])}):")
    for spath, ev, snd, expected in results['sounds_issues']:
        print(f"  - {spath} [{ev}] sound '{snd}' -> missing: {expected}")
        
    print("\n" + "="*80)
    print("AUDIT COMPLETE")
    print("="*80)

if __name__ == "__main__":
    audit_repo()
