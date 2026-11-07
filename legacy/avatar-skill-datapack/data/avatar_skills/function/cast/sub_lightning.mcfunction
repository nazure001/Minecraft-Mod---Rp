# Lightning Generation
scoreboard players remove @s avatar_chi 40
scoreboard players set @s avatar_cd 60
playsound minecraft:entity.lightning_bolt.thunder player @a ~ ~ ~ 1.2 1.2
playsound minecraft:item.trident.thunder player @a ~ ~ ~ 1.5 1.5

execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^6 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^12 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^12 as @e[type=!player,distance=..4] run damage @s 18 minecraft:lightning_bolt
