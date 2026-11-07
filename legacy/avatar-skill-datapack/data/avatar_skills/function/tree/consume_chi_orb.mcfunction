# Consume Chi Orb to gain Skill Points and instantly refill Chi to 100%
clear @s minecraft:warped_fungus_on_a_stick[custom_data~{avatar_skill:"chi_orb"}] 1
scoreboard players add @s av_chi_points 1
scoreboard players operation @s avatar_chi = @s avatar_chi_max
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.2 1.6
particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.05 20 normal
tellraw @s [{"text":"✨ [CHI MASTERY] ","color":"aqua","bold":true},{"text":"+1 Skill Point earned! ","color":"gold","bold":true},{"text":"Chi fully restored (100%)! Click Tome to upgrade.","color":"green"}]
