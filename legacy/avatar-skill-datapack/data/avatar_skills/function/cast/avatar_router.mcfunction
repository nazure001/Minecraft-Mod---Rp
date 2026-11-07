# Avatar Relic Router
# Shift = Activate Avatar State, Normal = Four-Element Orbital Sphere
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:avatar_state/activate
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:avatar_state/sphere_ultimate
