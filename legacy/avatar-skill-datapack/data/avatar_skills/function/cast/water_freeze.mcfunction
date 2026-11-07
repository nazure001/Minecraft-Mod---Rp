# Glacial Freeze - Freeze existing water into real frosted ice
scoreboard players remove @s avatar_chi 30
scoreboard players set @s avatar_cd 40
playsound minecraft:block.glass.break player @a ~ ~ ~ 1.5 1.4
playsound minecraft:entity.player.hurt_freeze player @a ~ ~ ~ 1.2 1.0

# Physically freeze water in 9x9 area into walkable ice
execute at @s run fill ~-4 ~-1 ~-4 ~4 ~1 ~4 frosted_ice replace water

# Blizzard frost nova
execute at @s run particle minecraft:snowflake ~ ~0.5 ~ 3.5 0.5 3.5 0.05 50 normal
execute at @s as @e[type=!player,distance=..6] run effect give @s minecraft:slowness 6 4 true
execute at @s as @e[type=!player,distance=..6] run damage @s 6 minecraft:freeze
