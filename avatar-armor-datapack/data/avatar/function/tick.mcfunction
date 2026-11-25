# ==============================================================================
# Avatar Armor Datapack - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# Increment global animation tick cycle (0..19)
scoreboard players add @a avatar_tick 1
execute as @a if score @s avatar_tick matches 20.. run scoreboard players set @s avatar_tick 0

# Reset active armor set status for all online players before detection
scoreboard players set @a avatar_set 0

# Fast nation routing: only execute nation check if player is wearing that nation's chestplate
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"fire"}}] run function avatar:detect/fire_nation
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"water"}}] run function avatar:detect/water_tribe
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"earth"}}] run function avatar:detect/earth_kingdom
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"air"}}] run function avatar:detect/air_nomad

# Particle & Elemental Combo Router (Executes for players wearing an Avatar Armor Set)
execute as @a[scores={avatar_set=11..47}] run function avatar:particles/router
