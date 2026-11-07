# ==============================================================================
# Avatar Skills - Cast Router (Minecraft Java 1.21.1)
# ==============================================================================

# Failsafe: ensure max chi is initialized (init_player handles new players, this catches edge cases)
execute unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player
execute unless score @s avatar_cd matches 0.. run scoreboard players set @s avatar_cd 0

# Chi empty: notify player and abort
execute if score @s avatar_chi matches 0 unless items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] unless items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run title @s actionbar {"text":"✦ Chi depleted — meditate to recover","color":"red","bold":true}
execute if score @s avatar_chi matches 0 unless items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] unless items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run return 0

# If CD == 0, cast skill:
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"fire"}] run function avatar_skills:cast/fire_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"water"}] run function avatar_skills:cast/water_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"earth"}] run function avatar_skills:cast/earth_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"air"}] run function avatar_skills:cast/air_router
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_skill:"avatar"}] run function avatar_skills:cast/avatar_router

# Sub-Bending Foci
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"lightning"}] run function avatar_skills:cast/sub_lightning
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"combustion"}] run function avatar_skills:cast/sub_combustion
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"blood"}] run function avatar_skills:cast/sub_blood
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"healing"}] run function avatar_skills:cast/sub_healing
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"lava"}] run function avatar_skills:cast/sub_lava
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"metal"}] run function avatar_skills:cast/sub_metal
execute if score @s avatar_cd matches 0 if items entity @s weapon.* *[custom_data~{avatar_sub:"flight"}] run function avatar_skills:cast/sub_flight

# Mastery Tome & Chi Orb (Always usable regardless of Chi / Cooldown)
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] run function avatar_skills:tree/open_menu
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run function avatar_skills:tree/consume_chi_orb
