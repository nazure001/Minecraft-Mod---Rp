# Activate Avatar State
# Requirements: all 4 element masteries unlocked, not already in state, cooldown clear, min 50 chi

# Block if already active
execute if score @s avatar_state matches 1.. run title @s actionbar {"text":"✦ Avatar State already active","color":"red"}
execute if score @s avatar_state matches 1.. run return 0

# Block if on cooldown
execute if score @s avatar_cd matches 1.. run title @s actionbar {"text":"✦ Avatar State on cooldown","color":"red"}
execute if score @s avatar_cd matches 1.. run return 0

# Block if not all 4 masteries unlocked
execute unless score @s av_mast_all matches 1.. run title @s actionbar {"text":"✦ Master all 4 elements to enter Avatar State","color":"red"}
execute unless score @s av_mast_all matches 1.. run return 0

# Block if insufficient chi (cost: 50)
execute if score @s avatar_chi matches ..49 run title @s actionbar {"text":"✦ Not enough chi (need 50)","color":"red"}
execute if score @s avatar_chi matches ..49 run return 0

# Deduct chi cost
scoreboard players remove @s avatar_chi 50

# Activate: 600 ticks = 30 seconds
scoreboard players set @s avatar_state 600

playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 1.5 1.0
playsound minecraft:entity.wither.spawn player @a ~ ~ ~ 0.8 1.8

effect give @s minecraft:resistance 30 1 true
effect give @s minecraft:speed 30 1 true
effect give @s minecraft:strength 30 1 true
effect give @s minecraft:regeneration 30 1 true
effect give @s minecraft:night_vision 30 0 true
effect give @s minecraft:glowing 30 0 true

title @s title {"text":"🌀 AVATAR STATE AWAKENED 🌀","color":"light_purple","bold":true}
title @s subtitle {"text":"Raava's Cosmic Power Channels Through You!","color":"gold"}
