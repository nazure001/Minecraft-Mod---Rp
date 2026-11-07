# ==============================================================================
# Tectonic Earth Wave (Gelombang Tanah Bergelombang) - VCraft / Avatar Style
# ==============================================================================
scoreboard players remove @s avatar_chi 20
scoreboard players set @s avatar_cd 25

# Deep tectonic seismic roar & stone crack sounds
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 2.0 0.5
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.5 0.6
playsound minecraft:block.stone.break player @a ~ ~ ~ 2.0 0.7

# --- WAVE STAGE 1 (Distance 2): Initial Ground Fracture ---
execute at @s anchored feet positioned ^-1.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.35,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.0 ^0.1 ^2 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.35,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:explosion ~ ~ ~ 0.5 0.2 0.5 0.02 2 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:poof ~ ~ ~ 0.6 0.3 0.6 0.05 10 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.4} ~ ~ ~ 0.8 0.4 0.8 0.1 20 normal
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 as @e[type=!player,distance=..2.5] run tp @s ~ ~0.8 ~
execute at @s anchored feet positioned ^0.0 ^0.3 ^2 as @e[type=!player,distance=..2.5] run damage @s 8 minecraft:generic

# --- WAVE STAGE 2 (Distance 4): Cresting Tectonic Swell ---
execute at @s anchored feet positioned ^-1.2 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:cobblestone"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.2 ^0.2 ^4 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.45,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:explosion ~ ~ ~ 0.6 0.2 0.6 0.02 3 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:poof ~ ~ ~ 0.8 0.4 0.8 0.05 15 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 run particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.6} ~ ~ ~ 1.0 0.5 1.0 0.1 25 normal
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 as @e[type=!player,distance=..2.8] run tp @s ~ ~1.2 ~
execute at @s anchored feet positioned ^0.0 ^0.4 ^4 as @e[type=!player,distance=..2.8] run damage @s 10 minecraft:generic

# --- WAVE STAGE 3 (Distance 6): Massive Earth Crest Surge ---
execute at @s anchored feet positioned ^-1.4 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.4 ^0.3 ^6 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:dirt"},Time:1,Motion:[0.0,0.55,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:explosion ~ ~ ~ 0.8 0.3 0.8 0.03 4 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:poof ~ ~ ~ 1.0 0.5 1.0 0.05 20 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 run particle minecraft:dust{color:[0.45,0.30,0.15],scale:1.8} ~ ~ ~ 1.2 0.5 1.2 0.1 30 normal
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 as @e[type=!player,distance=..3.2] run tp @s ~ ~1.6 ~
execute at @s anchored feet positioned ^0.0 ^0.5 ^6 as @e[type=!player,distance=..3.2] run damage @s 13 minecraft:generic

# --- WAVE STAGE 4 (Distance 8): Cataclysmic Impact Crash ---
execute at @s anchored feet positioned ^-1.2 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:cobblestone"},Time:1,Motion:[0.0,0.75,0.0],DropItem:0b}
execute at @s anchored feet positioned ^1.2 ^0.4 ^8 run summon falling_block ~ ~ ~ {BlockState:{Name:"minecraft:stone"},Time:1,Motion:[0.0,0.65,0.0],DropItem:0b}
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2.0 0.8
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:poof ~ ~ ~ 1.2 0.6 1.2 0.08 30 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 run particle minecraft:dust{color:[0.40,0.25,0.10],scale:2.0} ~ ~ ~ 1.5 0.8 1.5 0.15 40 normal
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 as @e[type=!player,distance=..3.5] run tp @s ~ ~2.0 ~
execute at @s anchored feet positioned ^0.0 ^0.8 ^8 as @e[type=!player,distance=..3.5] run damage @s 16 minecraft:generic
