import os
import json
import uuid
import shutil

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"

def finalize_fixes():
    print("="*70)
    print("FINALIZING ASSET CORRECTIONS & BLOCKBENCH UUID INJECTIONS")
    print("="*70)

    # 1. Fix remaining texture paths in art-source/asset_pack
    art_item_dir = os.path.join(REPO_ROOT, "art-source", "asset_pack", "assets", "avatar_elements", "models", "item")
    if os.path.exists(art_item_dir):
        # Fix construct models
        for mname, tex in [
            ("earth_boulder_construct.json", "avatar_elements:vfx/construct_material_stone"),
            ("lava_crucible_container.json", "avatar_elements:vfx/construct_material_lava"),
            ("water_skin_container.json", "avatar_elements:vfx/construct_material_water")
        ]:
            p = os.path.join(art_item_dir, mname)
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                d["textures"]["layer0"] = tex
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(d, f, indent=2)
                print(f"  -> Fixed texture in {mname}")

        # Fix weapon models texture prefix (remove textures/)
        for f in os.listdir(art_item_dir):
            if f.endswith(".json"):
                p = os.path.join(art_item_dir, f)
                with open(p, "r", encoding="utf-8") as jf:
                    text = jf.read()
                if "avatar_elements:textures/weapons/" in text:
                    text = text.replace("avatar_elements:textures/weapons/", "avatar_elements:weapons/")
                    with open(p, "w", encoding="utf-8") as jf:
                        jf.write(text)
                    print(f"  -> Fixed weapon texture prefix in {f}")

    # 2. Fix old prototype air_staff.json texture reference
    old_air_staff = os.path.join(REPO_ROOT, "art-source", "models", "air_staff", "air_staff.json")
    if os.path.exists(old_air_staff):
        canonical_v02 = os.path.join(REPO_ROOT, "art-source", "models", "air_staff", "v0.2", "air_staff.json")
        if os.path.exists(canonical_v02):
            shutil.copy2(canonical_v02, old_air_staff)
            print("  -> Updated art-source/models/air_staff/air_staff.json to canonical v0.2")

    # 3. Inject UUIDs into all .bbmodel files across art-source
    fixed_bb_count = 0
    for root, dirs, files in os.walk(os.path.join(REPO_ROOT, "art-source")):
        for f in files:
            if f.endswith(".bbmodel"):
                bbpath = os.path.join(root, f)
                try:
                    with open(bbpath, "r", encoding="utf-8") as bf:
                        bbdata = json.load(bf)
                    elements = bbdata.get("elements", [])
                    outliner = bbdata.get("outliner", [])
                    modified = False
                    for el in elements:
                        if isinstance(el, dict) and "uuid" not in el:
                            el["uuid"] = str(uuid.uuid4())
                            modified = True
                    if modified:
                        if isinstance(outliner, list):
                            elem_uuids = [el["uuid"] for el in elements if isinstance(el, dict) and "uuid" in el]
                            bbdata["outliner"] = elem_uuids
                        with open(bbpath, "w", encoding="utf-8") as bf:
                            json.dump(bbdata, bf, indent=2)
                        fixed_bb_count += 1
                except Exception as e:
                    pass
    print(f"  -> Injected UUIDs into {fixed_bb_count} .bbmodel files across art-source")

    # 4. Clean zero-byte empty .mca files in test worlds
    run_dir = os.path.join(REPO_ROOT, "mod", "run")
    cleaned_mca = 0
    if os.path.exists(run_dir):
        for root, dirs, files in os.walk(run_dir):
            for f in files:
                if f.endswith(".mca"):
                    p = os.path.join(root, f)
                    if os.path.getsize(p) == 0:
                        try:
                            os.remove(p)
                            cleaned_mca += 1
                        except:
                            pass
    print(f"  -> Cleaned {cleaned_mca} zero-byte .mca files from test runs")

    # 5. Update total_asset_audit.py to recognize type == 'event'
    audit_script = os.path.join(REPO_ROOT, "scripts", "total_asset_audit.py")
    with open(audit_script, "r", encoding="utf-8") as af:
        asource = af.read()
    
    # Update sound verification logic
    old_sound_check = """                for event_name, event_data in sdata.items():
                    for snd in event_data.get("sounds", []):
                        sname = snd if isinstance(snd, str) else snd.get("name", "")
                        if ":" in sname:
                            _, subname = sname.split(":", 1)
                        else:
                            subname = sname
                        ogg_path = os.path.join(base_sounds_dir, subname + ".ogg")
                        if not os.path.exists(ogg_path):
                            results["sounds_issues"].append((spath, event_name, sname, ogg_path))"""
                            
    new_sound_check = """                for event_name, event_data in sdata.items():
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
                            results["sounds_issues"].append((spath, event_name, sname, ogg_path))"""

    if old_sound_check in asource:
        asource = asource.replace(old_sound_check, new_sound_check)
        with open(audit_script, "w", encoding="utf-8") as af:
            af.write(asource)
        print("  -> Updated total_asset_audit.py to recognize sound event delegation")

    print("\n" + "="*70)
    print("FINALIZATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    finalize_fixes()
