# Elemental Combo: Magma / Volcanic Eruption (Fire + Earth)
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
