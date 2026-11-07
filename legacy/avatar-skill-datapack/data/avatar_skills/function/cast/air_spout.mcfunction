# Air Spout Sky Leap
scoreboard players remove @s avatar_chi 20
scoreboard players set @s avatar_cd 25
playsound minecraft:entity.breeze.wind_burst player @a ~ ~ ~ 1.2 1.0

execute at @s run tp @s ~ ~8 ~
effect give @s minecraft:slow_falling 8 0 true
execute at @s run particle minecraft:cloud ~ ~ ~ 0.8 1.5 0.8 0.1 30 normal
execute at @s as @e[type=!player,distance=..4] run tp @s ^ ^0.5 ^-1.5
