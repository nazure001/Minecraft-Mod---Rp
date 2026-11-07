import os
import shutil

base_rp = r"d:\repo\avatar-armor-resourcepack"
optifine_dir = os.path.join(base_rp, "assets", "minecraft", "optifine", "cit", "armor")
citresewn_dir = os.path.join(base_rp, "assets", "minecraft", "citresewn", "cit", "armor")

for d in [optifine_dir, citresewn_dir]:
    os.makedirs(d, exist_ok=True)

nations = {
    "fire": {
        "names": "ipattern:*Fire* ipattern:*Dragon* ipattern:*Ember*",
        "l1": "fire_layer_1",
        "l2": "fire_layer_2"
    },
    "water": {
        "names": "ipattern:*Water* ipattern:*Ocean* ipattern:*Leviathan* ipattern:*Tidal* ipattern:*Tundra* ipattern:*Chieftain*",
        "l1": "water_layer_1",
        "l2": "water_layer_2"
    },
    "earth": {
        "names": "ipattern:*Earth* ipattern:*Titan* ipattern:*Terra* ipattern:*Dai Li* ipattern:*Monarch* ipattern:*Bedrock*",
        "l1": "earth_layer_1",
        "l2": "earth_layer_2"
    },
    "air": {
        "names": "ipattern:*Air* ipattern:*Zephyr* ipattern:*Glider* ipattern:*Aeromancer* ipattern:*Nimbus* ipattern:*Monk*",
        "l1": "air_layer_1",
        "l2": "air_layer_2"
    }
}

helm_chest_boots = "minecraft:netherite_helmet minecraft:netherite_chestplate minecraft:netherite_boots minecraft:diamond_helmet minecraft:diamond_chestplate minecraft:diamond_boots minecraft:iron_helmet minecraft:iron_chestplate minecraft:iron_boots minecraft:chainmail_helmet minecraft:chainmail_chestplate minecraft:chainmail_boots minecraft:leather_helmet minecraft:leather_chestplate minecraft:leather_boots"
leggings = "minecraft:netherite_leggings minecraft:diamond_leggings minecraft:iron_leggings minecraft:chainmail_leggings minecraft:leather_leggings"

for nat, conf in nations.items():
    # Properties for layer 1 (Head, Chest, Boots)
    prop1_content = f"""type=armor
items={helm_chest_boots}
texture.layer_1={conf['l1']}
nbt.display.Name={conf['names']}
"""

    # Properties for layer 2 (Leggings)
    prop2_content = f"""type=armor
items={leggings}
texture.layer_2={conf['l2']}
nbt.display.Name={conf['names']}
"""

    for target_dir in [optifine_dir, citresewn_dir]:
        with open(os.path.join(target_dir, f"{nat}_layer_1.properties"), "w", encoding="utf-8") as f:
            f.write(prop1_content)
        with open(os.path.join(target_dir, f"{nat}_layer_2.properties"), "w", encoding="utf-8") as f:
            f.write(prop2_content)

# Copy PNG textures to both directories
src_tex = os.path.join(base_rp, "assets", "avatar", "textures", "entity", "equipment")
for f in os.listdir(src_tex):
    if f.endswith(".png"):
        shutil.copy2(os.path.join(src_tex, f), os.path.join(optifine_dir, f))
        shutil.copy2(os.path.join(src_tex, f), os.path.join(citresewn_dir, f))

print("CIT armor properties & textures successfully installed to optifine/cit and citresewn/cit!")
