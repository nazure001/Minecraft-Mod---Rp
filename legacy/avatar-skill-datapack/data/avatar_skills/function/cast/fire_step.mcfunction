particle minecraft:flame ~ ~ ~ 0.4 0.4 0.4 0.05 12 normal
particle minecraft:small_flame ~ ~ ~ 0.3 0.3 0.3 0.02 8 normal
particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0.01 2 normal
particle minecraft:smoke ~ ~ ~ 0.3 0.3 0.3 0.02 4 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/fire_hit
