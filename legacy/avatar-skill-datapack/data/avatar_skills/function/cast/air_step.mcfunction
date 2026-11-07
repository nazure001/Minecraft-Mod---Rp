particle minecraft:cloud ~ ~ ~ 0.4 0.4 0.4 0.05 10 normal
particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.05 8 normal
particle minecraft:sweep_attack ~ ~ ~ 0.2 0.2 0.2 0.01 2 normal
particle minecraft:gust ~ ~ ~ 0.2 0.2 0.2 0.02 1 normal
execute as @e[type=!player,distance=..2.2,limit=4] run function avatar_skills:cast/air_hit
