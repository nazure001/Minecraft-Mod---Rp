# Combustion Bending
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 80
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.5 0.8

execute at @s anchored eyes positioned ^ ^ ^15 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 normal
execute at @s anchored eyes positioned ^ ^ ^15 as @e[type=!player,distance=..5] run damage @s 20 minecraft:explosion
execute at @s anchored eyes positioned ^ ^ ^15 as @e[type=!player,distance=..5] run execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
