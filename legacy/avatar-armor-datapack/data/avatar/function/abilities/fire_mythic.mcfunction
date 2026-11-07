# Rebalanced Avatar Ability - fire_mythic.mcfunction
scoreboard players set @s avatar_set 16
effect give @s minecraft:fire_resistance 3 0 true
effect give @s minecraft:strength 3 1 true
effect give @s minecraft:speed 3 1 true
effect give @s minecraft:haste 3 1 true
function avatar:particles/fire_mythic
