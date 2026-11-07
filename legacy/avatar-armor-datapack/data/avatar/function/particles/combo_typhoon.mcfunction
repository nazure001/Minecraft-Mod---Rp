# Elemental Combo: Typhoon / Tempest Monsoon (Air + Water)
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
