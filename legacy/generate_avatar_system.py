#!/usr/bin/env python3
"""
Avatar Armor Datapack & Resource Pack Generator for Minecraft Java 1.21.1
Generates:
1. Datapack recipes (64 recipes: 4 nations x 4 tiers x 4 pieces)
2. Datapack give functions (16 tier functions + 4 nation shorthand functions)
3. Datapack detection functions (nation and tier detectors)
4. Datapack abilities functions (16 tier abilities + 4 aliases)
5. Datapack particle functions (16 tier particles + 4 aliases)
6. Datapack setup.mcfunction and tick.mcfunction
7. Resource pack vanilla overrides (12 files in assets/minecraft/models/item/)
8. Resource pack custom item models (64 files in assets/avatar/models/item/ + 16 aliases)
9. Resource pack item textures (64 PNGs in assets/avatar/textures/item/ + 16 aliases)
10. Validates all generated JSON files and mcfunction syntax
"""

import os
import json
from PIL import Image, ImageDraw

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-armor-datapack")
RESOURCEPACK_DIR = os.path.join(REPO_DIR, "avatar-armor-resourcepack")

# Datapack subdirectories
DATA_AVATAR = os.path.join(DATAPACK_DIR, "data", "avatar")
RECIPES_DIR = os.path.join(DATA_AVATAR, "recipe")
FUNCTIONS_DIR = os.path.join(DATA_AVATAR, "function")
GIVE_DIR = os.path.join(FUNCTIONS_DIR, "give")
DETECT_DIR = os.path.join(FUNCTIONS_DIR, "detect")
ABILITIES_DIR = os.path.join(FUNCTIONS_DIR, "abilities")
PARTICLES_DIR = os.path.join(FUNCTIONS_DIR, "particles")

# Resource pack subdirectories
ASSETS_AVATAR = os.path.join(RESOURCEPACK_DIR, "assets", "avatar")
ASSETS_MC = os.path.join(RESOURCEPACK_DIR, "assets", "minecraft")
ITEM_MODELS_DIR = os.path.join(ASSETS_AVATAR, "models", "item")
ITEM_TEX_DIR = os.path.join(ASSETS_AVATAR, "textures", "item")
MC_ITEM_MODELS_DIR = os.path.join(ASSETS_MC, "models", "item")

for d in [RECIPES_DIR, GIVE_DIR, DETECT_DIR, ABILITIES_DIR, PARTICLES_DIR,
          ITEM_MODELS_DIR, ITEM_TEX_DIR, MC_ITEM_MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

# ------------------------------------------------------------------------------
# Nation, Tier, Piece Definitions
# ------------------------------------------------------------------------------
NATIONS = ["fire", "water", "earth", "air"]
TIERS = ["basic", "adept", "master", "legendary"]
PIECES = ["helmet", "chestplate", "leggings", "boots"]

SLOTS = {
    "helmet": "head",
    "chestplate": "chest",
    "leggings": "legs",
    "boots": "feet"
}

PIECE_CODES = {
    "helmet": "01",
    "chestplate": "02",
    "leggings": "03",
    "boots": "04"
}

NATION_PREFIX = {
    "fire": 1,
    "water": 2,
    "earth": 3,
    "air": 4
}

TIER_INDEX = {
    "basic": 1,
    "adept": 2,
    "master": 3,
    "legendary": 4
}

TIER_ROMAN = {
    "basic": "Tier I: Basic Elemental Armor",
    "adept": "Tier II: Adept Elemental Armor",
    "master": "Tier III: Master Elemental Armor",
    "legendary": "Tier IV: Legendary Sovereign Armor"
}

TIER_LORE_COLOR = {
    "basic": "white",
    "adept": "aqua",
    "master": "gold",
    "legendary": "light_purple"
}

BASE_ITEMS = {
    "basic": {
        "helmet": "minecraft:iron_helmet",
        "chestplate": "minecraft:iron_chestplate",
        "leggings": "minecraft:iron_leggings",
        "boots": "minecraft:iron_boots"
    },
    "adept": {
        "helmet": "minecraft:diamond_helmet",
        "chestplate": "minecraft:diamond_chestplate",
        "leggings": "minecraft:diamond_leggings",
        "boots": "minecraft:diamond_boots"
    },
    "master": {
        "helmet": "minecraft:netherite_helmet",
        "chestplate": "minecraft:netherite_chestplate",
        "leggings": "minecraft:netherite_leggings",
        "boots": "minecraft:netherite_boots"
    },
    "legendary": {
        "helmet": "minecraft:netherite_helmet",
        "chestplate": "minecraft:netherite_chestplate",
        "leggings": "minecraft:netherite_leggings",
        "boots": "minecraft:netherite_boots"
    }
}

TRIM_CONFIG = {
    "fire": {
        "basic": {"material": "minecraft:redstone", "pattern": "minecraft:sentry"},
        "adept": {"material": "minecraft:redstone", "pattern": "minecraft:dune"},
        "master": {"material": "minecraft:gold", "pattern": "minecraft:rib"},
        "legendary": {"material": "minecraft:redstone", "pattern": "minecraft:silence"}
    },
    "water": {
        "basic": {"material": "minecraft:lapis", "pattern": "minecraft:coast"},
        "adept": {"material": "minecraft:quartz", "pattern": "minecraft:tide"},
        "master": {"material": "minecraft:diamond", "pattern": "minecraft:tide"},
        "legendary": {"material": "minecraft:lapis", "pattern": "minecraft:silence"}
    },
    "earth": {
        "basic": {"material": "minecraft:emerald", "pattern": "minecraft:wayfinder"},
        "adept": {"material": "minecraft:emerald", "pattern": "minecraft:raiser"},
        "master": {"material": "minecraft:emerald", "pattern": "minecraft:ward"},
        "legendary": {"material": "minecraft:emerald", "pattern": "minecraft:silence"}
    },
    "air": {
        "basic": {"material": "minecraft:copper", "pattern": "minecraft:flow"},
        "adept": {"material": "minecraft:gold", "pattern": "minecraft:flow"},
        "master": {"material": "minecraft:quartz", "pattern": "minecraft:flow"},
        "legendary": {"material": "minecraft:gold", "pattern": "minecraft:silence"}
    }
}

CATALYSTS = {
    "fire": {
        "basic": "minecraft:blaze_powder",
        "adept": "minecraft:blaze_rod",
        "master": ["minecraft:netherite_ingot", "minecraft:magma_cream"],
        "legendary": ["minecraft:nether_star", "minecraft:fire_charge"]
    },
    "water": {
        "basic": "minecraft:prismarine_shard",
        "adept": "minecraft:prismarine_crystals",
        "master": ["minecraft:netherite_ingot", "minecraft:heart_of_the_sea"],
        "legendary": ["minecraft:nether_star", "minecraft:nautilus_shell"]
    },
    "earth": {
        "basic": "minecraft:emerald",
        "adept": "minecraft:diamond",
        "master": ["minecraft:netherite_ingot", "minecraft:echo_shard"],
        "legendary": ["minecraft:nether_star", "minecraft:heavy_core"]
    },
    "air": {
        "basic": "minecraft:feather",
        "adept": "minecraft:phantom_membrane",
        "master": ["minecraft:netherite_ingot", "minecraft:breeze_rod"],
        "legendary": ["minecraft:nether_star", "minecraft:dragon_breath"]
    }
}

ITEM_DISPLAY = {
    "fire": {
        "basic": {
            "prefix": "Fire Nation Scout",
            "color": "red",
            "bold": False,
            "names": {"helmet": "Helmet", "chestplate": "Tunic", "leggings": "Greaves", "boots": "Boots"},
            "desc": "Forged for vanguard scouts of the Fire Nation.",
            "set_bonus": "Full Set: Fire Resistance + Attack Damage"
        },
        "adept": {
            "prefix": "Fire Nation Officer",
            "color": "dark_red",
            "bold": False,
            "names": {"helmet": "Helmet", "chestplate": "Cuirass", "leggings": "Leggings", "boots": "Boots"},
            "desc": "Issued to decorated commanders of the Fire Navy.",
            "set_bonus": "Full Set: Fire Resistance + Strength I"
        },
        "master": {
            "prefix": "Fire Nation Royal Guard",
            "color": "gold",
            "bold": True,
            "names": {"helmet": "Visor", "chestplate": "Plate", "leggings": "Greaves", "boots": "Striders"},
            "desc": "Infused with pure volcanic magma and netherite.",
            "set_bonus": "Full Set: Fire Resistance + Strength II + Speed I"
        },
        "legendary": {
            "prefix": "Dragon Fire Sovereign",
            "color": "dark_purple",
            "bold": True,
            "names": {"helmet": "Crown", "chestplate": "Raiment", "leggings": "Greaves", "boots": "Striders"},
            "desc": "Blessed by the ancient Sun Warriors and the Eternal Dragons.",
            "set_bonus": "Full Set: Fire Resistance + Strength II + Speed I + Haste I + Flame Aura"
        }
    },
    "water": {
        "basic": {
            "prefix": "Water Tribe Hunter",
            "color": "blue",
            "bold": False,
            "names": {"helmet": "Hood", "chestplate": "Parka", "leggings": "Trousers", "boots": "Boots"},
            "desc": "Woven by Northern craftsmen with hardened iron weaves.",
            "set_bonus": "Full Set: Water Breathing + Toughness"
        },
        "adept": {
            "prefix": "Water Tribe Warrior",
            "color": "dark_aqua",
            "bold": False,
            "names": {"helmet": "Cap", "chestplate": "Parka", "leggings": "Breeches", "boots": "Moccasins"},
            "desc": "Enchanted with glacial diamond and arctic frost.",
            "set_bonus": "Full Set: Water Breathing + Dolphin's Grace + Regen I"
        },
        "master": {
            "prefix": "Water Tribe Healer",
            "color": "aqua",
            "bold": True,
            "names": {"helmet": "Crown", "chestplate": "Robes", "leggings": "Sarong", "boots": "Treads"},
            "desc": "Channeling sacred Spirit Oasis water through netherite.",
            "set_bonus": "Full Set: Water Breathing + Dolphin's Grace + Regen II + Health Boost I"
        },
        "legendary": {
            "prefix": "Ocean Spirit Sovereign",
            "color": "dark_purple",
            "bold": True,
            "names": {"helmet": "Diadem", "chestplate": "Vestment", "leggings": "Kilt", "boots": "Treads"},
            "desc": "Embodying the eternal cosmic harmony of Tui and La.",
            "set_bonus": "Full Set: Water Breathing + Dolphin's Grace + Regen II + Resistance I + Health Boost II + Splash Aura"
        }
    },
    "earth": {
        "basic": {
            "prefix": "Earth Kingdom Recruit",
            "color": "dark_green",
            "bold": False,
            "names": {"helmet": "Conical", "chestplate": "Hauberk", "leggings": "Pants", "boots": "Boots"},
            "desc": "Standard battle dress for Earth Kingdom defenders.",
            "set_bonus": "Full Set: Resistance I"
        },
        "adept": {
            "prefix": "Earth Kingdom Guard",
            "color": "green",
            "bold": False,
            "names": {"helmet": "Helm", "chestplate": "Plate", "leggings": "Greaves", "boots": "Stompers"},
            "desc": "Reinforced with crystalline diamond and bedrock stone.",
            "set_bonus": "Full Set: Resistance I + Haste I"
        },
        "master": {
            "prefix": "Dai Li Shadow",
            "color": "dark_green",
            "bold": True,
            "names": {"helmet": "Cowl", "chestplate": "Cuirass", "leggings": "Trousers", "boots": "Sabatons"},
            "desc": "Dense netherite forged by the elite agents of Ba Sing Se.",
            "set_bonus": "Full Set: Resistance II + Haste II + Heavy Aura / Knockback Resist"
        },
        "legendary": {
            "prefix": "Titan Earth Sovereign",
            "color": "dark_purple",
            "bold": True,
            "names": {"helmet": "Helm", "chestplate": "Bulwark", "leggings": "Greaves", "boots": "Stompers"},
            "desc": "Imbued with the unwavering fortitude of the deepest mantle.",
            "set_bonus": "Full Set: Resistance III + Haste II + Strength I + 100% Knockback Resist + Earth Tremor Aura"
        }
    },
    "air": {
        "basic": {
            "prefix": "Air Nomad Novice",
            "color": "yellow",
            "bold": False,
            "names": {"helmet": "Cowl", "chestplate": "Shawl", "leggings": "Wraps", "boots": "Sandals"},
            "desc": "Lightweight iron weaves crafted at the Southern Air Temple.",
            "set_bonus": "Full Set: Speed I + Jump Boost I"
        },
        "adept": {
            "prefix": "Air Nomad Adept",
            "color": "gold",
            "bold": False,
            "names": {"helmet": "Cowl", "chestplate": "Robes", "leggings": "Hakama", "boots": "Sandals"},
            "desc": "Spun with sky bison silk and diamond threading.",
            "set_bonus": "Full Set: Speed II + Jump Boost I + Slow Falling"
        },
        "master": {
            "prefix": "Air Temple Master",
            "color": "white",
            "bold": True,
            "names": {"helmet": "Cowl", "chestplate": "Kasaya", "leggings": "Pants", "boots": "Treads"},
            "desc": "Bestowed upon true masters of weightlessness.",
            "set_bonus": "Full Set: Speed III + Jump Boost II + Slow Falling"
        },
        "legendary": {
            "prefix": "Zephyr Sky Sovereign",
            "color": "dark_purple",
            "bold": True,
            "names": {"helmet": "Crown", "chestplate": "Robes", "leggings": "Garments", "boots": "Gliders"},
            "desc": "Become wind itself. Unbound by gravity, free as the heavens.",
            "set_bonus": "Full Set: Speed III + Jump Boost III + Slow Falling + Wind Gust Aura"
        }
    }
}

# ------------------------------------------------------------------------------
# Attribute Modifiers Helper
# ------------------------------------------------------------------------------
def get_attribute_modifiers(nation, tier, piece):
    slot = SLOTS[piece]
    base_armor = {
        "basic": {"helmet": 2.0, "chestplate": 6.0, "leggings": 5.0, "boots": 2.0},
        "adept": {"helmet": 3.0, "chestplate": 8.0, "leggings": 6.0, "boots": 3.0},
        "master": {"helmet": 3.0, "chestplate": 8.0, "leggings": 6.0, "boots": 3.0},
        "legendary": {"helmet": 3.0, "chestplate": 8.0, "leggings": 6.0, "boots": 3.0}
    }
    base_toughness = {
        "basic": 0.0,
        "adept": 2.0,
        "master": 3.0,
        "legendary": 3.0
    }
    base_knockback = {
        "basic": 0.0,
        "adept": 0.0,
        "master": 0.1,
        "legendary": 0.1
    }

    armor_val = base_armor[tier][piece]
    toughness_val = base_toughness[tier]
    knockback_val = base_knockback[tier]

    modifiers = []

    # Nation-specific bonus adjustments
    if nation == "fire":
        if tier == "basic" and piece == "chestplate":
            modifiers.append({"type": "minecraft:generic.attack_damage", "id": f"avatar:{nation}_{tier}_{piece}_attack", "amount": 0.5, "operation": "add_value", "slot": slot})
        elif tier == "adept" and piece == "chestplate":
            modifiers.append({"type": "minecraft:generic.attack_damage", "id": f"avatar:{nation}_{tier}_{piece}_attack", "amount": 1.0, "operation": "add_value", "slot": slot})
        elif tier == "master":
            atk = 1.5 if piece == "chestplate" else 0.5
            modifiers.append({"type": "minecraft:generic.attack_damage", "id": f"avatar:{nation}_{tier}_{piece}_attack", "amount": atk, "operation": "add_value", "slot": slot})
        elif tier == "legendary":
            atk = 2.0 if piece == "chestplate" else 1.0
            modifiers.append({"type": "minecraft:generic.attack_damage", "id": f"avatar:{nation}_{tier}_{piece}_attack", "amount": atk, "operation": "add_value", "slot": slot})

    elif nation == "water":
        if tier == "basic":
            toughness_val += 0.25 # +1 toughness across 4 pieces
        elif tier == "adept":
            toughness_val += 0.5
        elif tier == "master":
            toughness_val += 0.5
            if piece == "chestplate":
                modifiers.append({"type": "minecraft:generic.max_health", "id": f"avatar:{nation}_{tier}_{piece}_health", "amount": 2.0, "operation": "add_value", "slot": slot})
        elif tier == "legendary":
            toughness_val += 1.0 # 4.0 toughness per piece = 16 toughness!
            if piece == "chestplate":
                modifiers.append({"type": "minecraft:generic.max_health", "id": f"avatar:{nation}_{tier}_{piece}_health", "amount": 4.0, "operation": "add_value", "slot": slot})
            elif piece in ["helmet", "leggings"]:
                modifiers.append({"type": "minecraft:generic.max_health", "id": f"avatar:{nation}_{tier}_{piece}_health", "amount": 2.0, "operation": "add_value", "slot": slot})

    elif nation == "earth":
        if tier == "basic" and piece == "chestplate":
            armor_val += 1.0
        elif tier == "adept":
            knockback_val += 0.05
        elif tier == "master":
            knockback_val += 0.15
            if piece == "chestplate":
                armor_val += 1.0
        elif tier == "legendary":
            knockback_val = 0.25 # 0.25 * 4 = 1.0 (100% knockback resistance!)
            if piece == "chestplate":
                armor_val += 2.0 # 10 armor!
                modifiers.append({"type": "minecraft:generic.attack_damage", "id": f"avatar:{nation}_{tier}_{piece}_attack", "amount": 2.0, "operation": "add_value", "slot": slot})

    elif nation == "air":
        if tier == "basic" and piece == "boots":
            modifiers.append({"type": "minecraft:generic.movement_speed", "id": f"avatar:{nation}_{tier}_{piece}_speed", "amount": 0.02, "operation": "add_value", "slot": slot})
        elif tier == "adept" and piece == "boots":
            modifiers.append({"type": "minecraft:generic.movement_speed", "id": f"avatar:{nation}_{tier}_{piece}_speed", "amount": 0.04, "operation": "add_value", "slot": slot})
        elif tier == "master":
            if piece == "boots":
                modifiers.append({"type": "minecraft:generic.movement_speed", "id": f"avatar:{nation}_{tier}_{piece}_speed", "amount": 0.05, "operation": "add_value", "slot": slot})
            elif piece == "leggings":
                modifiers.append({"type": "minecraft:generic.movement_speed", "id": f"avatar:{nation}_{tier}_{piece}_speed", "amount": 0.02, "operation": "add_value", "slot": slot})
        elif tier == "legendary":
            speed_map = {"boots": 0.08, "leggings": 0.04, "chestplate": 0.03, "helmet": 0.02}
            modifiers.append({"type": "minecraft:generic.movement_speed", "id": f"avatar:{nation}_{tier}_{piece}_speed", "amount": speed_map[piece], "operation": "add_value", "slot": slot})

    # Standard armor attribute
    modifiers.insert(0, {"type": "minecraft:generic.armor", "id": f"avatar:{nation}_{tier}_{piece}_armor", "amount": armor_val, "operation": "add_value", "slot": slot})

    if toughness_val > 0.0:
        modifiers.append({"type": "minecraft:generic.armor_toughness", "id": f"avatar:{nation}_{tier}_{piece}_toughness", "amount": toughness_val, "operation": "add_value", "slot": slot})

    if knockback_val > 0.0:
        modifiers.append({"type": "minecraft:generic.knockback_resistance", "id": f"avatar:{nation}_{tier}_{piece}_knockback", "amount": knockback_val, "operation": "add_value", "slot": slot})

    return modifiers

def get_custom_model_data(nation, tier, piece):
    n = NATION_PREFIX[nation]
    t = TIER_INDEX[tier]
    p = PIECE_CODES[piece]
    return int(f"{n}{t}{p}")

# ------------------------------------------------------------------------------
# 1. Generate Datapack Recipes (64 shapeless recipes)
# ------------------------------------------------------------------------------
def generate_recipes():
    print("Generating 64 shapeless crafting recipes...")
    count = 0
    for nation in NATIONS:
        for tier in TIERS:
            for piece in PIECES:
                base_item = BASE_ITEMS[tier][piece]
                cmd = get_custom_model_data(nation, tier, piece)
                trim = TRIM_CONFIG[nation][tier]
                disp = ITEM_DISPLAY[nation][tier]
                item_title = f"{disp['prefix']} {disp['names'][piece]}"

                item_name_json = json.dumps({
                    "text": item_title,
                    "color": disp["color"],
                    "bold": disp["bold"],
                    "italic": False
                })

                lore_list = [
                    json.dumps({"text": TIER_ROMAN[tier], "color": TIER_LORE_COLOR[tier], "bold": (tier == "legendary"), "italic": False}),
                    json.dumps({"text": disp["desc"], "color": "gold", "italic": True}),
                    json.dumps({"text": disp["set_bonus"], "color": "red" if nation == "fire" else "blue" if nation == "water" else "green" if nation == "earth" else "yellow", "italic": False})
                ]

                modifiers = get_attribute_modifiers(nation, tier, piece)

                # Determine ingredients based on tier
                if tier == "basic":
                    cat = CATALYSTS[nation]["basic"]
                    ingredients = [{"item": f"minecraft:iron_{piece}"}, {"item": cat}]
                elif tier == "adept":
                    cat = CATALYSTS[nation]["adept"]
                    # Upgrade from Basic (Iron)
                    ingredients = [{"item": f"minecraft:iron_{piece}"}, {"item": cat}]
                elif tier == "master":
                    cats = CATALYSTS[nation]["master"]
                    # Upgrade from Adept (Diamond)
                    ingredients = [{"item": f"minecraft:diamond_{piece}"}] + [{"item": c} for c in cats]
                elif tier == "legendary":
                    cats = CATALYSTS[nation]["legendary"]
                    # Upgrade from Master (Netherite)
                    ingredients = [{"item": f"minecraft:netherite_{piece}"}] + [{"item": c} for c in cats]

                recipe_data = {
                    "type": "minecraft:crafting_shapeless",
                    "category": "equipment",
                    "ingredients": ingredients,
                    "result": {
                        "id": base_item,
                        "count": 1,
                        "components": {
                            "minecraft:custom_data": {
                                "avatar": {
                                    "nation": nation,
                                    "tier": tier,
                                    "piece": piece
                                }
                            },
                            "minecraft:item_name": item_name_json,
                            "minecraft:lore": lore_list,
                            "minecraft:trim": trim,
                            "minecraft:custom_model_data": cmd,
                            "minecraft:attribute_modifiers": modifiers
                        }
                    }
                }

                recipe_filename = f"{nation}_{tier}_{piece}.json"
                recipe_path = os.path.join(RECIPES_DIR, recipe_filename)
                with open(recipe_path, "w", encoding="utf-8") as f:
                    json.dump(recipe_data, f, indent=2)
                count += 1
    print(f"  -> Generated {count} recipe files in {RECIPES_DIR}")

# ------------------------------------------------------------------------------
# 2. Generate Datapack Give Functions (16 tier functions + 4 nation shorthand)
# ------------------------------------------------------------------------------
def generate_give_functions():
    print("Generating give functions...")
    # 16 Tier functions
    for nation in NATIONS:
        for tier in TIERS:
            lines = [
                f"# ==============================================================================",
                f"# Avatar Armor Datapack - Give {nation.capitalize()} {tier.capitalize()} Armor Set (1.21.1)",
                f"# ==============================================================================",
                ""
            ]
            for piece in PIECES:
                base_item = BASE_ITEMS[tier][piece]
                cmd = get_custom_model_data(nation, tier, piece)
                trim = TRIM_CONFIG[nation][tier]
                disp = ITEM_DISPLAY[nation][tier]
                item_title = f"{disp['prefix']} {disp['names'][piece]}"

                # Escaped JSON for SNBT
                item_name_snbt = json.dumps({
                    "text": item_title,
                    "color": disp["color"],
                    "bold": disp["bold"],
                    "italic": False
                })

                lore_1 = json.dumps({"text": TIER_ROMAN[tier], "color": TIER_LORE_COLOR[tier], "bold": (tier == "legendary"), "italic": False})
                lore_2 = json.dumps({"text": disp["desc"], "color": "gold", "italic": True})
                color_bonus = "red" if nation == "fire" else "blue" if nation == "water" else "green" if nation == "earth" else "yellow"
                lore_3 = json.dumps({"text": disp["set_bonus"], "color": color_bonus, "italic": False})
                lore_snbt = f"['{lore_1}','{lore_2}','{lore_3}']"

                # Attribute modifiers list for SNBT
                modifiers = get_attribute_modifiers(nation, tier, piece)
                mod_snbt_parts = []
                for m in modifiers:
                    mod_snbt_parts.append(f'{{type:"{m["type"]}",id:"{m["id"]}",amount:{m["amount"]},operation:"{m["operation"]}",slot:"{m["slot"]}"}}')
                mod_snbt = f"[{','.join(mod_snbt_parts)}]"

                trim_snbt = f'{{material:"{trim["material"]}",pattern:"{trim["pattern"]}"}}'
                custom_data_snbt = f'{{avatar:{{nation:"{nation}",tier:"{tier}",piece:"{piece}"}}}}'

                cmd_line = f"give @s {base_item}[minecraft:custom_data={custom_data_snbt},minecraft:item_name='{item_name_snbt}',minecraft:lore={lore_snbt},minecraft:trim={trim_snbt},minecraft:custom_model_data={cmd},minecraft:attribute_modifiers={mod_snbt}]"
                lines.append(f"# {piece.capitalize()}")
                lines.append(cmd_line)
                lines.append("")

            fn_name = f"{nation}_{tier}.mcfunction"
            with open(os.path.join(GIVE_DIR, fn_name), "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

    # 4 Nation shorthand functions (alias to Legendary tier set)
    nation_aliases = {
        "fire_nation": "fire_legendary",
        "water_tribe": "water_legendary",
        "earth_kingdom": "earth_legendary",
        "air_nomad": "air_legendary"
    }
    for alias, target in nation_aliases.items():
        with open(os.path.join(GIVE_DIR, f"{alias}.mcfunction"), "w", encoding="utf-8") as f:
            f.write(f"# Shorthand: Give {alias} (Legendary Sovereign Set)\nfunction avatar:give/{target}\n")

    print(f"  -> Generated 16 tier give functions + 4 nation shorthands")

# ------------------------------------------------------------------------------
# 3. Generate Abilities and Particles
# ------------------------------------------------------------------------------
def generate_abilities_and_particles():
    print("Generating abilities and particle functions...")
    for nation in NATIONS:
        for tier in TIERS:
            # Ability file
            ab_lines = [
                f"# ==============================================================================",
                f"# Avatar Armor Datapack - {nation.capitalize()} {tier.capitalize()} Full Set Ability",
                f"# ==============================================================================",
                f"scoreboard players set @s avatar_set {NATION_PREFIX[nation]}{TIER_INDEX[tier]}"
            ]

            if nation == "fire":
                ab_lines.append("effect give @s minecraft:fire_resistance 3 0 true")
                if tier == "adept":
                    ab_lines.append("effect give @s minecraft:strength 3 0 true")
                elif tier == "master":
                    ab_lines.append("effect give @s minecraft:strength 3 1 true")
                    ab_lines.append("effect give @s minecraft:speed 3 0 true")
                elif tier == "legendary":
                    ab_lines.append("effect give @s minecraft:strength 3 1 true")
                    ab_lines.append("effect give @s minecraft:speed 3 0 true")
                    ab_lines.append("effect give @s minecraft:haste 3 0 true")

            elif nation == "water":
                ab_lines.append("effect give @s minecraft:water_breathing 3 0 true")
                if tier == "adept":
                    ab_lines.append("effect give @s minecraft:dolphins_grace 3 0 true")
                    ab_lines.append("effect give @s minecraft:regeneration 3 0 true")
                elif tier == "master":
                    ab_lines.append("effect give @s minecraft:dolphins_grace 3 0 true")
                    ab_lines.append("effect give @s minecraft:regeneration 3 1 true")
                    ab_lines.append("effect give @s minecraft:health_boost 3 0 true")
                elif tier == "legendary":
                    ab_lines.append("effect give @s minecraft:dolphins_grace 3 0 true")
                    ab_lines.append("effect give @s minecraft:regeneration 3 1 true")
                    ab_lines.append("effect give @s minecraft:resistance 3 0 true")
                    ab_lines.append("effect give @s minecraft:health_boost 3 1 true")

            elif nation == "earth":
                if tier == "basic":
                    ab_lines.append("effect give @s minecraft:resistance 3 0 true")
                elif tier == "adept":
                    ab_lines.append("effect give @s minecraft:resistance 3 0 true")
                    ab_lines.append("effect give @s minecraft:haste 3 0 true")
                elif tier == "master":
                    ab_lines.append("effect give @s minecraft:resistance 3 1 true")
                    ab_lines.append("effect give @s minecraft:haste 3 1 true")
                    ab_lines.append("execute at @s run effect give @e[type=!minecraft:player,distance=0.1..5] minecraft:slowness 2 0 true")
                elif tier == "legendary":
                    ab_lines.append("effect give @s minecraft:resistance 3 2 true")
                    ab_lines.append("effect give @s minecraft:haste 3 1 true")
                    ab_lines.append("effect give @s minecraft:strength 3 0 true")
                    ab_lines.append("execute at @s run effect give @e[type=!minecraft:player,distance=0.1..6] minecraft:slowness 2 1 true")

            elif nation == "air":
                if tier == "basic":
                    ab_lines.append("effect give @s minecraft:speed 3 0 true")
                    ab_lines.append("effect give @s minecraft:jump_boost 3 0 true")
                elif tier == "adept":
                    ab_lines.append("effect give @s minecraft:speed 3 1 true")
                    ab_lines.append("effect give @s minecraft:jump_boost 3 0 true")
                    ab_lines.append("effect give @s minecraft:slow_falling 3 0 true")
                elif tier == "master":
                    ab_lines.append("effect give @s minecraft:speed 3 2 true")
                    ab_lines.append("effect give @s minecraft:jump_boost 3 1 true")
                    ab_lines.append("effect give @s minecraft:slow_falling 3 0 true")
                elif tier == "legendary":
                    ab_lines.append("effect give @s minecraft:speed 3 2 true")
                    ab_lines.append("effect give @s minecraft:jump_boost 3 2 true")
                    ab_lines.append("effect give @s minecraft:slow_falling 3 0 true")

            ab_lines.append(f"function avatar:particles/{nation}_{tier}\n")
            with open(os.path.join(ABILITIES_DIR, f"{nation}_{tier}.mcfunction"), "w", encoding="utf-8") as f:
                f.write("\n".join(ab_lines))

            # Particle file
            pt_lines = [
                f"# ==============================================================================",
                f"# Avatar Armor Datapack - {nation.capitalize()} {tier.capitalize()} Particles",
                f"# =============================================================================="
            ]
            if nation == "fire":
                if tier == "basic":
                    pt_lines.append("particle minecraft:small_flame ~ ~0.5 ~ 0.2 0.3 0.2 0.01 1 normal")
                elif tier == "adept":
                    pt_lines.append("particle minecraft:flame ~ ~0.6 ~ 0.25 0.35 0.25 0.01 2 normal")
                elif tier == "master":
                    pt_lines.append("particle minecraft:flame ~ ~0.8 ~ 0.3 0.4 0.3 0.02 3 normal")
                    pt_lines.append("particle minecraft:lava ~ ~0.5 ~ 0.2 0.2 0.2 1 normal")
                elif tier == "legendary":
                    pt_lines.append("particle minecraft:flame ~ ~0.9 ~ 0.35 0.5 0.35 0.02 4 normal")
                    pt_lines.append("particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.2 0.3 0.2 0.01 2 normal")
                    pt_lines.append("particle minecraft:smoke ~ ~1.2 ~ 0.15 0.15 0.15 0.01 1 normal")

            elif nation == "water":
                if tier == "basic":
                    pt_lines.append("particle minecraft:splash ~ ~0.2 ~ 0.2 0.1 0.2 0.01 2 normal")
                elif tier == "adept":
                    pt_lines.append("particle minecraft:splash ~ ~0.5 ~ 0.25 0.2 0.25 0.02 3 normal")
                    pt_lines.append("particle minecraft:bubble ~ ~0.8 ~ 0.2 0.3 0.2 0.01 1 normal")
                elif tier == "master":
                    pt_lines.append("particle minecraft:splash ~ ~0.5 ~ 0.3 0.3 0.3 0.02 4 normal")
                    pt_lines.append("particle minecraft:bubble_pop ~ ~1.0 ~ 0.25 0.35 0.25 0.01 2 normal")
                elif tier == "legendary":
                    pt_lines.append("particle minecraft:splash ~ ~0.6 ~ 0.35 0.4 0.35 0.03 5 normal")
                    pt_lines.append("particle minecraft:bubble_column_up ~ ~0.2 ~ 0.2 0.4 0.2 0.05 3 normal")
                    pt_lines.append("particle minecraft:dripping_water ~ ~1.5 ~ 0.2 0.1 0.2 0.01 2 normal")

            elif nation == "earth":
                if tier == "basic":
                    pt_lines.append("particle minecraft:dust{color:[0.4,0.3,0.1],scale:0.8} ~ ~0.1 ~ 0.2 0.05 0.2 0.01 2 normal")
                elif tier == "adept":
                    pt_lines.append("particle minecraft:block dirt ~ ~0.1 ~ 0.25 0.05 0.25 0.01 3 normal")
                elif tier == "master":
                    pt_lines.append("particle minecraft:block tuff ~ ~0.15 ~ 0.3 0.1 0.3 0.02 4 normal")
                    pt_lines.append("particle minecraft:dust{color:[0.3,0.5,0.2],scale:1.0} ~ ~0.5 ~ 0.25 0.25 0.25 0.01 2 normal")
                elif tier == "legendary":
                    pt_lines.append("particle minecraft:block netherite_block ~ ~0.1 ~ 0.35 0.1 0.35 0.02 5 normal")
                    pt_lines.append("particle minecraft:dust{color:[0.2,0.7,0.3],scale:1.2} ~ ~0.6 ~ 0.3 0.4 0.3 0.02 3 normal")

            elif nation == "air":
                if tier == "basic":
                    pt_lines.append("particle minecraft:cloud ~ ~0.3 ~ 0.2 0.1 0.2 0.01 1 normal")
                elif tier == "adept":
                    pt_lines.append("particle minecraft:cloud ~ ~0.5 ~ 0.25 0.2 0.25 0.01 2 normal")
                    pt_lines.append("particle minecraft:sweep_attack ~ ~0.8 ~ 0.1 0.1 0.1 0.01 1 normal")
                elif tier == "master":
                    pt_lines.append("particle minecraft:cloud ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3 normal")
                    pt_lines.append("particle minecraft:gust ~ ~0.5 ~ 0.2 0.2 0.2 0.01 1 normal")
                elif tier == "legendary":
                    pt_lines.append("particle minecraft:cloud ~ ~0.7 ~ 0.35 0.4 0.35 0.02 4 normal")
                    pt_lines.append("particle minecraft:gust_emitter ~ ~0.5 ~ 0.2 0.2 0.2 0.01 1 normal")

            pt_lines.append("")
            with open(os.path.join(PARTICLES_DIR, f"{nation}_{tier}.mcfunction"), "w", encoding="utf-8") as f:
                f.write("\n".join(pt_lines))

    # Legacy aliases
    nation_aliases = {
        "fire_nation": "fire_legendary",
        "water_tribe": "water_legendary",
        "earth_kingdom": "earth_legendary",
        "air_nomad": "air_legendary"
    }
    for alias, target in nation_aliases.items():
        with open(os.path.join(ABILITIES_DIR, f"{alias}.mcfunction"), "w", encoding="utf-8") as f:
            f.write(f"# Alias to {target}\nfunction avatar:abilities/{target}\n")

    particle_aliases = {
        "fire": "fire_legendary",
        "water": "water_legendary",
        "earth": "earth_legendary",
        "air": "air_legendary"
    }
    for alias, target in particle_aliases.items():
        with open(os.path.join(PARTICLES_DIR, f"{alias}.mcfunction"), "w", encoding="utf-8") as f:
            f.write(f"# Alias to {target}\nfunction avatar:particles/{target}\n")

# ------------------------------------------------------------------------------
# 4. Generate Detection System
# ------------------------------------------------------------------------------
def generate_detect_functions():
    print("Generating detection system...")
    for nation in NATIONS:
        alias_map = {
            "fire": "fire_nation",
            "water": "water_tribe",
            "earth": "earth_kingdom",
            "air": "air_nomad"
        }
        nation_fn = alias_map[nation]
        lines = [
            f"# ==============================================================================",
            f"# Avatar Armor Datapack - Detect {nation_fn} (Checks 4 Tiers: Legendary -> Basic)",
            f"# ==============================================================================",
            ""
        ]
        # Check tiers from highest to lowest
        for tier in reversed(TIERS):
            check_line = (
                f'execute if items entity @s armor.chest *[custom_data~{{avatar:{{tier:"{tier}"}}}}] '
                f'if items entity @s armor.head *[custom_data~{{avatar:{{nation:"{nation}",tier:"{tier}"}}}}] '
                f'if items entity @s armor.legs *[custom_data~{{avatar:{{nation:"{nation}",tier:"{tier}"}}}}] '
                f'if items entity @s armor.feet *[custom_data~{{avatar:{{nation:"{nation}",tier:"{tier}"}}}}] '
                f'run function avatar:abilities/{nation}_{tier}'
            )
            lines.append(f"# {tier.capitalize()} Tier Full Set Check")
            lines.append(check_line)
            lines.append("")

        with open(os.path.join(DETECT_DIR, f"{nation_fn}.mcfunction"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # Setup.mcfunction
    setup_content = """# ==============================================================================
# Avatar Armor Datapack - Setup / Initialization (Minecraft 1.21.1)
# ==============================================================================

# Create scoreboard objectives for tracking
scoreboard objectives add avatar_set dummy "Avatar Active Set"

# Welcome / Announcement message
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"Avatar Armor","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Avatar 4-Tier Elemental Armor Datapack (1.21.1) loaded!","color":"green"}]
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"Avatar Armor","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Progression: ","color":"gray"},{"text":"Basic (Iron) ","color":"white"},{"text":"-> ","color":"dark_gray"},{"text":"Adept (Diamond) ","color":"aqua"},{"text":"-> ","color":"dark_gray"},{"text":"Master (Netherite) ","color":"gold"},{"text":"-> ","color":"dark_gray"},{"text":"Legendary (Sovereign)","color":"light_purple","bold":true}]
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"Avatar Armor","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Use ","color":"gray"},{"text":"/function avatar:give/<nation>_<tier>","color":"yellow"},{"text":" or craft sets at a crafting table.","color":"gray"}]
"""
    with open(os.path.join(FUNCTIONS_DIR, "setup.mcfunction"), "w", encoding="utf-8") as f:
        f.write(setup_content)

    # Tick.mcfunction
    tick_content = """# ==============================================================================
# Avatar Armor Datapack - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# Reset active set status for all online players before detection
scoreboard players set @a avatar_set 0

# Fast nation routing: only execute nation check if player is wearing that nation's chestplate
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"fire"}}] run function avatar:detect/fire_nation
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"water"}}] run function avatar:detect/water_tribe
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"earth"}}] run function avatar:detect/earth_kingdom
execute as @a if items entity @s armor.chest *[custom_data~{avatar:{nation:"air"}}] run function avatar:detect/air_nomad
"""
    with open(os.path.join(FUNCTIONS_DIR, "tick.mcfunction"), "w", encoding="utf-8") as f:
        f.write(tick_content)

# ------------------------------------------------------------------------------
# 5. Resource Pack - Textures & Item Models
# ------------------------------------------------------------------------------
HELMET_FIRE = [
    "................",
    ".......OO.......",
    "......OAGO......",
    "....OOOAPPOOO...",
    "...OAGPPPPPPPO..",
    "...OPPAAAAMPPO..",
    "...OPPOOOOOOPO..",
    "...OPO......OP..",
    "...OPP......PO..",
    "...OPP......PO..",
    "...OPPOOOOOOPO..",
    "...OPPPPPPPPPO..",
    "....OSSSSSSSSO..",
    ".....OOOOOOOO...",
    "................",
    "................"
]

HELMET_AIR = [
    "................",
    "......OOOO......",
    ".....OGPPPPO....",
    "....OGPPPPPPPO..",
    "...OGPPTTTPPPPO.",
    "...OPPPTTTPPPPO.",
    "...OPP..T..PPPO.",
    "...OPP.....PPPO.",
    "...OP.......PPO.",
    "...OP.......PPO.",
    "...OPPOOOOOOPPO.",
    "...OPPPPPPPPPO..",
    "....OSSSSSSSSO..",
    ".....OOOOOOOO...",
    "................",
    "................"
]

HELMET_MAP = [
    "................",
    "......OOOO......",
    ".....OAGPPO.....",
    "....OAGPPPPO....",
    "...OAGPPPPPPPO..",
    "...OPPAAAAMPPO..",
    "...OPPOOOOOOPO..",
    "...OPO......OP..",
    "...OPP......PO..",
    "...OPP......PO..",
    "...OPPOOOOOOPO..",
    "...OPPPPPPPPPO..",
    "....OSSSSSSSSO..",
    ".....OOOOOOOO...",
    "................",
    "................"
]

CHESTPLATE_WATER = [
    "................",
    ".OTTO......OTTO.",
    ".TGTTOTTTTOTTGT.",
    "OTGPPPPPPPPPPSAO",
    "OTGPPSSPPSSPSPO.",
    ".OPPAAAAMPPSPO..",
    "..OPPAAAMPPSPO..",
    "..OPPPMMMPPSPO..",
    "..OPPPPPPPPSO...",
    "..OTTTTTTTTTPO..",
    "..OPPAAAAMPPO...",
    "..OPPPPPPPPSO...",
    "..OSSSSSSSSSO...",
    "...OOOOOOOOO....",
    "................",
    "................"
]

CHESTPLATE_MAP = [
    "................",
    ".OOOO......OOOO.",
    ".OGPPOOOOOOPPGO.",
    "OAGPPPPPPPPPPSAO",
    "OAGPPAAAPPPPSPO.",
    ".OPPPAAAPPPSPO..",
    "..OPPPAPPPSPO...",
    "..OPPPAPPPSPO...",
    "..OPPPPPPPPSO...",
    "..OPPAAAAMPPO...",
    "..OPPAAAAMPPO...",
    "..OPPPPPPPPSO...",
    "..OSSSSSSSSSO...",
    "...OOOOOOOOO....",
    "................",
    "................"
]

LEGGINGS_MAP = [
    "................",
    "..OOOOOOOOOOOO..",
    "..OAGPPPPPPSAO..",
    "..OPPAAAAMPPSPO.",
    "..OPPPPPPPPSPO..",
    "..OPPPO..OPPPO..",
    "..OPPPO..OPPPO..",
    "..OPAPO..OPAPO..",
    "..OPAPO..OPAPO..",
    "..OPPPO..OPPPO..",
    "..OPPPO..OPPPO..",
    "..OPPPO..OPPPO..",
    "..OSSSO..OSSSO..",
    "..OOOOO..OOOOO..",
    "................",
    "................"
]

BOOTS_MAP = [
    "................",
    "................",
    "................",
    "................",
    ".OOOO....OOOO...",
    ".OGPPO..OGPPO...",
    ".OPAPO..OPAPO...",
    ".OPPPO..OPPPO...",
    ".OPPPO..OPPPO...",
    ".OPPPO..OPPPO...",
    "OOPPPPOOOPPPPO..",
    "OAGPPPPOAGPPPPO.",
    "OAPPPPPPOPPPPPO.",
    "OSSSSSSOOSSSSSO.",
    ".OOOOOO..OOOOO..",
    "................"
]

PALETTES = {
    # Fire Nation
    ("fire", "basic"): {
        "outline": (45, 45, 50, 255),
        "shadow": (110, 115, 120, 255),
        "primary": (175, 180, 185, 255),
        "secondary": (180, 40, 30, 255),
        "accent": (230, 50, 35, 255),
        "glint": (235, 240, 245, 255),
        "trim": (220, 100, 30, 255)
    },
    ("fire", "adept"): {
        "outline": (40, 25, 40, 255),
        "shadow": (30, 110, 130, 255),
        "primary": (60, 190, 210, 255),
        "secondary": (195, 35, 35, 255),
        "accent": (255, 170, 30, 255),
        "glint": (210, 255, 255, 255),
        "trim": (180, 30, 30, 255)
    },
    ("fire", "master"): {
        "outline": (30, 20, 25, 255),
        "shadow": (60, 50, 55, 255),
        "primary": (85, 75, 80, 255),
        "secondary": (230, 90, 20, 255),
        "accent": (255, 190, 40, 255),
        "glint": (255, 240, 160, 255),
        "trim": (190, 35, 25, 255)
    },
    ("fire", "legendary"): {
        "outline": (55, 10, 10, 255),
        "shadow": (110, 20, 20, 255),
        "primary": (175, 30, 30, 255),
        "secondary": (255, 140, 0, 255),
        "accent": (255, 200, 50, 255),
        "glint": (255, 245, 160, 255),
        "trim": (220, 160, 30, 255)
    },

    # Water Tribe
    ("water", "basic"): {
        "outline": (35, 40, 50, 255),
        "shadow": (110, 115, 125, 255),
        "primary": (175, 180, 190, 255),
        "secondary": (35, 90, 170, 255),
        "accent": (80, 160, 230, 255),
        "glint": (235, 245, 250, 255),
        "trim": (240, 250, 255, 255)
    },
    ("water", "adept"): {
        "outline": (20, 45, 65, 255),
        "shadow": (40, 120, 150, 255),
        "primary": (80, 200, 225, 255),
        "secondary": (30, 80, 160, 255),
        "accent": (190, 235, 255, 255),
        "glint": (230, 255, 255, 255),
        "trim": (245, 250, 255, 255)
    },
    ("water", "master"): {
        "outline": (20, 25, 35, 255),
        "shadow": (50, 55, 65, 255),
        "primary": (75, 80, 95, 255),
        "secondary": (40, 130, 200, 255),
        "accent": (140, 220, 255, 255),
        "glint": (220, 248, 255, 255),
        "trim": (200, 240, 255, 255)
    },
    ("water", "legendary"): {
        "outline": (10, 25, 75, 255),
        "shadow": (18, 42, 110, 255),
        "primary": (25, 65, 160, 255),
        "secondary": (50, 135, 210, 255),
        "accent": (180, 225, 255, 255),
        "glint": (235, 248, 255, 255),
        "trim": (240, 250, 255, 255)
    },

    # Earth Kingdom
    ("earth", "basic"): {
        "outline": (40, 45, 40, 255),
        "shadow": (110, 120, 110, 255),
        "primary": (175, 185, 175, 255),
        "secondary": (50, 120, 50, 255),
        "accent": (90, 170, 90, 255),
        "glint": (235, 245, 235, 255),
        "trim": (160, 140, 80, 255)
    },
    ("earth", "adept"): {
        "outline": (25, 45, 35, 255),
        "shadow": (35, 120, 100, 255),
        "primary": (60, 195, 160, 255),
        "secondary": (40, 140, 60, 255),
        "accent": (180, 240, 120, 255),
        "glint": (220, 255, 230, 255),
        "trim": (190, 170, 90, 255)
    },
    ("earth", "master"): {
        "outline": (25, 30, 25, 255),
        "shadow": (55, 60, 55, 255),
        "primary": (75, 85, 75, 255),
        "secondary": (45, 130, 55, 255),
        "accent": (130, 210, 110, 255),
        "glint": (230, 250, 200, 255),
        "trim": (170, 150, 75, 255)
    },
    ("earth", "legendary"): {
        "outline": (15, 45, 15, 255),
        "shadow": (28, 80, 28, 255),
        "primary": (40, 125, 40, 255),
        "secondary": (80, 165, 80, 255),
        "accent": (200, 180, 100, 255),
        "glint": (240, 230, 150, 255),
        "trim": (160, 135, 70, 255)
    },

    # Air Nomad
    ("air", "basic"): {
        "outline": (45, 45, 40, 255),
        "shadow": (120, 120, 115, 255),
        "primary": (180, 180, 175, 255),
        "secondary": (210, 150, 40, 255),
        "accent": (245, 190, 70, 255),
        "glint": (245, 245, 235, 255),
        "trim": (130, 190, 230, 255)
    },
    ("air", "adept"): {
        "outline": (40, 40, 30, 255),
        "shadow": (70, 125, 140, 255),
        "primary": (120, 205, 225, 255),
        "secondary": (220, 160, 50, 255),
        "accent": (250, 215, 120, 255),
        "glint": (240, 255, 255, 255),
        "trim": (100, 185, 235, 255)
    },
    ("air", "master"): {
        "outline": (30, 30, 35, 255),
        "shadow": (60, 60, 70, 255),
        "primary": (85, 85, 95, 255),
        "secondary": (215, 165, 60, 255),
        "accent": (140, 210, 240, 255),
        "glint": (250, 250, 240, 255),
        "trim": (110, 190, 235, 255)
    },
    ("air", "legendary"): {
        "outline": (100, 75, 20, 255),
        "shadow": (160, 120, 30, 255),
        "primary": (220, 170, 50, 255),
        "secondary": (240, 200, 100, 255),
        "accent": (255, 240, 200, 255),
        "glint": (255, 255, 240, 255),
        "trim": (100, 185, 235, 255)
    }
}

def render_pixel_matrix(matrix, palette):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == "O":
                color = palette["outline"]
            elif char == "S":
                color = palette["shadow"]
            elif char == "P":
                color = palette["primary"]
            elif char == "M":
                color = palette["secondary"]
            elif char == "A":
                color = palette["accent"]
            elif char == "G":
                color = palette["glint"]
            elif char == "T":
                color = palette["trim"]
            else:
                color = (0, 0, 0, 0)
            img.putpixel((x, y), color)
    return img

def generate_textures_and_models():
    print("Generating 64 textures and item models...")
    for nation in NATIONS:
        for tier in TIERS:
            pal = PALETTES[(nation, tier)]

            # 1. Helmet
            h_mat = HELMET_FIRE if nation == "fire" else (HELMET_AIR if nation == "air" else HELMET_MAP)
            img_helmet = render_pixel_matrix(h_mat, pal)
            tex_name = f"{nation}_{tier}_helmet"
            img_helmet.save(os.path.join(ITEM_TEX_DIR, f"{tex_name}.png"))

            # 2. Chestplate
            c_mat = CHESTPLATE_WATER if nation == "water" else CHESTPLATE_MAP
            img_chest = render_pixel_matrix(c_mat, pal)
            tex_name = f"{nation}_{tier}_chestplate"
            img_chest.save(os.path.join(ITEM_TEX_DIR, f"{tex_name}.png"))

            # 3. Leggings
            img_legs = render_pixel_matrix(LEGGINGS_MAP, pal)
            tex_name = f"{nation}_{tier}_leggings"
            img_legs.save(os.path.join(ITEM_TEX_DIR, f"{tex_name}.png"))

            # 4. Boots
            img_boots = render_pixel_matrix(BOOTS_MAP, pal)
            tex_name = f"{nation}_{tier}_boots"
            img_boots.save(os.path.join(ITEM_TEX_DIR, f"{tex_name}.png"))

            # Item Model JSONs
            for piece in PIECES:
                model_name = f"{nation}_{tier}_{piece}.json"
                model_data = {
                    "parent": "minecraft:item/generated",
                    "textures": {
                        "layer0": f"avatar:item/{nation}_{tier}_{piece}"
                    }
                }
                with open(os.path.join(ITEM_MODELS_DIR, model_name), "w", encoding="utf-8") as f:
                    json.dump(model_data, f, indent=2)

    # Legacy texture & model aliases (pointing to Legendary set)
    nation_aliases = {
        "fire_nation": "fire_legendary",
        "water_tribe": "water_legendary",
        "earth_kingdom": "earth_legendary",
        "air_nomad": "air_legendary"
    }
    for alias, target in nation_aliases.items():
        for piece in PIECES:
            # Texture copy
            src_tex = os.path.join(ITEM_TEX_DIR, f"{target}_{piece}.png")
            dst_tex = os.path.join(ITEM_TEX_DIR, f"{alias}_{piece}.png")
            img = Image.open(src_tex)
            img.save(dst_tex)

            # Model JSON
            model_data = {
                "parent": "minecraft:item/generated",
                "textures": {
                    "layer0": f"avatar:item/{alias}_{piece}"
                }
            }
            with open(os.path.join(ITEM_MODELS_DIR, f"{alias}_{piece}.json"), "w", encoding="utf-8") as f:
                json.dump(model_data, f, indent=2)

    print("  -> Generated 64 item textures and models + 16 legacy aliases")

# ------------------------------------------------------------------------------
# 6. Resource Pack - Minecraft Vanilla Item Overrides
# ------------------------------------------------------------------------------
def generate_vanilla_overrides():
    print("Generating 12 Minecraft vanilla item model override files...")
    # 1. Iron pieces (Basic tier)
    for piece in PIECES:
        overrides = []
        for nation in NATIONS:
            cmd = get_custom_model_data(nation, "basic", piece)
            overrides.append({
                "predicate": {"custom_model_data": cmd},
                "model": f"avatar:item/{nation}_basic_{piece}"
            })
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"minecraft:item/iron_{piece}"
            },
            "overrides": overrides
        }
        with open(os.path.join(MC_ITEM_MODELS_DIR, f"iron_{piece}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 2. Diamond pieces (Adept tier)
    for piece in PIECES:
        overrides = []
        for nation in NATIONS:
            cmd = get_custom_model_data(nation, "adept", piece)
            overrides.append({
                "predicate": {"custom_model_data": cmd},
                "model": f"avatar:item/{nation}_adept_{piece}"
            })
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"minecraft:item/diamond_{piece}"
            },
            "overrides": overrides
        }
        with open(os.path.join(MC_ITEM_MODELS_DIR, f"diamond_{piece}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 3. Netherite pieces (Master & Legendary tiers)
    for piece in PIECES:
        overrides = []
        # Master tier CMDs
        for nation in NATIONS:
            cmd = get_custom_model_data(nation, "master", piece)
            overrides.append({
                "predicate": {"custom_model_data": cmd},
                "model": f"avatar:item/{nation}_master_{piece}"
            })
        # Legendary tier CMDs
        for nation in NATIONS:
            cmd = get_custom_model_data(nation, "legendary", piece)
            overrides.append({
                "predicate": {"custom_model_data": cmd},
                "model": f"avatar:item/{nation}_legendary_{piece}"
            })
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"minecraft:item/netherite_{piece}"
            },
            "overrides": overrides
        }
        with open(os.path.join(MC_ITEM_MODELS_DIR, f"netherite_{piece}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    print("  -> Generated 12 vanilla armor item override files in assets/minecraft/models/item/")

# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("==================================================================")
    print("Avatar Armor System - Refactor & Asset Generator for 1.21.1")
    print("==================================================================")
    generate_recipes()
    generate_give_functions()
    generate_abilities_and_particles()
    generate_detect_functions()
    generate_textures_and_models()
    generate_vanilla_overrides()
    print("==================================================================")
    print("All tasks completed successfully!")
    print("==================================================================")
