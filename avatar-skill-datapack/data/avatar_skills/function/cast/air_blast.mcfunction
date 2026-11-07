# Concentric Expanding Air Shockwave (Sonic Vacuum Burst)
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 10
playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 2.0 1.2
playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 1.8 0.7

# Deflect all incoming projectiles immediately
execute at @s as @e[type=arrow,distance=..6] run kill @s
execute at @s as @e[type=spectral_arrow,distance=..6] run kill @s
execute at @s as @e[type=trident,distance=..6] run kill @s

# --- Sonic Ring at Distance 2.5 (Radius 0.9) ---
execute at @s anchored eyes positioned ^0.90 ^0.00 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^0.90 ^0.00 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.64 ^0.64 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^0.64 ^0.64 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.00 ^0.90 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^0.00 ^0.90 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.64 ^0.64 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^-0.64 ^0.64 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.90 ^0.00 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^-0.90 ^0.00 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.64 ^-0.64 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^-0.64 ^-0.64 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.00 ^-0.90 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^-0.00 ^-0.90 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.64 ^-0.64 ^2.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.03 1 normal
execute at @s anchored eyes positioned ^0.64 ^-0.64 ^2.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^2.50 as @e[type=!player,distance=..1.7] run function avatar_skills:cast/air_hit

# --- Sonic Ring at Distance 5.0 (Radius 1.8) ---
execute at @s anchored eyes positioned ^1.80 ^0.00 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^1.80 ^0.00 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.56 ^0.90 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^1.56 ^0.90 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.90 ^1.56 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^0.90 ^1.56 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.00 ^1.80 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^0.00 ^1.80 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.90 ^1.56 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-0.90 ^1.56 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.56 ^0.90 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-1.56 ^0.90 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.80 ^0.00 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-1.80 ^0.00 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.56 ^-0.90 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-1.56 ^-0.90 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.90 ^-1.56 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-0.90 ^-1.56 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.00 ^-1.80 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^-0.00 ^-1.80 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.90 ^-1.56 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^0.90 ^-1.56 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.56 ^-0.90 ^5.00 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.05 1 normal
execute at @s anchored eyes positioned ^1.56 ^-0.90 ^5.00 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^5.00 as @e[type=!player,distance=..2.6] run function avatar_skills:cast/air_hit

# --- Sonic Ring at Distance 7.5 (Radius 2.7) ---
execute at @s anchored eyes positioned ^2.70 ^0.00 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^2.70 ^0.00 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^2.49 ^1.03 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^2.49 ^1.03 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.91 ^1.91 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^1.91 ^1.91 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.03 ^2.49 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^1.03 ^2.49 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.00 ^2.70 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^0.00 ^2.70 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.03 ^2.49 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-1.03 ^2.49 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.91 ^1.91 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-1.91 ^1.91 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-2.49 ^1.03 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-2.49 ^1.03 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-2.70 ^0.00 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-2.70 ^0.00 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-2.49 ^-1.03 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-2.49 ^-1.03 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.91 ^-1.91 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-1.91 ^-1.91 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-1.03 ^-2.49 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-1.03 ^-2.49 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^-0.00 ^-2.70 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^-0.00 ^-2.70 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.03 ^-2.49 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^1.03 ^-2.49 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^1.91 ^-1.91 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^1.91 ^-1.91 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^2.49 ^-1.03 ^7.50 run particle minecraft:wind_charge ~ ~ ~ 0.05 0.05 0.05 0.08 1 normal
execute at @s anchored eyes positioned ^2.49 ^-1.03 ^7.50 run particle minecraft:cloud ~ ~ ~ 0.1 0.1 0.1 0.02 2 normal
execute at @s anchored eyes positioned ^0.0 ^0.0 ^7.50 as @e[type=!player,distance=..3.5] run function avatar_skills:cast/air_hit
