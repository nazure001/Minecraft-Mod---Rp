# Metalbending Cable Pull
scoreboard players remove @s avatar_chi 25
scoreboard players set @s avatar_cd 25
playsound minecraft:entity.iron_golem.repair player @a ~ ~ ~ 1.2 1.4

execute at @s anchored eyes positioned ^ ^ ^10 run particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.05 20 normal
execute at @s anchored eyes positioned ^ ^ ^10 as @e[type=!player,distance=..3] run tp @s ^ ^ ^-6
execute at @s anchored eyes positioned ^ ^ ^10 as @e[type=!player,distance=..3] run damage @s 10 minecraft:generic
# Or launch player forward
execute at @s run tp @s ^ ^0.3 ^4.0
