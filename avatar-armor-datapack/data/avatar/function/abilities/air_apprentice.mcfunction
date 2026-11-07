# Rebalanced Avatar Ability - air_apprentice.mcfunction
scoreboard players set @s avatar_set 42
effect give @s minecraft:speed 3 0 true
effect give @s minecraft:jump_boost 3 0 true
effect give @s minecraft:slow_falling 3 0 true
function avatar:particles/air_apprentice
