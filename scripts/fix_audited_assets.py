import os
import json
import uuid
import shutil
from PIL import Image, ImageDraw

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"

def fix_all():
    print("="*70)
    print("EXECUTING ASSET REMEDIATION & CORRECTION")
    print("="*70)

    # -------------------------------------------------------------
    # 1. FIX P0 CRITICAL: Corrupt icon.png (IDAT checksum error)
    # -------------------------------------------------------------
    print("\n[1] Fixing P0: Regenerating valid icon.png...")
    icon_paths = [
        os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "icon.png"),
        os.path.join(REPO_ROOT, "avatar-verify", "mod", "src", "main", "resources", "assets", "avatar_elements", "icon.png"),
    ]
    
    # Create a beautiful 128x128 RGBA icon for Avatar: Elements
    size = (128, 128)
    img = Image.new("RGBA", size, (18, 22, 28, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer circular boundary
    draw.ellipse([4, 4, 124, 124], outline=(212, 175, 55, 255), width=3)
    draw.ellipse([8, 8, 120, 120], outline=(40, 48, 60, 255), width=2)
    
    # 4 Elemental Quadrants / Orbs
    # Top: Air (#A8DADC)
    draw.ellipse([52, 16, 76, 40], fill=(168, 218, 220, 255), outline=(241, 250, 238, 255), width=2)
    # Right: Fire (#E63946)
    draw.ellipse([88, 52, 112, 76], fill=(230, 57, 70, 255), outline=(255, 183, 3, 255), width=2)
    # Bottom: Earth (#2A9D8F)
    draw.ellipse([52, 88, 76, 112], fill=(42, 157, 143, 255), outline=(88, 129, 87, 255), width=2)
    # Left: Water (#1D3557)
    draw.ellipse([16, 52, 40, 76], fill=(29, 53, 87, 255), outline=(69, 123, 157, 255), width=2)
    
    # Center White Lotus Core
    draw.ellipse([48, 48, 80, 80], fill=(245, 245, 240, 255), outline=(212, 175, 55, 255), width=2)
    draw.ellipse([56, 56, 72, 72], fill=(212, 175, 55, 255))
    
    for p in icon_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, format="PNG", optimize=True)
        print(f"  -> Generated valid icon.png at: {p} ({os.path.getsize(p)} bytes)")
        # Verify immediately with PIL
        with Image.open(p) as check_img:
            check_img.verify()
        print(f"  -> Verified PNG checksum OK.")

    # -------------------------------------------------------------
    # 2. FIX P1 HIGH: sounds.json event references
    # -------------------------------------------------------------
    print("\n[2] Fixing P1: sounds.json event delegation...")
    sounds_path = os.path.join(REPO_ROOT, "mod", "src", "client", "resources", "assets", "avatar_elements", "sounds.json")
    if os.path.exists(sounds_path):
        with open(sounds_path, "r", encoding="utf-8") as f:
            sdata = json.load(f)
            
        fixed_count = 0
        events_to_fix = ["combat.martial_punch", "combat.martial_kick", "combat.martial_dive", "combat.hitstop_impact"]
        for ev in events_to_fix:
            if ev in sdata:
                for snd in sdata[ev].get("sounds", []):
                    if isinstance(snd, dict) and "name" in snd:
                        if snd["name"].startswith("minecraft:") and "type" not in snd:
                            snd["type"] = "event"
                            fixed_count += 1
                            
        with open(sounds_path, "w", encoding="utf-8") as f:
            json.dump(sdata, f, indent=2)
        print(f"  -> Corrected {fixed_count} vanilla sound event references in {sounds_path}")

    # -------------------------------------------------------------
    # 3. FIX P1 HIGH: Construct item model texture paths
    # -------------------------------------------------------------
    print("\n[3] Fixing P1: Construct item models texture paths...")
    construct_models = [
        (os.path.join(REPO_ROOT, "mod", "src", "client", "resources", "assets", "avatar_elements", "models", "item", "earth_boulder_construct.json"), "avatar_elements:vfx/construct_material_stone"),
        (os.path.join(REPO_ROOT, "mod", "src", "client", "resources", "assets", "avatar_elements", "models", "item", "lava_crucible_container.json"), "avatar_elements:vfx/construct_material_lava"),
        (os.path.join(REPO_ROOT, "mod", "src", "client", "resources", "assets", "avatar_elements", "models", "item", "water_skin_container.json"), "avatar_elements:vfx/construct_material_water")
    ]
    for mpath, correct_tex in construct_models:
        if os.path.exists(mpath):
            with open(mpath, "r", encoding="utf-8") as f:
                mdata = json.load(f)
            mdata["textures"]["layer0"] = correct_tex
            with open(mpath, "w", encoding="utf-8") as f:
                json.dump(mdata, f, indent=2)
            print(f"  -> Fixed {os.path.basename(mpath)}: layer0 = '{correct_tex}'")

    # -------------------------------------------------------------
    # 4. FIX P1 HIGH: Quarantine broken prototype models in art-source/asset_pack
    # -------------------------------------------------------------
    print("\n[4] Fixing P1: Quarantining broken prototype models in art-source/asset_pack...")
    quarantine_dir = os.path.join(REPO_ROOT, "art-source", "archive", "quarantine_broken_prototypes")
    os.makedirs(quarantine_dir, exist_ok=True)
    
    broken_models = [
        "air_vortex_funnel.json", "boulder_launch_megalith.json",
        "captured_earth_shards.json", "charge_orb_elemental.json",
        "earth_armor_overlay.json", "water_whip_stream.json",
        "SM_Dual_Swords.json", "SM_Earth_Hammer.json",
        "SM_War_Fan.json", "SM_Water_Spear.json"
    ]
    
    # Sources of broken files
    art_models_dir = os.path.join(REPO_ROOT, "art-source", "asset_pack", "models")
    art_item_models_dir = os.path.join(REPO_ROOT, "art-source", "asset_pack", "assets", "avatar_elements", "models", "item")
    
    # Canonical sources to synchronize from (properly formatted Java models)
    vfx_canonical_dir = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "models", "vfx")
    weapons_canonical_dir = os.path.join(REPO_ROOT, "Avatar_Elements_Production_Bundle_v3", "assets", "avatar_elements", "models", "item")
    
    for bm in broken_models:
        # Check in art_models_dir
        p1 = os.path.join(art_models_dir, bm)
        if os.path.exists(p1):
            shutil.copy2(p1, os.path.join(quarantine_dir, bm + ".bak"))
            # If canonical exists in vfx_canonical_dir, copy canonical
            cand = os.path.join(vfx_canonical_dir, bm)
            if os.path.exists(cand):
                shutil.copy2(cand, p1)
                print(f"  -> Replaced {bm} in asset_pack/models with canonical version from mod/vfx")
            else:
                # Weapon candidate
                w_cand = os.path.join(weapons_canonical_dir, bm.lower().replace("sm_", ""))
                if not os.path.exists(w_cand):
                    w_cand = os.path.join(weapons_canonical_dir, bm)
                if os.path.exists(w_cand):
                    shutil.copy2(w_cand, p1)
                    print(f"  -> Replaced {bm} in asset_pack/models with canonical weapon model")
                else:
                    # Fix texture prefix in place: remove 'textures/' from avatar_elements:textures/
                    with open(p1, "r", encoding="utf-8") as f:
                        text = f.read()
                    fixed_text = text.replace("avatar_elements:textures/vfx/", "avatar_elements:vfx/")
                    fixed_text = fixed_text.replace("avatar_elements:textures/weapons/", "avatar_elements:weapons/")
                    with open(p1, "w", encoding="utf-8") as f:
                        f.write(fixed_text)
                    print(f"  -> Fixed texture namespaces in {bm}")

        # Check in art_item_models_dir
        p2 = os.path.join(art_item_models_dir, bm)
        if os.path.exists(p2):
            shutil.copy2(p2, os.path.join(quarantine_dir, "item_" + bm + ".bak"))
            # Sync with canonical
            cand = os.path.join(vfx_canonical_dir, bm)
            if os.path.exists(cand):
                shutil.copy2(cand, p2)
                print(f"  -> Replaced {bm} in asset_pack/.../models/item with canonical version")
            else:
                with open(p2, "r", encoding="utf-8") as f:
                    text = f.read()
                fixed_text = text.replace("avatar_elements:textures/vfx/", "avatar_elements:vfx/")
                fixed_text = fixed_text.replace("avatar_elements:textures/weapons/", "avatar_elements:weapons/")
                with open(p2, "w", encoding="utf-8") as f:
                    f.write(fixed_text)
                print(f"  -> Fixed texture namespaces in item/{bm}")

    # -------------------------------------------------------------
    # 5. FIX P2 MEDIUM: Blockbench model UUIDs in animation_studies
    # -------------------------------------------------------------
    print("\n[5] Fixing P2: Injecting missing UUIDs into Blockbench study models...")
    bb_files = [
        os.path.join(REPO_ROOT, "art-source", "animation_studies", "staff_thrust", "player_staff_thrust_rigged.bbmodel"),
        os.path.join(REPO_ROOT, "art-source", "animation_studies", "staff_thrust", "player_staff_thrust_study.bbmodel")
    ]
    for bbp in bb_files:
        if os.path.exists(bbp):
            with open(bbp, "r", encoding="utf-8") as f:
                bbdata = json.load(f)
            elements = bbdata.get("elements", [])
            outliner = bbdata.get("outliner", [])
            modified = False
            for el in elements:
                if "uuid" not in el:
                    el["uuid"] = str(uuid.uuid4())
                    modified = True
            if modified:
                # Update outliner with element uuids if outliner is list of string ids or empty
                if isinstance(outliner, list):
                    elem_uuids = [el["uuid"] for el in elements]
                    bbdata["outliner"] = elem_uuids
                with open(bbp, "w", encoding="utf-8") as f:
                    json.dump(bbdata, f, indent=2)
                print(f"  -> Injected UUIDs into: {os.path.basename(bbp)}")

    # -------------------------------------------------------------
    # 6. FIX P2 MEDIUM: Clean / Quarantine zero-byte junk files
    # -------------------------------------------------------------
    print("\n[6] Fixing P2: Cleaning zero-byte junk files...")
    zero_bytes = [
        os.path.join(REPO_ROOT, "avatar-verify", "mod", "run", "downloads", "log.json"),
        os.path.join(REPO_ROOT, "mod", "run", "downloads", "log.json"),
        os.path.join(REPO_ROOT, "mod", "tools", "raw_captions.txt"),
        os.path.join(REPO_ROOT, "mod", "tools", "yt_transcript.txt"),
        os.path.join(REPO_ROOT, "mod", "tools", "yt_transcript_9FxjDpXvtuo.txt")
    ]
    for zb in zero_bytes:
        if os.path.exists(zb) and os.path.getsize(zb) == 0:
            try:
                os.remove(zb)
                print(f"  -> Removed zero-byte file: {os.path.basename(zb)}")
            except Exception as e:
                print(f"  -> Could not remove {zb}: {e}")

    print("\n" + "="*70)
    print("ALL REMEDIATIONS APPLIED")
    print("="*70)

if __name__ == "__main__":
    fix_all()
