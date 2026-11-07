# Fortified Earth Wall (Dynamic 100% Direction-Aligned via Caret ^ Coordinates)
scoreboard players remove @s avatar_chi 25
scoreboard players set @s avatar_cd 40
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 2.0 0.5
playsound minecraft:block.stone.place player @a ~ ~ ~ 2.0 0.6
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.2 0.7

# Height Layer Y=0.0
execute at @s anchored feet positioned ^-1.6 ^0.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^-0.8 ^0.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.0 ^0.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.8 ^0.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^1.6 ^0.0 ^3.2 run function avatar_skills:cast/earth_wall_block
# Height Layer Y=1.0
execute at @s anchored feet positioned ^-1.6 ^1.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^-0.8 ^1.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.0 ^1.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.8 ^1.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^1.6 ^1.0 ^3.2 run function avatar_skills:cast/earth_wall_block
# Height Layer Y=2.0
execute at @s anchored feet positioned ^-1.6 ^2.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^-0.8 ^2.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.0 ^2.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^0.8 ^2.0 ^3.2 run function avatar_skills:cast/earth_wall_block
execute at @s anchored feet positioned ^1.6 ^2.0 ^3.2 run function avatar_skills:cast/earth_wall_block

# Ground fissure dust along the wall base
execute at @s anchored feet positioned ^0.0 ^0.5 ^3.2 run particle minecraft:poof ~ ~ ~ 1.6 0.8 0.5 0.05 40 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^3.2 run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.8} ~ ~ ~ 1.6 0.8 0.5 0.1 50 normal

# Knockback & stun hostiles in front
execute at @s anchored feet positioned ^0.0 ^1.0 ^3.5 as @e[type=!player,distance=..3.5] run tp @s ^ ^1.0 ^-2.5
execute at @s anchored feet positioned ^0.0 ^1.0 ^3.5 as @e[type=!player,distance=..3.5] run damage @s 8 minecraft:generic
effect give @s minecraft:resistance 5 1 true