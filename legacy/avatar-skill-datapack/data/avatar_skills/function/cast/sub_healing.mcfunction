# Spirit Healing
scoreboard players remove @s avatar_chi 35
scoreboard players set @s avatar_cd 50
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1.0 1.8

execute at @s run particle minecraft:happy_villager ~ ~1 ~ 1.0 1.0 1.0 0.1 25 normal
execute at @s run particle minecraft:heart ~ ~1.5 ~ 0.5 0.5 0.5 0.1 8 normal
effect give @s minecraft:instant_health 1 1 true
effect give @s minecraft:regeneration 8 1 true
