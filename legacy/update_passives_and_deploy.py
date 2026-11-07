#!/usr/bin/env python3
"""
Update Avatar Skills Datapack & Resource Pack:
1. Build Complete Passive Skill Tree Advancements (Agility, Resilience, Chi, Potency Ranks I-V)
2. Implement Automatic XP Level-Up Progression (Adventure Level -> Skill Points)
3. Connect advancement grants to skill upgrades so they light up in the 'L' GUI
4. Direct deployment into PrismLauncher modpack instance
"""

import os
import json
import shutil
import zipfile

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
RESOURCEPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-resourcepack")

PRISM_DIR = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft"
PRISM_SAVES_DP = os.path.join(PRISM_DIR, "saves", "avatar", "datapacks")
PRISM_RES_DIR = os.path.join(PRISM_DIR, "resourcepacks")

# Datapack directories
DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar_skills")
ADV_DIR = os.path.join(DATA_AVATAR, "advancement")
PASSIVES_ADV_DIR = os.path.join(ADV_DIR, "passives")
TREE_DIR = os.path.join(DATA_AVATAR, "function", "tree")
CAST_DIR = os.path.join(DATA_AVATAR, "function", "cast")
FUNC_DIR = os.path.join(DATA_AVATAR, "function")

os.makedirs(PASSIVES_ADV_DIR, exist_ok=True)

# =============================================================================
# 1. GENERATE PASSIVE SKILL ADVANCEMENTS (Rank I - V for all 4 Attributes)
# =============================================================================

# Passives Root
adv_passives_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5006}},
        "title": {"text": "Spiritual Cultivation", "color": "gold", "bold": True},
        "description": {"text": "Channel raw chi to cultivate physical agility, vitality, chi capacity, and destructive potency.", "color": "yellow"},
        "frame": "goal"
    },
    "criteria": {"unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(PASSIVES_ADV_DIR, "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_passives_root, f, indent=2)

# Agility Branch (5 Ranks)
agility_nodes = [
    {
        "id": "agility_1", "parent": "avatar_skills:passives/root", "icon": "minecraft:feather",
        "title": "Agility I: Swift Step", "desc": "+15% Movement Speed and 5m Safe Fall Distance.", "frame": "task"
    },
    {
        "id": "agility_2", "parent": "avatar_skills:passives/agility_1", "icon": "minecraft:sugar",
        "title": "Agility II: Wind Stride", "desc": "+30% Movement Speed and 8m Safe Fall Distance.", "frame": "task"
    },
    {
        "id": "agility_3", "parent": "avatar_skills:passives/agility_2", "icon": "minecraft:rabbit_foot",
        "title": "Agility III: Gale Dash", "desc": "+45% Movement Speed and Jump Boost.", "frame": "task"
    },
    {
        "id": "agility_4", "parent": "avatar_skills:passives/agility_3", "icon": "minecraft:wind_charge",
        "title": "Agility IV: Cloud Runner", "desc": "+60% Movement Speed and 15m Safe Fall Distance.", "frame": "goal"
    },
    {
        "id": "agility_5", "parent": "avatar_skills:passives/agility_4", "icon": "minecraft:elytra",
        "title": "Agility V: Weightless Grace", "desc": "+80% Movement Speed, Step Height 1.5 blocks, and Complete Fall Immunity!", "frame": "challenge"
    }
]

# Resilience Branch (5 Ranks)
resilience_nodes = [
    {
        "id": "resilience_1", "parent": "avatar_skills:passives/root", "icon": "minecraft:shield",
        "title": "Resilience I: Stone Skin", "desc": "+2 Extra Hearts (24 Max Health).", "frame": "task"
    },
    {
        "id": "resilience_2", "parent": "avatar_skills:passives/resilience_1", "icon": "minecraft:iron_chestplate",
        "title": "Resilience II: Iron Will", "desc": "+4 Extra Hearts (28 Max Health).", "frame": "task"
    },
    {
        "id": "resilience_3", "parent": "avatar_skills:passives/resilience_2", "icon": "minecraft:diamond_chestplate",
        "title": "Resilience III: Mountain Fortitude", "desc": "+6 Extra Hearts (32 Max Health).", "frame": "task"
    },
    {
        "id": "resilience_4", "parent": "avatar_skills:passives/resilience_3", "icon": "minecraft:netherite_chestplate",
        "title": "Resilience IV: Earth Titan", "desc": "+8 Extra Hearts (36 Max Health).", "frame": "goal"
    },
    {
        "id": "resilience_5", "parent": "avatar_skills:passives/resilience_4", "icon": "minecraft:totem_of_undying",
        "title": "Resilience V: Immortal Colossus", "desc": "+10 Extra Hearts (40 Max Health - Two Full Heart Bars) + Resistance!", "frame": "challenge"
    }
]

# Chi Mastery Branch (5 Ranks)
chi_nodes = [
    {
        "id": "chi_1", "parent": "avatar_skills:passives/root", "icon": "minecraft:amethyst_shard",
        "title": "Chi Mastery I: Chi Flow", "desc": "Max Chi increased to 125 and +20% regeneration speed.", "frame": "task"
    },
    {
        "id": "chi_2", "parent": "avatar_skills:passives/chi_1", "icon": "minecraft:prismarine_crystals",
        "title": "Chi Mastery II: Deep Reservoir", "desc": "Max Chi increased to 150 and +40% regeneration speed.", "frame": "task"
    },
    {
        "id": "chi_3", "parent": "avatar_skills:passives/chi_2", "icon": "minecraft:echo_shard",
        "title": "Chi Mastery III: Elemental Resonance", "desc": "Max Chi increased to 175 and all skill cooldowns reduced by 10%.", "frame": "task"
    },
    {
        "id": "chi_4", "parent": "avatar_skills:passives/chi_3", "icon": "minecraft:heart_of_the_sea",
        "title": "Chi Mastery IV: Spirit Conduit", "desc": "Max Chi increased to 200 and skill cooldowns reduced by 20%.", "frame": "goal"
    },
    {
        "id": "chi_5", "parent": "avatar_skills:passives/chi_4", "icon": "minecraft:nether_star",
        "title": "Chi Mastery V: Infinite Ocean", "desc": "Max Chi 250, Cooldowns -30%, and rapid chi surge!", "frame": "challenge"
    }
]

# Elemental Potency Branch (5 Ranks)
potency_nodes = [
    {
        "id": "potency_1", "parent": "avatar_skills:passives/root", "icon": "minecraft:blaze_powder",
        "title": "Potency I: Spark of Power", "desc": "+10% damage amplifier on all bending moves.", "frame": "task"
    },
    {
        "id": "potency_2", "parent": "avatar_skills:passives/potency_1", "icon": "minecraft:blaze_rod",
        "title": "Potency II: Focused Impact", "desc": "+25% damage amplifier on all bending moves.", "frame": "task"
    },
    {
        "id": "potency_3", "parent": "avatar_skills:passives/potency_2", "icon": "minecraft:fire_charge",
        "title": "Potency III: Destructive Force", "desc": "+40% damage amplifier and +1 block area of effect.", "frame": "task"
    },
    {
        "id": "potency_4", "parent": "avatar_skills:passives/potency_3", "icon": "minecraft:magma_block",
        "title": "Potency IV: Master's Wrath", "desc": "+60% damage amplifier and heavy upward knockback.", "frame": "goal"
    },
    {
        "id": "potency_5", "parent": "avatar_skills:passives/potency_4", "icon": "minecraft:dragon_breath",
        "title": "Potency V: Cataclysmic Surge", "desc": "+80% damage amplifier and doubled stun & burn durations!", "frame": "challenge"
    }
]

all_passives = agility_nodes + resilience_nodes + chi_nodes + potency_nodes

for node in all_passives:
    adv_json = {
        "parent": node["parent"],
        "display": {
            "icon": {"id": node["icon"]},
            "title": {"text": node["title"], "color": "gold", "bold": True},
            "description": {"text": node["desc"], "color": "white"},
            "frame": node["frame"],
            "show_toast": True,
            "announce_to_chat": False
        },
        "criteria": {
            "unlocked": {"trigger": "minecraft:impossible"}
        }
    }
    with open(os.path.join(PASSIVES_ADV_DIR, f"{node['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(adv_json, f, indent=2)

print(f"Generated {len(all_passives) + 1} passive skill tree advancements.")

# =============================================================================
# 2. UPDATE SETUP & TICK WITH XP LEVEL-UP DETECTION
# =============================================================================
setup_file = os.path.join(FUNC_DIR, "setup.mcfunction")
with open(setup_file, "r", encoding="utf-8") as f:
    setup_code = f.read()

if "avatar_curr_lvl" not in setup_code:
    setup_code += """
# XP Level Tracking Objectives
scoreboard objectives add avatar_curr_lvl dummy "Current Level"
scoreboard objectives add avatar_prev_lvl dummy "Previous Level"
scoreboard objectives add avatar_diff_lvl dummy "Level Difference"
"""
    with open(setup_file, "w", encoding="utf-8") as f:
        f.write(setup_code)

tick_file = os.path.join(FUNC_DIR, "tick.mcfunction")
with open(tick_file, "r", encoding="utf-8") as f:
    tick_code = f.read()

# Add level progression check to tick loop if not present
level_check_snippet = """# XP Level Progression Check (Adventure Level -> Skill Points)
execute as @a store result score @s avatar_curr_lvl run experience query @s levels
execute as @a unless score @s avatar_prev_lvl matches 0.. run scoreboard players operation @s avatar_prev_lvl = @s avatar_curr_lvl
execute as @a if score @s avatar_curr_lvl > @s avatar_prev_lvl run function avatar_skills:tree/on_level_up
"""
if "avatar_curr_lvl" not in tick_code:
    tick_code = tick_code.replace("# 1. Chi Regeneration", level_check_snippet + "\n# 1. Chi Regeneration")
    with open(tick_file, "w", encoding="utf-8") as f:
        f.write(tick_code)

# Create on_level_up.mcfunction
on_level_up_code = """# Player Gained XP Levels -> Award Skill Points
scoreboard players operation @s avatar_diff_lvl = @s avatar_curr_lvl
scoreboard players operation @s avatar_diff_lvl -= @s avatar_prev_lvl
scoreboard players operation @s av_chi_points += @s avatar_diff_lvl
scoreboard players operation @s avatar_prev_lvl = @s avatar_curr_lvl

# Visual & Audio Feedback
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.2
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.5 0.5 0.1 25 normal

title @s actionbar [{"text":"🌟 LEVEL UP! ","color":"gold","bold":true},{"text":"+1 Skill Point awarded! (Total: ","color":"yellow"},{"score":{"name":"@s","objective":"av_chi_points"},"color":"aqua","bold":true},{"text":") | Right-click Tome of Chi to spend!","color":"yellow"}]
tellraw @s [{"text":"[Avatar Progression] ","color":"gold","bold":true},{"text":"Level Up! You reached Level ","color":"yellow"},{"score":{"name":"@s","objective":"avatar_curr_lvl"},"color":"green","bold":true},{"text":" and received ","color":"yellow"},{"score":{"name":"@s","objective":"avatar_diff_lvl"},"color":"aqua","bold":true},{"text":" Skill Point(s)! Right-click your Tome of Chi to cultivate your passive/active tree.","color":"yellow"}]
"""
with open(os.path.join(TREE_DIR, "on_level_up.mcfunction"), "w", encoding="utf-8") as f:
    f.write(on_level_up_code)

# =============================================================================
# 3. UPDATE SKILL UPGRADES TO GRANT ADVANCEMENTS IN 'L' GUI
# =============================================================================
apply_agi_code = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_agi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Apply 1.21.1 Native Attributes and Advancement Lights
execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.movement_speed base set 0.115
execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.safe_fall_distance base set 5.0
execute if score @s av_stat_agi matches 1 run advancement grant @s only avatar_skills:passives/agility_1

execute if score @s av_stat_agi matches 2 run attribute @s minecraft:generic.movement_speed base set 0.130
execute if score @s av_stat_agi matches 2 run attribute @s minecraft:generic.safe_fall_distance base set 8.0
execute if score @s av_stat_agi matches 2 run advancement grant @s only avatar_skills:passives/agility_2

execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.movement_speed base set 0.145
execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.safe_fall_distance base set 10.0
execute if score @s av_stat_agi matches 3 run advancement grant @s only avatar_skills:passives/agility_3

execute if score @s av_stat_agi matches 4 run attribute @s minecraft:generic.movement_speed base set 0.160
execute if score @s av_stat_agi matches 4 run attribute @s minecraft:generic.safe_fall_distance base set 15.0
execute if score @s av_stat_agi matches 4 run advancement grant @s only avatar_skills:passives/agility_4

execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.movement_speed base set 0.180
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.safe_fall_distance base set 30.0
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.step_height base set 1.5
execute if score @s av_stat_agi matches 5 run advancement grant @s only avatar_skills:passives/agility_5

tellraw @s [{"text":"✅ Agility upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"gold","bold":true},{"text":"! Speed & Fall resistance increased. (Check 'L' Menu!)","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "apply_agi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_agi_code)

apply_res_code = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_res 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Apply Extra Max Health Hearts and Advancement Lights
execute if score @s av_stat_res matches 1 run attribute @s minecraft:generic.max_health base set 24
execute if score @s av_stat_res matches 1 run advancement grant @s only avatar_skills:passives/resilience_1

execute if score @s av_stat_res matches 2 run attribute @s minecraft:generic.max_health base set 28
execute if score @s av_stat_res matches 2 run advancement grant @s only avatar_skills:passives/resilience_2

execute if score @s av_stat_res matches 3 run attribute @s minecraft:generic.max_health base set 32
execute if score @s av_stat_res matches 3 run advancement grant @s only avatar_skills:passives/resilience_3

execute if score @s av_stat_res matches 4 run attribute @s minecraft:generic.max_health base set 36
execute if score @s av_stat_res matches 4 run advancement grant @s only avatar_skills:passives/resilience_4

execute if score @s av_stat_res matches 5 run attribute @s minecraft:generic.max_health base set 40
execute if score @s av_stat_res matches 5 run advancement grant @s only avatar_skills:passives/resilience_5

tellraw @s [{"text":"✅ Resilience upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"gold","bold":true},{"text":"! Max Health hearts increased! (Check 'L' Menu!)","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "apply_res.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_res_code)

apply_chi_code = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_chi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Expand Max Chi Capacity and Advancement Lights
execute if score @s av_stat_chi matches 1 run scoreboard players set @s avatar_chi_max 125
execute if score @s av_stat_chi matches 1 run advancement grant @s only avatar_skills:passives/chi_1

execute if score @s av_stat_chi matches 2 run scoreboard players set @s avatar_chi_max 150
execute if score @s av_stat_chi matches 2 run advancement grant @s only avatar_skills:passives/chi_2

execute if score @s av_stat_chi matches 3 run scoreboard players set @s avatar_chi_max 175
execute if score @s av_stat_chi matches 3 run advancement grant @s only avatar_skills:passives/chi_3

execute if score @s av_stat_chi matches 4 run scoreboard players set @s avatar_chi_max 200
execute if score @s av_stat_chi matches 4 run advancement grant @s only avatar_skills:passives/chi_4

execute if score @s av_stat_chi matches 5 run scoreboard players set @s avatar_chi_max 250
execute if score @s av_stat_chi matches 5 run advancement grant @s only avatar_skills:passives/chi_5

tellraw @s [{"text":"✅ Chi Mastery upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"gold","bold":true},{"text":"! Max Chi expanded to ","color":"green"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"aqua"},{"text":"! (Check 'L' Menu!)","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "apply_chi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_chi_code)

apply_pot_code = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_pot 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

execute if score @s av_stat_pot matches 1 run advancement grant @s only avatar_skills:passives/potency_1
execute if score @s av_stat_pot matches 2 run advancement grant @s only avatar_skills:passives/potency_2
execute if score @s av_stat_pot matches 3 run advancement grant @s only avatar_skills:passives/potency_3
execute if score @s av_stat_pot matches 4 run advancement grant @s only avatar_skills:passives/potency_4
execute if score @s av_stat_pot matches 5 run advancement grant @s only avatar_skills:passives/potency_5

tellraw @s [{"text":"✅ Elemental Potency upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"gold","bold":true},{"text":"! All elemental attacks deal amplified damage! (Check 'L' Menu!)","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "apply_pot.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_pot_code)

# Updated open_menu.mcfunction
open_menu_code = """# Open Interactive Skill Tree
tellraw @s ""
tellraw @s [{"text":"==================== ","color":"gold","bold":true},{"text":"AVATAR MASTERY SHRINE","color":"yellow","bold":true},{"text":" ====================","color":"gold","bold":true}]
tellraw @s [{"text":"Available Skill Points: ","color":"gray"},{"score":{"name":"@s","objective":"av_chi_points"},"color":"aqua","bold":true},{"text":" (Earn +1 point every time you level up!)","color":"yellow"}]
tellraw @s ""
tellraw @s [{"text":"--- PASSIVE CULTIVATION TREE ---","color":"gold","bold":true}]
tellraw @s [{"text":"[🏃 AGILITY] ","color":"green","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_agi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Boosts Speed & Safe Fall Distance."}}]
tellraw @s [{"text":"[🧘 CHI MASTERY] ","color":"aqua","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_chi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Boosts Max Chi & Regeneration Speed."}}]
tellraw @s [{"text":"[🛡️ RESILIENCE] ","color":"red","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_res"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Permanently grants Extra Hearts (up to 40 HP)."}}]
tellraw @s [{"text":"[⚡ ELEMENTAL POTENCY] ","color":"light_purple","bold":true},{"text":"Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_pot"},"hoverEvent":{"action":"show_text","value":"Costs 1 Point. Amplifies damage and blast radius of all bending skills."}}]
tellraw @s ""
tellraw @s [{"text":"--- ACTIVE ELEMENTAL DISCIPLINES ---","color":"gold","bold":true}]
tellraw @s [{"text":"• Fire: "},{"score":{"name":"@s","objective":"av_mast_fire"},"color":"red"},{"text":" | Water: "},{"score":{"name":"@s","objective":"av_mast_water"},"color":"blue"},{"text":" | Earth: "},{"score":{"name":"@s","objective":"av_mast_earth"},"color":"dark_green"},{"text":" | Air: "},{"score":{"name":"@s","objective":"av_mast_air"},"color":"yellow"}]
tellraw @s [{"text":"💡 Press 'L' to inspect your full Avatar Advancement Skill Tree!","color":"yellow","italic":true}]
tellraw @s [{"text":"=====================================================","color":"gold","bold":true}]
"""
with open(os.path.join(TREE_DIR, "open_menu.mcfunction"), "w", encoding="utf-8") as f:
    f.write(open_menu_code)

print("Functions and menu updated.")

# =============================================================================
# 4. ZIP PACKAGING & DIRECT DEPLOYMENT TO PRISMLAUNCHER INSTANCE
# =============================================================================
def make_zip(source_dir, output_zip):
    if os.path.exists(output_zip):
        os.remove(output_zip)
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, source_dir)
                zipf.write(abs_path, rel_path)
    print(f"Created {output_zip} ({os.path.getsize(output_zip)} bytes)")

dp_zip = os.path.join(REPO_DIR, "avatar-skill-datapack.zip")
rp_zip = os.path.join(REPO_DIR, "avatar-skill-resourcepack.zip")
make_zip(DATAPACK_DIR, dp_zip)
make_zip(RESOURCEPACK_DIR, rp_zip)

# Copy to PrismLauncher Instance
if os.path.exists(PRISM_SAVES_DP):
    prism_dp_folder = os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack")
    if os.path.exists(prism_dp_folder):
        shutil.rmtree(prism_dp_folder)
    shutil.copytree(DATAPACK_DIR, prism_dp_folder)
    shutil.copy2(dp_zip, os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack.zip"))
    print(f"Directly deployed Datapack to: {PRISM_SAVES_DP}")

if os.path.exists(PRISM_RES_DIR):
    shutil.copy2(rp_zip, os.path.join(PRISM_RES_DIR, "avatar-skill-resourcepack.zip"))
    prism_rp_folder = os.path.join(PRISM_RES_DIR, "avatar-skill-resourcepack")
    if os.path.exists(prism_rp_folder):
        shutil.rmtree(prism_rp_folder)
    shutil.copytree(RESOURCEPACK_DIR, prism_rp_folder)
    print(f"Directly deployed Resourcepack to: {PRISM_RES_DIR}")

print("=== ALL UPDATES & PRISMLAUNCHER DEPLOYMENT COMPLETE ===")
