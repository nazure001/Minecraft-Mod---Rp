# Shift = Air Spout, Normal = Air Blast
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/air_spout
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/air_blast
