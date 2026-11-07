# Elemental Combo: Firestorm / Fire Tornado (Air + Fire)
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
