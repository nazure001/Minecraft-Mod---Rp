scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_res 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Apply Extra Max Health Hearts and Advancement Lights
execute if score @s av_stat_res matches 1 run attribute @s minecraft:generic.max_health base set 24
execute if score @s av_stat_res matches 1 run advancement grant @s only avatar_skills:passives/resilience_1

execute if score @s av_stat_res matches 2 run attribute @s minecraft:generic.max_health base set 28
execute if score @s av_stat_res matches 2 run advancement grant @s only avatar_skills:passives/resilience_2

execute if score @s av_stat_res matches 3 run attribute @s minecraft:generic.max_health base set 32
execute if score @s av_stat_res matches 3 run advancement grant @s only avatar_skills:passives/resilience_3

execute if score @s av_stat_res matches 4 run attribute @s minecraft:generic.max_health base set 36
execute if score @s av_stat_res matches 4 run advancement grant @s only avatar_skills:passives/resilience_4

execute if score @s av_stat_res matches 5 run attribute @s minecraft:generic.max_health base set 40
execute if score @s av_stat_res matches 5 run advancement grant @s only avatar_skills:passives/resilience_5

tellraw @s [{"text":"✅ Resilience upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"gold","bold":true},{"text":"! Max Health hearts increased! (Check 'L' Menu!)","color":"green"}]
