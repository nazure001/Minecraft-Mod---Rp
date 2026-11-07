import os
import re

give_dir = r"d:\repo\avatar-armor-datapack\data\avatar\function\give"

nations = ["fire", "water", "earth", "air"]
tiers = ["initiate", "apprentice", "adept", "veteran", "master", "mythic", "sovereign"]

files = [f for f in os.listdir(give_dir) if f.endswith(".mcfunction")]

for fname in files:
    fpath = os.path.join(give_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # If already has carved_pumpkin, skip
    if "minecraft:carved_pumpkin" in content:
        continue

    # Look for the helmet give command
    # Pattern: give @s minecraft:(leather|chainmail|iron|diamond|netherite)_helmet[...]
    m = re.search(r"give @s minecraft:(?:leather|chainmail|iron|diamond|netherite)_helmet(\[.*?\])", content)
    if not m:
        continue

    helmet_components = m.group(1)
    
    # Create the 3D headwear pumpkin command with identical components
    # We replace item_name with a distinct tag or prefix if desired, or keep it intact
    pumpkin_cmd = f"# Custom 3D Headwear (Equip on head for 3D Horns / Crown / Halo / Goggles)\ngive @s minecraft:carved_pumpkin{helmet_components}\n\n# Classic Armor Helmet\n"
    
    # Insert right before the helmet give command
    idx = m.start()
    new_content = content[:idx] + pumpkin_cmd + content[idx:]

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

print(f"Updated all give functions with 3D Headwear options!")
