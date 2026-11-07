# Four-Element Orbital Sphere Cataclysm
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 50
playsound minecraft:entity.lightning_bolt.thunder player @a ~ ~ ~ 2.0 1.0
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2.0 0.7
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 2.0 0.8

# Quad-Element Cataclysm Ring
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:flame ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:splash ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.8} ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:cloud ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 2 normal

# Heavy Cumulative Quad Damage & Knockback
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run damage @s 32 minecraft:magic
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run tp @s ^ ^1.5 ^-3.0
