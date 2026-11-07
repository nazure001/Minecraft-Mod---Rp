# Upgrade Potency Node
execute if score @s av_chi_points matches 1.. if score @s av_stat_pot matches ..4 run function avatar_skills:tree/apply_pot
execute unless score @s av_chi_points matches 1.. run tellraw @s {"text":"❌ You do not have enough Chi Points! Defeat mobs or consume Chi Orbs.","color":"red"}
