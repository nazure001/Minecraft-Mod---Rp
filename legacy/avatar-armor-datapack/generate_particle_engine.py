import os
import json

base_dp = r"d:\repo\avatar-armor-datapack"
func_dir = os.path.join(base_dp, "data", "avatar", "function")
particles_dir = os.path.join(func_dir, "particles")
skill_dir = os.path.join(func_dir, "skill")
give_dir = os.path.join(func_dir, "give")

os.makedirs(particles_dir, exist_ok=True)
os.makedirs(skill_dir, exist_ok=True)
os.makedirs(give_dir, exist_ok=True)

nations = ["fire", "water", "earth", "air"]
tiers = ["initiate", "apprentice", "adept", "veteran", "master", "mythic", "sovereign"]

# -----------------------------------------------------------------------------
# 1. SETUP.MCFUNCTION
# -----------------------------------------------------------------------------
setup_content = """# ==============================================================================
# Avatar Armor Datapack - Setup (Minecraft 1.21.1)
# ==============================================================================
scoreboard objectives add avatar_set dummy "Avatar Armor Set ID"
scoreboard objectives add avatar_skill dummy "Avatar Active Skill Element"
scoreboard objectives add avatar_skill_timer dummy "Avatar Skill Duration Timer"
scoreboard objectives add avatar_tick dummy "Avatar Internal Tick Cycle"

# Default values
scoreboard players set @a avatar_skill 0
scoreboard players set @a avatar_skill_timer 0
scoreboard players set @a avatar_tick 0

tellraw @a [{"text":"[Avatar Armor] ","color":"gold","bold":true},{"text":"System initialized with 7 Tiers, 3D Headwear & Skill Combo Engine!","color":"green"}]
"""

with open(os.path.join(func_dir, "setup.mcfunction"), "w", encoding="utf-8") as f:
    f.write(setup_content)

# -----------------------------------------------------------------------------
# 2. TICK.MCFUNCTION
# -----------------------------------------------------------------------------
tick_content = """# ==============================================================================
# Avatar Armor Datapack - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# Increment global animation tick cycle (0..19)
scoreboard players add @a avatar_tick 1
execute as @a if score @s avatar_tick matches 20.. run scoreboard players set @s avatar_tick 0

# Tag-based Skill Ingestion (allows external mods/commands to trigger skills via simple tags)
execute as @a[tag=avatar.skill.fire] run function avatar:skill/cast_fire
execute as @a[tag=avatar.skill.fire] run tag @s remove avatar.skill.fire

execute as @a[tag=avatar.skill.water] run function avatar:skill/cast_water
execute as @a[tag=avatar.skill.water] run tag @s remove avatar.skill.water

execute as @a[tag=avatar.skill.earth] run function avatar:skill/cast_earth
execute as @a[tag=avatar.skill.earth] run tag @s remove avatar.skill.earth

execute as @a[tag=avatar.skill.air] run function avatar:skill/cast_air
execute as @a[tag=avatar.skill.air] run tag @s remove avatar.skill.air

# Countdown active skill duration timer
execute as @a[scores={avatar_skill_timer=1..}] run scoreboard players remove @s avatar_skill_timer 1
execute as @a[scores={avatar_skill_timer=0,avatar_skill=1..}] run scoreboard players set @s avatar_skill 0

# Reset active armor set status for all online players before detection
scoreboard players set @a avatar_set 0

# Fast nation routing: only execute nation check if player is wearing that nation's chestplate
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"fire"}}] run function avatar:detect/fire_nation
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"water"}}] run function avatar:detect/water_tribe
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"earth"}}] run function avatar:detect/earth_kingdom
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"air"}}] run function avatar:detect/air_nomad

# Particle & Elemental Combo Router (Executes for players wearing an Avatar Armor Set)
execute as @a[scores={avatar_set=11..47}] run function avatar:particles/router
"""

with open(os.path.join(func_dir, "tick.mcfunction"), "w", encoding="utf-8") as f:
    f.write(tick_content)

# -----------------------------------------------------------------------------
# 3. SKILL TRIGGER FUNCTIONS
# -----------------------------------------------------------------------------
skills_def = {
    "cast_fire": ("Fire", "1", "red", "flame"),
    "cast_water": ("Water", "2", "aqua", "splash"),
    "cast_earth": ("Earth", "3", "green", "block dirt"),
    "cast_air": ("Air", "4", "gold", "small_gust")
}

for sk_name, (elem, val, col, p_type) in skills_def.items():
    content = f"""# Avatar Armor Skill Cast - {elem}
scoreboard players set @s avatar_skill {val}
scoreboard players set @s avatar_skill_timer 80
particle minecraft:{p_type} ~ ~1 ~ 0.5 0.5 0.5 0.05 15 normal
title @s actionbar [{{"text":"[SKILL] ","color":"gold","bold":true}},{{"text":"{elem} Skill Activated (80 ticks)","color":"{col}"}}]
playsound minecraft:entity.illusioner.cast_spell player @s ~ ~ ~ 0.7 1.2
"""
    with open(os.path.join(skill_dir, f"{sk_name}.mcfunction"), "w", encoding="utf-8") as f:
        f.write(content)

# Clear skill function
with open(os.path.join(skill_dir, "clear.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Avatar Armor - Clear Skill
scoreboard players set @s avatar_skill 0
scoreboard players set @s avatar_skill_timer 0
title @s actionbar [{"text":"[SKILL] ","color":"gold","bold":true},{"text":"Skill Deactivated","color":"gray"}]
""")

# Demo test all combos
with open(os.path.join(skill_dir, "test_combos.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Avatar Armor - Test Combos Helper
tellraw @s [{"text":"=== [Avatar Skill Combo Test Commands] ===","color":"gold","bold":true}]
tellraw @s [{"text":"1. Cast Fire Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_fire]","color":"red","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_fire"}}]
tellraw @s [{"text":"2. Cast Water Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_water]","color":"aqua","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_water"}}]
tellraw @s [{"text":"3. Cast Earth Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_earth]","color":"green","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_earth"}}]
tellraw @s [{"text":"4. Cast Air Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_air]","color":"gold","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_air"}}]
tellraw @s [{"text":"5. Clear Skill: ","color":"yellow"},{"text":"[/function avatar:skill/clear]","color":"gray","clickEvent":{"action":"run_command","value":"/function avatar:skill/clear"}}]
""")

# -----------------------------------------------------------------------------
# 4. TIER IDLE PARTICLES (28 files)
# -----------------------------------------------------------------------------
# Clean, distinct animations that scale smoothly from Initiate to Sovereign Godplate
for nat in nations:
    for t_idx, t in enumerate(tiers, start=1):
        lines = [f"# Avatar Armor Datapack - {nat.capitalize()} {t.capitalize()} Idle Particles"]
        
        # Fire
        if nat == "fire":
            if t_idx == 1:
                lines.append("particle minecraft:flame ~ ~0.2 ~ 0.15 0.1 0.15 0.01 1 normal")
            elif t_idx == 2:
                lines.append("particle minecraft:flame ~ ~0.5 ~ 0.25 0.25 0.25 0.01 2 normal")
                lines.append("particle minecraft:smoke ~ ~0.9 ~ 0.2 0.2 0.2 0.01 1 normal")
            elif t_idx == 3:
                lines.append("particle minecraft:flame ~ ~0.8 ~ 0.3 0.4 0.3 0.02 3 normal")
                lines.append("particle minecraft:smoke ~ ~1.1 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 4:
                lines.append("particle minecraft:flame ~ ~0.9 ~ 0.35 0.5 0.35 0.02 5 normal")
                lines.append("particle minecraft:small_flame ~ ~0.4 ~ 0.3 0.3 0.3 0.01 3 normal")
            elif t_idx == 5:
                lines.append("particle minecraft:flame ~ ~1.0 ~ 0.4 0.6 0.4 0.02 7 normal")
                lines.append("particle minecraft:lava ~ ~0.6 ~ 0.2 0.2 0.2 0.01 1 normal")
                lines.append("particle minecraft:smoke ~ ~1.4 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 6:
                lines.append("particle minecraft:flame ~ ~1.1 ~ 0.45 0.7 0.45 0.03 10 normal")
                lines.append("particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.4 0.3 0.02 3 normal")
                lines.append("particle minecraft:lava ~ ~1.0 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 7: # Sovereign Dragon Godplate
                lines.append("particle minecraft:flame ~ ~1.0 ~ 0.5 0.8 0.5 0.03 12 normal")
                lines.append("particle minecraft:soul_fire_flame ~ ~0.7 ~ 0.4 0.5 0.4 0.02 6 normal")
                lines.append("particle minecraft:lava ~ ~1.2 ~ 0.3 0.3 0.3 0.02 3 normal")
                lines.append("particle minecraft:smoke ~ ~1.6 ~ 0.3 0.3 0.3 0.01 4 normal")

        # Water
        elif nat == "water":
            if t_idx == 1:
                lines.append("particle minecraft:splash ~ ~0.2 ~ 0.15 0.1 0.15 0.01 1 normal")
            elif t_idx == 2:
                lines.append("particle minecraft:splash ~ ~0.5 ~ 0.25 0.25 0.25 0.01 2 normal")
                lines.append("particle minecraft:dripping_water ~ ~0.8 ~ 0.2 0.2 0.2 0.01 1 normal")
            elif t_idx == 3:
                lines.append("particle minecraft:splash ~ ~0.8 ~ 0.3 0.4 0.3 0.02 4 normal")
                lines.append("particle minecraft:dripping_water ~ ~1.1 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 4:
                lines.append("particle minecraft:splash ~ ~0.9 ~ 0.35 0.5 0.35 0.02 6 normal")
                lines.append("particle minecraft:bubble_pop ~ ~0.5 ~ 0.3 0.3 0.3 0.01 3 normal")
            elif t_idx == 5:
                lines.append("particle minecraft:splash ~ ~1.0 ~ 0.4 0.6 0.4 0.02 8 normal")
                lines.append("particle minecraft:bubble_pop ~ ~0.7 ~ 0.35 0.4 0.35 0.02 4 normal")
                lines.append("particle minecraft:falling_water ~ ~1.3 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 6:
                lines.append("particle minecraft:splash ~ ~1.1 ~ 0.45 0.7 0.45 0.03 12 normal")
                lines.append("particle minecraft:bubble_pop ~ ~0.8 ~ 0.4 0.5 0.4 0.02 6 normal")
                lines.append("particle minecraft:rain ~ ~1.2 ~ 0.4 0.4 0.4 0.02 4 normal")
            elif t_idx == 7: # Sovereign Ocean Spirit
                lines.append("particle minecraft:splash ~ ~1.0 ~ 0.5 0.8 0.5 0.03 14 normal")
                lines.append("particle minecraft:bubble_pop ~ ~0.8 ~ 0.45 0.6 0.45 0.02 8 normal")
                lines.append("particle minecraft:rain ~ ~1.3 ~ 0.5 0.5 0.5 0.02 6 normal")
                lines.append("particle minecraft:dripping_water ~ ~1.6 ~ 0.3 0.3 0.3 0.01 4 normal")

        # Earth
        elif nat == "earth":
            if t_idx == 1:
                lines.append("particle minecraft:block dirt ~ ~0.1 ~ 0.15 0.05 0.15 0.01 1 normal")
            elif t_idx == 2:
                lines.append("particle minecraft:block dirt ~ ~0.3 ~ 0.25 0.15 0.25 0.01 2 normal")
                lines.append("particle minecraft:falling_dust dirt ~ ~0.7 ~ 0.2 0.2 0.2 0.01 1 normal")
            elif t_idx == 3:
                lines.append("particle minecraft:block dirt ~ ~0.5 ~ 0.3 0.3 0.3 0.02 3 normal")
                lines.append("particle minecraft:spore_blossom_air ~ ~0.9 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 4:
                lines.append("particle minecraft:block dirt ~ ~0.6 ~ 0.35 0.4 0.35 0.02 5 normal")
                lines.append("particle minecraft:dust 0.1 0.8 0.4 1.0 ~ ~0.5 ~ 0.3 0.3 0.3 0.01 3 normal")
            elif t_idx == 5:
                lines.append("particle minecraft:block dirt ~ ~0.8 ~ 0.4 0.5 0.4 0.02 7 normal")
                lines.append("particle minecraft:dust 0.1 0.8 0.4 1.2 ~ ~0.7 ~ 0.35 0.4 0.35 0.01 4 normal")
                lines.append("particle minecraft:falling_obsidian_tear ~ ~1.2 ~ 0.2 0.2 0.2 0.01 1 normal")
            elif t_idx == 6:
                lines.append("particle minecraft:block dirt ~ ~0.9 ~ 0.45 0.6 0.45 0.03 9 normal")
                lines.append("particle minecraft:dust 0.05 0.9 0.45 1.5 ~ ~0.8 ~ 0.4 0.5 0.4 0.02 6 normal")
                lines.append("particle minecraft:falling_obsidian_tear ~ ~1.3 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 7: # Sovereign Titan Bedrock
                lines.append("particle minecraft:block emerald_block ~ ~0.8 ~ 0.5 0.7 0.5 0.03 10 normal")
                lines.append("particle minecraft:dust 0.1 0.95 0.5 1.8 ~ ~0.9 ~ 0.45 0.6 0.45 0.02 8 normal")
                lines.append("particle minecraft:falling_obsidian_tear ~ ~1.4 ~ 0.3 0.3 0.3 0.02 4 normal")
                lines.append("particle minecraft:block dirt ~ ~0.3 ~ 0.4 0.2 0.4 0.01 5 normal")

        # Air
        elif nat == "air":
            if t_idx == 1:
                lines.append("particle minecraft:cloud ~ ~0.2 ~ 0.15 0.1 0.15 0.01 1 normal")
            elif t_idx == 2:
                lines.append("particle minecraft:cloud ~ ~0.5 ~ 0.25 0.25 0.25 0.01 2 normal")
                lines.append("particle minecraft:small_gust ~ ~0.7 ~ 0.2 0.2 0.2 0.01 1 normal")
            elif t_idx == 3:
                lines.append("particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.4 0.3 0.02 3 normal")
                lines.append("particle minecraft:cloud ~ ~1.0 ~ 0.25 0.25 0.25 0.01 2 normal")
            elif t_idx == 4:
                lines.append("particle minecraft:small_gust ~ ~0.9 ~ 0.35 0.5 0.35 0.02 5 normal")
                lines.append("particle minecraft:gust ~ ~0.6 ~ 0.3 0.3 0.3 0.01 2 normal")
            elif t_idx == 5:
                lines.append("particle minecraft:small_gust ~ ~1.0 ~ 0.4 0.6 0.4 0.02 7 normal")
                lines.append("particle minecraft:gust ~ ~0.8 ~ 0.35 0.4 0.35 0.02 3 normal")
                lines.append("particle minecraft:cloud ~ ~1.3 ~ 0.3 0.3 0.3 0.01 3 normal")
            elif t_idx == 6:
                lines.append("particle minecraft:small_gust ~ ~1.1 ~ 0.45 0.7 0.45 0.03 9 normal")
                lines.append("particle minecraft:gust ~ ~0.9 ~ 0.4 0.5 0.4 0.02 4 normal")
                lines.append("particle minecraft:electric_spark ~ ~1.2 ~ 0.35 0.35 0.35 0.02 3 normal")
            elif t_idx == 7: # Sovereign Divine Nimbus
                lines.append("particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.5 0.7 0.5 0.03 2 normal")
                lines.append("particle minecraft:small_gust ~ ~1.2 ~ 0.5 0.8 0.5 0.03 10 normal")
                lines.append("particle minecraft:cloud ~ ~1.5 ~ 0.4 0.4 0.4 0.02 5 normal")
                lines.append("particle minecraft:electric_spark ~ ~1.3 ~ 0.4 0.4 0.4 0.02 5 normal")

        with open(os.path.join(particles_dir, f"{nat}_{t}.mcfunction"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

print("Generated 28 tier idle particle functions!")

# -----------------------------------------------------------------------------
# 5. COMBO PARTICLES (STEAM, MAGMA, FIRESTORM, TYPHOON, MUD, SANDSTORM, RESONANCES)
# -----------------------------------------------------------------------------

# A. STEAM / VAPOR (Water Armor + Fire Skill, or Fire Armor + Water Skill)
steam_content = """# Elemental Combo: Steam / Scalding Vapor (Water + Fire)
# Tier 1..2 (Low)
execute if score @s avatar_set matches 11..12 run particle minecraft:cloud ~ ~0.8 ~ 0.25 0.3 0.25 0.02 3 normal
execute if score @s avatar_set matches 21..22 run particle minecraft:cloud ~ ~0.8 ~ 0.25 0.3 0.25 0.02 3 normal

# Tier 3..4 (Medium)
execute if score @s avatar_set matches 13..14 run particle minecraft:cloud ~ ~1.0 ~ 0.4 0.5 0.4 0.03 6 normal
execute if score @s avatar_set matches 13..14 run particle minecraft:bubble_pop ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3 normal
execute if score @s avatar_set matches 23..24 run particle minecraft:cloud ~ ~1.0 ~ 0.4 0.5 0.4 0.03 6 normal
execute if score @s avatar_set matches 23..24 run particle minecraft:bubble_pop ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3 normal

# Tier 5..6 (High)
execute if score @s avatar_set matches 15..16 run particle minecraft:campfire_cosy_smoke ~ ~1.1 ~ 0.45 0.6 0.45 0.03 5 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:splash ~ ~0.7 ~ 0.4 0.3 0.4 0.02 6 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:campfire_cosy_smoke ~ ~1.1 ~ 0.45 0.6 0.45 0.03 5 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:splash ~ ~0.7 ~ 0.4 0.3 0.4 0.02 6 normal

# Tier 7 (Sovereign Superheated Vapor Geyser)
execute if score @s avatar_set matches 17 run particle minecraft:campfire_cosy_smoke ~ ~1.3 ~ 0.6 0.8 0.6 0.04 8 normal
execute if score @s avatar_set matches 17 run particle minecraft:cloud ~ ~1.2 ~ 0.5 0.7 0.5 0.03 10 normal
execute if score @s avatar_set matches 17 run particle minecraft:splash ~ ~0.8 ~ 0.5 0.4 0.5 0.03 10 normal
execute if score @s avatar_set matches 17 run particle minecraft:flame ~ ~0.6 ~ 0.3 0.3 0.3 0.02 4 normal

execute if score @s avatar_set matches 27 run particle minecraft:campfire_cosy_smoke ~ ~1.3 ~ 0.6 0.8 0.6 0.04 8 normal
execute if score @s avatar_set matches 27 run particle minecraft:cloud ~ ~1.2 ~ 0.5 0.7 0.5 0.03 10 normal
execute if score @s avatar_set matches 27 run particle minecraft:splash ~ ~0.8 ~ 0.5 0.4 0.5 0.03 10 normal
execute if score @s avatar_set matches 27 run particle minecraft:flame ~ ~0.6 ~ 0.3 0.3 0.3 0.02 4 normal
"""
with open(os.path.join(particles_dir, "combo_steam.mcfunction"), "w", encoding="utf-8") as f:
    f.write(steam_content)

# B. MAGMA / VOLCANIC ERUPTION (Fire Armor + Earth Skill, or Earth Armor + Fire Skill)
magma_content = """# Elemental Combo: Magma / Volcanic Eruption (Fire + Earth)
# Tier 1..2
execute if score @s avatar_set matches 11..12 run particle minecraft:lava ~ ~0.7 ~ 0.25 0.25 0.25 0.01 2 normal
execute if score @s avatar_set matches 31..32 run particle minecraft:lava ~ ~0.7 ~ 0.25 0.25 0.25 0.01 2 normal

# Tier 3..4
execute if score @s avatar_set matches 13..14 run particle minecraft:lava ~ ~0.9 ~ 0.35 0.4 0.35 0.02 4 normal
execute if score @s avatar_set matches 13..14 run particle minecraft:falling_obsidian_tear ~ ~1.2 ~ 0.3 0.3 0.3 0.01 2 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:lava ~ ~0.9 ~ 0.35 0.4 0.35 0.02 4 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:falling_obsidian_tear ~ ~1.2 ~ 0.3 0.3 0.3 0.01 2 normal

# Tier 5..6
execute if score @s avatar_set matches 15..16 run particle minecraft:lava ~ ~1.1 ~ 0.45 0.6 0.45 0.02 6 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:flame ~ ~0.8 ~ 0.4 0.4 0.4 0.02 8 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:lava ~ ~1.1 ~ 0.45 0.6 0.45 0.02 6 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:flame ~ ~0.8 ~ 0.4 0.4 0.4 0.02 8 normal

# Tier 7 (Sovereign Caldera Eruption)
execute if score @s avatar_set matches 17 run particle minecraft:lava ~ ~1.3 ~ 0.6 0.8 0.6 0.03 10 normal
execute if score @s avatar_set matches 17 run particle minecraft:landing_lava ~ ~0.4 ~ 0.6 0.2 0.6 0.02 6 normal
execute if score @s avatar_set matches 17 run particle minecraft:flame ~ ~1.0 ~ 0.5 0.6 0.5 0.03 12 normal
execute if score @s avatar_set matches 17 run particle minecraft:falling_obsidian_tear ~ ~1.5 ~ 0.4 0.4 0.4 0.02 5 normal

execute if score @s avatar_set matches 37 run particle minecraft:lava ~ ~1.3 ~ 0.6 0.8 0.6 0.03 10 normal
execute if score @s avatar_set matches 37 run particle minecraft:landing_lava ~ ~0.4 ~ 0.6 0.2 0.6 0.02 6 normal
execute if score @s avatar_set matches 37 run particle minecraft:flame ~ ~1.0 ~ 0.5 0.6 0.5 0.03 12 normal
execute if score @s avatar_set matches 37 run particle minecraft:falling_obsidian_tear ~ ~1.5 ~ 0.4 0.4 0.4 0.02 5 normal
"""
with open(os.path.join(particles_dir, "combo_magma.mcfunction"), "w", encoding="utf-8") as f:
    f.write(magma_content)

# C. FIRESTORM / FIRE TORNADO (Air Armor + Fire Skill, or Fire Armor + Air Skill)
firestorm_content = """# Elemental Combo: Firestorm / Fire Tornado (Air + Fire)
# Tier 1..2
execute if score @s avatar_set matches 11..12 run particle minecraft:flame ~ ~0.6 ~ 0.25 0.3 0.25 0.02 3 normal
execute if score @s avatar_set matches 41..42 run particle minecraft:flame ~ ~0.6 ~ 0.25 0.3 0.25 0.02 3 normal

# Tier 3..4
execute if score @s avatar_set matches 13..14 run particle minecraft:flame ~ ~0.9 ~ 0.35 0.5 0.35 0.03 6 normal
execute if score @s avatar_set matches 13..14 run particle minecraft:small_gust ~ ~0.8 ~ 0.3 0.3 0.3 0.02 2 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:flame ~ ~0.9 ~ 0.35 0.5 0.35 0.03 6 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:small_gust ~ ~0.8 ~ 0.3 0.3 0.3 0.02 2 normal

# Tier 5..6
execute if score @s avatar_set matches 15..16 run particle minecraft:flame ~ ~1.1 ~ 0.45 0.6 0.45 0.03 10 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:small_gust ~ ~1.0 ~ 0.4 0.4 0.4 0.03 4 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:flame ~ ~1.1 ~ 0.45 0.6 0.45 0.03 10 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:small_gust ~ ~1.0 ~ 0.4 0.4 0.4 0.03 4 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3 normal

# Tier 7 (Sovereign Solar Firestorm)
execute if score @s avatar_set matches 17 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 17 run particle minecraft:flame ~ ~1.2 ~ 0.6 0.8 0.6 0.04 15 normal
execute if score @s avatar_set matches 17 run particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.4 0.5 0.4 0.03 6 normal
execute if score @s avatar_set matches 17 run particle minecraft:smoke ~ ~1.6 ~ 0.4 0.4 0.4 0.02 4 normal

execute if score @s avatar_set matches 47 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 47 run particle minecraft:flame ~ ~1.2 ~ 0.6 0.8 0.6 0.04 15 normal
execute if score @s avatar_set matches 47 run particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.4 0.5 0.4 0.03 6 normal
execute if score @s avatar_set matches 47 run particle minecraft:smoke ~ ~1.6 ~ 0.4 0.4 0.4 0.02 4 normal
"""
with open(os.path.join(particles_dir, "combo_firestorm.mcfunction"), "w", encoding="utf-8") as f:
    f.write(firestorm_content)

# D. TYPHOON / MONSOON (Air Armor + Water Skill, or Water Armor + Air Skill)
typhoon_content = """# Elemental Combo: Typhoon / Tempest Monsoon (Air + Water)
# Tier 1..2
execute if score @s avatar_set matches 21..22 run particle minecraft:rain ~ ~0.8 ~ 0.25 0.3 0.25 0.02 4 normal
execute if score @s avatar_set matches 41..42 run particle minecraft:rain ~ ~0.8 ~ 0.25 0.3 0.25 0.02 4 normal

# Tier 3..4
execute if score @s avatar_set matches 23..24 run particle minecraft:rain ~ ~1.0 ~ 0.4 0.5 0.4 0.03 8 normal
execute if score @s avatar_set matches 23..24 run particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.3 0.3 0.02 2 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:rain ~ ~1.0 ~ 0.4 0.5 0.4 0.03 8 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.3 0.3 0.02 2 normal

# Tier 5..6
execute if score @s avatar_set matches 25..26 run particle minecraft:rain ~ ~1.2 ~ 0.5 0.6 0.5 0.03 14 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:splash ~ ~0.8 ~ 0.4 0.4 0.4 0.03 6 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:small_gust ~ ~1.0 ~ 0.4 0.4 0.4 0.02 4 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:rain ~ ~1.2 ~ 0.5 0.6 0.5 0.03 14 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:splash ~ ~0.8 ~ 0.4 0.4 0.4 0.03 6 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:small_gust ~ ~1.0 ~ 0.4 0.4 0.4 0.02 4 normal

# Tier 7 (Sovereign Primordial Typhoon)
execute if score @s avatar_set matches 27 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 27 run particle minecraft:rain ~ ~1.3 ~ 0.6 0.8 0.6 0.04 20 normal
execute if score @s avatar_set matches 27 run particle minecraft:splash ~ ~0.9 ~ 0.5 0.5 0.5 0.03 10 normal
execute if score @s avatar_set matches 27 run particle minecraft:cloud ~ ~1.5 ~ 0.5 0.4 0.5 0.02 5 normal

execute if score @s avatar_set matches 47 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 47 run particle minecraft:rain ~ ~1.3 ~ 0.6 0.8 0.6 0.04 20 normal
execute if score @s avatar_set matches 47 run particle minecraft:splash ~ ~0.9 ~ 0.5 0.5 0.5 0.03 10 normal
execute if score @s avatar_set matches 47 run particle minecraft:cloud ~ ~1.5 ~ 0.5 0.4 0.5 0.02 5 normal
"""
with open(os.path.join(particles_dir, "combo_typhoon.mcfunction"), "w", encoding="utf-8") as f:
    f.write(typhoon_content)

# E. MUD / QUAGMIRE (Water Armor + Earth Skill, or Earth Armor + Water Skill)
mud_content = """# Elemental Combo: Mud / Quagmire Surge (Water + Earth)
# Tier 1..2
execute if score @s avatar_set matches 21..22 run particle minecraft:block dirt ~ ~0.3 ~ 0.25 0.15 0.25 0.01 2 normal
execute if score @s avatar_set matches 31..32 run particle minecraft:block dirt ~ ~0.3 ~ 0.25 0.15 0.25 0.01 2 normal

# Tier 3..4
execute if score @s avatar_set matches 23..24 run particle minecraft:block dirt ~ ~0.5 ~ 0.35 0.3 0.35 0.02 4 normal
execute if score @s avatar_set matches 23..24 run particle minecraft:splash ~ ~0.4 ~ 0.3 0.2 0.3 0.02 3 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:block dirt ~ ~0.5 ~ 0.35 0.3 0.35 0.02 4 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:splash ~ ~0.4 ~ 0.3 0.2 0.3 0.02 3 normal

# Tier 5..6
execute if score @s avatar_set matches 25..26 run particle minecraft:block dirt ~ ~0.7 ~ 0.45 0.4 0.45 0.02 8 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:spore_blossom_air ~ ~0.9 ~ 0.4 0.4 0.4 0.02 5 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:block dirt ~ ~0.7 ~ 0.45 0.4 0.45 0.02 8 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:spore_blossom_air ~ ~0.9 ~ 0.4 0.4 0.4 0.02 5 normal

# Tier 7 (Sovereign Terra-Hydra Mud Geyser)
execute if score @s avatar_set matches 27 run particle minecraft:block mud ~ ~0.8 ~ 0.6 0.6 0.6 0.03 12 normal
execute if score @s avatar_set matches 27 run particle minecraft:splash ~ ~0.6 ~ 0.5 0.3 0.5 0.03 8 normal
execute if score @s avatar_set matches 27 run particle minecraft:spore_blossom_air ~ ~1.2 ~ 0.5 0.5 0.5 0.02 8 normal
execute if score @s avatar_set matches 27 run particle minecraft:witch ~ ~1.0 ~ 0.4 0.4 0.4 0.02 5 normal

execute if score @s avatar_set matches 37 run particle minecraft:block mud ~ ~0.8 ~ 0.6 0.6 0.6 0.03 12 normal
execute if score @s avatar_set matches 37 run particle minecraft:splash ~ ~0.6 ~ 0.5 0.3 0.5 0.03 8 normal
execute if score @s avatar_set matches 37 run particle minecraft:spore_blossom_air ~ ~1.2 ~ 0.5 0.5 0.5 0.02 8 normal
execute if score @s avatar_set matches 37 run particle minecraft:witch ~ ~1.0 ~ 0.4 0.4 0.4 0.02 5 normal
"""
with open(os.path.join(particles_dir, "combo_mud.mcfunction"), "w", encoding="utf-8") as f:
    f.write(mud_content)

# F. SANDSTORM / DESERT TEMPEST (Earth Armor + Air Skill, or Air Armor + Earth Skill)
sandstorm_content = """# Elemental Combo: Sandstorm / Desert Tempest (Earth + Air)
# Tier 1..2
execute if score @s avatar_set matches 31..32 run particle minecraft:block sand ~ ~0.4 ~ 0.25 0.25 0.25 0.01 2 normal
execute if score @s avatar_set matches 41..42 run particle minecraft:block sand ~ ~0.4 ~ 0.25 0.25 0.25 0.01 2 normal

# Tier 3..4
execute if score @s avatar_set matches 33..34 run particle minecraft:block sand ~ ~0.8 ~ 0.35 0.4 0.35 0.02 5 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.3 0.3 0.02 2 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:block sand ~ ~0.8 ~ 0.35 0.4 0.35 0.02 5 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.3 0.3 0.02 2 normal

# Tier 5..6
execute if score @s avatar_set matches 35..36 run particle minecraft:block sand ~ ~1.0 ~ 0.5 0.5 0.5 0.03 9 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:small_gust ~ ~0.9 ~ 0.4 0.4 0.4 0.02 4 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:dust 0.85 0.70 0.35 1.5 ~ ~0.8 ~ 0.4 0.4 0.4 0.02 6 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:block sand ~ ~1.0 ~ 0.5 0.5 0.5 0.03 9 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:small_gust ~ ~0.9 ~ 0.4 0.4 0.4 0.02 4 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:dust 0.85 0.70 0.35 1.5 ~ ~0.8 ~ 0.4 0.4 0.4 0.02 6 normal

# Tier 7 (Sovereign Haboob Sand Cataclysm)
execute if score @s avatar_set matches 37 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 37 run particle minecraft:block sand ~ ~1.2 ~ 0.6 0.7 0.6 0.04 15 normal
execute if score @s avatar_set matches 37 run particle minecraft:dust 0.90 0.75 0.40 2.0 ~ ~1.0 ~ 0.5 0.6 0.5 0.03 10 normal
execute if score @s avatar_set matches 37 run particle minecraft:cloud ~ ~1.4 ~ 0.4 0.4 0.4 0.02 4 normal

execute if score @s avatar_set matches 47 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 2 normal
execute if score @s avatar_set matches 47 run particle minecraft:block sand ~ ~1.2 ~ 0.6 0.7 0.6 0.04 15 normal
execute if score @s avatar_set matches 47 run particle minecraft:dust 0.90 0.75 0.40 2.0 ~ ~1.0 ~ 0.5 0.6 0.5 0.03 10 normal
execute if score @s avatar_set matches 47 run particle minecraft:cloud ~ ~1.4 ~ 0.4 0.4 0.4 0.02 4 normal
"""
with open(os.path.join(particles_dir, "combo_sandstorm.mcfunction"), "w", encoding="utf-8") as f:
    f.write(sandstorm_content)

# G. SAME ELEMENT RESONANCE (Fire+Fire, Water+Water, Earth+Earth, Air+Air)
res_fire = """# Elemental Resonance: Pure Fire Overdrive (Fire Armor + Fire Skill)
execute if score @s avatar_set matches 11..12 run particle minecraft:flame ~ ~0.7 ~ 0.3 0.4 0.3 0.02 6 normal
execute if score @s avatar_set matches 13..14 run particle minecraft:flame ~ ~0.9 ~ 0.4 0.5 0.4 0.03 12 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:flame ~ ~1.1 ~ 0.5 0.7 0.5 0.03 18 normal
execute if score @s avatar_set matches 15..16 run particle minecraft:lava ~ ~0.8 ~ 0.3 0.3 0.3 0.02 3 normal
execute if score @s avatar_set matches 17 run particle minecraft:flame ~ ~1.2 ~ 0.6 0.9 0.6 0.04 25 normal
execute if score @s avatar_set matches 17 run particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.4 0.6 0.4 0.03 10 normal
execute if score @s avatar_set matches 17 run particle minecraft:lava ~ ~1.0 ~ 0.4 0.4 0.4 0.02 5 normal
"""
with open(os.path.join(particles_dir, "resonance_fire.mcfunction"), "w", encoding="utf-8") as f:
    f.write(res_fire)

res_water = """# Elemental Resonance: Pure Water Overdrive (Water Armor + Water Skill)
execute if score @s avatar_set matches 21..22 run particle minecraft:splash ~ ~0.7 ~ 0.3 0.4 0.3 0.02 6 normal
execute if score @s avatar_set matches 23..24 run particle minecraft:splash ~ ~0.9 ~ 0.4 0.5 0.4 0.03 12 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:splash ~ ~1.1 ~ 0.5 0.7 0.5 0.03 18 normal
execute if score @s avatar_set matches 25..26 run particle minecraft:bubble_pop ~ ~0.8 ~ 0.35 0.4 0.35 0.02 6 normal
execute if score @s avatar_set matches 27 run particle minecraft:splash ~ ~1.2 ~ 0.6 0.9 0.6 0.04 25 normal
execute if score @s avatar_set matches 27 run particle minecraft:bubble_pop ~ ~0.9 ~ 0.5 0.6 0.5 0.03 12 normal
execute if score @s avatar_set matches 27 run particle minecraft:rain ~ ~1.4 ~ 0.5 0.5 0.5 0.03 8 normal
"""
with open(os.path.join(particles_dir, "resonance_water.mcfunction"), "w", encoding="utf-8") as f:
    f.write(res_water)

res_earth = """# Elemental Resonance: Pure Earth Overdrive (Earth Armor + Earth Skill)
execute if score @s avatar_set matches 31..32 run particle minecraft:block dirt ~ ~0.4 ~ 0.3 0.2 0.3 0.02 6 normal
execute if score @s avatar_set matches 33..34 run particle minecraft:dust 0.1 0.8 0.4 1.2 ~ ~0.7 ~ 0.4 0.4 0.4 0.02 8 normal
execute if score @s avatar_set matches 35..36 run particle minecraft:block emerald_block ~ ~0.9 ~ 0.5 0.6 0.5 0.03 12 normal
execute if score @s avatar_set matches 37 run particle minecraft:block emerald_block ~ ~1.0 ~ 0.6 0.8 0.6 0.04 18 normal
execute if score @s avatar_set matches 37 run particle minecraft:dust 0.1 0.95 0.5 2.0 ~ ~1.1 ~ 0.5 0.6 0.5 0.03 14 normal
execute if score @s avatar_set matches 37 run particle minecraft:falling_obsidian_tear ~ ~1.3 ~ 0.3 0.3 0.3 0.02 6 normal
"""
with open(os.path.join(particles_dir, "resonance_earth.mcfunction"), "w", encoding="utf-8") as f:
    f.write(res_earth)

res_air = """# Elemental Resonance: Pure Air Overdrive (Air Armor + Air Skill)
execute if score @s avatar_set matches 41..42 run particle minecraft:small_gust ~ ~0.7 ~ 0.3 0.3 0.3 0.02 4 normal
execute if score @s avatar_set matches 43..44 run particle minecraft:small_gust ~ ~0.9 ~ 0.4 0.4 0.4 0.03 8 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:small_gust ~ ~1.1 ~ 0.5 0.6 0.5 0.03 14 normal
execute if score @s avatar_set matches 45..46 run particle minecraft:gust ~ ~0.8 ~ 0.4 0.4 0.4 0.02 4 normal
execute if score @s avatar_set matches 47 run particle minecraft:gust_emitter_large ~ ~1.0 ~ 0.6 0.8 0.6 0.04 3 normal
execute if score @s avatar_set matches 47 run particle minecraft:small_gust ~ ~1.2 ~ 0.6 0.8 0.6 0.04 18 normal
execute if score @s avatar_set matches 47 run particle minecraft:electric_spark ~ ~1.3 ~ 0.4 0.4 0.4 0.03 8 normal
"""
with open(os.path.join(particles_dir, "resonance_air.mcfunction"), "w", encoding="utf-8") as f:
    f.write(res_air)

# -----------------------------------------------------------------------------
# 6. MASTER PARTICLES ROUTER
# -----------------------------------------------------------------------------
router_lines = [
    "# ==============================================================================",
    "# Avatar Armor Datapack - Master Particle & Skill Combo Router",
    "# ==============================================================================",
    "",
    "# -----------------------------------------------------------------------------",
    "# CASE 1: NO ACTIVE SKILL (Idle Ambient Tier Particles)",
    "# -----------------------------------------------------------------------------",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 11 run function avatar:particles/fire_initiate",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 12 run function avatar:particles/fire_apprentice",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 13 run function avatar:particles/fire_adept",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 14 run function avatar:particles/fire_veteran",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 15 run function avatar:particles/fire_master",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 16 run function avatar:particles/fire_mythic",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 17 run function avatar:particles/fire_sovereign",
    "",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 21 run function avatar:particles/water_initiate",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 22 run function avatar:particles/water_apprentice",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 23 run function avatar:particles/water_adept",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 24 run function avatar:particles/water_veteran",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 25 run function avatar:particles/water_master",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 26 run function avatar:particles/water_mythic",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 27 run function avatar:particles/water_sovereign",
    "",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 31 run function avatar:particles/earth_initiate",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 32 run function avatar:particles/earth_apprentice",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 33 run function avatar:particles/earth_adept",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 34 run function avatar:particles/earth_veteran",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 35 run function avatar:particles/earth_master",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 36 run function avatar:particles/earth_mythic",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 37 run function avatar:particles/earth_sovereign",
    "",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 41 run function avatar:particles/air_initiate",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 42 run function avatar:particles/air_apprentice",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 43 run function avatar:particles/air_adept",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 44 run function avatar:particles/air_veteran",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 45 run function avatar:particles/air_master",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 46 run function avatar:particles/air_mythic",
    "execute if score @s avatar_skill matches 0 if score @s avatar_set matches 47 run function avatar:particles/air_sovereign",
    "",
    "# -----------------------------------------------------------------------------",
    "# CASE 2: CROSS-ELEMENT COMBOS (Skill != Armor Element)",
    "# -----------------------------------------------------------------------------",
    "# Steam: Water Armor (21..27) + Fire Skill (1) OR Fire Armor (11..17) + Water Skill (2)",
    "execute if score @s avatar_skill matches 1 if score @s avatar_set matches 21..27 run function avatar:particles/combo_steam",
    "execute if score @s avatar_skill matches 2 if score @s avatar_set matches 11..17 run function avatar:particles/combo_steam",
    "",
    "# Magma: Fire Armor (11..17) + Earth Skill (3) OR Earth Armor (31..37) + Fire Skill (1)",
    "execute if score @s avatar_skill matches 3 if score @s avatar_set matches 11..17 run function avatar:particles/combo_magma",
    "execute if score @s avatar_skill matches 1 if score @s avatar_set matches 31..37 run function avatar:particles/combo_magma",
    "",
    "# Firestorm: Air Armor (41..47) + Fire Skill (1) OR Fire Armor (11..17) + Air Skill (4)",
    "execute if score @s avatar_skill matches 1 if score @s avatar_set matches 41..47 run function avatar:particles/combo_firestorm",
    "execute if score @s avatar_skill matches 4 if score @s avatar_set matches 11..17 run function avatar:particles/combo_firestorm",
    "",
    "# Typhoon: Air Armor (41..47) + Water Skill (2) OR Water Armor (21..27) + Air Skill (4)",
    "execute if score @s avatar_skill matches 2 if score @s avatar_set matches 41..47 run function avatar:particles/combo_typhoon",
    "execute if score @s avatar_skill matches 4 if score @s avatar_set matches 21..27 run function avatar:particles/combo_typhoon",
    "",
    "# Mud: Water Armor (21..27) + Earth Skill (3) OR Earth Armor (31..37) + Water Skill (2)",
    "execute if score @s avatar_skill matches 3 if score @s avatar_set matches 21..27 run function avatar:particles/combo_mud",
    "execute if score @s avatar_skill matches 2 if score @s avatar_set matches 31..37 run function avatar:particles/combo_mud",
    "",
    "# Sandstorm: Earth Armor (31..37) + Air Skill (4) OR Air Armor (41..47) + Earth Skill (3)",
    "execute if score @s avatar_skill matches 4 if score @s avatar_set matches 31..37 run function avatar:particles/combo_sandstorm",
    "execute if score @s avatar_skill matches 3 if score @s avatar_set matches 41..47 run function avatar:particles/combo_sandstorm",
    "",
    "# -----------------------------------------------------------------------------",
    "# CASE 3: ELEMENTAL RESONANCE (Skill == Armor Element)",
    "# -----------------------------------------------------------------------------",
    "execute if score @s avatar_skill matches 1 if score @s avatar_set matches 11..17 run function avatar:particles/resonance_fire",
    "execute if score @s avatar_skill matches 2 if score @s avatar_set matches 21..27 run function avatar:particles/resonance_water",
    "execute if score @s avatar_skill matches 3 if score @s avatar_set matches 31..37 run function avatar:particles/resonance_earth",
    "execute if score @s avatar_skill matches 4 if score @s avatar_set matches 41..47 run function avatar:particles/resonance_air"
]

with open(os.path.join(particles_dir, "router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("\n".join(router_lines) + "\n")

print("Generated master particles router and combo effect functions!")
