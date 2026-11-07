# Player Gained XP Levels -> Award Skill Points
scoreboard players operation @s avatar_diff_lvl = @s avatar_curr_lvl
scoreboard players operation @s avatar_diff_lvl -= @s avatar_prev_lvl
scoreboard players operation @s av_chi_points += @s avatar_diff_lvl
scoreboard players operation @s avatar_prev_lvl = @s avatar_curr_lvl

# Visual & Audio Feedback
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.2
particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.5 0.5 0.1 25 normal

title @s actionbar [{"text":"🌟 LEVEL UP! ","color":"gold","bold":true},{"text":"+1 Skill Point awarded! (Total: ","color":"yellow"},{"score":{"name":"@s","objective":"av_chi_points"},"color":"aqua","bold":true},{"text":") | Right-click Tome of Chi to spend!","color":"yellow"}]
tellraw @s [{"text":"[Avatar Progression] ","color":"gold","bold":true},{"text":"Level Up! You reached Level ","color":"yellow"},{"score":{"name":"@s","objective":"avatar_curr_lvl"},"color":"green","bold":true},{"text":" and received ","color":"yellow"},{"score":{"name":"@s","objective":"avatar_diff_lvl"},"color":"aqua","bold":true},{"text":" Skill Point(s)! Right-click your Tome of Chi to cultivate your passive/active tree.","color":"yellow"}]
