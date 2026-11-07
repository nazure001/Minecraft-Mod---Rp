# Serpentine Double-Helix Water Whip (Katara Spiraling Flow)
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 12
playsound minecraft:entity.generic.splash player @a ~ ~ ~ 1.8 1.3
playsound minecraft:entity.player.splash.high_speed player @a ~ ~ ~ 1.5 1.5

execute at @s anchored eyes positioned ^0.38 ^0.24 ^1.45 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.38 ^0.24 ^1.45 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.38 ^-0.24 ^1.45 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.38 ^-0.24 ^1.45 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.20 ^0.40 ^2.10 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.20 ^0.40 ^2.10 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.20 ^-0.40 ^2.10 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.20 ^-0.40 ^2.10 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^-0.04 ^0.45 ^2.75 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.04 ^0.45 ^2.75 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.04 ^-0.45 ^2.75 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.04 ^-0.45 ^2.75 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^2.75 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/water_hit
execute at @s anchored eyes positioned ^-0.26 ^0.36 ^3.40 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.26 ^0.36 ^3.40 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.26 ^-0.36 ^3.40 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.26 ^-0.36 ^3.40 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^-0.42 ^0.17 ^4.05 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.42 ^0.17 ^4.05 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.42 ^-0.17 ^4.05 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.42 ^-0.17 ^4.05 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^-0.44 ^-0.07 ^4.70 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.44 ^-0.07 ^4.70 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.44 ^0.07 ^4.70 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.44 ^0.07 ^4.70 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^4.70 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/water_hit
execute at @s anchored eyes positioned ^-0.34 ^-0.29 ^5.35 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.34 ^-0.29 ^5.35 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.34 ^0.29 ^5.35 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.34 ^0.29 ^5.35 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^-0.14 ^-0.43 ^6.00 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^-0.14 ^-0.43 ^6.00 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^0.14 ^0.43 ^6.00 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^0.14 ^0.43 ^6.00 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.11 ^-0.44 ^6.65 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.11 ^-0.44 ^6.65 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.11 ^0.44 ^6.65 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.11 ^0.44 ^6.65 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^6.65 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/water_hit
execute at @s anchored eyes positioned ^0.32 ^-0.32 ^7.30 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.32 ^-0.32 ^7.30 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.32 ^0.32 ^7.30 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.32 ^0.32 ^7.30 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.44 ^-0.10 ^7.95 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.44 ^-0.10 ^7.95 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.44 ^0.10 ^7.95 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.44 ^0.10 ^7.95 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.43 ^0.14 ^8.60 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.43 ^0.14 ^8.60 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.43 ^-0.14 ^8.60 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.43 ^-0.14 ^8.60 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^8.60 as @e[type=!player,distance=..2.0] run function avatar_skills:cast/water_hit
execute at @s anchored eyes positioned ^0.29 ^0.34 ^9.25 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.29 ^0.34 ^9.25 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.29 ^-0.34 ^9.25 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.29 ^-0.34 ^9.25 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal
execute at @s anchored eyes positioned ^0.07 ^0.44 ^9.90 run particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0.02 5 normal
execute at @s anchored eyes positioned ^0.07 ^0.44 ^9.90 run particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0.01 4 normal
execute at @s anchored eyes positioned ^-0.07 ^-0.44 ^9.90 run particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0.02 4 normal
execute at @s anchored eyes positioned ^-0.07 ^-0.44 ^9.90 run particle minecraft:dust{color:[0.25,0.60,0.95],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0.01 3 normal

# Impact Splash at the whip tip
execute at @s anchored eyes positioned ^0.0 ^0.0 ^10.0 run particle minecraft:splash ~ ~ ~ 1.0 1.0 1.0 0.1 50 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^10.0 run playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 1.5 1.4