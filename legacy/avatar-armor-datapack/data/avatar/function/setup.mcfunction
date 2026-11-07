# ==============================================================================
# Avatar Armor Datapack - Setup (Minecraft 1.21.1)
# ==============================================================================
scoreboard objectives add avatar_set dummy "Avatar Armor Set ID"
scoreboard objectives add avatar_skill dummy "Avatar Active Skill Element"
scoreboard objectives add avatar_skill_timer dummy "Avatar Skill Duration Timer"
scoreboard objectives add avatar_tick dummy "Avatar Internal Tick Cycle"

# Default values
scoreboard players set @a avatar_skill 0
scoreboard players set @a avatar_skill_timer 0
scoreboard players set @a avatar_tick 0

tellraw @a [{"text":"[Avatar Armor] ","color":"gold","bold":true},{"text":"System initialized with 7 Tiers, 3D Headwear & Skill Combo Engine!","color":"green"}]
