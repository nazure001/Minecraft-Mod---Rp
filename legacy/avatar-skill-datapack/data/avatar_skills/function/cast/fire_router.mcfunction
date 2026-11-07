# Shift = Fire Jet (propulsion), Normal = Flame Sweep (wide arc)
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/fire_jet
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/fire_blast
