scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_pot 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5
advancement grant @s only avatar_skills:passives/root

execute if score @s av_stat_pot matches 1 run advancement grant @s only avatar_skills:passives/potency_1
execute if score @s av_stat_pot matches 2 run advancement grant @s only avatar_skills:passives/potency_2
execute if score @s av_stat_pot matches 3 run advancement grant @s only avatar_skills:passives/potency_3
execute if score @s av_stat_pot matches 4 run advancement grant @s only avatar_skills:passives/potency_4
execute if score @s av_stat_pot matches 5 run advancement grant @s only avatar_skills:passives/potency_5

tellraw @s [{"text":"✅ Elemental Potency upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"gold","bold":true},{"text":"! All elemental attacks deal amplified damage! (Check 'L' Menu!)","color":"green"}]
