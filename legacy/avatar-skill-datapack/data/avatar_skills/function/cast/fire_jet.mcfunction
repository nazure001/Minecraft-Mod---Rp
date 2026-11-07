# Fire Jet Propulsion
scoreboard players remove @s avatar_chi 25
scoreboard players set @s avatar_cd 30
playsound minecraft:entity.firework_rocket.launch player @a ~ ~ ~ 1.2 0.8
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.0 0.9

# Boost forward — check destination is passable before teleporting
execute at @s if block ^ ^0.4 ^2.5 air run tp @s ^ ^0.4 ^2.5
execute at @s unless block ^ ^0.4 ^2.5 air if block ^ ^0.4 ^1.5 air run tp @s ^ ^0.4 ^1.5
effect give @s minecraft:fire_resistance 3 0 true
execute at @s run particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.05 15 normal
execute at @s run particle minecraft:smoke ~ ~0.2 ~ 0.2 0.2 0.2 0.02 10 normal
execute at @s as @e[type=!player,distance=..3] run function avatar_skills:cast/fire_hit
