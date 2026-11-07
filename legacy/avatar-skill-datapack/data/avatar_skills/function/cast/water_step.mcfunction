particle minecraft:splash ~ ~ ~ 0.4 0.4 0.4 0.08 15 normal
particle minecraft:falling_water ~ ~ ~ 0.3 0.3 0.3 0.04 10 normal
particle minecraft:bubble ~ ~ ~ 0.2 0.2 0.2 0.05 8 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/water_hit
