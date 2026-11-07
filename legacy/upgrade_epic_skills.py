#!/usr/bin/env python3
"""
Epic Avatar Skills Overhaul:
1. Fix all 1.21.1 broken particle commands (particle minecraft:block dirt/stone -> valid dust & explosion & falling_block)
2. Implement Tectonic Ground Wave (Gelombang Tanah Bergelombang) with physical rising falling_block waves, shockwave explosions, and knockup
3. Implement Epic Fire, Water, Air, and Avatar State Ultimate particle & sound effects
4. Failsafe Chi System: Chi auto-refills to 100 if at 0, consuming Chi Orb refills 100% Chi + gives Skill Point
5. Skills ALWAYS fire and never get locked out
6. Synchronize with generator and deploy directly to PrismLauncher
"""

import os
import shutil
import zipfile

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar_skills")
CAST_DIR = os.path.join(DATA_AVATAR, "function", "cast")
FUNC_DIR = os.path.join(DATA_AVATAR, "function")
TREE_DIR = os.path.join(FUNC_DIR, "tree")
AVATAR_DIR = os.path.join(FUNC_DIR, "avatar_state")

PRISM_DIR = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft"
PRISM_SAVES_DP = os.path.join(PRISM_DIR, "saves", "avatar", "datapacks")

# =============================================================================
# 1. EPIC EARTH WAVE (GELOMBANG TANAH BERGELOMBANG) & EARTH SKILLS
# =============================================================================
earth_wave_content = """# ==============================================================================
# Tectonic Earth Wave (Gelombang Tanah Bergelombang) - VCraft / Avatar Style
# ==============================================================================
scoreboard players remove @s avatar_chi 20
scoreboard players set @s avatar_cd 25

# Deep tectonic seismic roar & stone crack sounds
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 2.0 0.5
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.5 0.6
playsound minecraft:block.stone.break player @a ~ ~ ~ 2.0 0.7

# --- WAVE STAGE 1 (Distance 2): Initial Ground Fracture ---
execute at @s anchored feet positioned ^-1.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.35,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.35,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:explosion ~ ~ ~ 0.5 0.2 0.5 0.02 2 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:poof ~ ~ ~ 0.6 0.3 0.6 0.05 10 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.4} ~ ~ ~ 0.8 0.4 0.8 0.1 20 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 as @e[type=!player,distance=..2.5] run tp @s ~ ~0.8 ~
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 as @e[type=!player,distance=..2.5] run damage @s 8 minecraft:generic

# --- WAVE STAGE 2 (Distance 4): Cresting Tectonic Swell ---
execute at @s anchored feet positioned ^-1.2 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:cobblestone"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.2 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:explosion ~ ~ ~ 0.6 0.2 0.6 0.02 3 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:poof ~ ~ ~ 0.8 0.4 0.8 0.05 15 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.6} ~ ~ ~ 1.0 0.5 1.0 0.1 25 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 as @e[type=!player,distance=..2.8] run tp @s ~ ~1.2 ~
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 as @e[type=!player,distance=..2.8] run damage @s 10 minecraft:generic

# --- WAVE STAGE 3 (Distance 6): Massive Earth Crest Surge ---
execute at @s anchored feet positioned ^-1.4 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.4 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:explosion ~ ~ ~ 0.8 0.3 0.8 0.03 4 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:poof ~ ~ ~ 1.0 0.5 1.0 0.05 20 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:dust{color:[0.45,0.30,0.15],scale:1.8} ~ ~ ~ 1.2 0.5 1.2 0.1 30 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 as @e[type=!player,distance=..3.2] run tp @s ~ ~1.6 ~
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 as @e[type=!player,distance=..3.2] run damage @s 13 minecraft:generic

# --- WAVE STAGE 4 (Distance 8): Cataclysmic Impact Crash ---
execute at @s anchored feet positioned ^-1.2 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:cobblestone"},Time:1,Motion:[0.0,0.75,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.2 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2.0 0.8
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:poof ~ ~ ~ 1.2 0.6 1.2 0.08 30 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:dust{color:[0.40,0.25,0.10],scale:2.0} ~ ~ ~ 1.5 0.8 1.5 0.15 40 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 as @e[type=!player,distance=..3.5] run tp @s ~ ~2.0 ~
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 as @e[type=!player,distance=..3.5] run damage @s 16 minecraft:generic
"""
with open(os.path.join(CAST_DIR, "earth_boulder.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_wave_content)

# Earth Wall Barrier
earth_wall_content = """# Earth Wall Barrier - Fortified Battlement Manipulation
scoreboard players remove @s avatar_chi 30
scoreboard players set @s avatar_cd 50
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 1.8 0.6
playsound minecraft:block.stone.place player @a ~ ~ ~ 2.0 0.7
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.2 0.5

# Raise physical 3x3 stone & cobblestone wall in front
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~2 ~ stone replace air
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~2 ~ stone replace short_grass
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~2 ~ stone replace tall_grass
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~2 ~ stone replace fern

# Tectonic dust & smoke cloud
execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:poof ~ ~0.5 ~ 1.2 1.0 0.8 0.05 40 normal
execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.6} ~ ~0.5 ~ 1.2 1.0 0.8 0.1 50 normal
execute at @s anchored eyes positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["avatar_earth_wall"],Age:0}

# Knockback & stun hostiles
execute at @s anchored eyes positioned ^ ^ ^3 as @e[type=!player,distance=..3.5] run tp @s ^ ^1.0 ^-2.5
execute at @s anchored eyes positioned ^ ^ ^3 as @e[type=!player,distance=..3.5] run damage @s 8 minecraft:generic
effect give @s minecraft:resistance 5 2 true
"""
with open(os.path.join(CAST_DIR, "earth_wall.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_wall_content)

# Earth Wall Remove
earth_wall_remove_content = """# Decay physical earth wall back to air
fill ~-1 ~-1 ~ ~1 ~2 ~ air replace stone
particle minecraft:poof ~ ~ ~ 1.0 1.0 0.5 0.05 40 normal
particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.4} ~ ~ ~ 1.0 1.0 0.5 0.1 40 normal
playsound minecraft:block.stone.break player @a ~ ~ ~ 1.2 0.8
kill @s
"""
with open(os.path.join(CAST_DIR, "earth_wall_remove.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_wall_remove_content)

print("Earthbending overhaul complete.")

# =============================================================================
# 2. EPIC FIREBENDING - DRAGON'S INFERNO & JET THRUSTER
# =============================================================================
fire_blast_content = """# Fire Blast - Roaring Dragon's Breath & Inferno Wave
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 15
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.5 1.1
playsound minecraft:entity.blaze.shoot player @a ~ ~ ~ 1.2 1.2
playsound minecraft:entity.generic.burn player @a ~ ~ ~ 1.5 1.0

# Cascading cone of flames
execute at @s anchored eyes positioned ^-1.2 ^0.1 ^2 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.0 ^0.2 ^2.5 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^1.2 ^0.1 ^2 run function avatar_skills:cast/fire_step

execute at @s anchored eyes positioned ^-1.5 ^0.2 ^4 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.0 ^0.3 ^4.5 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^1.5 ^0.2 ^4 run function avatar_skills:cast/fire_step

execute at @s anchored eyes positioned ^-1.8 ^0.3 ^6.5 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.0 ^0.4 ^7.0 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^1.8 ^0.3 ^6.5 run function avatar_skills:cast/fire_step

# Ignite ground surface
execute at @s anchored feet positioned ^ ^ ^3 if block ~ ~ ~ air if block ~ ~-1 ~ #minecraft:inside_step_sound_blocks run setblock ~ ~ ~ fire
"""
with open(os.path.join(CAST_DIR, "fire_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_blast_content)

fire_step_content = """particle minecraft:flame ~ ~ ~ 0.4 0.4 0.4 0.05 12 normal
particle minecraft:small_flame ~ ~ ~ 0.3 0.3 0.3 0.02 8 normal
particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0.01 2 normal
particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 4 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/fire_hit
"""
with open(os.path.join(CAST_DIR, "fire_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_step_content)

print("Firebending overhaul complete.")

# =============================================================================
# 3. EPIC WATERBENDING - SURGE TORRENT & FROST NOVA
# =============================================================================
water_whip_content = """# Water Whip - Tidal Surge Vortex
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 15
playsound minecraft:entity.generic.splash player @a ~ ~ ~ 1.5 1.2
playsound minecraft:entity.player.splash.high_speed player @a ~ ~ ~ 1.2 1.4

# Torrent line
execute at @s anchored eyes positioned ^ ^ ^1.5 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^ ^ ^3.0 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^ ^ ^4.5 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^ ^ ^6.0 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^ ^ ^7.5 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^ ^ ^9.0 run function avatar_skills:cast/water_step
"""
with open(os.path.join(CAST_DIR, "water_whip.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_whip_content)

water_step_content = """particle minecraft:splash ~ ~ ~ 0.4 0.4 0.4 0.08 15 normal
particle minecraft:falling_water ~ ~ ~ 0.3 0.3 0.3 0.04 10 normal
particle minecraft:bubble ~ ~ ~ 0.2 0.2 0.2 0.05 8 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/water_hit
"""
with open(os.path.join(CAST_DIR, "water_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_step_content)

print("Waterbending overhaul complete.")

# =============================================================================
# 4. EPIC AIRBENDING - GALE SHOCKWAVE & VACUUM BURST
# =============================================================================
air_blast_content = """# Air Blast - Sonic Gale Shockwave & Deflection Burst
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 12
playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 1.5 1.2
playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 1.5 0.8

# Sonic boom wave
execute at @s anchored eyes positioned ^ ^ ^1.5 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^ ^ ^3.0 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^ ^ ^4.5 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^ ^ ^6.0 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^ ^ ^7.5 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^ ^ ^9.0 run function avatar_skills:cast/air_step

# Deflect incoming projectiles
execute at @s as @e[type=arrow,distance=..5] run kill @s
execute at @s as @e[type=spectral_arrow,distance=..5] run kill @s
"""
with open(os.path.join(CAST_DIR, "air_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_blast_content)

air_step_content = """particle minecraft:cloud ~ ~ ~ 0.4 0.4 0.4 0.05 10 normal
particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.05 8 normal
particle minecraft:sweep_attack ~ ~ ~ 0.2 0.2 0.2 0.01 2 normal
particle minecraft:gust ~ ~ ~ 0.2 0.2 0.2 0.02 1 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/air_hit
"""
with open(os.path.join(CAST_DIR, "air_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_step_content)

print("Airbending overhaul complete.")

# =============================================================================
# 5. AVATAR STATE ULTIMATE & TICK OVERHAUL
# =============================================================================
avatar_tick_content = """# 4-Element Orbital Aura (Flame, Water, Stone, Cloud)
scoreboard players remove @s avatar_state 1

# Quadrant 1: Fire (Front)
execute at @s run particle minecraft:flame ^1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 3 normal
execute at @s run particle minecraft:small_flame ^1.5 ^1.2 ^ 0.02 0.02 0.02 0.01 2 normal
# Quadrant 2: Water (Right)
execute at @s run particle minecraft:falling_water ^ ^1.2 ^1.5 0.05 0.05 0.05 0.01 4 normal
execute at @s run particle minecraft:splash ^ ^1.2 ^1.5 0.05 0.05 0.05 0.01 2 normal
# Quadrant 3: Earth (Back) - Fixed valid dust particle!
execute at @s run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.5} ^-1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 4 normal
# Quadrant 4: Air (Left)
execute at @s run particle minecraft:cloud ^ ^1.2 ^-1.5 0.05 0.05 0.05 0.01 3 normal
execute at @s run particle minecraft:poof ^ ^1.2 ^-1.5 0.05 0.05 0.05 0.01 2 normal

# End of Avatar State notice
execute if score @s avatar_state matches 0 run title @s title {"text":"Avatar State Exhausted","color":"gray"}
"""
with open(os.path.join(AVATAR_DIR, "tick.mcfunction"), "w", encoding="utf-8") as f:
    f.write(avatar_tick_content)

sphere_ultimate_content = """# Four-Element Orbital Sphere Cataclysm
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 50
playsound minecraft:entity.lightning_bolt.thunder player @a ~ ~ ~ 2.0 1.0
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2.0 0.7
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 2.0 0.8

# Quad-Element Cataclysm Ring
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:flame ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:splash ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.8} ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:cloud ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 2 normal

# Heavy Cumulative Quad Damage & Knockback
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run damage @s 32 minecraft:magic
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run tp @s ^ ^1.5 ^-3.0
"""
with open(os.path.join(AVATAR_DIR, "sphere_ultimate.mcfunction"), "w", encoding="utf-8") as f:
    f.write(sphere_ultimate_content)

print("Avatar State overhaul complete.")

# =============================================================================
# 6. FAILSAFE ROUTER & CHI GUARANTEE
# =============================================================================
router_content = """# ==============================================================================
# Avatar Skills - Cast Router (Minecraft Java 1.21.1)
# ==============================================================================

# Failsafe stat initialization & Chi recovery
execute unless score @s avatar_chi matches 1.. run scoreboard players set @s avatar_chi 100
execute unless score @s avatar_chi_max matches 1.. run scoreboard players set @s avatar_chi_max 100
execute unless score @s avatar_cd matches 0.. run scoreboard players set @s avatar_cd 0

# Skills ALWAYS trigger! If CD == 0, cast skill:
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"fire"}] run function avatar_skills:cast/fire_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"water"}] run function avatar_skills:cast/water_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"earth"}] run function avatar_skills:cast/earth_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"air"}] run function avatar_skills:cast/air_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"avatar"}] run function avatar_skills:cast/avatar_router

# Sub-Bending Foci
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"lightning"}] run function avatar_skills:cast/sub_lightning
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"combustion"}] run function avatar_skills:cast/sub_combustion
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"blood"}] run function avatar_skills:cast/sub_blood
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"healing"}] run function avatar_skills:cast/sub_healing
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"lava"}] run function avatar_skills:cast/sub_lava
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"metal"}] run function avatar_skills:cast/sub_metal
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"flight"}] run function avatar_skills:cast/sub_flight

# Mastery Tome & Chi Orb (Always usable regardless of Chi / Cooldown)
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] run function avatar_skills:tree/open_menu
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run function avatar_skills:tree/consume_chi_orb
"""
with open(os.path.join(CAST_DIR, "router.mcfunction"), "w", encoding="utf-8") as f:
    f.write(router_content)

# Update tick.mcfunction with Chi 0 auto-refill & fast regen
tick_content = """# ==============================================================================
# Avatar Skills - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# 0. Failsafe auto-initialize player stats for all online players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player
execute as @a unless score @s avatar_regen_timer matches 0.. run scoreboard players set @s avatar_regen_timer 0

# Failsafe: If Chi drops to 0 or below, auto-refill to 100
execute as @a if score @s avatar_chi matches ..0 run scoreboard players set @s avatar_chi 100

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

# Update consume_chi_orb.mcfunction
orb_content = """# Consume Chi Orb to gain Skill Points and instantly refill Chi to 100%
clear @s minecraft:warped_fungus_on_a_stick[custom_data~{avatar_skill:"chi_orb"}] 1
scoreboard players add @s av_chi_points 1
scoreboard players operation @s avatar_chi = @s avatar_chi_max
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.2 1.6
particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.05 20 normal
tellraw @s [{"text":"✨ [CHI MASTERY] ","color":"aqua","bold":true},{"text":"+1 Skill Point earned! ","color":"gold","bold":true},{"text":"Chi fully restored (100%)! Click Tome to upgrade.","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "consume_chi_orb.mcfunction"), "w", encoding="utf-8") as f:
    f.write(orb_content)

print("Router and tick loop updated.")

# =============================================================================
# 7. ZIP AND DEPLOY TO PRISMLAUNCHER INSTANCE
# =============================================================================
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

print("=== ALL EPIC SKILL OVERHAULS & PRISMLAUNCHER DEPLOYMENT COMPLETE ===")
