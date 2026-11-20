import json
from pathlib import Path

MODELS_DIR = Path(r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets\avatar_elements\models\item")

DUAL_SWORDS_DISPLAY = {
    "thirdperson_righthand": { "rotation": [0, 90, -35], "translation": [0, 3.2, 0.5], "scale": [0.85, 0.85, 0.85] },
    "thirdperson_lefthand":  { "rotation": [0, -90, 35], "translation": [0, 3.2, 0.5], "scale": [0.85, 0.85, 0.85] },
    "firstperson_righthand": { "rotation": [0, 85, -25], "translation": [2.2, 1.8, -1.2], "scale": [0.75, 0.75, 0.75] },
    "firstperson_lefthand":  { "rotation": [0, -85, 25], "translation": [-2.2, 1.8, -1.2], "scale": [0.75, 0.75, 0.75] },
    "ground": { "rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5] },
    "gui": { "rotation": [0, 0, -45], "translation": [0, 0, 0], "scale": [0.65, 0.65, 0.65] },
    "fixed": { "rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.65, 0.65, 0.65] }
}

HAMMER_DISPLAY = {
    "thirdperson_righthand": { "rotation": [0, 90, -25], "translation": [0, 3.0, 0.8], "scale": [0.85, 0.85, 0.85] },
    "thirdperson_lefthand":  { "rotation": [0, -90, 25], "translation": [0, 3.0, 0.8], "scale": [0.85, 0.85, 0.85] },
    "firstperson_righthand": { "rotation": [15, 80, -25], "translation": [2.4, 1.0, -1.2], "scale": [0.7, 0.7, 0.7] },
    "firstperson_lefthand":  { "rotation": [15, -80, 25], "translation": [-2.4, 1.0, -1.2], "scale": [0.7, 0.7, 0.7] },
    "ground": { "rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5] },
    "gui": { "rotation": [0, 0, -45], "translation": [0, 0, 0], "scale": [0.55, 0.55, 0.55] },
    "fixed": { "rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.6, 0.6, 0.6] }
}

FAN_DISPLAY = {
    "thirdperson_righthand": { "rotation": [0, 90, -15], "translation": [0, 2.8, 0.5], "scale": [0.82, 0.82, 0.82] },
    "thirdperson_lefthand":  { "rotation": [0, -90, 15], "translation": [0, 2.8, 0.5], "scale": [0.82, 0.82, 0.82] },
    "firstperson_righthand": { "rotation": [10, 85, -15], "translation": [1.8, 1.5, -1.0], "scale": [0.75, 0.75, 0.75] },
    "firstperson_lefthand":  { "rotation": [10, -85, 15], "translation": [-1.8, 1.5, -1.0], "scale": [0.75, 0.75, 0.75] },
    "ground": { "rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5] },
    "gui": { "rotation": [0, 0, 0], "translation": [0, -1, 0], "scale": [0.75, 0.75, 0.75] },
    "fixed": { "rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.7, 0.7, 0.7] }
}

SPEAR_DISPLAY = {
    "thirdperson_righthand": { "rotation": [0, 90, -35], "translation": [0, 3.2, 0.6], "scale": [0.9, 0.9, 0.9] },
    "thirdperson_lefthand":  { "rotation": [0, -90, 35], "translation": [0, 3.2, 0.6], "scale": [0.9, 0.9, 0.9] },
    "firstperson_righthand": { "rotation": [10, 85, -25], "translation": [2.2, 1.2, -1.8], "scale": [0.8, 0.8, 0.8] },
    "firstperson_lefthand":  { "rotation": [10, -85, 25], "translation": [-2.2, 1.2, -1.8], "scale": [0.8, 0.8, 0.8] },
    "ground": { "rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5] },
    "gui": { "rotation": [0, 0, -45], "translation": [0, 0, 0], "scale": [0.55, 0.55, 0.55] },
    "fixed": { "rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.6, 0.6, 0.6] }
}

STAFF_DISPLAY = {
    "thirdperson_righthand": { "rotation": [0, 90, -30], "translation": [0, 2.8, 0.5], "scale": [0.95, 0.95, 0.95] },
    "thirdperson_lefthand":  { "rotation": [0, -90, 30], "translation": [0, 2.8, 0.5], "scale": [0.95, 0.95, 0.95] },
    "firstperson_righthand": { "rotation": [12, 85, -18], "translation": [2.0, 1.8, -1.5], "scale": [0.85, 0.85, 0.85] },
    "firstperson_lefthand":  { "rotation": [12, -85, 18], "translation": [-2.0, 1.8, -1.5], "scale": [0.85, 0.85, 0.85] },
    "ground": { "rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5] },
    "gui": { "rotation": [0, 0, -45], "translation": [0, 0, 0], "scale": [0.55, 0.55, 0.55] },
    "fixed": { "rotation": [0, -180, 0], "translation": [0, 0, 0], "scale": [0.7, 0.7, 0.7] }
}

def update_model(filename, display_config, filter_primary_only=False):
    path = MODELS_DIR / filename
    if not path.exists():
        print(f"File not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if filter_primary_only and "elements" in data:
        orig_count = len(data["elements"])
        data["elements"] = [e for e in data["elements"] if e.get("name", "").startswith("primary")]
        print(f"{filename}: filtered elements {orig_count} -> {len(data['elements'])}")
    
    data["display"] = display_config
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Updated {filename}")

def main():
    for f in ["dual_swords.json", "SM_Dual_Swords.json", "weapon_zuko_dual_dao.json"]:
        update_model(f, DUAL_SWORDS_DISPLAY, filter_primary_only=True)
    
    for f in ["earth_hammer.json", "SM_Earth_Hammer.json", "weapon_earth_war_hammer.json"]:
        update_model(f, HAMMER_DISPLAY, filter_primary_only=False)
        
    for f in ["war_fan.json", "SM_War_Fan.json", "weapon_kyoshi_war_fans.json"]:
        update_model(f, FAN_DISPLAY, filter_primary_only=False)
        
    for f in ["water_spear.json", "SM_Water_Spear.json", "weapon_water_jaw_blade.json"]:
        update_model(f, SPEAR_DISPLAY, filter_primary_only=False)

    for f in ["air_staff.json"]:
        update_model(f, STAFF_DISPLAY, filter_primary_only=False)

if __name__ == "__main__":
    main()
