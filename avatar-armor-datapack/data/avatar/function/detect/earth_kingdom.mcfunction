# ==============================================================================
# Avatar Armor Datapack - Detect earth_kingdom (Checks 7 Tiers: Sovereign -> Initiate)
# ==============================================================================

# Sovereign Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"sovereign"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"sovereign"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"sovereign"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"sovereign"}}] run function avatar:abilities/earth_sovereign

# Mythic Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"mythic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"mythic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"mythic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"mythic"}}] run function avatar:abilities/earth_mythic

# Master Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"master"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"master"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"master"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"master"}}] run function avatar:abilities/earth_master

# Veteran Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"veteran"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"veteran"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"veteran"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"veteran"}}] run function avatar:abilities/earth_veteran

# Adept Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"adept"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"adept"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"adept"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"adept"}}] run function avatar:abilities/earth_adept

# Apprentice Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"apprentice"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"apprentice"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"apprentice"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"apprentice"}}] run function avatar:abilities/earth_apprentice

# Initiate Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"initiate"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"initiate"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"initiate"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"initiate"}}] run function avatar:abilities/earth_initiate

# Legacy Compatibility Checks
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"legendary"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"legendary"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"legendary"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"legendary"}}] run function avatar:abilities/earth_sovereign
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"basic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"earth",tier:"basic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"earth",tier:"basic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"earth",tier:"basic"}}] run function avatar:abilities/earth_initiate
