# Avatar Armor - Test Combos Helper
tellraw @s [{"text":"=== [Avatar Skill Combo Test Commands] ===","color":"gold","bold":true}]
tellraw @s [{"text":"1. Cast Fire Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_fire]","color":"red","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_fire"}}]
tellraw @s [{"text":"2. Cast Water Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_water]","color":"aqua","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_water"}}]
tellraw @s [{"text":"3. Cast Earth Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_earth]","color":"green","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_earth"}}]
tellraw @s [{"text":"4. Cast Air Skill: ","color":"yellow"},{"text":"[/function avatar:skill/cast_air]","color":"gold","clickEvent":{"action":"run_command","value":"/function avatar:skill/cast_air"}}]
tellraw @s [{"text":"5. Clear Skill: ","color":"yellow"},{"text":"[/function avatar:skill/clear]","color":"gray","clickEvent":{"action":"run_command","value":"/function avatar:skill/clear"}}]
