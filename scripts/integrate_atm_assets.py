import os
import json
import shutil
from PIL import Image

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
REF_BISON_GEO = os.path.join(REPO_ROOT, "reference", "avatar-legend-reforged-1.3.0", "assets", "av3", "geo", "entity", "skybison.geo.json")
REF_BISON_ANIM = os.path.join(REPO_ROOT, "reference", "avatar-legend-reforged-1.3.0", "assets", "av3", "animations", "entity", "skybison.animation.json")
REF_BISON_TEX = os.path.join(REPO_ROOT, "reference", "avatar-legend-reforged-1.3.0", "assets", "av3", "textures", "entity", "skybison.png")

MOD_ENTITY_MODELS = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "models", "entity")
MOD_ENTITY_ANIMS = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "animations", "entity")
MOD_PET_TEX = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity", "pet")
MOD_MOBS_TEX = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity", "mobs")
MOD_BOSS_TEX = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity", "boss")

os.makedirs(MOD_ENTITY_MODELS, exist_ok=True)
os.makedirs(MOD_ENTITY_ANIMS, exist_ok=True)
os.makedirs(MOD_PET_TEX, exist_ok=True)
os.makedirs(MOD_MOBS_TEX, exist_ok=True)
os.makedirs(MOD_BOSS_TEX, exist_ok=True)

def step1_integrate_flying_bison():
    print("\n[Step 1] Integrating 71-Bone Flying Bison from Canonical Reference...")
    # 1. Geo JSON: modify identifier to geometry.flying_bison
    with open(REF_BISON_GEO, "r", encoding="utf-8") as f:
        geo_data = json.load(f)
    geo_data["minecraft:geometry"][0]["description"]["identifier"] = "geometry.flying_bison"
    
    target_geo = os.path.join(MOD_ENTITY_MODELS, "flying_bison.geo.json")
    with open(target_geo, "w", encoding="utf-8") as f:
        json.dump(geo_data, f, indent=2)
    print(f"  -> Saved 71-bone geometry to: {target_geo}")
    
    # Also update staging
    staging_geo = os.path.join(REPO_ROOT, "art-source", "Avatar_Elements_Missing_Assets_Staging", "models", "entity", "flying_bison.geo.json")
    if os.path.exists(os.path.dirname(staging_geo)):
        shutil.copy2(target_geo, staging_geo)
        print(f"  -> Mirrored to staging: {staging_geo}")

    # 2. Animation JSON
    with open(REF_BISON_ANIM, "r", encoding="utf-8") as f:
        anim_data = json.load(f)
    
    # Rename animation keys to avatar_elements standard
    new_anims = {}
    for k, v in anim_data.get("animations", {}).items():
        new_key = k.replace("animation.", "animation.flying_bison.")
        new_anims[new_key] = v
    anim_data["animations"] = new_anims

    target_anim = os.path.join(MOD_ENTITY_ANIMS, "flying_bison.animation.json")
    with open(target_anim, "w", encoding="utf-8") as f:
        json.dump(anim_data, f, indent=2)
    print(f"  -> Saved 8-set keyframe animations to: {target_anim}")

    # 3. High-Res 512x512 Texture
    target_tex = os.path.join(MOD_PET_TEX, "flying_bison.png")
    shutil.copy2(REF_BISON_TEX, target_tex)
    print(f"  -> Installed 512x512 high-res texture to: {target_tex} ({os.path.getsize(target_tex)} bytes)")

if __name__ == "__main__":
    step1_integrate_flying_bison()
