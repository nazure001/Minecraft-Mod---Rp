# Zaheer's Weightless Flight
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 120
playsound minecraft:entity.bat.takeoff player @a ~ ~ ~ 1.2 0.8

execute at @s run particle minecraft:cloud ~ ~ ~ 1.0 0.5 1.0 0.05 20 normal
effect give @s minecraft:levitation 10 1 true
effect give @s minecraft:slow_falling 15 0 true
effect give @s minecraft:speed 10 2 true
title @s actionbar {"text":"🕊️ Entering the void... Empty, and become wind.","color":"light_purple","bold":true}
