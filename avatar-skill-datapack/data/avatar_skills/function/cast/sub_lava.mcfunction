# Lavabending - Transmute rock & dirt into molten magma
scoreboard players remove @s avatar_chi 40
scoreboard players set @s avatar_cd 70
playsound minecraft:block.lava.ambient player @a ~ ~ ~ 1.5 1.0
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.2 0.7

# Transmute terrain in front of player
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace stone
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace dirt
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace grass_block
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace deepslate
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace cobblestone

execute at @s anchored feet positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["avatar_lava_pool"],Age:0}
execute at @s anchored feet positioned ^ ^ ^3 run particle minecraft:lava ~ ~0.5 ~ 1.5 0.3 1.5 0.05 40 normal
execute at @s anchored feet positioned ^ ^ ^3 as @e[type=!player,distance=..4.5] run damage @s 14 minecraft:in_fire
execute at @s anchored feet positioned ^ ^ ^3 as @e[type=!player,distance=..4.5] run execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
