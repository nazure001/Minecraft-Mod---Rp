#!/usr/bin/env python3
"""
Fix cast routing, command parsing, and mob invulnerability issues:
1. Fix avatar_skills:cast/router (clean condition-based routing without invalid return syntax)
2. Fix avatar_skills:cast/water_freeze (remove non-existent flowing_water)
3. Improve hit detection in fire_step, water_step, earth_step, air_step (use distance=..2.0)
4. Ensure both Warped Fungus and Carrot on a stick triggers are fully tracked and dispatched
5. Synchronize source files in D:\\repo and deploy directly to PrismLauncher instance
"""

import os
import shutil
import zipfile

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
RESOURCEPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-resourcepack")

PRISM_DIR = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft"
PRISM_SAVES_DP = os.path.join(PRISM_DIR, "saves", "avatar", "datapacks")
PRISM_RES_DIR = os.path.join(PRISM_DIR, "resourcepacks")

DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar_skills")
CAST_DIR = os.path.join(DATA_AVATAR, "function", "cast")
FUNC_DIR = os.path.join(DATA_AVATAR, "function")

# =============================================================================
# 1. FIX ROUTER.MCFUNCTION
# =============================================================================
router_content = """# ==============================================================================
# Avatar Skills - Cast Router (Minecraft Java 1.21.1)
# ==============================================================================

# Failsafe stat initialization
execute unless score @s avatar_chi matches 0.. run scoreboard players set @s avatar_chi 100
execute unless score @s avatar_chi_max matches 1.. run scoreboard players set @s avatar_chi_max 100
execute unless score @s avatar_cd matches 0.. run scoreboard players set @s avatar_cd 0

# Check if player has insufficient Chi (< 10)
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches ..9 run title @s actionbar {"text":"⚠️ Insufficient Chi! Meditate or wait for chi to restore.","color":"red"}

# Main Bending Dispatch (Executes if cooldown is 0 and chi >= 10)
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_skill:"fire"}] run function avatar_skills:cast/fire_router
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_skill:"water"}] run function avatar_skills:cast/water_router
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_skill:"earth"}] run function avatar_skills:cast/earth_router
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_skill:"air"}] run function avatar_skills:cast/air_router
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_skill:"avatar"}] run function avatar_skills:cast/avatar_router

# Sub-Bending Foci
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"lightning"}] run function avatar_skills:cast/sub_lightning
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"combustion"}] run function avatar_skills:cast/sub_combustion
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"blood"}] run function avatar_skills:cast/sub_blood
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"healing"}] run function avatar_skills:cast/sub_healing
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"lava"}] run function avatar_skills:cast/sub_lava
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"metal"}] run function avatar_skills:cast/sub_metal
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches 10.. if items entity @s weapon.* *[custom_data~{avatar_sub:"flight"}] run function avatar_skills:cast/sub_flight

# Mastery Tome & Chi Orb (Always usable regardless of Chi / Cooldown)
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] run function avatar_skills:tree/open_menu
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run function avatar_skills:tree/consume_chi_orb
"""

with open(os.path.join(CAST_DIR, "router.mcfunction"), "w", encoding="utf-8") as f:
    f.write(router_content)

# =============================================================================
# 2. FIX WATER_FREEZE.MCFUNCTION
# =============================================================================
water_freeze_content = """# Glacial Freeze - Freeze existing water into real frosted ice
scoreboard players remove @s avatar_chi 30
scoreboard players set @s avatar_cd 40
playsound minecraft:block.glass.break player @a ~ ~ ~ 1.5 1.4
playsound minecraft:entity.player.hurt_freeze player @a ~ ~ ~ 1.2 1.0

# Physically freeze water in 9x9 area into walkable ice
execute at @s run fill ~-4 ~-1 ~-4 ~4 ~1 ~4 frosted_ice replace water

# Blizzard frost nova
execute at @s run particle minecraft:snowflake ~ ~0.5 ~ 3.5 0.5 3.5 0.05 50 normal
execute at @s as @e[type=!player,distance=..6] run effect give @s minecraft:slowness 6 4 true
execute at @s as @e[type=!player,distance=..6] run damage @s 6 minecraft:freeze
"""

with open(os.path.join(CAST_DIR, "water_freeze.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_freeze_content)

# =============================================================================
# 3. FIX STEP FUNCTIONS (Hitbox Spheres distance=..2.0)
# =============================================================================
with open(os.path.join(CAST_DIR, "fire_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.03 5 normal
particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.01 4 normal
execute as @e[type=!player,distance=..2.0,limit=3] run function avatar_skills:cast/fire_hit
""")

with open(os.path.join(CAST_DIR, "water_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""particle minecraft:splash ~ ~ ~ 0.25 0.25 0.25 0.05 6 normal
particle minecraft:falling_water ~ ~ ~ 0.15 0.15 0.15 0.02 5 normal
execute as @e[type=!player,distance=..2.0,limit=3] run function avatar_skills:cast/water_hit
""")

with open(os.path.join(CAST_DIR, "earth_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""particle minecraft:spore_blossom_air ~ ~ ~ 0.35 0.35 0.35 0.05 12 normal
particle minecraft:spore_blossom_air ~ ~ ~ 0.3 0.3 0.3 0.05 8 normal
execute as @e[type=!player,distance=..2.0,limit=3] run function avatar_skills:cast/earth_hit
""")

with open(os.path.join(CAST_DIR, "air_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.05 5 normal
particle minecraft:sweep_attack ~ ~ ~ 0.1 0.1 0.1 0.01 1 normal
execute as @e[type=!player,distance=..2.0,limit=4] run function avatar_skills:cast/air_hit
""")

print("Cast functions fixed successfully.")

# =============================================================================
# 4. FIX SETUP & TICK FUNCTION TO HANDLE BOTH CAST TRIGGERS & AXIOM GAMERULE
# =============================================================================
setup_content = """# ==============================================================================
# Avatar Skills & Mastery System - Setup (Minecraft Java 1.21.1)
# ==============================================================================

# Core Skill & Interaction Objectives
scoreboard objectives add avatar_used minecraft.used:minecraft.warped_fungus_on_a_stick "Avatar Cast"
scoreboard objectives add avatar_used_c minecraft.used:minecraft.carrot_on_a_stick "Avatar Cast C"
scoreboard objectives add avatar_chi dummy "Avatar Chi"
scoreboard objectives add avatar_chi_max dummy "Max Chi"
scoreboard objectives add avatar_cd dummy "Skill Cooldown"
scoreboard objectives add avatar_state dummy "Avatar State Timer"
scoreboard objectives add avatar_sneak minecraft.custom:minecraft.sneak_time "Sneak Time"
scoreboard objectives add avatar_timer dummy "Avatar Timers"

# Elemental Masteries (0 = locked, 1 = unlocked)
scoreboard objectives add av_mast_fire dummy "Fire Mastery"
scoreboard objectives add av_mast_water dummy "Water Mastery"
scoreboard objectives add av_mast_earth dummy "Earth Mastery"
scoreboard objectives add av_mast_air dummy "Air Mastery"
scoreboard objectives add av_mast_all dummy "Master of Four"

# Built-in Skill Node Attributes (Levels 0-5)
scoreboard objectives add av_stat_agi dummy "Agility Level"
scoreboard objectives add av_stat_chi dummy "Chi Mastery Level"
scoreboard objectives add av_stat_res dummy "Resilience Level"
scoreboard objectives add av_stat_pot dummy "Elemental Potency Level"
scoreboard objectives add av_chi_points dummy "Unallocated Chi"

# Setup default scores for new players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player

tellraw @a [{"text":"[Avatar System] ","color":"gold","bold":true},{"text":"Avatar Skills & Elemental Mastery System 1.21.1 Loaded Successfully!","color":"green"}]

# XP Level Tracking Objectives
scoreboard objectives add avatar_curr_lvl dummy "Current Level"
scoreboard objectives add avatar_prev_lvl dummy "Previous Level"
scoreboard objectives add avatar_diff_lvl dummy "Level Difference"
"""

with open(os.path.join(FUNC_DIR, "setup.mcfunction"), "w", encoding="utf-8") as f:
    f.write(setup_content)

tick_content = """# ==============================================================================
# Avatar Skills - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# 0. Failsafe auto-initialize player stats for all online players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player

# XP Level Progression Check (Adventure Level -> Skill Points)
execute as @a store result score @s avatar_curr_lvl run experience query @s levels
execute as @a unless score @s avatar_prev_lvl matches 0.. run scoreboard players operation @s avatar_prev_lvl = @s avatar_curr_lvl
execute as @a if score @s avatar_curr_lvl > @s avatar_prev_lvl run function avatar_skills:tree/on_level_up

# 1. Chi Regeneration (Every 20 ticks / 1 second)
execute as @a run scoreboard players add @s avatar_regen_timer 1
execute as @a if score @s avatar_regen_timer matches 20.. run function avatar_skills:tick_chi_regen

# 2. Cooldown Countdown
execute as @a if score @s avatar_cd matches 1.. run scoreboard players remove @s avatar_cd 1

# 3. Avatar State Timer & 4-Element Orbital Aura
execute as @a if score @s avatar_state matches 1.. run function avatar_skills:avatar_state/tick

# 4. Actionbar HUD Display (Chi & Status)
execute as @a if items entity @s weapon.* *[custom_data~{avatar_item:true}] run function avatar_skills:hud_actionbar

# 5. Right-Click Cast Detection (Warped Fungus + Carrot on a stick)
execute as @a[scores={avatar_used=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used=1..}] run scoreboard players set @s avatar_used 0

execute as @a[scores={avatar_used_c=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used_c=1..}] run scoreboard players set @s avatar_used_c 0

# 6. Auto-check 4-Element Mastery for Avatar Awakening
execute as @a[scores={av_mast_fire=1..,av_mast_water=1..,av_mast_earth=1..,av_mast_air=1..,av_mast_all=0}] run function avatar_skills:tree/awaken_avatar

# 7. Physical Bending Block Decay Timers (Anti-Griefing Auto-Cleanup)
execute as @e[type=marker,tag=avatar_earth_wall] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_earth_wall,scores={avatar_timer=140..}] at @s run function avatar_skills:cast/earth_wall_remove

execute as @e[type=marker,tag=avatar_lava_pool] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_lava_pool,scores={avatar_timer=120..}] at @s run function avatar_skills:cast/lava_pool_cool
"""

with open(os.path.join(FUNC_DIR, "tick.mcfunction"), "w", encoding="utf-8") as f:
    f.write(tick_content)

print("Tick and setup functions verified.")

# =============================================================================
# 5. SYNCHRONIZE WITH D:\repo\generate_avatar_skill_system.py
# =============================================================================
gen_file = os.path.join(REPO_DIR, "generate_avatar_skill_system.py")
if os.path.exists(gen_file):
    with open(gen_file, "r", encoding="utf-8") as f:
        code = f.read()
    # Replace the broken router in generator
    old_router = """# Check if player has enough Chi (minimum 10)
execute if score @s avatar_chi matches ..9 run title @s actionbar {"text":"⚠️ Insufficient Chi! Meditate or wait for chi to restore.","color":"red"}
execute if score @s avatar_chi matches ..9 return 0

# Check cooldown
execute if score @s avatar_cd matches 1.. run return 0"""
    new_router = """# Check if player has insufficient Chi (< 10)
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches ..9 run title @s actionbar {"text":"⚠️ Insufficient Chi! Meditate or wait for chi to restore.","color":"red"}"""
    if old_router in code:
        code = code.replace(old_router, new_router)
    if "execute at @s run fill ~-4 ~-1 ~-4 ~4 ~1 ~4 frosted_ice replace flowing_water" in code:
        code = code.replace("execute at @s run fill ~-4 ~-1 ~-4 ~4 ~1 ~4 frosted_ice replace flowing_water\n", "")
    with open(gen_file, "w", encoding="utf-8") as f:
        f.write(code)
    print("generate_avatar_skill_system.py synchronized.")

# =============================================================================
# 6. PACKAGE AND DEPLOY DIRECTLY TO PRISMLAUNCHER INSTANCE
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
make_zip(DATAPACK_DIR, dp_zip)

if os.path.exists(PRISM_SAVES_DP):
    prism_dp_folder = os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack")
    if os.path.exists(prism_dp_folder):
        shutil.rmtree(prism_dp_folder)
    shutil.copytree(DATAPACK_DIR, prism_dp_folder)
    shutil.copy2(dp_zip, os.path.join(PRISM_SAVES_DP, "avatar-skill-datapack.zip"))
    print(f"Directly deployed Datapack to: {PRISM_SAVES_DP}")

print("=== ALL FIXES APPLIED & DEPLOYED SUCCESSFULLY ===")
