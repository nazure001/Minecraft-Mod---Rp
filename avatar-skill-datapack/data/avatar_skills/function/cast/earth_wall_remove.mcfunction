# Decay physical earth wall back to air
fill ~-1 ~-1 ~ ~1 ~2 ~ air replace stone
particle minecraft:poof ~ ~ ~ 1.0 1.0 0.5 0.05 40 normal
particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.4} ~ ~ ~ 1.0 1.0 0.5 0.1 40 normal
playsound minecraft:block.stone.break player @a ~ ~ ~ 1.2 0.8
kill @s
