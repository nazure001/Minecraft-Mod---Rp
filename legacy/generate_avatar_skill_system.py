#!/usr/bin/env python3
"""
Comprehensive Generator for Avatar Skill Datapack & Resource Pack (Minecraft Java 1.21.1)
Author: Senior Modding & Datapack Engineer
Target: Minecraft Java Edition 1.21.1 (Datapack format 48, Resource Pack format 34)
"""

import os
import json
from PIL import Image, ImageDraw

REPO_DIR = r"D:\repo"
DATAPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-datapack")
RESOURCEPACK_DIR = os.path.join(REPO_DIR, "avatar-skill-resourcepack")

# Datapack directories
DATA_DIR = os.path.join(DATAPACK_DIR, "data")
AVATAR_DATA = os.path.join(DATA_DIR, "avatar_skills")
MC_DATA = os.path.join(DATA_DIR, "minecraft")
MC_TAGS_FUNC = os.path.join(MC_DATA, "tags", "function")

ADVANCEMENT_DIR = os.path.join(AVATAR_DATA, "advancement")
ADV_BRANCHES = {
    "root": ADVANCEMENT_DIR,
    "fire": os.path.join(ADVANCEMENT_DIR, "fire"),
    "water": os.path.join(ADVANCEMENT_DIR, "water"),
    "earth": os.path.join(ADVANCEMENT_DIR, "earth"),
    "air": os.path.join(ADVANCEMENT_DIR, "air"),
    "avatar": os.path.join(ADVANCEMENT_DIR, "avatar"),
    "attributes": os.path.join(ADVANCEMENT_DIR, "attributes")
}

FUNCTION_DIR = os.path.join(AVATAR_DATA, "function")
CAST_DIR = os.path.join(FUNCTION_DIR, "cast")
TREE_DIR = os.path.join(FUNCTION_DIR, "tree")
STATE_DIR = os.path.join(FUNCTION_DIR, "avatar_state")
GIVE_DIR = os.path.join(FUNCTION_DIR, "give")
PARTICLES_DIR = os.path.join(FUNCTION_DIR, "particles")
COMBOS_DIR = os.path.join(FUNCTION_DIR, "combos")

# Resourcepack directories
ASSETS_DIR = os.path.join(RESOURCEPACK_DIR, "assets")
AVATAR_ASSETS = os.path.join(ASSETS_DIR, "avatar_skills")
MC_ASSETS = os.path.join(ASSETS_DIR, "minecraft")

MODELS_ITEM_DIR = os.path.join(AVATAR_ASSETS, "models", "item")
TEXTURES_ITEM_DIR = os.path.join(AVATAR_ASSETS, "textures", "item")
LANG_DIR = os.path.join(AVATAR_ASSETS, "lang")
MC_MODELS_ITEM_DIR = os.path.join(MC_ASSETS, "models", "item")

ALL_DIRS = [
    ADVANCEMENT_DIR, FUNCTION_DIR, CAST_DIR, TREE_DIR, STATE_DIR, GIVE_DIR,
    PARTICLES_DIR, COMBOS_DIR, MC_TAGS_FUNC, MODELS_ITEM_DIR, TEXTURES_ITEM_DIR,
    LANG_DIR, MC_MODELS_ITEM_DIR
] + list(ADV_BRANCHES.values())

for d in ALL_DIRS:
    os.makedirs(d, exist_ok=True)

# Also create alias directory for avatar: namespace
AVATAR_ALIAS_GIVE = os.path.join(DATA_DIR, "avatar", "function", "give")
AVATAR_ALIAS_TREE = os.path.join(DATA_DIR, "avatar", "function", "tree")
os.makedirs(AVATAR_ALIAS_GIVE, exist_ok=True)
os.makedirs(AVATAR_ALIAS_TREE, exist_ok=True)

# -----------------------------------------------------------------------------
# Pack MCMETA Manifests & Function Tags
# -----------------------------------------------------------------------------
datapack_mcmeta = {
    "pack": {
        "pack_format": 48,
        "description": "Avatar Skills & Elemental Mastery Datapack (1.21.1)"
    }
}
with open(os.path.join(DATAPACK_DIR, "pack.mcmeta"), "w", encoding="utf-8") as f:
    json.dump(datapack_mcmeta, f, indent=2)

resourcepack_mcmeta = {
    "pack": {
        "pack_format": 34,
        "description": "Avatar Skills & Relics Resource Pack (1.21.1)"
    }
}
with open(os.path.join(RESOURCEPACK_DIR, "pack.mcmeta"), "w", encoding="utf-8") as f:
    json.dump(resourcepack_mcmeta, f, indent=2)

# Function tags for load and tick
with open(os.path.join(MC_TAGS_FUNC, "load.json"), "w", encoding="utf-8") as f:
    json.dump({"values": ["avatar_skills:setup"]}, f, indent=2)

with open(os.path.join(MC_TAGS_FUNC, "tick.json"), "w", encoding="utf-8") as f:
    json.dump({"values": ["avatar_skills:tick"]}, f, indent=2)

# Pack icons (64x64 PNG)
def create_pack_icon(path, color_primary, color_secondary):
    img = Image.new("RGBA", (64, 64), color_primary)
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, 59, 59], outline=color_secondary, width=3)
    draw.ellipse([16, 16, 47, 47], fill=color_secondary)
    img.save(path)

create_pack_icon(os.path.join(DATAPACK_DIR, "pack.png"), (20, 25, 35, 255), (255, 200, 50, 255))
create_pack_icon(os.path.join(RESOURCEPACK_DIR, "pack.png"), (20, 25, 35, 255), (100, 200, 255, 255))

print("Directories, manifests, icons, and tags initialized.")

# =============================================================================
# 1. PIXEL ART TEXTURE GENERATOR (High-Fidelity 16x16 Pixel Art)
# =============================================================================
def create_texture(name, draw_func):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw)
    path = os.path.join(TEXTURES_ITEM_DIR, f"{name}.png")
    img.save(path)
    return path

# --- Scroll of Firebending ---
def draw_scroll_fire(d):
    # Scroll parchment
    for y in range(3, 13):
        for x in range(4, 12):
            d.point((x, y), fill=(245, 215, 175, 255))
    # Spool ends (Gold/Bronze)
    for x in range(3, 13):
        d.point((x, 2), fill=(185, 120, 20, 255))
        d.point((x, 13), fill=(185, 120, 20, 255))
    d.point((2, 2), fill=(240, 190, 40, 255))
    d.point((13, 2), fill=(240, 190, 40, 255))
    d.point((2, 13), fill=(240, 190, 40, 255))
    d.point((13, 13), fill=(240, 190, 40, 255))
    # Red ribbon & Crimson Fire Emblem
    for y in range(6, 10):
        d.point((3, y), fill=(160, 20, 20, 255))
        d.point((12, y), fill=(160, 20, 20, 255))
    # Fire flame icon in center
    d.point((7, 5), fill=(255, 100, 0, 255))
    d.point((8, 5), fill=(255, 60, 0, 255))
    for x in [6, 7, 8, 9]:
        d.point((x, 6), fill=(255, 140, 0, 255))
    for x in [5, 6, 7, 8, 9, 10]:
        d.point((x, 7), fill=(255, 200, 50, 255))
        d.point((x, 8), fill=(255, 160, 0, 255))
    d.point((6, 9), fill=(220, 40, 0, 255))
    d.point((7, 9), fill=(255, 240, 100, 255))
    d.point((8, 9), fill=(255, 240, 100, 255))
    d.point((9, 9), fill=(220, 40, 0, 255))
    d.point((7, 10), fill=(180, 20, 0, 255))
    d.point((8, 10), fill=(180, 20, 0, 255))

# --- Scroll of Waterbending ---
def draw_scroll_water(d):
    for y in range(3, 13):
        for x in range(4, 12):
            d.point((x, y), fill=(220, 235, 245, 255))
    # Spool ends (Silver/Cobalt)
    for x in range(3, 13):
        d.point((x, 2), fill=(40, 90, 160, 255))
        d.point((x, 13), fill=(40, 90, 160, 255))
    d.point((2, 2), fill=(100, 180, 240, 255))
    d.point((13, 2), fill=(100, 180, 240, 255))
    d.point((2, 13), fill=(100, 180, 240, 255))
    d.point((13, 13), fill=(100, 180, 240, 255))
    # Water Wave Crest
    d.point((7, 5), fill=(0, 160, 240, 255))
    d.point((8, 5), fill=(0, 190, 255, 255))
    d.point((6, 6), fill=(0, 130, 220, 255))
    d.point((9, 6), fill=(180, 230, 255, 255))
    for x in [5, 6, 7, 8, 9, 10]:
        d.point((x, 7), fill=(0, 100, 200, 255))
        d.point((x, 8), fill=(50, 170, 255, 255))
    d.point((6, 9), fill=(0, 80, 170, 255))
    d.point((7, 9), fill=(210, 245, 255, 255))
    d.point((8, 9), fill=(210, 245, 255, 255))
    d.point((9, 9), fill=(0, 80, 170, 255))

# --- Scroll of Earthbending ---
def draw_scroll_earth(d):
    for y in range(3, 13):
        for x in range(4, 12):
            d.point((x, y), fill=(235, 225, 205, 255))
    # Spool ends (Bronze & Jade)
    for x in range(3, 13):
        d.point((x, 2), fill=(100, 75, 40, 255))
        d.point((x, 13), fill=(100, 75, 40, 255))
    d.point((2, 2), fill=(40, 150, 80, 255))
    d.point((13, 2), fill=(40, 150, 80, 255))
    d.point((2, 13), fill=(40, 150, 80, 255))
    d.point((13, 13), fill=(40, 150, 80, 255))
    # Mountain / Earth crest
    d.point((7, 5), fill=(45, 140, 70, 255))
    d.point((8, 5), fill=(70, 180, 95, 255))
    d.point((6, 6), fill=(35, 110, 55, 255))
    d.point((7, 6), fill=(90, 210, 120, 255))
    d.point((8, 6), fill=(90, 210, 120, 255))
    d.point((9, 6), fill=(35, 110, 55, 255))
    for x in range(5, 11):
        d.point((x, 7), fill=(80, 60, 35, 255))
        d.point((x, 8), fill=(130, 95, 55, 255))
    for x in range(4, 12):
        d.point((x, 9), fill=(60, 45, 25, 255))

# --- Scroll of Airbending ---
def draw_scroll_air(d):
    for y in range(3, 13):
        for x in range(4, 12):
            d.point((x, y), fill=(255, 250, 235, 255))
    # Spool ends (Monk Saffron / Orange Gold)
    for x in range(3, 13):
        d.point((x, 2), fill=(210, 130, 20, 255))
        d.point((x, 13), fill=(210, 130, 20, 255))
    d.point((2, 2), fill=(250, 200, 60, 255))
    d.point((13, 2), fill=(250, 200, 60, 255))
    d.point((2, 13), fill=(250, 200, 60, 255))
    d.point((13, 13), fill=(250, 200, 60, 255))
    # Air Spiral Triskelion
    d.point((7, 5), fill=(240, 170, 40, 255))
    d.point((8, 5), fill=(255, 215, 80, 255))
    d.point((6, 6), fill=(230, 150, 30, 255))
    d.point((8, 6), fill=(255, 240, 160, 255))
    d.point((9, 6), fill=(230, 150, 30, 255))
    d.point((7, 7), fill=(255, 210, 70, 255))
    d.point((8, 7), fill=(210, 120, 10, 255))
    d.point((6, 8), fill=(240, 170, 40, 255))
    d.point((7, 8), fill=(255, 230, 120, 255))
    d.point((9, 8), fill=(240, 170, 40, 255))
    d.point((7, 9), fill=(210, 130, 20, 255))
    d.point((8, 9), fill=(210, 130, 20, 255))

# --- Avatar Relic (Cosmic Raava Eye & 4 Elements) ---
def draw_avatar_relic(d):
    # Platinum cosmic amulet ring
    for x in range(4, 12):
        d.point((x, 2), fill=(210, 225, 245, 255))
        d.point((x, 13), fill=(210, 225, 245, 255))
    for y in range(4, 12):
        d.point((2, y), fill=(210, 225, 245, 255))
        d.point((13, y), fill=(210, 225, 245, 255))
    d.point((3, 3), fill=(245, 250, 255, 255))
    d.point((12, 3), fill=(245, 250, 255, 255))
    d.point((3, 12), fill=(245, 250, 255, 255))
    d.point((12, 12), fill=(245, 250, 255, 255))
    # 4 Elemental Gems at cardinal directions
    d.point((7, 3), fill=(255, 60, 0, 255))   # Top: Fire
    d.point((8, 3), fill=(255, 120, 20, 255))
    d.point((7, 12), fill=(50, 150, 80, 255)) # Bottom: Earth
    d.point((8, 12), fill=(80, 210, 120, 255))
    d.point((3, 7), fill=(0, 160, 255, 255))  # Left: Water
    d.point((3, 8), fill=(100, 210, 255, 255))
    d.point((12, 7), fill=(255, 215, 60, 255))# Right: Air
    d.point((12, 8), fill=(255, 245, 150, 255))
    # Central Raava Glowing Spirit Core
    for y in range(6, 10):
        for x in range(6, 10):
            d.point((x, y), fill=(140, 220, 255, 255))
    d.point((7, 7), fill=(255, 255, 255, 255))
    d.point((8, 7), fill=(230, 250, 255, 255))
    d.point((7, 8), fill=(180, 240, 255, 255))
    d.point((8, 8), fill=(255, 255, 255, 255))

# --- Scroll of Mastery / Skill Tree Tome ---
def draw_scroll_mastery(d):
    for y in range(2, 14):
        for x in range(3, 13):
            d.point((x, y), fill=(90, 50, 25, 255))
    # Gold border
    for x in range(4, 12):
        d.point((x, 3), fill=(230, 180, 40, 255))
        d.point((x, 12), fill=(230, 180, 40, 255))
    for y in range(4, 12):
        d.point((4, y), fill=(230, 180, 40, 255))
        d.point((11, y), fill=(230, 180, 40, 255))
    # White Lotus Emblem in center
    d.point((7, 6), fill=(255, 255, 255, 255))
    d.point((8, 6), fill=(255, 255, 255, 255))
    d.point((6, 7), fill=(230, 240, 250, 255))
    d.point((7, 7), fill=(255, 210, 50, 255)) # Golden core
    d.point((8, 7), fill=(255, 210, 50, 255))
    d.point((9, 7), fill=(230, 240, 250, 255))
    d.point((6, 8), fill=(230, 240, 250, 255))
    d.point((7, 8), fill=(255, 210, 50, 255))
    d.point((8, 8), fill=(255, 210, 50, 255))
    d.point((9, 8), fill=(230, 240, 250, 255))
    d.point((7, 9), fill=(255, 255, 255, 255))
    d.point((8, 9), fill=(255, 255, 255, 255))

# --- Chi Orb / Spirit Essence ---
def draw_chi_orb(d):
    for y in range(4, 12):
        for x in range(4, 12):
            d.point((x, y), fill=(0, 200, 255, 200))
    d.point((7, 3), fill=(100, 230, 255, 255))
    d.point((8, 3), fill=(100, 230, 255, 255))
    d.point((7, 12), fill=(0, 140, 210, 255))
    d.point((8, 12), fill=(0, 140, 210, 255))
    d.point((3, 7), fill=(0, 160, 230, 255))
    d.point((3, 8), fill=(0, 160, 230, 255))
    d.point((12, 7), fill=(120, 240, 255, 255))
    d.point((12, 8), fill=(120, 240, 255, 255))
    # Glowing center
    for y in range(6, 10):
        for x in range(6, 10):
            d.point((x, y), fill=(210, 250, 255, 255))
    d.point((7, 7), fill=(255, 255, 255, 255))

# Sub-Bending Foci
def draw_focus_lightning(d):
    # Azure electric bolt
    for y in range(2, 14):
        for x in range(2, 14):
            if (x+y) % 4 == 0:
                d.point((x, y), fill=(40, 80, 180, 100))
    # Lightning bolt zigzag
    d.point((9, 2), fill=(255, 255, 255, 255))
    d.point((8, 3), fill=(180, 230, 255, 255))
    d.point((7, 4), fill=(120, 200, 255, 255))
    d.point((6, 5), fill=(70, 160, 255, 255))
    for x in range(5, 11):
        d.point((x, 6), fill=(220, 245, 255, 255))
    d.point((8, 7), fill=(120, 200, 255, 255))
    d.point((7, 8), fill=(80, 170, 255, 255))
    d.point((6, 9), fill=(50, 140, 255, 255))
    d.point((5, 10), fill=(20, 110, 255, 255))
    d.point((4, 11), fill=(150, 220, 255, 255))
    d.point((4, 12), fill=(255, 255, 255, 255))

def draw_focus_combustion(d):
    # Third eye burst
    for y in range(4, 12):
        for x in range(3, 13):
            d.point((x, y), fill=(140, 15, 15, 220))
    d.point((8, 4), fill=(255, 220, 50, 255))
    d.point((8, 11), fill=(255, 220, 50, 255))
    d.point((3, 7), fill=(255, 220, 50, 255))
    d.point((12, 8), fill=(255, 220, 50, 255))
    # Center eye
    for y in range(6, 10):
        for x in range(6, 10):
            d.point((x, y), fill=(255, 80, 0, 255))
    d.point((7, 7), fill=(255, 255, 100, 255))
    d.point((8, 8), fill=(40, 0, 0, 255)) # Pupil

def draw_focus_blood(d):
    # Crimson blood vessel sphere
    for y in range(3, 13):
        for x in range(3, 13):
            if ((x-7.5)**2 + (y-7.5)**2) <= 22:
                d.point((x, y), fill=(160, 10, 25, 255))
    d.point((6, 5), fill=(240, 60, 80, 255))
    d.point((7, 5), fill=(255, 100, 120, 255))
    d.point((5, 8), fill=(100, 5, 15, 255))
    d.point((9, 9), fill=(80, 0, 10, 255))
    d.point((7, 8), fill=(200, 20, 40, 255))

def draw_focus_healing(d):
    # Glowing aquamarine lotus
    for y in range(4, 12):
        for x in range(4, 12):
            d.point((x, y), fill=(60, 210, 180, 200))
    d.point((7, 3), fill=(140, 255, 230, 255))
    d.point((8, 3), fill=(140, 255, 230, 255))
    d.point((7, 12), fill=(20, 160, 130, 255))
    d.point((8, 12), fill=(20, 160, 130, 255))
    for y in range(6, 10):
        for x in range(6, 10):
            d.point((x, y), fill=(220, 255, 245, 255))
    d.point((7, 7), fill=(255, 255, 255, 255))

def draw_focus_lava(d):
    # Obsidian with glowing molten cracks
    for y in range(3, 13):
        for x in range(3, 13):
            d.point((x, y), fill=(35, 30, 35, 255))
    d.point((5, 4), fill=(255, 120, 0, 255))
    d.point((6, 5), fill=(255, 60, 0, 255))
    d.point((7, 6), fill=(255, 200, 40, 255))
    d.point((8, 7), fill=(255, 80, 0, 255))
    d.point((9, 7), fill=(255, 140, 0, 255))
    d.point((7, 8), fill=(255, 50, 0, 255))
    d.point((6, 9), fill=(255, 180, 20, 255))
    d.point((5, 10), fill=(220, 30, 0, 255))

def draw_focus_metal(d):
    # Refined steel coil and cables
    for y in range(3, 13):
        for x in range(4, 12):
            d.point((x, y), fill=(160, 170, 185, 255))
    for x in range(4, 12):
        d.point((x, 3), fill=(225, 235, 245, 255))
        d.point((x, 7), fill=(90, 100, 115, 255))
        d.point((x, 12), fill=(60, 70, 80, 255))
    d.point((5, 5), fill=(240, 245, 255, 255))
    d.point((6, 10), fill=(240, 245, 255, 255))

def draw_focus_flight(d):
    # Celestial Zaheer's Cloud Plume
    for y in range(2, 14):
        for x in range(4, 12):
            if (x+y) % 2 == 0:
                d.point((x, y), fill=(240, 245, 255, 230))
            else:
                d.point((x, y), fill=(210, 225, 245, 200))
    d.point((7, 2), fill=(255, 255, 255, 255))
    d.point((8, 2), fill=(255, 255, 255, 255))
    d.point((6, 7), fill=(255, 255, 255, 255))
    d.point((7, 7), fill=(255, 255, 255, 255))

# Generate textures
textures_to_create = {
    "scroll_fire": draw_scroll_fire,
    "scroll_water": draw_scroll_water,
    "scroll_earth": draw_scroll_earth,
    "scroll_air": draw_scroll_air,
    "avatar_relic": draw_avatar_relic,
    "scroll_mastery": draw_scroll_mastery,
    "chi_orb": draw_chi_orb,
    "focus_lightning": draw_focus_lightning,
    "focus_combustion": draw_focus_combustion,
    "focus_blood": draw_focus_blood,
    "focus_healing": draw_focus_healing,
    "focus_lava": draw_focus_lava,
    "focus_metal": draw_focus_metal,
    "focus_flight": draw_focus_flight
}

for name, func in textures_to_create.items():
    create_texture(name, func)

print(f"Generated {len(textures_to_create)} HD pixel art textures.")

# =============================================================================
# 2. RESOURCE PACK MODELS (CMD MAPPING 5001 - 5014)
# =============================================================================
CMD_MAP = {
    "scroll_fire": 5001,
    "scroll_water": 5002,
    "scroll_earth": 5003,
    "scroll_air": 5004,
    "avatar_relic": 5005,
    "scroll_mastery": 5006,
    "chi_orb": 5007,
    "focus_lightning": 5008,
    "focus_combustion": 5009,
    "focus_blood": 5010,
    "focus_healing": 5011,
    "focus_lava": 5012,
    "focus_metal": 5013,
    "focus_flight": 5014
}

# Item models in assets/avatar_skills/models/item/
for item_name in CMD_MAP.keys():
    model_json = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"avatar_skills:item/{item_name}"
        }
    }
    with open(os.path.join(MODELS_ITEM_DIR, f"{item_name}.json"), "w", encoding="utf-8") as f:
        json.dump(model_json, f, indent=2)

# Override in assets/minecraft/models/item/warped_fungus_on_a_stick.json
overrides = []
for item_name, cmd in sorted(CMD_MAP.items(), key=lambda x: x[1]):
    overrides.append({
        "predicate": {
            "custom_model_data": cmd
        },
        "model": f"avatar_skills:item/{item_name}"
    })

mc_override_json = {
    "parent": "minecraft:item/handheld_rod",
    "textures": {
        "layer0": "minecraft:item/warped_fungus_on_a_stick"
    },
    "overrides": overrides
}
with open(os.path.join(MC_MODELS_ITEM_DIR, "warped_fungus_on_a_stick.json"), "w", encoding="utf-8") as f:
    json.dump(mc_override_json, f, indent=2)

mc_carrot_override_json = {
    "parent": "minecraft:item/handheld_rod",
    "textures": {
        "layer0": "minecraft:item/carrot_on_a_stick"
    },
    "overrides": overrides
}
with open(os.path.join(MC_MODELS_ITEM_DIR, "carrot_on_a_stick.json"), "w", encoding="utf-8") as f:
    json.dump(mc_carrot_override_json, f, indent=2)

print("Resource pack item models and vanilla overrides generated.")

# Language file (en_us.json)
lang_dict = {
    "item.avatar_skills.scroll_fire": "Scroll of Firebending",
    "item.avatar_skills.scroll_water": "Scroll of Waterbending",
    "item.avatar_skills.scroll_earth": "Scroll of Earthbending",
    "item.avatar_skills.scroll_air": "Scroll of Airbending",
    "item.avatar_skills.avatar_relic": "Cosmic Avatar Relic",
    "item.avatar_skills.scroll_mastery": "Tome of Chi Mastery",
    "item.avatar_skills.chi_orb": "Condensed Chi Orb",
    "item.avatar_skills.focus_lightning": "Focus of Lightning Generation",
    "item.avatar_skills.focus_combustion": "Focus of Combustion Bending",
    "item.avatar_skills.focus_blood": "Focus of Bloodbending",
    "item.avatar_skills.focus_healing": "Focus of Spirit Healing",
    "item.avatar_skills.focus_lava": "Focus of Lavabending",
    "item.avatar_skills.focus_metal": "Focus of Metalbending",
    "item.avatar_skills.focus_flight": "Focus of Weightless Flight",
    "advancements.avatar.root.title": "Avatar: The Way of Bending",
    "advancements.avatar.root.description": "Awaken the latent elemental chi within your spirit.",
    "advancements.avatar.avatar_state.title": "Master of All Four Elements",
    "advancements.avatar.avatar_state.description": "Unlock Fire, Water, Earth, and Air to awaken the Avatar State!"
}
with open(os.path.join(LANG_DIR, "en_us.json"), "w", encoding="utf-8") as f:
    json.dump(lang_dict, f, indent=2)

# =============================================================================
# 3. DATAPACK ADVANCEMENTS (SKILL NODE TREE IN ADVANCEMENTS 'L' MENU)
# =============================================================================
# Root
adv_root = {
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5005}},
        "title": {"text": "Avatar: The Way of Bending", "color": "gold", "bold": True},
        "description": {"text": "Awaken your elemental chi and begin your journey across the Four Nations.", "color": "yellow"},
        "background": "minecraft:textures/block/amethyst_block.png",
        "frame": "challenge",
        "show_toast": True,
        "announce_to_chat": True
    },
    "criteria": {
        "tick": {"trigger": "minecraft:tick"}
    }
}
with open(os.path.join(ADVANCEMENT_DIR, "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_root, f, indent=2)

# Fire Branch
adv_fire_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5001}},
        "title": {"text": "Firebending Discipline", "color": "red", "bold": True},
        "description": {"text": "Master breath, passion, and explosive flame momentum.", "color": "gold"},
        "frame": "task"
    },
    "criteria": {"fire_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["fire"], "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_fire_root, f, indent=2)

adv_fire_sub1 = {
    "parent": "avatar_skills:fire/root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5008}},
        "title": {"text": "Sub-Bending: Lightning Generation", "color": "aqua", "bold": True},
        "description": {"text": "Separate positive and negative chi to unleash pure electric fury.", "color": "white"},
        "frame": "goal"
    },
    "criteria": {"lightning_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["fire"], "lightning.json"), "w", encoding="utf-8") as f:
    json.dump(adv_fire_sub1, f, indent=2)

adv_fire_sub2 = {
    "parent": "avatar_skills:fire/lightning",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5009}},
        "title": {"text": "Mastery: Combustion Bending", "color": "dark_red", "bold": True},
        "description": {"text": "Channel explosive telekinetic beams through the third eye.", "color": "yellow"},
        "frame": "challenge"
    },
    "criteria": {"combustion_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["fire"], "combustion.json"), "w", encoding="utf-8") as f:
    json.dump(adv_fire_sub2, f, indent=2)

# Water Branch
adv_water_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5002}},
        "title": {"text": "Waterbending Discipline", "color": "blue", "bold": True},
        "description": {"text": "Flow like the ocean tides, adapting between liquid, ice, and mist.", "color": "aqua"},
        "frame": "task"
    },
    "criteria": {"water_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["water"], "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_water_root, f, indent=2)

adv_water_sub1 = {
    "parent": "avatar_skills:water/root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5011}},
        "title": {"text": "Sub-Bending: Spirit Healing", "color": "green", "bold": True},
        "description": {"text": "Channel glowing water to mend flesh and purify ailments.", "color": "white"},
        "frame": "goal"
    },
    "criteria": {"healing_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["water"], "healing.json"), "w", encoding="utf-8") as f:
    json.dump(adv_water_sub1, f, indent=2)

adv_water_sub2 = {
    "parent": "avatar_skills:water/healing",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5010}},
        "title": {"text": "Forbidden Art: Bloodbending", "color": "dark_red", "bold": True},
        "description": {"text": "Manipulate the fluid inside living beings, immobilizing their bodies.", "color": "red"},
        "frame": "challenge"
    },
    "criteria": {"bloodbending_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["water"], "bloodbending.json"), "w", encoding="utf-8") as f:
    json.dump(adv_water_sub2, f, indent=2)

# Earth Branch
adv_earth_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5003}},
        "title": {"text": "Earthbending Discipline", "color": "dark_green", "bold": True},
        "description": {"text": "Stand firm with neutral jing. Move mountains with unwavering will.", "color": "green"},
        "frame": "task"
    },
    "criteria": {"earth_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["earth"], "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_earth_root, f, indent=2)

adv_earth_sub1 = {
    "parent": "avatar_skills:earth/root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5013}},
        "title": {"text": "Sub-Bending: Metalbending", "color": "gray", "bold": True},
        "description": {"text": "Sense unpurified earth particles within forged metal cables.", "color": "white"},
        "frame": "goal"
    },
    "criteria": {"metal_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["earth"], "metalbending.json"), "w", encoding="utf-8") as f:
    json.dump(adv_earth_sub1, f, indent=2)

adv_earth_sub2 = {
    "parent": "avatar_skills:earth/metalbending",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5012}},
        "title": {"text": "Rare Discipline: Lavabending", "color": "gold", "bold": True},
        "description": {"text": "Superheat stone molecules into liquid magma flows.", "color": "yellow"},
        "frame": "challenge"
    },
    "criteria": {"lava_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["earth"], "lavabending.json"), "w", encoding="utf-8") as f:
    json.dump(adv_earth_sub2, f, indent=2)

# Air Branch
adv_air_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5004}},
        "title": {"text": "Airbending Discipline", "color": "yellow", "bold": True},
        "description": {"text": "Embrace negative jing: evade, circle, and control the atmosphere.", "color": "white"},
        "frame": "task"
    },
    "criteria": {"air_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["air"], "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_air_root, f, indent=2)

adv_air_sub1 = {
    "parent": "avatar_skills:air/root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5014}},
        "title": {"text": "Sovereign Art: Weightless Flight", "color": "light_purple", "bold": True},
        "description": {"text": "Let go your earthly tether. Enter the void, empty, and become wind.", "color": "aqua"},
        "frame": "challenge"
    },
    "criteria": {"flight_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["air"], "flight.json"), "w", encoding="utf-8") as f:
    json.dump(adv_air_sub1, f, indent=2)

# Avatar State Pinnacle
adv_avatar_state = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5005}},
        "title": {"text": "Master of All Four Elements: Avatar State", "color": "light_purple", "bold": True},
        "description": {"text": "Channel the infinite power of Raava. Command all 4 elements simultaneously!", "color": "gold"},
        "frame": "challenge"
    },
    "criteria": {"avatar_state_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["avatar"], "state.json"), "w", encoding="utf-8") as f:
    json.dump(adv_avatar_state, f, indent=2)

# Attributes Branch
adv_attrib_root = {
    "parent": "avatar_skills:root",
    "display": {
        "icon": {"id": "minecraft:warped_fungus_on_a_stick", "components": {"minecraft:custom_model_data": 5006}},
        "title": {"text": "Physical & Spiritual Nodes", "color": "gold", "bold": True},
        "description": {"text": "Invest Chi Orbs to cultivate Agility, Chi Capacity, Resilience, and Potency.", "color": "yellow"},
        "frame": "goal"
    },
    "criteria": {"attrib_unlocked": {"trigger": "minecraft:impossible"}}
}
with open(os.path.join(ADV_BRANCHES["attributes"], "root.json"), "w", encoding="utf-8") as f:
    json.dump(adv_attrib_root, f, indent=2)

print("Skill node tree advancements created.")

# =============================================================================
# 4. DATAPACK SETUP & TICK FUNCTIONS
# =============================================================================
setup_mcfunction = """# ==============================================================================
# Avatar Skills & Mastery System - Setup (Minecraft Java 1.21.1)
# ==============================================================================

# Core Skill & Interaction Objectives
scoreboard objectives add avatar_used minecraft.used:minecraft.warped_fungus_on_a_stick "Avatar Cast"
scoreboard objectives add avatar_used_c minecraft.used:minecraft.carrot_on_a_stick "Avatar Cast C"
scoreboard objectives add avatar_chi dummy "Avatar Chi"
scoreboard objectives add avatar_chi_max dummy "Max Chi"
scoreboard objectives add avatar_cd dummy "Skill Cooldown"
scoreboard objectives add avatar_state dummy "Avatar State Timer"
scoreboard objectives add avatar_sneak minecraft.custom:minecraft.sneak_time "Sneak Time"
scoreboard objectives add avatar_timer dummy "Avatar Timers"

# Elemental Masteries (0 = locked, 1 = unlocked)
scoreboard objectives add av_mast_fire dummy "Fire Mastery"
scoreboard objectives add av_mast_water dummy "Water Mastery"
scoreboard objectives add av_mast_earth dummy "Earth Mastery"
scoreboard objectives add av_mast_air dummy "Air Mastery"
scoreboard objectives add av_mast_all dummy "Master of Four"

# Built-in Skill Node Attributes (Levels 0-5)
scoreboard objectives add av_stat_agi dummy "Agility Level"
scoreboard objectives add av_stat_chi dummy "Chi Mastery Level"
scoreboard objectives add av_stat_res dummy "Resilience Level"
scoreboard objectives add av_stat_pot dummy "Elemental Potency Level"
scoreboard objectives add av_chi_points dummy "Unallocated Chi"

# Setup default scores for new players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player

tellraw @a [{"text":"[Avatar System] ","color":"gold","bold":true},{"text":"Avatar Skills & Elemental Mastery System 1.21.1 Loaded Successfully!","color":"green"}]
"""
with open(os.path.join(FUNCTION_DIR, "setup.mcfunction"), "w", encoding="utf-8") as f:
    f.write(setup_mcfunction)

# Player initial values
init_player_mcfunction = """# Initialize new player stats
scoreboard players set @s avatar_chi 100
scoreboard players set @s avatar_chi_max 100
scoreboard players set @s avatar_cd 0
scoreboard players set @s avatar_state 0
scoreboard players set @s av_mast_fire 0
scoreboard players set @s av_mast_water 0
scoreboard players set @s av_mast_earth 0
scoreboard players set @s av_mast_air 0
scoreboard players set @s av_mast_all 0
scoreboard players set @s av_stat_agi 0
scoreboard players set @s av_stat_chi 0
scoreboard players set @s av_stat_res 0
scoreboard players set @s av_stat_pot 0
scoreboard players set @s av_chi_points 5
advancement grant @s only avatar_skills:root
advancement grant @s only avatar_skills:attributes/root
"""
with open(os.path.join(TREE_DIR, "init_player.mcfunction"), "w", encoding="utf-8") as f:
    f.write(init_player_mcfunction)

# Tick function
tick_mcfunction = """# ==============================================================================
# Avatar Skills - Main Tick Loop (Minecraft 1.21.1)
# ==============================================================================

# 0. Failsafe auto-initialize player stats for all online players
execute as @a unless score @s avatar_chi_max matches 1.. run function avatar_skills:tree/init_player

# 1. Chi Regeneration (Every 20 ticks / 1 second)
execute as @a run scoreboard players add @s avatar_regen_timer 1
execute as @a if score @s avatar_regen_timer matches 20.. run function avatar_skills:tick_chi_regen

# 2. Cooldown Countdown
execute as @a if score @s avatar_cd matches 1.. run scoreboard players remove @s avatar_cd 1

# 3. Avatar State Timer & 4-Element Orbital Aura
execute as @a if score @s avatar_state matches 1.. run function avatar_skills:avatar_state/tick

# 4. Actionbar HUD Display (Chi & Status)
execute as @a if items entity @s weapon.* *[custom_data~{avatar_item:true}] run function avatar_skills:hud_actionbar

# 5. Right-Click Cast Detection (Warped Fungus + Carrot on a stick)
execute as @a[scores={avatar_used=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used=1..}] run scoreboard players set @s avatar_used 0

execute as @a[scores={avatar_used_c=1..}] at @s run function avatar_skills:cast/router
execute as @a[scores={avatar_used_c=1..}] run scoreboard players set @s avatar_used_c 0

# 6. Auto-check 4-Element Mastery for Avatar Awakening
execute as @a[scores={av_mast_fire=1..,av_mast_water=1..,av_mast_earth=1..,av_mast_air=1..,av_mast_all=0}] run function avatar_skills:tree/awaken_avatar

# 7. Physical Bending Block Decay Timers (Anti-Griefing Auto-Cleanup)
execute as @e[type=marker,tag=avatar_earth_wall] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_earth_wall,scores={avatar_timer=140..}] at @s run function avatar_skills:cast/earth_wall_remove

execute as @e[type=marker,tag=avatar_lava_pool] run scoreboard players add @s avatar_timer 1
execute as @e[type=marker,tag=avatar_lava_pool,scores={avatar_timer=120..}] at @s run function avatar_skills:cast/lava_pool_cool
"""
with open(os.path.join(FUNCTION_DIR, "tick.mcfunction"), "w", encoding="utf-8") as f:
    f.write(tick_mcfunction)

# Chi Regen Function
chi_regen_mcfunction = """# Chi Regeneration tick
scoreboard players set @s avatar_regen_timer 0
execute if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5
# Bonus regen from Chi Mastery node
execute if score @s av_stat_chi matches 1.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 2
execute if score @s av_stat_chi matches 3.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 3
execute if score @s av_stat_chi matches 5.. if score @s avatar_chi < @s avatar_chi_max run scoreboard players add @s avatar_chi 5
"""
with open(os.path.join(FUNCTION_DIR, "tick_chi_regen.mcfunction"), "w", encoding="utf-8") as f:
    f.write(chi_regen_mcfunction)

# HUD Actionbar
hud_actionbar = """# Show Chi and Cooldown on Actionbar
execute if score @s avatar_state matches 1.. run title @s actionbar [{"text":"🌀 [AVATAR STATE] ","color":"light_purple","bold":true},{"text":"CHI: ","color":"aqua"},{"score":{"name":"@s","objective":"avatar_chi"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"},{"text":" | 4-ELEMENTS ACTIVE","color":"gold","bold":true}]
execute unless score @s avatar_state matches 1.. if score @s avatar_cd matches 1.. run title @s actionbar [{"text":"⏳ COOLDOWN: ","color":"red","bold":true},{"score":{"name":"@s","objective":"avatar_cd"},"color":"yellow"},{"text":" ticks | CHI: ","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi"},"color":"aqua"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"}]
execute unless score @s avatar_state matches 1.. unless score @s avatar_cd matches 1.. run title @s actionbar [{"text":"⚡ CHI: ","color":"aqua","bold":true},{"score":{"name":"@s","objective":"avatar_chi"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"white"},{"text":" [READY]","color":"green","bold":true}]
"""
with open(os.path.join(FUNCTION_DIR, "hud_actionbar.mcfunction"), "w", encoding="utf-8") as f:
    f.write(hud_actionbar)

print("Core setup and tick functions generated.")

# =============================================================================
# 5. CAST ROUTING & SKILL LOGIC (RAYCASTS, PARTICLES, COOLDOWNS)
# =============================================================================
cast_router = """# Route Right-Click based on held item
# Failsafe stat initialization
execute unless score @s avatar_chi matches 0.. run scoreboard players set @s avatar_chi 100
execute unless score @s avatar_chi_max matches 1.. run scoreboard players set @s avatar_chi_max 100
execute unless score @s avatar_cd matches 0.. run scoreboard players set @s avatar_cd 0

# Check if player has insufficient Chi (< 10)
execute if score @s avatar_cd matches 0 if score @s avatar_chi matches ..9 run title @s actionbar {"text":"⚠️ Insufficient Chi! Meditate or wait for chi to restore.","color":"red"}

# Route by held item custom_data (Mainhand or Offhand)
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"fire"}] run function avatar_skills:cast/fire_router
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"water"}] run function avatar_skills:cast/water_router
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"earth"}] run function avatar_skills:cast/earth_router
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"air"}] run function avatar_skills:cast/air_router
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"avatar"}] run function avatar_skills:cast/avatar_router
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"mastery"}] run function avatar_skills:tree/open_menu
execute if items entity @s weapon.* *[custom_data~{avatar_skill:"chi_orb"}] run function avatar_skills:tree/consume_chi_orb

# Sub-Bending Foci
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"lightning"}] run function avatar_skills:cast/sub_lightning
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"combustion"}] run function avatar_skills:cast/sub_combustion
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"blood"}] run function avatar_skills:cast/sub_blood
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"healing"}] run function avatar_skills:cast/sub_healing
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"lava"}] run function avatar_skills:cast/sub_lava
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"metal"}] run function avatar_skills:cast/sub_metal
execute if items entity @s weapon.* *[custom_data~{avatar_sub:"flight"}] run function avatar_skills:cast/sub_flight
"""
with open(os.path.join(CAST_DIR, "router.mcfunction"), "w", encoding="utf-8") as f:
    f.write(cast_router)

# --- FIRE SKILLS ---
with open(os.path.join(CAST_DIR, "fire_router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Shift = Jet Propulsion, Normal = Fire Blast
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/fire_jet
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/fire_blast
""")

# Fire Blast - Shaolin Crescent Flame Sweep
fire_blast = """# Fire Blast - Shaolin Crescent Flame Sweep
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 15
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.2 1.1
playsound minecraft:entity.blaze.shoot player @a ~ ~ ~ 1.0 1.2

# Crescent sweep from left to right (Shaolin roundhouse arc)
execute at @s anchored eyes positioned ^-1.2 ^0.1 ^2 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^-0.8 ^0.2 ^3 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^-0.4 ^0.3 ^4 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.0 ^0.3 ^5 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.4 ^0.3 ^5 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^0.8 ^0.2 ^4 run function avatar_skills:cast/fire_step
execute at @s anchored eyes positioned ^1.2 ^0.1 ^3 run function avatar_skills:cast/fire_step

# Ignite ground surface where blast sweeps
execute at @s anchored feet positioned ^ ^ ^3 run execute at @s if block ~ ~ ~ air if block ~ ~-1 ~ #minecraft:inside_step_sound_blocks run setblock ~ ~ ~ fire
"""
with open(os.path.join(CAST_DIR, "fire_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_blast)

fire_step = """particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.03 5 normal
particle minecraft:small_flame ~ ~ ~ 0.15 0.15 0.15 0.01 4 normal
execute as @e[type=!player,dx=0.5,dy=0.5,dz=0.5,limit=3] run function avatar_skills:cast/fire_hit
"""
with open(os.path.join(CAST_DIR, "fire_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_step)

fire_hit = """damage @s 7 minecraft:in_fire
execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
playsound minecraft:entity.generic.burn player @a ~ ~ ~ 0.8 1.0
"""
with open(os.path.join(CAST_DIR, "fire_hit.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_hit)

# Fire Jet
fire_jet = """# Fire Jet Propulsion
scoreboard players remove @s avatar_chi 25
scoreboard players set @s avatar_cd 30
playsound minecraft:entity.firework_rocket.launch player @a ~ ~ ~ 1.2 0.8
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.0 0.9

# Boost forward
execute at @s run tp @s ^ ^0.4 ^2.5
effect give @s minecraft:fire_resistance 3 0 true
execute at @s run particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.05 15 normal
execute at @s run particle minecraft:smoke ~ ~0.2 ~ 0.2 0.2 0.2 0.02 10 normal
execute at @s as @e[type=!player,distance=..3] run function avatar_skills:cast/fire_hit
"""
with open(os.path.join(CAST_DIR, "fire_jet.mcfunction"), "w", encoding="utf-8") as f:
    f.write(fire_jet)

# --- WATER SKILLS ---
with open(os.path.join(CAST_DIR, "water_router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Shift = Glacial Freeze, Normal = Water Whip
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/water_freeze
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/water_whip
""")

# Water Whip (Tai Chi Fluid Serpentine Wave)
water_whip = """# Water Whip - Fluid Serpentine Arc (Tai Chi Flow)
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 12
playsound minecraft:entity.generic.splash player @a ~ ~ ~ 1.2 1.4
playsound minecraft:item.bucket.empty player @a ~ ~ ~ 1.0 1.2

# Fluid wave positions
execute at @s anchored eyes positioned ^0.3 ^-0.1 ^1 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^0.6 ^0.0 ^2 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^0.8 ^0.1 ^3 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^0.5 ^0.2 ^4 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^0.0 ^0.1 ^5 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^-0.5 ^0.0 ^6 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^-0.7 ^-0.1 ^7 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^-0.4 ^-0.2 ^8 run function avatar_skills:cast/water_step
execute at @s anchored eyes positioned ^0.0 ^0.0 ^9 run function avatar_skills:cast/water_step
"""
with open(os.path.join(CAST_DIR, "water_whip.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_whip)

water_step = """particle minecraft:splash ~ ~ ~ 0.25 0.25 0.25 0.05 6 normal
particle minecraft:falling_water ~ ~ ~ 0.15 0.15 0.15 0.02 5 normal
execute as @e[type=!player,dx=0.6,dy=0.6,dz=0.6,limit=3] run function avatar_skills:cast/water_hit
"""
with open(os.path.join(CAST_DIR, "water_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_step)

water_hit = """damage @s 6 minecraft:magic
effect give @s minecraft:slowness 3 1 true
# Pull target towards player
execute facing entity @p feet run tp @s ^ ^ ^0.8
playsound minecraft:entity.player.attack.sweep player @a ~ ~ ~ 0.8 1.5
"""
with open(os.path.join(CAST_DIR, "water_hit.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_hit)

# Water Freeze (Phase Change to Physical Frosted Ice)
water_freeze = """# Glacial Freeze - Freeze existing water into real frosted ice
scoreboard players remove @s avatar_chi 30
scoreboard players set @s avatar_cd 40
playsound minecraft:block.glass.break player @a ~ ~ ~ 1.5 1.4
playsound minecraft:entity.player.hurt_freeze player @a ~ ~ ~ 1.2 1.0

# Physically freeze water in 9x9 area into walkable ice
execute at @s run fill ~-4 ~-1 ~-4 ~4 ~1 ~4 frosted_ice replace water

# Blizzard frost nova
execute at @s run particle minecraft:snowflake ~ ~0.5 ~ 3.5 0.5 3.5 0.05 50 normal
execute at @s as @e[type=!player,distance=..6] run effect give @s minecraft:slowness 6 4 true
execute at @s as @e[type=!player,distance=..6] run damage @s 6 minecraft:freeze
"""
with open(os.path.join(CAST_DIR, "water_freeze.mcfunction"), "w", encoding="utf-8") as f:
    f.write(water_freeze)

# --- EARTH SKILLS ---
with open(os.path.join(CAST_DIR, "earth_router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Shift = Earth Wall, Normal = Boulder Toss
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/earth_wall
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/earth_boulder
""")

# Boulder Toss (Ground extraction & clustered rock projectile)
earth_boulder = """# Boulder Toss - Stomp Ground & Hurl Dense Rock Mass
scoreboard players remove @s avatar_chi 20
scoreboard players set @s avatar_cd 20

# Ground Stomp extraction
execute at @s anchored feet positioned ^ ^ ^1.5 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.4} ~ ~ ~ 0.8 0.4 0.8 0.1 20 normal
execute at @s anchored feet positioned ^ ^ ^1.5 run particle minecraft:poof ~ ~ ~ 0.6 0.3 0.6 0.05 10 normal
playsound minecraft:block.stone.break player @a ~ ~ ~ 1.5 0.8
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 1.2 0.9

# Hurl heavy rock cluster along trajectory
execute at @s anchored eyes positioned ^ ^ ^1 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^2 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^3 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^4 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^5 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^6 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^7 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^8 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^9 run function avatar_skills:cast/earth_step
execute at @s anchored eyes positioned ^ ^ ^10 run function avatar_skills:cast/earth_step
"""
with open(os.path.join(CAST_DIR, "earth_boulder.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_boulder)

earth_step = """particle minecraft:block stone ~ ~ ~ 0.35 0.35 0.35 0.05 12 normal
particle minecraft:block dirt ~ ~ ~ 0.3 0.3 0.3 0.05 8 normal
execute as @e[type=!player,dx=0.6,dy=0.6,dz=0.6,limit=3] run function avatar_skills:cast/earth_hit
"""
with open(os.path.join(CAST_DIR, "earth_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_step)

earth_hit = """damage @s 10 minecraft:generic
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 0.8 1.6
execute facing entity @p feet run tp @s ^ ^0.6 ^-1.2
"""
with open(os.path.join(CAST_DIR, "earth_hit.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_hit)

# Earth Wall (Lifting Physical Ground into 3x2 Stone Barrier + Decay Marker)
earth_wall = """# Earth Wall Barrier - Physical Earth Manipulation
scoreboard players remove @s avatar_chi 30
scoreboard players set @s avatar_cd 60
playsound minecraft:entity.iron_golem.attack player @a ~ ~ ~ 1.5 0.6
playsound minecraft:block.stone.place player @a ~ ~ ~ 1.8 0.7

# Raise physical 3x2 stone wall 3 blocks in front
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~1 ~ stone replace air
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~1 ~ stone replace short_grass
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~1 ~ stone replace tall_grass
execute at @s anchored eyes positioned ^ ^ ^3 run fill ~-1 ~-1 ~ ~1 ~1 ~ stone replace fern
execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:poof ~ ~0.5 ~ 1.2 1.0 0.8 0.05 40 normal
execute at @s anchored eyes positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["avatar_earth_wall"],Age:0}

# Knockback & stun hostiles
execute at @s anchored eyes positioned ^ ^ ^3 as @e[type=!player,distance=..3.5] run tp @s ^ ^0.8 ^-2.0
execute at @s anchored eyes positioned ^ ^ ^3 as @e[type=!player,distance=..3.5] run damage @s 7 minecraft:generic
effect give @s minecraft:resistance 5 2 true
"""
with open(os.path.join(CAST_DIR, "earth_wall.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_wall)

earth_wall_remove = """# Collapse Earth Wall back to rubble
fill ~-1 ~-1 ~ ~1 ~1 ~ air replace stone
particle minecraft:poof ~ ~ ~ 1.0 1.0 0.5 0.05 40 normal
particle minecraft:dust{color:[0.50,0.35,0.20],scale:1.4} ~ ~ ~ 1.0 1.0 0.5 0.1 40 normal
playsound minecraft:block.stone.break player @a ~ ~ ~ 1.5 0.8
kill @s
"""
with open(os.path.join(CAST_DIR, "earth_wall_remove.mcfunction"), "w", encoding="utf-8") as f:
    f.write(earth_wall_remove)

# --- AIR SKILLS ---
with open(os.path.join(CAST_DIR, "air_router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Shift = Air Spout, Normal = Air Blast
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/air_spout
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:cast/air_blast
""")

# Air Blast (Ba Gua Zhang Rotating Vortex Funnel)
air_blast = """# Air Blast - Ba Gua Zhang Vortex Funnel
scoreboard players remove @s avatar_chi 15
scoreboard players set @s avatar_cd 10
playsound minecraft:entity.breeze.shoot player @a ~ ~ ~ 1.3 1.2
playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 1.2 1.0

# Funnel rotation
execute at @s anchored eyes positioned ^0.5 ^0.3 ^2 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^-0.5 ^-0.3 ^3 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^-0.5 ^0.3 ^4 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^0.5 ^-0.3 ^5 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^0.0 ^0.0 ^6 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^0.0 ^0.0 ^7 run function avatar_skills:cast/air_step
execute at @s anchored eyes positioned ^0.0 ^0.0 ^8 run function avatar_skills:cast/air_step
"""
with open(os.path.join(CAST_DIR, "air_blast.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_blast)

air_step = """particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.05 5 normal
particle minecraft:sweep_attack ~ ~ ~ 0.1 0.1 0.1 0.01 1 normal
execute as @e[type=!player,dx=0.6,dy=0.6,dz=0.6,limit=4] run function avatar_skills:cast/air_hit
"""
with open(os.path.join(CAST_DIR, "air_step.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_step)

air_hit = """damage @s 5 minecraft:magic
execute facing entity @p feet run tp @s ^ ^0.4 ^-2.2
playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 0.8 1.4
"""
with open(os.path.join(CAST_DIR, "air_hit.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_hit)

# Air Spout / Sky Leap
air_spout = """# Air Spout Sky Leap
scoreboard players remove @s avatar_chi 20
scoreboard players set @s avatar_cd 25
playsound minecraft:entity.breeze.wind_burst player @a ~ ~ ~ 1.2 1.0

execute at @s run tp @s ~ ~8 ~
effect give @s minecraft:slow_falling 8 0 true
execute at @s run particle minecraft:cloud ~ ~ ~ 0.8 1.5 0.8 0.1 30 normal
execute at @s as @e[type=!player,distance=..4] run tp @s ^ ^0.5 ^-1.5
"""
with open(os.path.join(CAST_DIR, "air_spout.mcfunction"), "w", encoding="utf-8") as f:
    f.write(air_spout)

# --- SUB-BENDING FOCI CASTS ---
# Lightning
with open(os.path.join(CAST_DIR, "sub_lightning.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Lightning Generation
scoreboard players remove @s avatar_chi 40
scoreboard players set @s avatar_cd 60
playsound minecraft:entity.lightning_bolt.thunder player @a ~ ~ ~ 1.2 1.2
playsound minecraft:item.trident.thunder player @a ~ ~ ~ 1.5 1.5

execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^6 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^12 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 20 normal
execute at @s anchored eyes positioned ^ ^ ^12 as @e[type=!player,distance=..4] run damage @s 18 minecraft:lightning_bolt
""")

# Combustion
with open(os.path.join(CAST_DIR, "sub_combustion.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Combustion Bending
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 80
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 1.5 0.8

execute at @s anchored eyes positioned ^ ^ ^15 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 normal
execute at @s anchored eyes positioned ^ ^ ^15 as @e[type=!player,distance=..5] run damage @s 20 minecraft:explosion
execute at @s anchored eyes positioned ^ ^ ^15 as @e[type=!player,distance=..5] run execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
""")

# Bloodbending
with open(os.path.join(CAST_DIR, "sub_blood.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Bloodbending (Immobilize Hostiles)
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 100
playsound minecraft:entity.wither.ambient player @a ~ ~ ~ 1.0 1.5

execute at @s run particle minecraft:dust{color:[0.8,0.05,0.1],scale:1.5} ~ ~1 ~ 4.0 1.0 4.0 0 60 normal
execute at @s as @e[type=!player,distance=..10] run effect give @s minecraft:levitation 4 0 true
execute at @s as @e[type=!player,distance=..10] run effect give @s minecraft:slowness 6 4 true
execute at @s as @e[type=!player,distance=..10] run damage @s 8 minecraft:magic
""")

# Spirit Healing
with open(os.path.join(CAST_DIR, "sub_healing.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Spirit Healing
scoreboard players remove @s avatar_chi 35
scoreboard players set @s avatar_cd 50
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1.0 1.8

execute at @s run particle minecraft:happy_villager ~ ~1 ~ 1.0 1.0 1.0 0.1 25 normal
execute at @s run particle minecraft:heart ~ ~1.5 ~ 0.5 0.5 0.5 0.1 8 normal
effect give @s minecraft:instant_health 1 1 true
effect give @s minecraft:regeneration 8 1 true
""")

# Lavabending (Transmute Real Ground to Magma Blocks + Cool Down)
with open(os.path.join(CAST_DIR, "sub_lava.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Lavabending - Transmute rock & dirt into molten magma
scoreboard players remove @s avatar_chi 40
scoreboard players set @s avatar_cd 70
playsound minecraft:block.lava.ambient player @a ~ ~ ~ 1.5 1.0
playsound minecraft:item.firecharge.use player @a ~ ~ ~ 1.2 0.7

# Transmute terrain in front of player
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace stone
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace dirt
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace grass_block
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace deepslate
execute at @s anchored feet positioned ^ ^ ^3 run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 magma_block replace cobblestone

execute at @s anchored feet positioned ^ ^ ^3 run summon marker ~ ~ ~ {Tags:["avatar_lava_pool"],Age:0}
execute at @s anchored feet positioned ^ ^ ^3 run particle minecraft:lava ~ ~0.5 ~ 1.5 0.3 1.5 0.05 40 normal
execute at @s anchored feet positioned ^ ^ ^3 as @e[type=!player,distance=..4.5] run damage @s 14 minecraft:in_fire
execute at @s anchored feet positioned ^ ^ ^3 as @e[type=!player,distance=..4.5] run execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
""")

with open(os.path.join(CAST_DIR, "lava_pool_cool.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Magma cools back to solidified cobblestone
fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 cobblestone replace magma_block
particle minecraft:smoke ~ ~0.5 ~ 1.5 0.3 1.5 0.05 30 normal
playsound minecraft:block.lava.extinguish player @a ~ ~ ~ 1.2 1.2
kill @s
""")

# Metalbending
with open(os.path.join(CAST_DIR, "sub_metal.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Metalbending Cable Pull
scoreboard players remove @s avatar_chi 25
scoreboard players set @s avatar_cd 25
playsound minecraft:entity.iron_golem.repair player @a ~ ~ ~ 1.2 1.4

execute at @s anchored eyes positioned ^ ^ ^10 run particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.05 20 normal
execute at @s anchored eyes positioned ^ ^ ^10 as @e[type=!player,distance=..3] run tp @s ^ ^ ^-6
execute at @s anchored eyes positioned ^ ^ ^10 as @e[type=!player,distance=..3] run damage @s 10 minecraft:generic
# Or launch player forward
execute at @s run tp @s ^ ^0.3 ^4.0
""")

# Flight
with open(os.path.join(CAST_DIR, "sub_flight.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Zaheer's Weightless Flight
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 120
playsound minecraft:entity.bat.takeoff player @a ~ ~ ~ 1.2 0.8

execute at @s run particle minecraft:cloud ~ ~ ~ 1.0 0.5 1.0 0.05 20 normal
effect give @s minecraft:levitation 10 1 true
effect give @s minecraft:slow_falling 15 0 true
effect give @s minecraft:speed 10 2 true
title @s actionbar {"text":"🕊️ Entering the void... Empty, and become wind.","color":"light_purple","bold":true}
""")

print("All skill casts and sub-bending functions generated.")

# =============================================================================
# 6. AVATAR STATE & FOUR-ELEMENT ORBITAL SPHERE
# =============================================================================
with open(os.path.join(CAST_DIR, "avatar_router.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Avatar Relic Router
# Shift = Activate Avatar State, Normal = Four-Element Orbital Sphere
execute if entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:avatar_state/activate
execute unless entity @s[predicate=avatar_skills:is_sneaking] run function avatar_skills:avatar_state/sphere_ultimate
""")

# Activate Avatar State
avatar_activate = """# Activate Avatar State
scoreboard players set @s avatar_state 600
playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 1.5 1.0
playsound minecraft:entity.wither.spawn player @a ~ ~ ~ 0.8 1.8

effect give @s minecraft:resistance 30 2 true
effect give @s minecraft:speed 30 2 true
effect give @s minecraft:strength 30 2 true
effect give @s minecraft:regeneration 30 1 true
effect give @s minecraft:night_vision 30 0 true
effect give @s minecraft:glowing 30 0 true

title @s title {"text":"🌀 AVATAR STATE AWAKENED 🌀","color":"light_purple","bold":true}
title @s subtitle {"text":"Raava's Cosmic Power Channels Through You!","color":"gold"}
"""
with open(os.path.join(STATE_DIR, "activate.mcfunction"), "w", encoding="utf-8") as f:
    f.write(avatar_activate)

# Avatar State Aura Tick (Every tick during active Avatar State)
avatar_aura_tick = """# 4-Element Orbital Aura (Flame, Water, Stone, Cloud)
scoreboard players remove @s avatar_state 1

# Quadrant 1: Fire (Front)
execute at @s run particle minecraft:flame ^1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 2 normal
# Quadrant 2: Water (Right)
execute at @s run particle minecraft:falling_water ^ ^1.2 ^1.5 0.05 0.05 0.05 0.01 2 normal
# Quadrant 3: Earth (Back)
execute at @s run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.5} ^-1.5 ^1.2 ^ 0.05 0.05 0.05 0.01 4 normal
# Quadrant 4: Air (Left)
execute at @s run particle minecraft:cloud ^ ^1.2 ^-1.5 0.05 0.05 0.05 0.01 2 normal

# End of Avatar State notice
execute if score @s avatar_state matches 0 run title @s title {"text":"Avatar State Exhausted","color":"gray"}
"""
with open(os.path.join(STATE_DIR, "tick.mcfunction"), "w", encoding="utf-8") as f:
    f.write(avatar_aura_tick)

# Four-Element Orbital Sphere Ultimate
avatar_sphere_ultimate = """# Four-Element Orbital Sphere Ultimate
scoreboard players remove @s avatar_chi 50
scoreboard players set @s avatar_cd 40
playsound minecraft:entity.dragon_fireball.explode player @a ~ ~ ~ 1.5 1.2
playsound minecraft:entity.wind_charge.wind_burst player @a ~ ~ ~ 1.5 0.8

# Step 1: Fire Blast
execute at @s anchored eyes positioned ^ ^ ^3 run particle minecraft:flame ~ ~ ~ 0.4 0.4 0.4 0.1 25 normal
# Step 2: Water Lance
execute at @s anchored eyes positioned ^ ^ ^6 run particle minecraft:splash ~ ~ ~ 0.5 0.5 0.5 0.1 30 normal
# Step 3: Earth Megalith
execute at @s anchored eyes positioned ^ ^ ^9 run particle minecraft:dust{color:[0.55,0.40,0.25],scale:1.8} ~ ~ ~ 1.5 1.5 1.5 0.1 80 normal
# Step 4: Air Shockwave
execute at @s anchored eyes positioned ^ ^ ^12 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 normal

# Heavy Cumulative Quad Damage
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run damage @s 28 minecraft:magic
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run execute at @s if block ~ ~ ~ air run setblock ~ ~ ~ fire
execute at @s anchored eyes positioned ^ ^ ^9 as @e[type=!player,distance=..6] run tp @s ^ ^1.0 ^-3.0
"""
with open(os.path.join(STATE_DIR, "sphere_ultimate.mcfunction"), "w", encoding="utf-8") as f:
    f.write(avatar_sphere_ultimate)

print("Avatar State and 4-Element Sphere generated.")

# =============================================================================
# 7. SKILL NODE TREE (TELLRAW INTERACTIVE GUI & ATTRIBUTE SYSTEM)
# =============================================================================
open_menu = """# Open Interactive Skill Tree
tellraw @s ""
tellraw @s [{"text":"==================== ","color":"gold","bold":true},{"text":"AVATAR MASTERY SHRINE","color":"yellow","bold":true},{"text":" ====================","color":"gold","bold":true}]
tellraw @s [{"text":"Unallocated Chi Points: ","color":"gray"},{"score":{"name":"@s","objective":"av_chi_points"},"color":"aqua","bold":true}]
tellraw @s ""
tellraw @s [{"text":"[🏃 AGILITY] ","color":"green","bold":true},{"text":"Current Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_agi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Chi Point. Increases Speed & Safe Fall Distance."}}]
tellraw @s [{"text":"[🧘 CHI MASTERY] ","color":"aqua","bold":true},{"text":"Current Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_chi"},"hoverEvent":{"action":"show_text","value":"Costs 1 Chi Point. Increases Max Chi & Chi Regeneration."}}]
tellraw @s [{"text":"[🛡️ RESILIENCE] ","color":"red","bold":true},{"text":"Current Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_res"},"hoverEvent":{"action":"show_text","value":"Costs 1 Chi Point. Permanently increases Max Health hearts!"}}]
tellraw @s [{"text":"[⚡ ELEMENTAL POTENCY] ","color":"light_purple","bold":true},{"text":"Current Level: ","color":"gray"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"white"},{"text":"/5  "},{"text":"[+] UPGRADE","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/function avatar_skills:tree/upgrade_pot"},"hoverEvent":{"action":"show_text","value":"Costs 1 Chi Point. Increases Damage & Knockback."}}]
tellraw @s ""
tellraw @s [{"text":"[ELEMENT MASTERY UNLOCKS]:","color":"gold","bold":true}]
tellraw @s [{"text":"• Fire: "},{"score":{"name":"@s","objective":"av_mast_fire"},"color":"red"},{"text":" | Water: "},{"score":{"name":"@s","objective":"av_mast_water"},"color":"blue"},{"text":" | Earth: "},{"score":{"name":"@s","objective":"av_mast_earth"},"color":"dark_green"},{"text":" | Air: "},{"score":{"name":"@s","objective":"av_mast_air"},"color":"yellow"}]
tellraw @s [{"text":"=====================================================","color":"gold","bold":true}]
"""
with open(os.path.join(TREE_DIR, "open_menu.mcfunction"), "w", encoding="utf-8") as f:
    f.write(open_menu)

# Upgrade Agility
upgrade_agi = """# Upgrade Agility Node
execute if score @s av_chi_points matches 1.. if score @s av_stat_agi matches ..4 run function avatar_skills:tree/apply_agi
execute unless score @s av_chi_points matches 1.. run tellraw @s {"text":"❌ You do not have enough Chi Points! Defeat mobs or consume Chi Orbs.","color":"red"}
"""
apply_agi = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_agi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5

# Apply 1.21.1 Native Attributes
execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.movement_speed base set 0.115
execute if score @s av_stat_agi matches 2 run attribute @s minecraft:generic.movement_speed base set 0.130
execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.movement_speed base set 0.145
execute if score @s av_stat_agi matches 4 run attribute @s minecraft:generic.movement_speed base set 0.160
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.movement_speed base set 0.180

execute if score @s av_stat_agi matches 1 run attribute @s minecraft:generic.safe_fall_distance base set 5.0
execute if score @s av_stat_agi matches 3 run attribute @s minecraft:generic.safe_fall_distance base set 8.0
execute if score @s av_stat_agi matches 5 run attribute @s minecraft:generic.safe_fall_distance base set 15.0

tellraw @s [{"text":"✅ Agility upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_agi"},"color":"gold","bold":true},{"text":"! Speed & Fall resistance increased.","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "upgrade_agi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(upgrade_agi)
with open(os.path.join(TREE_DIR, "apply_agi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_agi)

# Upgrade Chi Mastery
upgrade_chi = """# Upgrade Chi Node
execute if score @s av_chi_points matches 1.. if score @s av_stat_chi matches ..4 run function avatar_skills:tree/apply_chi
execute unless score @s av_chi_points matches 1.. run tellraw @s {"text":"❌ You do not have enough Chi Points! Defeat mobs or consume Chi Orbs.","color":"red"}
"""
apply_chi = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_chi 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5

# Expand Max Chi Capacity
execute if score @s av_stat_chi matches 1 run scoreboard players set @s avatar_chi_max 125
execute if score @s av_stat_chi matches 2 run scoreboard players set @s avatar_chi_max 150
execute if score @s av_stat_chi matches 3 run scoreboard players set @s avatar_chi_max 175
execute if score @s av_stat_chi matches 4 run scoreboard players set @s avatar_chi_max 200
execute if score @s av_stat_chi matches 5 run scoreboard players set @s avatar_chi_max 250

tellraw @s [{"text":"✅ Chi Mastery upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_chi"},"color":"gold","bold":true},{"text":"! Max Chi expanded to ","color":"green"},{"score":{"name":"@s","objective":"avatar_chi_max"},"color":"aqua"},{"text":" & regen speed boosted!","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "upgrade_chi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(upgrade_chi)
with open(os.path.join(TREE_DIR, "apply_chi.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_chi)

# Upgrade Resilience
upgrade_res = """# Upgrade Resilience Node
execute if score @s av_chi_points matches 1.. if score @s av_stat_res matches ..4 run function avatar_skills:tree/apply_res
execute unless score @s av_chi_points matches 1.. run tellraw @s {"text":"❌ You do not have enough Chi Points! Defeat mobs or consume Chi Orbs.","color":"red"}
"""
apply_res = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_res 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5

# Apply Extra Max Health Hearts
execute if score @s av_stat_res matches 1 run attribute @s minecraft:generic.max_health base set 24
execute if score @s av_stat_res matches 2 run attribute @s minecraft:generic.max_health base set 28
execute if score @s av_stat_res matches 3 run attribute @s minecraft:generic.max_health base set 32
execute if score @s av_stat_res matches 4 run attribute @s minecraft:generic.max_health base set 36
execute if score @s av_stat_res matches 5 run attribute @s minecraft:generic.max_health base set 40

tellraw @s [{"text":"✅ Resilience upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_res"},"color":"gold","bold":true},{"text":"! Max Health hearts increased!","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "upgrade_res.mcfunction"), "w", encoding="utf-8") as f:
    f.write(upgrade_res)
with open(os.path.join(TREE_DIR, "apply_res.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_res)

# Upgrade Elemental Potency
upgrade_pot = """# Upgrade Potency Node
execute if score @s av_chi_points matches 1.. if score @s av_stat_pot matches ..4 run function avatar_skills:tree/apply_pot
execute unless score @s av_chi_points matches 1.. run tellraw @s {"text":"❌ You do not have enough Chi Points! Defeat mobs or consume Chi Orbs.","color":"red"}
"""
apply_pot = """scoreboard players remove @s av_chi_points 1
scoreboard players add @s av_stat_pot 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1.0 1.5

tellraw @s [{"text":"✅ Elemental Potency upgraded to Level ","color":"green"},{"score":{"name":"@s","objective":"av_stat_pot"},"color":"gold","bold":true},{"text":"! All elemental attacks deal amplified damage!","color":"green"}]
"""
with open(os.path.join(TREE_DIR, "upgrade_pot.mcfunction"), "w", encoding="utf-8") as f:
    f.write(upgrade_pot)
with open(os.path.join(TREE_DIR, "apply_pot.mcfunction"), "w", encoding="utf-8") as f:
    f.write(apply_pot)

# Consume Chi Orb
consume_chi_orb = """# Consume Chi Orb to gain Chi Points
clear @s minecraft:warped_fungus_on_a_stick[custom_data~{avatar_skill:"chi_orb"}] 1
scoreboard players add @s av_chi_points 1
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 1.8
particle minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.05 15 normal
tellraw @s [{"text":"✨ Chi Orb absorbed! Gained ","color":"aqua"},{"text":"+1 Chi Point","color":"gold","bold":true},{"text":" for skill upgrades.","color":"aqua"}]
"""
with open(os.path.join(TREE_DIR, "consume_chi_orb.mcfunction"), "w", encoding="utf-8") as f:
    f.write(consume_chi_orb)

# Awaken Avatar State
awaken_avatar = """# Awaken Avatar
scoreboard players set @s av_mast_all 1
advancement grant @s only avatar_skills:avatar/state
playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 2.0 1.0
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5005,custom_data={avatar_item:true,avatar_skill:"avatar"},item_name='{"text":"Cosmic Avatar Relic","color":"gold","bold":true}',lore=['{"text":"The sacred conduit of Raava","color":"yellow"}','{"text":"Right-Click: Four-Element Orbital Sphere","color":"aqua"}','{"text":"Shift + Right-Click: Enter Avatar State!","color":"light_purple"}']]
tellraw @a [{"text":"🌟 [AVATAR PROPHECY] ","color":"gold","bold":true},{"selector":"@s","color":"yellow","bold":true},{"text":" has mastered all Four Elements and unlocked the AVATAR STATE!","color":"green","bold":true}]
"""
with open(os.path.join(TREE_DIR, "awaken_avatar.mcfunction"), "w", encoding="utf-8") as f:
    f.write(awaken_avatar)

# Predicate for Sneaking detection in 1.21.1
predicate_dir = os.path.join(AVATAR_DATA, "predicate")
os.makedirs(predicate_dir, exist_ok=True)
with open(os.path.join(predicate_dir, "is_sneaking.json"), "w", encoding="utf-8") as f:
    json.dump({
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {
            "flags": {
                "is_sneaking": True
            }
        }
    }, f, indent=2)

print("Skill node tree functions and sneaking predicate created.")

# =============================================================================
# 8. GIVE FUNCTIONS FOR ALL ITEMS
# =============================================================================
# Give Fire Scroll
with open(os.path.join(GIVE_DIR, "fire.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5001,custom_data={avatar_item:true,avatar_skill:"fire"},item_name='{"text":"Scroll of Firebending","color":"red","bold":true}',lore=['{"text":"Discipline of the Sun Warriors","color":"gold"}','{"text":"Right-Click: Fire Blast","color":"yellow"}','{"text":"Shift + Right-Click: Jet Propulsion","color":"yellow"}']]
scoreboard players set @s av_mast_fire 1
advancement grant @s only avatar_skills:fire/root
""")

# Give Water Scroll
with open(os.path.join(GIVE_DIR, "water.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5002,custom_data={avatar_item:true,avatar_skill:"water"},item_name='{"text":"Scroll of Waterbending","color":"blue","bold":true}',lore=['{"text":"Discipline of the Ocean & Moon","color":"aqua"}','{"text":"Right-Click: Water Whip & Pull","color":"yellow"}','{"text":"Shift + Right-Click: Glacial Freeze","color":"yellow"}']]
scoreboard players set @s av_mast_water 1
advancement grant @s only avatar_skills:water/root
""")

# Give Earth Scroll
with open(os.path.join(GIVE_DIR, "earth.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5003,custom_data={avatar_item:true,avatar_skill:"earth"},item_name='{"text":"Scroll of Earthbending","color":"dark_green","bold":true}',lore=['{"text":"Discipline of Badger-Moles","color":"green"}','{"text":"Right-Click: Boulder Toss","color":"yellow"}','{"text":"Shift + Right-Click: Earth Wall Barrier","color":"yellow"}']]
scoreboard players set @s av_mast_earth 1
advancement grant @s only avatar_skills:earth/root
""")

# Give Air Scroll
with open(os.path.join(GIVE_DIR, "air.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5004,custom_data={avatar_item:true,avatar_skill:"air"},item_name='{"text":"Scroll of Airbending","color":"yellow","bold":true}',lore=['{"text":"Discipline of the Flying Bison","color":"white"}','{"text":"Right-Click: Air Blast & Arrow Deflect","color":"yellow"}','{"text":"Shift + Right-Click: Air Spout Sky Leap","color":"yellow"}']]
scoreboard players set @s av_mast_air 1
advancement grant @s only avatar_skills:air/root
""")

# Give Avatar Relic
with open(os.path.join(GIVE_DIR, "avatar_relic.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5005,custom_data={avatar_item:true,avatar_skill:"avatar"},item_name='{"text":"Cosmic Avatar Relic","color":"gold","bold":true}',lore=['{"text":"The sacred conduit of Raava","color":"yellow"}','{"text":"Right-Click: Four-Element Orbital Sphere","color":"aqua"}','{"text":"Shift + Right-Click: Enter Avatar State!","color":"light_purple"}']]
scoreboard players set @s av_mast_fire 1
scoreboard players set @s av_mast_water 1
scoreboard players set @s av_mast_earth 1
scoreboard players set @s av_mast_air 1
scoreboard players set @s av_mast_all 1
advancement grant @s only avatar_skills:avatar/state
""")

# Give Tome of Mastery
with open(os.path.join(GIVE_DIR, "mastery.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5006,custom_data={avatar_item:true,avatar_skill:"mastery"},item_name='{"text":"Tome of Chi Mastery","color":"gold","bold":true}',lore=['{"text":"Right-Click to open the Skill Node Tree Shrine","color":"yellow"}','{"text":"Allocate Chi Points into Agility, Chi, Resilience, & Potency","color":"gray"}']]
""")

# Give Chi Orbs
with open(os.path.join(GIVE_DIR, "chi_orbs.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5007,custom_data={avatar_item:true,avatar_skill:"chi_orb"},item_name='{"text":"Condensed Chi Orb","color":"aqua","bold":true}',lore=['{"text":"Right-Click to consume for +1 Chi Point","color":"yellow"}']] 16
""")

# Give Sub-Bending Foci
with open(os.path.join(GIVE_DIR, "sub_bending_foci.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Sub-bending foci
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5008,custom_data={avatar_item:true,avatar_sub:"lightning"},item_name='{"text":"Focus of Lightning Generation","color":"aqua","bold":true}',lore=['{"text":"Right-Click to cast piercing lightning strike","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5009,custom_data={avatar_item:true,avatar_sub:"combustion"},item_name='{"text":"Focus of Combustion Bending","color":"dark_red","bold":true}',lore=['{"text":"Right-Click to launch telekinetic explosive beam","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5010,custom_data={avatar_item:true,avatar_sub:"blood"},item_name='{"text":"Focus of Bloodbending","color":"red","bold":true}',lore=['{"text":"Right-Click to immobilize and levitate all nearby entities","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5011,custom_data={avatar_item:true,avatar_sub:"healing"},item_name='{"text":"Focus of Spirit Healing","color":"green","bold":true}',lore=['{"text":"Right-Click to mend wounds and grant regeneration","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5012,custom_data={avatar_item:true,avatar_sub:"lava"},item_name='{"text":"Focus of Lavabending","color":"gold","bold":true}',lore=['{"text":"Right-Click to fissure the earth with molten lava","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5013,custom_data={avatar_item:true,avatar_sub:"metal"},item_name='{"text":"Focus of Metalbending","color":"gray","bold":true}',lore=['{"text":"Right-Click to fire high-velocity steel cables","color":"yellow"}']]
give @s minecraft:warped_fungus_on_a_stick[custom_model_data=5014,custom_data={avatar_item:true,avatar_sub:"flight"},item_name='{"text":"Focus of Weightless Flight","color":"light_purple","bold":true}',lore=['{"text":"Right-Click to achieve true Zaheer flight","color":"yellow"}']]
advancement grant @s only avatar_skills:fire/lightning
advancement grant @s only avatar_skills:fire/combustion
advancement grant @s only avatar_skills:water/healing
advancement grant @s only avatar_skills:water/bloodbending
advancement grant @s only avatar_skills:earth/metalbending
advancement grant @s only avatar_skills:earth/lavabending
advancement grant @s only avatar_skills:air/flight
""")

# Give All
with open(os.path.join(GIVE_DIR, "all_skills.mcfunction"), "w", encoding="utf-8") as f:
    f.write("""# Give All Avatar Skills
function avatar_skills:setup
function avatar_skills:tree/init_player
function avatar_skills:give/fire
function avatar_skills:give/water
function avatar_skills:give/earth
function avatar_skills:give/air
function avatar_skills:give/avatar_relic
function avatar_skills:give/mastery
function avatar_skills:give/chi_orbs
function avatar_skills:give/sub_bending_foci
tellraw @s [{"text":"[Avatar System] ","color":"gold","bold":true},{"text":"All Avatar Scrolls, Relics, and Sub-bending Foci have been granted!","color":"green"}]
tellraw @s [{"text":"[Controls Guide] ","color":"aqua","bold":true},{"text":"Right-Click (Mouse Klik Kanan) to cast primary bending. Shift + Right-Click to cast defensive/mobility bending. (Make sure you are in Survival/Adventure mode).","color":"yellow"}]
""")

# Aliases under avatar: namespace so either /function avatar:... or /function avatar_skills:... works
with open(os.path.join(AVATAR_ALIAS_GIVE, "all_skills.mcfunction"), "w", encoding="utf-8") as f:
    f.write("function avatar_skills:give/all_skills\n")
with open(os.path.join(AVATAR_ALIAS_GIVE, "skills.mcfunction"), "w", encoding="utf-8") as f:
    f.write("function avatar_skills:give/all_skills\n")
with open(os.path.join(AVATAR_ALIAS_TREE, "open_menu.mcfunction"), "w", encoding="utf-8") as f:
    f.write("function avatar_skills:tree/open_menu\n")
with open(os.path.join(DATA_DIR, "avatar", "function", "skills.mcfunction"), "w", encoding="utf-8") as f:
    f.write("function avatar_skills:give/all_skills\n")

print("Give functions and aliases generated.")

# =============================================================================
# 9. DOCUMENTATION (README.MD IN BOTH PACKS)
# =============================================================================
readme_datapack = """# 🌀 Avatar: The Way of Bending — Skills & Mastery Datapack (1.21.1)

A complete, high-performance Minecraft Java Edition **1.21.1** Datapack bringing **Active Bending Skills, Sub-Bending Arts, an Interactive Skill Node Tree, and the Avatar State with Elemental Combinations** from *Avatar: The Last Airbender* & *The Legend of Korra*.

---

## 🌟 Key Features

1. **4 Elemental Disciplines**:
   - **🔥 Firebending**: Fire Blast, Jet Propulsion.
   - **🌊 Waterbending**: Water Whip, Glacial Freeze.
   - **🪨 Earthbending**: Boulder Toss, Earth Wall.
   - **💨 Airbending**: Air Blast, Air Spout Sky Leap.
2. **Sub-Bending Disciplines**:
   - **Lightning Generation & Combustion Bending** (Fire)
   - **Spirit Healing & Bloodbending** (Water)
   - **Metalbending & Lavabending** (Earth)
   - **Zaheer's Weightless Flight** (Air)
3. **Built-in Physical & Spiritual Skill Node Tree**:
   - **🏃 Agility**: Adds movement speed and reduces fall damage.
   - **🧘 Chi Mastery**: Expands Max Chi (100 -> 250) and accelerates Chi regen.
   - **🛡️ Resilience**: Permanently grants extra Max Health hearts (up to 40 HP).
   - **⚡ Elemental Potency**: Amplifies damage and knockback.
   - *Upgraded by consuming Chi Orbs via the Tome of Chi Mastery*.
4. **🌀 Avatar State & 4-Element Orbital Sphere**:
   - Unlocked when all 4 elements are mastered.
   - **Avatar State**: 4 elemental aura particles circling the player simultaneously with God-tier buffs.
   - **Four-Element Orbital Sphere**: Devastating ultimate firing Fireball -> Water Lance -> Boulder -> Sonic Gale!

---

## 💻 Commands

```mcfunction
# Give All Skills, Relics & Foci
/function avatar_skills:give/all_skills

# Give Individual Scrolls
/function avatar_skills:give/fire
/function avatar_skills:give/water
/function avatar_skills:give/earth
/function avatar_skills:give/air
/function avatar_skills:give/avatar_relic
/function avatar_skills:give/mastery
/function avatar_skills:give/sub_bending_foci
/function avatar_skills:give/chi_orbs

# Open Skill Node Tree Shrine
/function avatar_skills:tree/open_menu
```
"""
with open(os.path.join(DATAPACK_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_datapack)

readme_resourcepack = """# 🎨 Avatar Skills & Relics Resource Pack (1.21.1)

Custom high-definition 16x16 pixel art textures and models for the Avatar Skills Datapack.

## 📦 Textures Included:
- `scroll_fire.png`: Crimson parchment with Sun Warrior fire crest.
- `scroll_water.png`: Deep ocean cyan parchment with tidal crest.
- `scroll_earth.png`: Terracotta and bronze parchment with mountain crest.
- `scroll_air.png`: Ivory and saffron silk parchment with triskelion air crest.
- `avatar_relic.png`: Cosmic Raava platinum amulet with 4 elemental cardinal gems.
- `scroll_mastery.png`: Ancient leather-bound tome with the White Lotus emblem.
- `chi_orb.png`: Radiant cyan spirit essence sphere.
- Sub-bending Foci: Lightning, Combustion, Blood, Healing, Lava, Metal, and Flight.
"""
with open(os.path.join(RESOURCEPACK_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_resourcepack)

print("Documentation generated.")

# =============================================================================
# 10. AUTOMATIC ZIP PACKAGING
# =============================================================================
import zipfile

def make_zip(source_dir, output_zip):
    if os.path.exists(output_zip):
        os.remove(output_zip)
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, source_dir)
                zipf.write(abs_path, rel_path)
    print(f"Package created: {output_zip} ({os.path.getsize(output_zip)} bytes)")

make_zip(DATAPACK_DIR, os.path.join(REPO_DIR, "avatar-skill-datapack.zip"))
make_zip(RESOURCEPACK_DIR, os.path.join(REPO_DIR, "avatar-skill-resourcepack.zip"))

print("=== All generation & zip packaging completed successfully! ===")
