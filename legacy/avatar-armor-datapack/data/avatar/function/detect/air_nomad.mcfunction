# ==============================================================================
# Avatar Armor Datapack - Detect air_nomad (Checks 7 Tiers: Sovereign -> Initiate)
# ==============================================================================

# Sovereign Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"sovereign"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"sovereign"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"sovereign"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"sovereign"}}] run function avatar:abilities/air_sovereign

# Mythic Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"mythic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"mythic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"mythic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"mythic"}}] run function avatar:abilities/air_mythic

# Master Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"master"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"master"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"master"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"master"}}] run function avatar:abilities/air_master

# Veteran Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"veteran"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"veteran"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"veteran"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"veteran"}}] run function avatar:abilities/air_veteran

# Adept Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"adept"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"adept"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"adept"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"adept"}}] run function avatar:abilities/air_adept

# Apprentice Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"apprentice"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"apprentice"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"apprentice"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"apprentice"}}] run function avatar:abilities/air_apprentice

# Initiate Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"initiate"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"initiate"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"initiate"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"initiate"}}] run function avatar:abilities/air_initiate

# Legacy Compatibility Checks
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"legendary"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"legendary"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"legendary"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"legendary"}}] run function avatar:abilities/air_sovereign
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"basic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"air",tier:"basic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"air",tier:"basic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"air",tier:"basic"}}] run function avatar:abilities/air_initiate
