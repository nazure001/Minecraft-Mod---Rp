scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_agi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Apply 1.21.1 Native Attributes and Advancement Lights
execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.movement_speed base set 0.115
execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.safe_fall_distance base set 5.0
execute if score @s av_stat_agi matches 1 run advancement grant @s only avatar_skills:passives/agility_1

execute if score @s av_stat_agi matches 2 run attribute @s minecraft:generic.movement_speed base set 0.130
execute if score @s av_stat_agi matches 2 run attribute @s minecraft:generic.safe_fall_distance base set 8.0
execute if score @s av_stat_agi matches 2 run advancement grant @s only avatar_skills:passives/agility_2

execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.movement_speed base set 0.145
execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.safe_fall_distance base set 10.0
execute if score @s av_stat_agi matches 3 run advancement grant @s only avatar_skills:passives/agility_3

execute if score @s av_stat_agi matches 4 run attribute @s minecraft:generic.movement_speed base set 0.160
execute if score @s av_stat_agi matches 4 run attribute @s minecraft:generic.safe_fall_distance base set 15.0
execute if score @s av_stat_agi matches 4 run advancement grant @s only avatar_skills:passives/agility_4

execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.movement_speed base set 0.180
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.safe_fall_distance base set 30.0
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.step_height base set 1.5
execute if score @s av_stat_agi matches 5 run advancement grant @s only avatar_skills:passives/agility_5

tellraw @s [{"text":"✅ Agility upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"gold","bold":true},{"text":"! Speed & Fall resistance increased. (Check 'L' Menu!)","color":"green"}]
