import json
import glob
import os

with open(r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\data\avatar_elements\skill_definitions.json") as f:
    data = json.load(f)

skills = data.get("skills", [])
anim_files = glob.glob(r"d:\repo\Minecraft Mod & Rp\mod\src\client\resources\assets\avatar_elements\player_animations\*.json")
anim_names = set(os.path.basename(a).replace(".animation.json", "").replace(".json", "") for a in anim_files)

print(f"Total skills: {len(skills)}")
print("=== SKILL ANIMATION COVERAGE ===")
for s in skills:
    sid = s["id"].replace("avatar:", "")
    has_anim = sid in anim_names
    status = "EXISTS" if has_anim else "MISSING!"
    print(f" - {s['id']:<25}: {status}")
