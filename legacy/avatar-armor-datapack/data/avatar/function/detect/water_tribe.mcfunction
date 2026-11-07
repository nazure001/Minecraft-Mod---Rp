# ==============================================================================
# Avatar Armor Datapack - Detect water_tribe (Checks 7 Tiers: Sovereign -> Initiate)
# ==============================================================================

# Sovereign Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"sovereign"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"sovereign"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"sovereign"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"sovereign"}}] run function avatar:abilities/water_sovereign

# Mythic Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"mythic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"mythic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"mythic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"mythic"}}] run function avatar:abilities/water_mythic

# Master Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"master"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"master"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"master"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"master"}}] run function avatar:abilities/water_master

# Veteran Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"veteran"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"veteran"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"veteran"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"veteran"}}] run function avatar:abilities/water_veteran

# Adept Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"adept"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"adept"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"adept"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"adept"}}] run function avatar:abilities/water_adept

# Apprentice Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"apprentice"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"apprentice"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"apprentice"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"apprentice"}}] run function avatar:abilities/water_apprentice

# Initiate Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"initiate"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"initiate"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"initiate"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"initiate"}}] run function avatar:abilities/water_initiate

# Legacy Compatibility Checks
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"legendary"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"legendary"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"legendary"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"legendary"}}] run function avatar:abilities/water_sovereign
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"basic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"water",tier:"basic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"water",tier:"basic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"water",tier:"basic"}}] run function avatar:abilities/water_initiate
