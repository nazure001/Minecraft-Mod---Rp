# ==============================================================================
# Avatar Skills - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# 0. Failsafe auto-initialize player stats for all online players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player
execute as @a unless score @s avatar_regen_timer matches 0.. run scoreboard players set @s avatar_regen_timer 0

# Clamp Chi floor at 0 (no negative chi)
execute as @a if score @s avatar_chi matches ..-1 run scoreboard players set @s avatar_chi 0

# XP Level Progression Check (Adventure Level -> Skill Points)
execute as @a store result score @s avatar_curr_lvl run experience query @s levels
execute as @a unless score @s avatar_prev_lvl matches 0.. run scoreboard players operation @s avatar_prev_lvl = @s avatar_curr_lvl
execute as @a if score @s avatar_curr_lvl > @s avatar_prev_lvl run function avatar_skills:tree/on_level_up

# 1. Chi Regeneration (Every 20 ticks / 1 second)
execute as @a run scoreboard players add @s avatar_regen_timer 1
execute as @a if score @s avatar_regen_timer matches 20.. run function avatar_skills:tick_chi_regen

# 2. Cooldown Countdown
execute as @a if score @s avatar_cd matches 1.. run scoreboard players remove @s avatar_cd 1

# 3. Avatar State Timer & 4-Element Orbital Aura
execute as @a if score @s avatar_state matches 1.. run function avatar_skills:avatar_state/tick

# 4. Actionbar HUD Display (Chi & Status)
execute as @a if items entity @s weapon.* *[custom_data~{avatar_item:true}] run function avatar_skills:hud_actionbar

# 5. Right-Click Cast Detection (Warped Fungus + Carrot on a stick)
execute as @a[scores={avatar_used=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used=1..}] run scoreboard players set @s avatar_used 0

execute as @a[scores={avatar_used_c=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used_c=1..}] run scoreboard players set @s avatar_used_c 0

# 6. Auto-check 4-Element Mastery for Avatar Awakening
execute as @a[scores={av_mast_fire=1..,av_mast_water=1..,av_mast_earth=1..,av_mast_air=1..,av_mast_all=0}] run function avatar_skills:tree/awaken_avatar

# 7. Physical Bending Block Decay Timers (Anti-Griefing Auto-Cleanup)
execute as @e[type=marker,tag=avatar_earth_wall] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_earth_wall,scores={avatar_timer=140..}] at @s run function avatar_skills:cast/earth_wall_remove

execute as @e[type=marker,tag=avatar_lava_pool] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_lava_pool,scores={avatar_timer=120..}] at @s run function avatar_skills:cast/lava_pool_cool

# 7b. Dynamic Direction-Aligned Earth Wall Block Decay
execute as @e[type=marker,tag=avatar_wall_marker] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] at @s run setblock ~ ~ ~ air replace stone
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] at @s run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.2} ~ ~ ~ 0.3 0.3 0.3 0.05 6 normal
execute as @e[type=marker,tag=avatar_wall_marker,scores={avatar_timer=120..}] run kill @s
