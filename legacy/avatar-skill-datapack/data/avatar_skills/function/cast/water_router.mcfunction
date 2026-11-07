# Shift = Glacial Freeze, Normal = Water Whip
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/water_freeze
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/water_whip
