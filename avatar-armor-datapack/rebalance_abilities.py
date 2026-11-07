import os

ab_dir = r"d:\repo\avatar-armor-datapack\data\avatar\function\abilities"

rebalanced = {
    # FIRE
    "fire_initiate.mcfunction": [
        "scoreboard players set @s avatar_set 11",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "function avatar:particles/fire_initiate"
    ],
    "fire_apprentice.mcfunction": [
        "scoreboard players set @s avatar_set 12",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 0 true",
        "function avatar:particles/fire_apprentice"
    ],
    "fire_adept.mcfunction": [
        "scoreboard players set @s avatar_set 13",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 0 true",
        "effect give @s minecraft:speed 3 0 true",
        "function avatar:particles/fire_adept"
    ],
    "fire_veteran.mcfunction": [
        "scoreboard players set @s avatar_set 14",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 1 true",
        "effect give @s minecraft:speed 3 0 true",
        "function avatar:particles/fire_veteran"
    ],
    "fire_master.mcfunction": [
        "scoreboard players set @s avatar_set 15",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 1 true",
        "effect give @s minecraft:speed 3 1 true",
        "effect give @s minecraft:haste 3 0 true",
        "function avatar:particles/fire_master"
    ],
    "fire_mythic.mcfunction": [
        "scoreboard players set @s avatar_set 16",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 1 true",
        "effect give @s minecraft:speed 3 1 true",
        "effect give @s minecraft:haste 3 1 true",
        "function avatar:particles/fire_mythic"
    ],
    "fire_sovereign.mcfunction": [
        "scoreboard players set @s avatar_set 17",
        "effect give @s minecraft:fire_resistance 3 0 true",
        "effect give @s minecraft:strength 3 2 true",
        "effect give @s minecraft:speed 3 1 true",
        "effect give @s minecraft:haste 3 1 true",
        "function avatar:particles/fire_sovereign"
    ],

    # WATER
    "water_initiate.mcfunction": [
        "scoreboard players set @s avatar_set 21",
        "effect give @s minecraft:water_breathing 3 0 true",
        "function avatar:particles/water_initiate"
    ],
    "water_apprentice.mcfunction": [
        "scoreboard players set @s avatar_set 22",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "function avatar:particles/water_apprentice"
    ],
    "water_adept.mcfunction": [
        "scoreboard players set @s avatar_set 23",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "function avatar:particles/water_adept"
    ],
    "water_veteran.mcfunction": [
        "scoreboard players set @s avatar_set 24",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "effect give @s minecraft:resistance 3 0 true",
        "function avatar:particles/water_veteran"
    ],
    "water_master.mcfunction": [
        "scoreboard players set @s avatar_set 25",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "effect give @s minecraft:resistance 3 0 true",
        "function avatar:particles/water_master"
    ],
    "water_mythic.mcfunction": [
        "scoreboard players set @s avatar_set 26",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "effect give @s minecraft:resistance 3 0 true",
        "function avatar:particles/water_mythic"
    ],
    "water_sovereign.mcfunction": [
        "scoreboard players set @s avatar_set 27",
        "effect give @s minecraft:water_breathing 3 0 true",
        "effect give @s minecraft:dolphins_grace 3 0 true",
        "effect give @s minecraft:conduit_power 3 0 true",
        "effect give @s minecraft:resistance 3 0 true",
        "function avatar:particles/water_sovereign"
    ],

    # EARTH
    "earth_initiate.mcfunction": [
        "scoreboard players set @s avatar_set 31",
        "effect give @s minecraft:resistance 3 0 true",
        "function avatar:particles/earth_initiate"
    ],
    "earth_apprentice.mcfunction": [
        "scoreboard players set @s avatar_set 32",
        "effect give @s minecraft:resistance 3 0 true",
        "effect give @s minecraft:haste 3 0 true",
        "function avatar:particles/earth_apprentice"
    ],
    "earth_adept.mcfunction": [
        "scoreboard players set @s avatar_set 33",
        "effect give @s minecraft:resistance 3 0 true",
        "effect give @s minecraft:haste 3 0 true",
        "function avatar:particles/earth_adept"
    ],
    "earth_veteran.mcfunction": [
        "scoreboard players set @s avatar_set 34",
        "effect give @s minecraft:resistance 3 0 true",
        "effect give @s minecraft:haste 3 1 true",
        "function avatar:particles/earth_veteran"
    ],
    "earth_master.mcfunction": [
        "scoreboard players set @s avatar_set 35",
        "effect give @s minecraft:resistance 3 0 true",
        "effect give @s minecraft:haste 3 1 true",
        "effect give @s minecraft:strength 3 0 true",
        "function avatar:particles/earth_master"
    ],
    "earth_mythic.mcfunction": [
        "scoreboard players set @s avatar_set 36",
        "effect give @s minecraft:resistance 3 1 true",
        "effect give @s minecraft:haste 3 1 true",
        "effect give @s minecraft:strength 3 1 true",
        "function avatar:particles/earth_mythic"
    ],
    "earth_sovereign.mcfunction": [
        "scoreboard players set @s avatar_set 37",
        "effect give @s minecraft:resistance 3 1 true",
        "effect give @s minecraft:haste 3 2 true",
        "effect give @s minecraft:strength 3 1 true",
        "function avatar:particles/earth_sovereign"
    ],

    # AIR
    "air_initiate.mcfunction": [
        "scoreboard players set @s avatar_set 41",
        "effect give @s minecraft:speed 3 0 true",
        "effect give @s minecraft:jump_boost 3 0 true",
        "function avatar:particles/air_initiate"
    ],
    "air_apprentice.mcfunction": [
        "scoreboard players set @s avatar_set 42",
        "effect give @s minecraft:speed 3 0 true",
        "effect give @s minecraft:jump_boost 3 0 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "function avatar:particles/air_apprentice"
    ],
    "air_adept.mcfunction": [
        "scoreboard players set @s avatar_set 43",
        "effect give @s minecraft:speed 3 1 true",
        "effect give @s minecraft:jump_boost 3 1 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "function avatar:particles/air_adept"
    ],
    "air_veteran.mcfunction": [
        "scoreboard players set @s avatar_set 44",
        "effect give @s minecraft:speed 3 1 true",
        "effect give @s minecraft:jump_boost 3 1 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "effect give @s minecraft:haste 3 0 true",
        "function avatar:particles/air_veteran"
    ],
    "air_master.mcfunction": [
        "scoreboard players set @s avatar_set 45",
        "effect give @s minecraft:speed 3 2 true",
        "effect give @s minecraft:jump_boost 3 1 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "effect give @s minecraft:haste 3 1 true",
        "function avatar:particles/air_master"
    ],
    "air_mythic.mcfunction": [
        "scoreboard players set @s avatar_set 46",
        "effect give @s minecraft:speed 3 2 true",
        "effect give @s minecraft:jump_boost 3 2 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "effect give @s minecraft:haste 3 1 true",
        "function avatar:particles/air_mythic"
    ],
    "air_sovereign.mcfunction": [
        "scoreboard players set @s avatar_set 47",
        "effect give @s minecraft:speed 3 3 true",
        "effect give @s minecraft:jump_boost 3 2 true",
        "effect give @s minecraft:slow_falling 3 0 true",
        "effect give @s minecraft:haste 3 2 true",
        "function avatar:particles/air_sovereign"
    ]
}

for fname, lines in rebalanced.items():
    path = os.path.join(ab_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Rebalanced Avatar Ability - {fname}\n")
        for line in lines:
            f.write(f"{line}\n")

print("All ability functions rebalanced cleanly without health_boost or regen tick loops!")
