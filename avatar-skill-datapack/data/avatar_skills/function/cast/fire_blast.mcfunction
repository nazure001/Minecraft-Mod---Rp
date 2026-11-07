# Flame Sweep — wide arc fire attack (matches fire_router: normal click = sweep, shift = Fire Jet)
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 12
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.8 1.1
playsound minecraft:entity.blaze.shoot player @a ~ ~ ~ 1.5 1.2
playsound minecraft:entity.generic.burn player @a ~ ~ ~ 1.5 1.0

# Lunge player forward — only if destination block is passable (air/non-solid)
# This prevents phasing through walls; edge/void cases remain possible but are edge cases for a datapack
execute at @s if block ^ ^0.1 ^0.5 air run tp @s ^ ^0.1 ^0.5

execute at @s anchored eyes positioned ^-2.20 ^-0.20 ^2.00 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^-2.20 ^-0.20 ^2.00 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^-2.20 ^-0.20 ^2.00 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^-2.20 ^-0.20 ^2.00 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^-1.80 ^-0.10 ^2.60 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^-1.80 ^-0.10 ^2.60 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^-1.80 ^-0.10 ^2.60 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^-1.80 ^-0.10 ^2.60 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^-1.40 ^0.00 ^3.30 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^-1.40 ^0.00 ^3.30 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^-1.40 ^0.00 ^3.30 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^-1.40 ^0.00 ^3.30 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^-0.90 ^0.10 ^4.00 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^-0.90 ^0.10 ^4.00 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^-0.90 ^0.10 ^4.00 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^-0.90 ^0.10 ^4.00 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^-0.40 ^0.20 ^4.70 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^-0.40 ^0.20 ^4.70 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^-0.40 ^0.20 ^4.70 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^-0.40 ^0.20 ^4.70 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^0.00 ^0.25 ^5.20 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^0.00 ^0.25 ^5.20 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^0.00 ^0.25 ^5.20 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^0.00 ^0.25 ^5.20 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^0.40 ^0.20 ^4.70 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^0.40 ^0.20 ^4.70 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^0.40 ^0.20 ^4.70 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^0.40 ^0.20 ^4.70 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^0.90 ^0.10 ^4.00 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^0.90 ^0.10 ^4.00 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^0.90 ^0.10 ^4.00 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^0.90 ^0.10 ^4.00 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^1.40 ^0.00 ^3.30 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^1.40 ^0.00 ^3.30 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^1.40 ^0.00 ^3.30 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^1.40 ^0.00 ^3.30 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^1.80 ^-0.10 ^2.60 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^1.80 ^-0.10 ^2.60 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^1.80 ^-0.10 ^2.60 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^1.80 ^-0.10 ^2.60 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit
execute at @s anchored eyes positioned ^2.20 ^-0.20 ^2.00 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 10 normal
execute at @s anchored eyes positioned ^2.20 ^-0.20 ^2.00 run particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.02 6 normal
execute at @s anchored eyes positioned ^2.20 ^-0.20 ^2.00 run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0.01 2 normal
execute at @s anchored eyes positioned ^2.20 ^-0.20 ^2.00 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/fire_hit

# Scorch ground in front
execute at @s anchored feet positioned ^0.0 ^0.0 ^3.5 if block ~ ~ ~ air if block ~ ~-1 ~ #minecraft:inside_step_sound_blocks run setblock ~ ~ ~ fire