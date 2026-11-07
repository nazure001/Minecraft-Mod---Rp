# ==============================================================================
# Avatar Skills & Mastery System - Setup (Minecraft Java 1.21.1)
# ==============================================================================

# Core Skill & Interaction Objectives
scoreboard objectives add avatar_used minecraft.used:minecraft.warped_fungus_on_a_stick "Avatar Cast"
scoreboard objectives add avatar_used_c minecraft.used:minecraft.carrot_on_a_stick "Avatar Cast C"
scoreboard objectives add avatar_chi dummy "Avatar Chi"
scoreboard objectives add avatar_chi_max dummy "Max Chi"
scoreboard objectives add avatar_cd dummy "Skill Cooldown"
scoreboard objectives add avatar_state dummy "Avatar State Timer"
scoreboard objectives add avatar_sneak minecraft.custom:minecraft.sneak_time "Sneak Time"
scoreboard objectives add avatar_timer dummy "Avatar Timers"
scoreboard objectives add avatar_regen_timer dummy "Chi Regen Timer"

# Elemental Masteries (0 = locked, 1 = unlocked)
scoreboard objectives add av_mast_fire dummy "Fire Mastery"
scoreboard objectives add av_mast_water dummy "Water Mastery"
scoreboard objectives add av_mast_earth dummy "Earth Mastery"
scoreboard objectives add av_mast_air dummy "Air Mastery"
scoreboard objectives add av_mast_all dummy "Master of Four"

# Built-in Skill Node Attributes (Levels 0-5)
scoreboard objectives add av_stat_agi dummy "Agility Level"
scoreboard objectives add av_stat_chi dummy "Chi Mastery Level"
scoreboard objectives add av_stat_res dummy "Resilience Level"
scoreboard objectives add av_stat_pot dummy "Elemental Potency Level"
scoreboard objectives add av_chi_points dummy "Unallocated Chi"

# Setup default scores for new players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player

tellraw @a [{"text":"[Avatar System] ","color":"gold","bold":true},{"text":"Avatar Skills & Elemental Mastery System 1.21.1 Loaded Successfully!","color":"green"}]

# XP Level Tracking Objectives
scoreboard objectives add avatar_curr_lvl dummy "Current Level"
scoreboard objectives add avatar_prev_lvl dummy "Previous Level"
scoreboard objectives add avatar_diff_lvl dummy "Level Difference"
