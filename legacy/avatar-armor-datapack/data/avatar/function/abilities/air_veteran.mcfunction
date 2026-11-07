# Rebalanced Avatar Ability - air_veteran.mcfunction
scoreboard players set @s avatar_set 44
effect give @s minecraft:speed 3 1 true
effect give @s minecraft:jump_boost 3 1 true
effect give @s minecraft:slow_falling 3 0 true
effect give @s minecraft:haste 3 0 true
function avatar:particles/air_veteran
