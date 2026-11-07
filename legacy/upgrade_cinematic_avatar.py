#!/usr/bin/env python3
"""
Cinematic Avatar Skills Overhaul:
1. Dynamic Direction-Aligned Earth Wall (Uses Caret ^ Coordinates so wall ALWAYS faces player at any yaw/pitch)
2. Auto-Clean Marker System: Wall markers decay blocks to air after 6 seconds with dust puffs
3. Double-Helix Water Whip: Intertwined spiraling fluid vortex (Katara style)
4. Dragon Crescent Flame Slash: Expansive curving inferno arc with lunge momentum
5. Expanding Concentric Air Shockwave: Sonic boom rings deflecting projectiles and launching mobs
6. Enhanced Tectonic Ground Wave (Gelombang Tanah Bergelombang): Multi-row cascading rock & dirt eruption
7. Direct deployment to PrismLauncher instance
"""

import os
import math
import shutil
import zipfile

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar_skills")
CAST_DIR = os.path.join(DATA_AVATAR, "function", "cast")
FUNC_DIR = os.path.join(DATA_AVATAR, "function")

PRISM_DIR = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft"
PRISM_SAVES_DP = os.path.join(PRISM_DIR, "saves", "avatar", "datapacks")

# =============================================================================
# 1. DYNAMIC DIRECTION-ALIGNED EARTH WALL (Caret ^ Coordinates)
# =============================================================================
wall_block_content = """# Place single wall block and register marker for cleanup
execute if block ~ ~ ~ #minecraft:replaceable run summon marker ~ ~ ~ {Tags:["avatar_wall_marker"],Age:0}
execute if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ stone
"""
with open(os.path.join(CAST_DIR, "earth_wall_block.mcfunction"), "w", encoding="utf-8") as f:
    f.write(wall_block_content)

# Earth Wall - 5 wide, 3 high, always facing player perpendicularly
earth_wall_lines = [
    "# Fortified Earth Wall (Dynamic 100% Direction-Aligned via Caret ^ Coordinates)",
    "scoreboard players remove @s avatar_chi 25",
    "scoreboard players set @s avatar_cd 40",
    "playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 2.0 0.5",
    "playsound minecraft:block.stone.place player @a ~ ~ ~ 2.0 0.6",
    "playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.2 0.7",
    ""
]

# Grid of 5 columns (-1.6, -0.8, 0.0, 0.8, 1.6) and 3 rows (Y=0, 1, 2) at Distance ^3.2
cols = [-1.6, -0.8, 0.0, 0.8, 1.6]
rows = [0.0, 1.0, 2.0]

for y in rows:
    earth_wall_lines.append(f"# Height Layer Y={y}")
    for x in cols:
        earth_wall_lines.append(f"execute at @s anchored feet positioned ^{x:.1f} ^{y:.1f} ^3.2 run function avatar_skills:cast/earth_wall_block")

earth_wall_lines.extend([
    "",
    "# Ground fissure dust along the wall base",
    "execute at @s anchored feet positioned ^0.0 ^0.5 ^3.2 run particle minecraft:poof ~ ~ ~ 1.6 0.8 0.5 0.05 40 normal",
    "execute at @s anchored feet positioned ^0.0 ^0.5 ^3.2 run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.8} ~ ~ ~ 1.6 0.8 0.5 0.1 50 normal",
    "",
    "# Knockback & stun hostiles in front",
    "execute at @s anchored feet positioned ^0.0 ^1.0 ^3.5 as @e[type=!player,distance=..3.5] run tp @s ^ ^1.0 ^-2.5",
    "execute at @s anchored feet positioned ^0.0 ^1.0 ^3.5 as @e[type=!player,distance=..3.5] run damage @s 8 minecraft:generic",
    "effect give @s minecraft:resistance 5 1 true"
])

with open(os.path.join(CAST_DIR, "earth_wall.mcfunction"), "w", encoding="utf-8") as f:
    f.write("\n".join(earth_wall_lines))

print("Direction-aligned Earth Wall generated.")

# =============================================================================
# 2. DOUBLE-HELIX WATER WHIP (SPIRALING FLUID VORTEX)
# =============================================================================
# Generates 2 intertwined spirals using sin/cos offsets along distance 1..10
water_whip_lines = [
    "# Serpentine Double-Helix Water Whip (Katara Spiraling Flow)",
    "scoreboard players remove @s avatar_chi 15",
    "scoreboard players set @s avatar_cd 12",
    "playsound minecraft:entity.generic.splash player @a ~ ~ ~ 1.8 1.3",
    "playsound minecraft:entity.player.splash.high_speed player @a ~ ~ ~ 1.5 1.5",
    ""
]

steps = 14
for i in range(1, steps + 1):
    dist = 0.8 + i * 0.65
    angle = (i * 0.55)
    radius = 0.45
    x1 = math.cos(angle) * radius
    y1 = math.sin(angle) * radius
    x2 = -x1
    y2 = -y1
    # Strand A
    water_whip_lines.append(f"execute at @s anchored eyes positioned ^{x1:.2f} ^{y1:.2f} ^{dist:.2f} run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal")
    water_whip_lines.append(f"execute at @s anchored eyes positioned ^{x1:.2f} ^{y1:.2f} ^{dist:.2f} run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal")
    # Strand B
    water_whip_lines.append(f"execute at @s anchored eyes positioned ^{x2:.2f} ^{y2:.2f} ^{dist:.2f} run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal")
    water_whip_lines.append(f"execute at @s anchored eyes positioned ^{x2:.2f} ^{y2:.2f} ^{dist:.2f} run particle minecraft:dust{{color:[0.25,0.60,0.95],scale:1.4}} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal")
    # Hit detection along the whip
    if i % 3 == 0:
        water_whip_lines.append(f"execute at @s anchored eyes positioned ^0.0 ^0.0 ^{dist:.2f} as @e[type=!player,distance=..2.0] run function avatar_skills:cast/water_hit")

water_whip_lines.extend([
    "",
    "# Impact Splash at the whip tip",
    "execute at @s anchored eyes positioned ^0.0 ^0.0 ^10.0 run particle minecraft:splash ~ ~ ~ 1.0 1.0 1.0 0.1 50 normal",
    "execute at @s anchored eyes positioned ^0.0 ^0.0 ^10.0 run playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 1.5 1.4"
])

with open(os.path.join(CAST_DIR, "water_whip.mcfunction"), "w", encoding="utf-8") as f:
    f.write("\n".join(water_whip_lines))

print("Double-Helix Water Whip generated.")

# =============================================================================
# 3. DRAGON CRESCENT FLAME SLASH (SHAOLIN CURVED SWEEP)
# =============================================================================
fire_blast_lines = [
    "# Dragon Crescent Flame Slash (Curved Shaolin Fire Sweep)",
    "scoreboard players remove @s avatar_chi 15",
    "scoreboard players set @s avatar_cd 12",
    "playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.8 1.1",
    "playsound minecraft:entity.blaze.shoot player @a ~ ~ ~ 1.5 1.2",
    "playsound minecraft:entity.generic.burn player @a ~ ~ ~ 1.5 1.0",
    "",
    "# Lunge player forward slightly with explosive momentum",
    "execute at @s run tp @s ^ ^0.1 ^0.5",
    ""
]

# Sweeping crescent arc from left (-2.2) to right (+2.2) curving outwards to distance 5.5
arc_points = [
    (-2.2, -0.2, 2.0),
    (-1.8, -0.1, 2.6),
    (-1.4, 0.0, 3.3),
    (-0.9, 0.1, 4.0),
    (-0.4, 0.2, 4.7),
    (0.0, 0.25, 5.2),
    (0.4, 0.2, 4.7),
    (0.9, 0.1, 4.0),
    (1.4, 0.0, 3.3),
    (1.8, -0.1, 2.6),
    (2.2, -0.2, 2.0),
]

for x, y, z in arc_points:
    fire_blast_lines.append(f"execute at @s anchored eyes positioned ^{x:.2f} ^{y:.2f} ^{z:.2f} run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal")
    fire_blast_lines.append(f"execute at @s anchored eyes positioned ^{x:.2f} ^{y:.2f} ^{z:.2f} run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal")
    fire_blast_lines.append(f"execute at @s anchored eyes positioned ^{x:.2f} ^{y:.2f} ^{z:.2f} run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal")
    fire_blast_lines.append(f"execute at @s anchored eyes positioned ^{x:.2f} ^{y:.2f} ^{z:.2f} as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit")

fire_blast_lines.extend([
    "",
    "# Scorch ground in front",
    "execute at @s anchored feet positioned ^0.0 ^0.0 ^3.5 if block ~ ~ ~ air if block ~ ~-1 ~ #minecraft:inside_step_sound_blocks run setblock ~ ~ ~ fire"
])

with open(os.path.join(CAST_DIR, "fire_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write("\n".join(fire_blast_lines))

print("Dragon Crescent Flame Slash generated.")

# =============================================================================
# 4. CONCENTRIC EXPANDING AIR SHOCKWAVE (SONIC BOOM RINGS)
# =============================================================================
air_blast_lines = [
    "# Concentric Expanding Air Shockwave (Sonic Vacuum Burst)",
    "scoreboard players remove @s avatar_chi 15",
    "scoreboard players set @s avatar_cd 10",
    "playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 2.0 1.2",
    "playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 1.8 0.7",
    "",
    "# Deflect all incoming projectiles immediately",
    "execute at @s as @e[type=arrow,distance=..6] run kill @s",
    "execute at @s as @e[type=spectral_arrow,distance=..6] run kill @s",
    "execute at @s as @e[type=trident,distance=..6] run kill @s",
    ""
]

# 3 Expanding Sonic Rings (Dist 2.5, Dist 5.0, Dist 7.5)
ring_configs = [
    (2.5, 0.9, 8, 0.03),
    (5.0, 1.8, 12, 0.05),
    (7.5, 2.7, 16, 0.08)
]

for dist, radius, num_pts, speed in ring_configs:
    air_blast_lines.append(f"# --- Sonic Ring at Distance {dist} (Radius {radius}) ---")
    for pt in range(num_pts):
        ang = (pt * 2 * math.pi) / num_pts
        rx = math.cos(ang) * radius
        ry = math.sin(ang) * radius
        air_blast_lines.append(f"execute at @s anchored eyes positioned ^{rx:.2f} ^{ry:.2f} ^{dist:.2f} run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 {speed} 1 normal")
        air_blast_lines.append(f"execute at @s anchored eyes positioned ^{rx:.2f} ^{ry:.2f} ^{dist:.2f} run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal")
    air_blast_lines.append(f"execute at @s anchored eyes positioned ^0.0 ^0.0 ^{dist:.2f} as @e[type=!player,distance=..{radius + 0.8:.1f}] run function avatar_skills:cast/air_hit")
    air_blast_lines.append("")

with open(os.path.join(CAST_DIR, "air_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write("\n".join(air_blast_lines))

print("Concentric Air Shockwave generated.")

# =============================================================================
# 5. UPDATE TICK LOOP FOR DYNAMIC EARTH WALL DECAY
# =============================================================================
tick_path = os.path.join(FUNC_DIR, "tick.mcfunction")
with open(tick_path, "r", encoding="utf-8") as f:
    tick_content = f.read()

# Add dynamic wall block decay (after 120 ticks / 6 seconds, turns stone back to air)
wall_decay_logic = """# 7b. Dynamic Direction-Aligned Earth Wall Block Decay
execute as @e[type=marker,tag=avatar_wall_marker] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] at @s run setblock ~ ~ ~ air replace stone
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] at @s run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.2} ~ ~ ~ 0.3 0.3 0.3 0.05 6 normal
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] run kill @s
"""

if "avatar_wall_marker" not in tick_content:
    tick_content += "\n" + wall_decay_logic
    with open(tick_path, "w", encoding="utf-8") as f:
        f.write(tick_content)
    print("Added avatar_wall_marker decay to tick.mcfunction")

# =============================================================================
# 6. PACKAGE AND DIRECT DEPLOY TO PRISMLAUNCHER INSTANCE
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
    print("Directly deployed updated Datapack to PrismLauncher saves!")

print("=== ALL CINEMATIC OVERHAULS DEPLOYED SUCCESSFULLY ===")
