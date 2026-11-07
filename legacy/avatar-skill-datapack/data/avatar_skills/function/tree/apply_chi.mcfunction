scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_chi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

# Expand Max Chi Capacity and Advancement Lights
execute if score @s av_stat_chi matches 1 run scoreboard players set @s avatar_chi_max 125
execute if score @s av_stat_chi matches 1 run advancement grant @s only avatar_skills:passives/chi_1

execute if score @s av_stat_chi matches 2 run scoreboard players set @s avatar_chi_max 150
execute if score @s av_stat_chi matches 2 run advancement grant @s only avatar_skills:passives/chi_2

execute if score @s av_stat_chi matches 3 run scoreboard players set @s avatar_chi_max 175
execute if score @s av_stat_chi matches 3 run advancement grant @s only avatar_skills:passives/chi_3

execute if score @s av_stat_chi matches 4 run scoreboard players set @s avatar_chi_max 200
execute if score @s av_stat_chi matches 4 run advancement grant @s only avatar_skills:passives/chi_4

execute if score @s av_stat_chi matches 5 run scoreboard players set @s avatar_chi_max 250
execute if score @s av_stat_chi matches 5 run advancement grant @s only avatar_skills:passives/chi_5

tellraw @s [{"text":"✅ Chi Mastery upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"gold","bold":true},{"text":"! Max Chi expanded to ","color":"green"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"aqua"},{"text":"! (Check 'L' Menu!)","color":"green"}]
