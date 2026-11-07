# Rebalanced Avatar Ability - air_master.mcfunction
scoreboard players set @s avatar_set 45
effect give @s minecraft:speed 3 2 true
effect give @s minecraft:jump_boost 3 1 true
effect give @s minecraft:slow_falling 3 0 true
effect give @s minecraft:haste 3 1 true
function avatar:particles/air_master
