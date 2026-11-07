# ==============================================================================
# Avatar Armor Datapack - Detect fire_nation (Checks 7 Tiers: Sovereign -> Initiate)
# ==============================================================================

# Sovereign Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"sovereign"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"sovereign"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"sovereign"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"sovereign"}}] run function avatar:abilities/fire_sovereign

# Mythic Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"mythic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"mythic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"mythic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"mythic"}}] run function avatar:abilities/fire_mythic

# Master Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"master"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"master"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"master"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"master"}}] run function avatar:abilities/fire_master

# Veteran Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"veteran"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"veteran"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"veteran"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"veteran"}}] run function avatar:abilities/fire_veteran

# Adept Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"adept"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"adept"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"adept"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"adept"}}] run function avatar:abilities/fire_adept

# Apprentice Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"apprentice"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"apprentice"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"apprentice"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"apprentice"}}] run function avatar:abilities/fire_apprentice

# Initiate Tier Full Set Check
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"initiate"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"initiate"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"initiate"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"initiate"}}] run function avatar:abilities/fire_initiate

# Legacy Compatibility Checks
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"legendary"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"legendary"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"legendary"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"legendary"}}] run function avatar:abilities/fire_sovereign
execute if items entity @s armor.chest *[custom_data~{avatar:{tier:"basic"}}] if items entity @s armor.head *[custom_data~{avatar:{nation:"fire",tier:"basic"}}] if items entity @s armor.legs *[custom_data~{avatar:{nation:"fire",tier:"basic"}}] if items entity @s armor.feet *[custom_data~{avatar:{nation:"fire",tier:"basic"}}] run function avatar:abilities/fire_initiate
