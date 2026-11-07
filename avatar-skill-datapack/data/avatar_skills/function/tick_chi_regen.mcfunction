# ==============================================================================
# Chi Regeneration Tick (Runs every 20 ticks / 1 second)
# ==============================================================================
scoreboard players set @s avatar_regen_timer 0

# Base passive regeneration (+5 Chi/sec)
execute if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5

# Bonus passive regen from Chi Mastery Node
execute if score @s av_stat_chi matches 1.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 2
execute if score @s av_stat_chi matches 2.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 2
execute if score @s av_stat_chi matches 3.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 3
execute if score @s av_stat_chi matches 4.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 3
execute if score @s av_stat_chi matches 5.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5

# Active Meditation Mode (Sneak/Crouch to focus Chi: +15 extra Chi/sec)
execute if entity @s[predicate=avatar_skills:is_sneaking] if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 15
execute if entity @s[predicate=avatar_skills:is_sneaking] at @s run particle minecraft:enchant ~ ~0.8 ~ 0.4 0.4 0.4 0.1 6 normal

# Clamp Chi to Max Chi (Prevent overflow)
execute if score @s avatar_chi > @s avatar_chi_max run scoreboard players operation @s avatar_chi = @s avatar_chi_max
