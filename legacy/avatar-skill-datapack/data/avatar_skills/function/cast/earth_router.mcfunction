# Shift = Earth Wall, Normal = Boulder Toss
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/earth_wall
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/earth_boulder
