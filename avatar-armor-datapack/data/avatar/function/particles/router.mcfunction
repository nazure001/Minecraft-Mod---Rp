# ==============================================================================
# Avatar Armor Datapack - Master Particle & Skill Combo Router
# ==============================================================================

# -----------------------------------------------------------------------------
# CASE 1: NO ACTIVE SKILL (Idle Ambient Tier Particles)
# -----------------------------------------------------------------------------
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 11 run function avatar:particles/fire_initiate
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 12 run function avatar:particles/fire_apprentice
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 13 run function avatar:particles/fire_adept
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 14 run function avatar:particles/fire_veteran
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 15 run function avatar:particles/fire_master
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 16 run function avatar:particles/fire_mythic
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 17 run function avatar:particles/fire_sovereign

execute if score @s avatar_skill matches 0 if score @s avatar_set matches 21 run function avatar:particles/water_initiate
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 22 run function avatar:particles/water_apprentice
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 23 run function avatar:particles/water_adept
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 24 run function avatar:particles/water_veteran
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 25 run function avatar:particles/water_master
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 26 run function avatar:particles/water_mythic
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 27 run function avatar:particles/water_sovereign

execute if score @s avatar_skill matches 0 if score @s avatar_set matches 31 run function avatar:particles/earth_initiate
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 32 run function avatar:particles/earth_apprentice
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 33 run function avatar:particles/earth_adept
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 34 run function avatar:particles/earth_veteran
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 35 run function avatar:particles/earth_master
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 36 run function avatar:particles/earth_mythic
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 37 run function avatar:particles/earth_sovereign

execute if score @s avatar_skill matches 0 if score @s avatar_set matches 41 run function avatar:particles/air_initiate
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 42 run function avatar:particles/air_apprentice
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 43 run function avatar:particles/air_adept
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 44 run function avatar:particles/air_veteran
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 45 run function avatar:particles/air_master
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 46 run function avatar:particles/air_mythic
execute if score @s avatar_skill matches 0 if score @s avatar_set matches 47 run function avatar:particles/air_sovereign

# -----------------------------------------------------------------------------
# CASE 2: CROSS-ELEMENT COMBOS (Skill != Armor Element)
# -----------------------------------------------------------------------------
# Steam: Water Armor (21..27) + Fire Skill (1) OR Fire Armor (11..17) + Water Skill (2)
execute if score @s avatar_skill matches 1 if score @s avatar_set matches 21..27 run function avatar:particles/combo_steam
execute if score @s avatar_skill matches 2 if score @s avatar_set matches 11..17 run function avatar:particles/combo_steam

# Magma: Fire Armor (11..17) + Earth Skill (3) OR Earth Armor (31..37) + Fire Skill (1)
execute if score @s avatar_skill matches 3 if score @s avatar_set matches 11..17 run function avatar:particles/combo_magma
execute if score @s avatar_skill matches 1 if score @s avatar_set matches 31..37 run function avatar:particles/combo_magma

# Firestorm: Air Armor (41..47) + Fire Skill (1) OR Fire Armor (11..17) + Air Skill (4)
execute if score @s avatar_skill matches 1 if score @s avatar_set matches 41..47 run function avatar:particles/combo_firestorm
execute if score @s avatar_skill matches 4 if score @s avatar_set matches 11..17 run function avatar:particles/combo_firestorm

# Typhoon: Air Armor (41..47) + Water Skill (2) OR Water Armor (21..27) + Air Skill (4)
execute if score @s avatar_skill matches 2 if score @s avatar_set matches 41..47 run function avatar:particles/combo_typhoon
execute if score @s avatar_skill matches 4 if score @s avatar_set matches 21..27 run function avatar:particles/combo_typhoon

# Mud: Water Armor (21..27) + Earth Skill (3) OR Earth Armor (31..37) + Water Skill (2)
execute if score @s avatar_skill matches 3 if score @s avatar_set matches 21..27 run function avatar:particles/combo_mud
execute if score @s avatar_skill matches 2 if score @s avatar_set matches 31..37 run function avatar:particles/combo_mud

# Sandstorm: Earth Armor (31..37) + Air Skill (4) OR Air Armor (41..47) + Earth Skill (3)
execute if score @s avatar_skill matches 4 if score @s avatar_set matches 31..37 run function avatar:particles/combo_sandstorm
execute if score @s avatar_skill matches 3 if score @s avatar_set matches 41..47 run function avatar:particles/combo_sandstorm

# -----------------------------------------------------------------------------
# CASE 3: ELEMENTAL RESONANCE (Skill == Armor Element)
# -----------------------------------------------------------------------------
execute if score @s avatar_skill matches 1 if score @s avatar_set matches 11..17 run function avatar:particles/resonance_fire
execute if score @s avatar_skill matches 2 if score @s avatar_set matches 21..27 run function avatar:particles/resonance_water
execute if score @s avatar_skill matches 3 if score @s avatar_set matches 31..37 run function avatar:particles/resonance_earth
execute if score @s avatar_skill matches 4 if score @s avatar_set matches 41..47 run function avatar:particles/resonance_air
