# 4-Element Orbital Aura (Flame, Water, Stone, Cloud)
scoreboard players remove @s avatar_state 1

# Quadrant 1: Fire (Front)
execute at @s run particle minecraft:flame ^1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 3 normal
execute at @s run particle minecraft:small_flame ^1.5 ^1.2 ^ 0.02 0.02 0.02 0.01 2 normal
# Quadrant 2: Water (Right)
execute at @s run particle minecraft:falling_water ^ ^1.2 ^1.5 0.05 0.05 0.05 0.01 4 normal
execute at @s run particle minecraft:splash ^ ^1.2 ^1.5 0.05 0.05 0.05 0.01 2 normal
# Quadrant 3: Earth (Back) - Fixed valid dust particle!
execute at @s run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.5} ^-1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 4 normal
# Quadrant 4: Air (Left)
execute at @s run particle minecraft:cloud ^ ^1.2 ^-1.5 0.05 0.05 0.05 0.01 3 normal
execute at @s run particle minecraft:poof ^ ^1.2 ^-1.5 0.05 0.05 0.05 0.01 2 normal

# End of Avatar State: on the exact tick it hits 0, apply recovery cooldown (200 ticks = 10s)
# avatar_cd check prevents re-triggering if something else already set a cooldown
execute if score @s avatar_state matches 0 if score @s avatar_cd matches 0 run scoreboard players set @s avatar_cd 200
execute if score @s avatar_state matches 0 if score @s avatar_cd matches 200 run title @s title {"text":"Avatar State Exhausted","color":"gray"}
execute if score @s avatar_state matches 0 if score @s avatar_cd matches 200 run title @s subtitle {"text":"Recovering... (10s cooldown)","color":"red"}
