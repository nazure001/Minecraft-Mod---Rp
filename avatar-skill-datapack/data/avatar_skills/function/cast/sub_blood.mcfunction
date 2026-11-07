# Bloodbending (Immobilize Hostiles)
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 100
playsound minecraft:entity.wither.ambient player @a ~ ~ ~ 1.0 1.5

execute at @s run particle minecraft:dust{color:[0.8,0.05,0.1],scale:1.5} ~ ~1 ~ 4.0 1.0 4.0 0 60 normal
execute at @s as @e[type=!player,distance=..10] run effect give @s minecraft:levitation 4 0 true
execute at @s as @e[type=!player,distance=..10] run effect give @s minecraft:slowness 6 4 true
execute at @s as @e[type=!player,distance=..10] run damage @s 8 minecraft:magic
