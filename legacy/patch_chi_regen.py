#!/usr/bin/env python3
"""
Patch Chi Regeneration System:
1. Register avatar_regen_timer in setup.mcfunction and initialize in tick.mcfunction / init_player.mcfunction
2. Active Meditation Mode: Sneaking (Shift) rapidly meditates to restore +20 Chi/second with chanting glyphs
3. Base Passive Regen: +5 Chi/sec, up to +15 Chi/sec with Chi Mastery nodes
4. Update Condensed Chi Orb: instantly refills Chi to maximum capacity
5. Update Actionbar HUD: displays Meditating status and live Chi flow
"""

import os
import shutil
import zipfile

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar_skills")
FUNC_DIR = os.path.join(DATA_AVATAR, "function")
TREE_DIR = os.path.join(FUNC_DIR, "tree")

PRISM_DIR = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft"
PRISM_SAVES_DP = os.path.join(PRISM_DIR, "saves", "avatar", "datapacks")

# 1. Update setup.mcfunction
setup_path = os.path.join(FUNC_DIR, "setup.mcfunction")
with open(setup_path, "r", encoding="utf-8") as f:
    setup_txt = f.read()

if "avatar_regen_timer" not in setup_txt:
    setup_txt = setup_txt.replace(
        'scoreboard objectives add avatar_timer dummy "Avatar Timers"',
        'scoreboard objectives add avatar_timer dummy "Avatar Timers"\nscoreboard objectives add avatar_regen_timer dummy "Chi Regen Timer"'
    )
    with open(setup_path, "w", encoding="utf-8") as f:
        f.write(setup_txt)
    print("Added avatar_regen_timer to setup.mcfunction")

# 2. Update init_player.mcfunction
init_path = os.path.join(TREE_DIR, "init_player.mcfunction")
with open(init_path, "r", encoding="utf-8") as f:
    init_txt = f.read()

if "avatar_regen_timer" not in init_txt:
    init_txt += "\nscoreboard players set @s avatar_regen_timer 0\n"
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(init_txt)
    print("Updated init_player.mcfunction")

# 3. Update tick.mcfunction
tick_path = os.path.join(FUNC_DIR, "tick.mcfunction")
with open(tick_path, "r", encoding="utf-8") as f:
    tick_txt = f.read()

failsafe_timer = "execute as @a unless score @s avatar_regen_timer matches 0.. run scoreboard players set @s avatar_regen_timer 0\n"
if failsafe_timer not in tick_txt:
    tick_txt = tick_txt.replace(
        "execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player\n",
        "execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player\n" + failsafe_timer
    )
    with open(tick_path, "w", encoding="utf-8") as f:
        f.write(tick_txt)
    print("Updated tick.mcfunction with timer failsafe")

# 4. Update tick_chi_regen.mcfunction
regen_content = """# ==============================================================================
# Chi Regeneration Tick (Runs every 20 ticks / 1 second)
# ==============================================================================
scoreboard players set @s avatar_regen_timer 0

# Base passive regeneration (+5 Chi/sec)
execute if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5

# Bonus passive regen from Chi Mastery Node
execute if score @s av_stat_chi matches 1.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 2
execute if score @s av_stat_chi matches 2.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 2
execute if score @s av_stat_chi matches 3.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 3
execute if score @s av_stat_chi matches 4.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 3
execute if score @s av_stat_chi matches 5.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5

# Active Meditation Mode (Sneak/Crouch to focus Chi: +15 extra Chi/sec)
execute if entity @s[predicate=avatar_skills:is_sneaking] if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 15
execute if entity @s[predicate=avatar_skills:is_sneaking] at @s run particle minecraft:enchant ~ ~0.8 ~ 0.4 0.4 0.4 0.1 6 normal

# Clamp Chi to Max Chi (Prevent overflow)
execute if score @s avatar_chi > @s avatar_chi_max run scoreboard players operation @s avatar_chi = @s avatar_chi_max
"""
with open(os.path.join(FUNC_DIR, "tick_chi_regen.mcfunction"), "w", encoding="utf-8") as f:
    f.write(regen_content)
print("Updated tick_chi_regen.mcfunction")

# 5. Update consume_chi_orb.mcfunction
orb_content = """# Consume Chi Orb to gain Chi Points and instantly restore Chi
clear @s minecraft:warped_fungus_on_a_stick[custom_data~{avatar_skill:"chi_orb"}] 1
scoreboard players add @s av_chi_points 1
scoreboard players operation @s avatar_chi = @s avatar_chi_max
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 1.8
particle minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.05 15 normal
tellraw @s [{"text":"✨ Chi Orb absorbed! Gained ","color":"aqua"},{"text":"+1 Chi Point","color":"gold","bold":true},{"text":" and ","color":"aqua"},{"text":"Full Chi Restored!","color":"green","bold":true}]
"""
with open(os.path.join(TREE_DIR, "consume_chi_orb.mcfunction"), "w", encoding="utf-8") as f:
    f.write(orb_content)
print("Updated consume_chi_orb.mcfunction")

# 6. Update hud_actionbar.mcfunction
hud_content = """# Show Chi and Cooldown on Actionbar
execute if score @s avatar_state matches 1.. run title @s actionbar [{"text":"🌀 [AVATAR STATE] ","color":"light_purple","bold":true},{"text":"CHI: ","color":"aqua"},{"score":{"name":"@s","objective":"avatar_chi"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"},{"text":" | 4-ELEMENTS ACTIVE","color":"gold","bold":true}]
execute unless score @s avatar_state matches 1.. if entity @s[predicate=avatar_skills:is_sneaking] if score @s avatar_chi < @s avatar_chi_max run title @s actionbar [{"text":"🧘 [MEDITATING] ","color":"gold","bold":true},{"text":"⚡ CHI: ","color":"aqua","bold":true},{"score":{"name":"@s","objective":"avatar_chi"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"},{"text":" (+20 Chi/s)","color":"green"}]
execute unless score @s avatar_state matches 1.. unless entity @s[predicate=avatar_skills:is_sneaking] if score @s avatar_cd matches 1.. run title @s actionbar [{"text":"⏳ COOLDOWN: ","color":"red","bold":true},{"score":{"name":"@s","objective":"avatar_cd"},"color":"yellow"},{"text":" ticks | CHI: ","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi"},"color":"aqua"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"}]
execute unless score @s avatar_state matches 1.. unless entity @s[predicate=avatar_skills:is_sneaking] unless score @s avatar_cd matches 1.. run title @s actionbar [{"text":"⚡ CHI: ","color":"aqua","bold":true},{"score":{"name":"@s","objective":"avatar_chi"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"},{"text":" [READY]","color":"green","bold":true}]
"""
with open(os.path.join(FUNC_DIR, "hud_actionbar.mcfunction"), "w", encoding="utf-8") as f:
    f.write(hud_content)
print("Updated hud_actionbar.mcfunction")

# 7. Zip and Deploy to PrismLauncher
def make_zip(source_dir, output_zip):
    if os.path.exists(output_zip):
        os.remove(output_zip)
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, source_dir)
                zipf.write(abs_path, rel_path)

dp_zip = os.path.join(REPO_DIR, "avatar-skill-datapack.zip")
make_zip(DATAPACK_DIR, dp_zip)

if os.path.exists(PRISM_SAVES_DP):
    prism_dp_folder = os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack")
    if os.path.exists(prism_dp_folder):
        shutil.rmtree(prism_dp_folder)
    shutil.copytree(DATAPACK_DIR, prism_dp_folder)
    shutil.copy2(dp_zip, os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack.zip"))
    print("Directly deployed Datapack to PrismLauncher saves!")

print("=== ALL CHI REGEN FIXES COMPLETE ===")
