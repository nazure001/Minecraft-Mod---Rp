# Elemental Combo: Steam / Scalding Vapor (Water + Fire)
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
