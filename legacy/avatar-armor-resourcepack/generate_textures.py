#!/usr/bin/env python3
"""
Avatar Armor Resource Pack - 7-Tier Elemental Progression Texture Generator (Minecraft 1.21.1)
Covers all 4 Nations (Fire, Water, Earth, Air) across all 7 Tiers (Initiate -> Sovereign)
Generates all 112 16x16 pixel-art icons with organic, non-stiff silhouettes.
"""

import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "avatar")
ITEM_TEX_DIR = os.path.join(ASSETS_DIR, "textures", "item")
ENTITY_EQUIP_DIR = os.path.join(ASSETS_DIR, "textures", "entity", "equipment")

for d in [ITEM_TEX_DIR, ENTITY_EQUIP_DIR]:
    os.makedirs(d, exist_ok=True)

NATIONS = ["fire", "water", "earth", "air"]
TIERS = ["initiate", "apprentice", "adept", "veteran", "master", "mythic", "sovereign"]
PIECES = ["helmet", "chestplate", "leggings", "boots"]

# ==============================================================================
# PALETTES FOR ALL 28 (NATION, TIER) COMBINATIONS
# ==============================================================================
PALETTES = {
    # --- FIRE NATION ---
    ("fire", "initiate"): {
        "outline": (45, 25, 25, 255), "shadow": (95, 40, 35, 255),
        "primary": (150, 48, 42, 255), "secondary": (105, 68, 48, 255),
        "accent": (215, 85, 42, 255), "glint": (235, 175, 140, 255),
        "trim": (85, 52, 38, 255), "glow": (255, 120, 60, 255), "visor": (30, 15, 15, 255)
    },
    ("fire", "apprentice"): {
        "outline": (35, 20, 22, 255), "shadow": (55, 30, 32, 255),
        "primary": (115, 35, 35, 255), "secondary": (60, 50, 52, 255),
        "accent": (230, 130, 30, 255), "glint": (245, 180, 120, 255),
        "trim": (180, 50, 30, 255), "glow": (255, 160, 40, 255), "visor": (25, 15, 18, 255)
    },
    ("fire", "adept"): {
        "outline": (40, 22, 20, 255), "shadow": (110, 55, 30, 255),
        "primary": (190, 85, 40, 255), "secondary": (140, 35, 30, 255),
        "accent": (245, 160, 50, 255), "glint": (255, 220, 150, 255),
        "trim": (160, 45, 30, 255), "glow": (255, 180, 50, 255), "visor": (30, 18, 18, 255)
    },
    ("fire", "veteran"): {
        "outline": (30, 15, 18, 255), "shadow": (95, 25, 25, 255),
        "primary": (170, 32, 30, 255), "secondary": (75, 65, 70, 255),
        "accent": (225, 170, 45, 255), "glint": (255, 235, 180, 255),
        "trim": (130, 25, 25, 255), "glow": (255, 80, 40, 255), "visor": (20, 10, 12, 255)
    },
    ("fire", "master"): {
        "outline": (25, 15, 20, 255), "shadow": (60, 48, 55, 255),
        "primary": (85, 75, 80, 255), "secondary": (215, 45, 30, 255),
        "accent": (255, 205, 50, 255), "glint": (255, 245, 190, 255),
        "trim": (235, 90, 30, 255), "glow": (255, 50, 50, 255), "visor": (20, 10, 15, 255)
    },
    ("fire", "mythic"): {
        "outline": (20, 10, 12, 255), "shadow": (45, 35, 40, 255),
        "primary": (60, 52, 58, 255), "secondary": (205, 55, 20, 255),
        "accent": (255, 145, 30, 255), "glint": (255, 230, 140, 255),
        "trim": (255, 95, 20, 255), "glow": (255, 200, 60, 255), "visor": (15, 8, 10, 255)
    },
    ("fire", "sovereign"): {
        "outline": (50, 10, 10, 255), "shadow": (115, 20, 20, 255),
        "primary": (195, 28, 28, 255), "secondary": (255, 140, 20, 255),
        "accent": (255, 220, 50, 255), "glint": (255, 255, 200, 255),
        "trim": (255, 70, 20, 255), "glow": (255, 240, 100, 255), "visor": (25, 5, 5, 255)
    },

    # --- WATER TRIBE ---
    ("water", "initiate"): {
        "outline": (25, 35, 45, 255), "shadow": (45, 75, 115, 255),
        "primary": (75, 115, 170, 255), "secondary": (235, 245, 255, 255),
        "accent": (140, 190, 235, 255), "glint": (250, 255, 255, 255),
        "trim": (50, 72, 98, 255), "glow": (180, 225, 255, 255), "visor": (20, 30, 42, 255)
    },
    ("water", "apprentice"): {
        "outline": (22, 32, 44, 255), "shadow": (40, 68, 105, 255),
        "primary": (68, 110, 168, 255), "secondary": (240, 245, 250, 255),
        "accent": (45, 155, 235, 255), "glint": (250, 255, 255, 255),
        "trim": (180, 205, 225, 255), "glow": (120, 210, 255, 255), "visor": (18, 28, 40, 255)
    },
    ("water", "adept"): {
        "outline": (20, 40, 60, 255), "shadow": (35, 95, 145, 255),
        "primary": (60, 145, 210, 255), "secondary": (225, 235, 240, 255),
        "accent": (90, 215, 240, 255), "glint": (235, 255, 255, 255),
        "trim": (35, 105, 175, 255), "glow": (150, 235, 255, 255), "visor": (15, 32, 50, 255)
    },
    ("water", "veteran"): {
        "outline": (15, 30, 50, 255), "shadow": (25, 65, 110, 255),
        "primary": (42, 105, 175, 255), "secondary": (30, 75, 130, 255),
        "accent": (235, 105, 115, 255), "glint": (210, 245, 255, 255),
        "trim": (70, 175, 235, 255), "glow": (100, 225, 255, 255), "visor": (12, 22, 38, 255)
    },
    ("water", "master"): {
        "outline": (18, 25, 38, 255), "shadow": (45, 58, 75, 255),
        "primary": (68, 82, 100, 255), "secondary": (45, 140, 220, 255),
        "accent": (240, 245, 255, 255), "glint": (230, 252, 255, 255),
        "trim": (120, 205, 255, 255), "glow": (255, 255, 255, 255), "visor": (14, 20, 30, 255)
    },
    ("water", "mythic"): {
        "outline": (12, 20, 35, 255), "shadow": (28, 45, 68, 255),
        "primary": (45, 60, 80, 255), "secondary": (35, 160, 235, 255),
        "accent": (75, 225, 255, 255), "glint": (220, 255, 255, 255),
        "trim": (60, 195, 245, 255), "glow": (255, 255, 255, 255), "visor": (10, 15, 28, 255)
    },
    ("water", "sovereign"): {
        "outline": (10, 25, 65, 255), "shadow": (20, 50, 125, 255),
        "primary": (28, 85, 192, 255), "secondary": (65, 190, 255, 255),
        "accent": (255, 255, 255, 255), "glint": (220, 255, 255, 255),
        "trim": (130, 235, 255, 255), "glow": (255, 255, 255, 255), "visor": (8, 18, 48, 255)
    },

    # --- EARTH KINGDOM ---
    ("earth", "initiate"): {
        "outline": (30, 35, 25, 255), "shadow": (60, 75, 45, 255),
        "primary": (95, 125, 75, 255), "secondary": (110, 80, 50, 255),
        "accent": (165, 195, 130, 255), "glint": (225, 240, 205, 255),
        "trim": (75, 55, 35, 255), "glow": (180, 220, 140, 255), "visor": (22, 28, 18, 255)
    },
    ("earth", "apprentice"): {
        "outline": (30, 32, 20, 255), "shadow": (65, 70, 40, 255),
        "primary": (85, 120, 65, 255), "secondary": (185, 150, 95, 255),
        "accent": (45, 195, 110, 255), "glint": (235, 245, 200, 255),
        "trim": (135, 105, 65, 255), "glow": (90, 240, 150, 255), "visor": (20, 25, 16, 255)
    },
    ("earth", "adept"): {
        "outline": (25, 35, 25, 255), "shadow": (40, 95, 50, 255),
        "primary": (70, 160, 85, 255), "secondary": (120, 95, 60, 255),
        "accent": (60, 215, 120, 255), "glint": (230, 255, 240, 255),
        "trim": (50, 130, 65, 255), "glow": (110, 245, 160, 255), "visor": (18, 28, 18, 255)
    },
    ("earth", "veteran"): {
        "outline": (22, 28, 22, 255), "shadow": (50, 75, 50, 255),
        "primary": (85, 115, 88, 255), "secondary": (95, 100, 95, 255),
        "accent": (180, 165, 90, 255), "glint": (225, 240, 225, 255),
        "trim": (45, 90, 50, 255), "glow": (80, 210, 120, 255), "visor": (15, 20, 15, 255)
    },
    ("earth", "master"): {
        "outline": (20, 25, 20, 255), "shadow": (50, 58, 50, 255),
        "primary": (75, 82, 75, 255), "secondary": (55, 175, 95, 255),
        "accent": (225, 195, 80, 255), "glint": (245, 250, 220, 255),
        "trim": (50, 140, 70, 255), "glow": (95, 235, 140, 255), "visor": (14, 18, 14, 255)
    },
    ("earth", "mythic"): {
        "outline": (15, 20, 15, 255), "shadow": (35, 42, 35, 255),
        "primary": (55, 60, 55, 255), "secondary": (45, 190, 95, 255),
        "accent": (100, 235, 140, 255), "glint": (230, 255, 230, 255),
        "trim": (60, 170, 90, 255), "glow": (120, 255, 165, 255), "visor": (10, 15, 10, 255)
    },
    ("earth", "sovereign"): {
        "outline": (15, 35, 20, 255), "shadow": (25, 75, 35, 255),
        "primary": (40, 140, 60, 255), "secondary": (110, 225, 130, 255),
        "accent": (255, 215, 50, 255), "glint": (230, 255, 235, 255),
        "trim": (180, 245, 160, 255), "glow": (255, 235, 120, 255), "visor": (10, 25, 12, 255)
    },

    # --- AIR NOMAD ---
    ("air", "initiate"): {
        "outline": (45, 35, 20, 255), "shadow": (120, 90, 40, 255),
        "primary": (215, 155, 50, 255), "secondary": (235, 195, 80, 255),
        "accent": (100, 180, 225, 255), "glint": (255, 245, 215, 255),
        "trim": (160, 110, 30, 255), "glow": (140, 215, 255, 255), "visor": (35, 26, 14, 255)
    },
    ("air", "apprentice"): {
        "outline": (38, 30, 18, 255), "shadow": (95, 75, 35, 255),
        "primary": (195, 140, 45, 255), "secondary": (210, 130, 70, 255),
        "accent": (120, 210, 245, 255), "glint": (250, 240, 200, 255),
        "trim": (220, 200, 160, 255), "glow": (180, 240, 255, 255), "visor": (28, 20, 12, 255)
    },
    ("air", "adept"): {
        "outline": (30, 35, 40, 255), "shadow": (75, 110, 130, 255),
        "primary": (130, 195, 220, 255), "secondary": (225, 165, 50, 255),
        "accent": (90, 210, 250, 255), "glint": (240, 255, 255, 255),
        "trim": (100, 185, 235, 255), "glow": (160, 240, 255, 255), "visor": (20, 32, 38, 255)
    },
    ("air", "veteran"): {
        "outline": (30, 28, 22, 255), "shadow": (70, 70, 75, 255),
        "primary": (195, 155, 60, 255), "secondary": (235, 235, 240, 255),
        "accent": (110, 205, 240, 255), "glint": (250, 248, 230, 255),
        "trim": (150, 115, 35, 255), "glow": (140, 230, 255, 255), "visor": (22, 20, 16, 255)
    },
    ("air", "master"): {
        "outline": (25, 25, 30, 255), "shadow": (55, 55, 65, 255),
        "primary": (80, 80, 90, 255), "secondary": (245, 190, 60, 255),
        "accent": (130, 220, 255, 255), "glint": (255, 250, 230, 255),
        "trim": (140, 210, 245, 255), "glow": (80, 225, 255, 255), "visor": (18, 18, 22, 255)
    },
    ("air", "mythic"): {
        "outline": (20, 22, 28, 255), "shadow": (45, 50, 60, 255),
        "primary": (75, 85, 100, 255), "secondary": (240, 245, 255, 255),
        "accent": (60, 215, 255, 255), "glint": (235, 250, 255, 255),
        "trim": (120, 220, 255, 255), "glow": (70, 230, 255, 255), "visor": (15, 18, 24, 255)
    },
    ("air", "sovereign"): {
        "outline": (55, 45, 15, 255), "shadow": (135, 105, 30, 255),
        "primary": (235, 185, 55, 255), "secondary": (255, 235, 130, 255),
        "accent": (65, 215, 255, 255), "glint": (255, 255, 245, 255),
        "trim": (135, 238, 255, 255), "glow": (80, 240, 255, 255), "visor": (30, 22, 10, 255)
    }
}

# ==============================================================================
# 1. PIXEL TEMPLATES: HELMETS (28 Specialized Archetypes)
# ==============================================================================

# --- TIER 1: INITIATE (Soft cloth hoodie / cowl with soft draped cloth neck) ---
HELMET_INITIATE = [
    "................",
    "......OOOO......",
    "....OOGGGGOO....",
    "...OGGGGGGGGO...",
    "..OGGGGGGGGGGO..",
    "..OGG..OOOO..GO.",
    "..OG..O....O.GO.",
    "..OG..O....O.GO.",
    "..OGG..OOOO..GO.",
    "...OGGGGGGGGO...",
    "....OGPTTTPGO...",
    "...OGPPTTTPGO...",
    "..OGGPPPPPPPGGO.",
    "...OOOOOOOOOO...",
    "................",
    "................"
]

# --- TIER 2: APPRENTICE ---
# Fire Apprentice: Ninja half-mask + flame topknot brow-band
HELMET_APP_FIRE = [
    ".......AA.......",
    "......OAAO......",
    ".....OAAPAO.....",
    "....OAPPPPAO....",
    "...OAGPPPPGAO...",
    "..OGPAAAAAAPGO..",
    "..OPPAAAAAAPPO..",
    "..OP..C..C..PO..",
    "..OP.CC..CC.PO..",
    "..OPSSSSSSSPO...",
    "..OPSSSSSSSPO...",
    "..OPPPOOOPPO....",
    "...OPPPPPPPO....",
    "....OOOOOOO.....",
    "................",
    "................"
]

# Water Apprentice: Wolf pelt headpiece with white wolf ears/fur & blue war-paint bandana
HELMET_APP_WATER = [
    "...OO......OO...",
    "..OAAO....OAAO..",
    "..OAPAO..OAPAO..",
    "..OAPPPAAPPPAO..",
    ".OAPPPPPPPPPPAO.",
    ".OAPTTTTTTTTPAO.",
    ".OAP..C..C..PAO.",
    ".OAP..C..C..PAO.",
    ".OAP........PAO.",
    ".OAA..OOOO..AAO.",
    ".OAA.OPPPPO.AAO.",
    "..OAAPPPPPPAAO..",
    "...OAAOOOAAO....",
    "....OOOOOO......",
    "................",
    "................"
]

# Earth Apprentice: Conical Dai Li straw/bamboo hat with emerald talisman & chin strap
HELMET_APP_EARTH = [
    ".......TT.......",
    "......OTTO......",
    ".....OTAAATO....",
    "....OTAAAAAATO..",
    "...OTAAAATAAATO.",
    "..OTAAAATTTTAATO",
    ".OTAAAAAAAAAAAAT",
    "OTTTTTTTTTTTTTTO",
    "OOOOOOOOOOOOOOOO",
    "...OP.C..C.PO...",
    "...OP.C..C.PO...",
    "...OP......PO...",
    "...OPPB..BPOO...",
    "....OPBBBBPO....",
    ".....OOOOOO.....",
    "................"
]

# Air Apprentice: Glider flight cowl with round copper wind goggles & fleece ear-flaps
HELMET_APP_AIR = [
    "......OOOO......",
    "....OOGGGGOO....",
    "...OGGGGGGGGO...",
    "..OGGGGGGGGGGO..",
    "..OGAAAAAAAAAGGO",
    "..OGACCCAACCCAGO",
    "..OGACVCAACVCAGO",
    "..OGACCCAACCCAGO",
    "..OGAAAAAAAAAGGO",
    "..OP..C..C..PPO.",
    "..OPTT....TTPO..",
    "..OPTTPOOPTTPO..",
    "...OPPPPPPPPO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# --- TIER 3: ADEPT ---
# Fire Adept: Bronze skirmisher helm with pointed brow & runic flame cheekguards
HELMET_ADEPT_FIRE = [
    ".......AA.......",
    "......OAAO......",
    ".....OAGPAO.....",
    "....OAGPPPAO....",
    "...OAGPPPPPAO...",
    "..OAGPPPPPPAO...",
    "..OAPAAAAAAPAO..",
    "..OAP.C..C.PAO..",
    "..OAP.C..C.PAO..",
    "..OAPT....TPAO..",
    "..OAPTT..TTPAO..",
    "..OAPPPPPPPAO...",
    "...OSSSSSSSO....",
    "....OOOOOO......",
    "................",
    "................"
]

# Water Adept: Tidal warrior helm with curved whalebone crests & frost crystal brow
HELMET_ADEPT_WATER = [
    "...OO......OO...",
    "..OAAO....OAAO..",
    "..OAPAO..OAPAO..",
    "...OAPG..GPAO...",
    "...OAGPPPAAGO...",
    "..OAGPTTTPGAO...",
    "..OAPTTTTTPAO...",
    "..OAP.C..C.PAO..",
    "..OAP.C..C.PAO..",
    "..OAP......PAO..",
    "..OAPPO..OPPAO..",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Earth Adept: Terra infantry battle cap with jade horn studs & angled earflaps
HELMET_ADEPT_EARTH = [
    "......OOOO......",
    "....OOTTTTOO....",
    "...OAGPTTPGAO...",
    "..OAGPPPPPPGAO..",
    "..OAGPPTTPGAO...",
    "..OAGPAAAAPGAO..",
    "..OAP.C..C.PAO..",
    "..OAP.C..C.PAO..",
    "..OAP......PAO..",
    "..OAPPO..OPPAO..",
    "..OAPPPPPPPAO...",
    "...OSSSSSSSO....",
    "....OOOOOO......",
    "................",
    "................",
    "................"
]

# Air Adept: Aeromancer flight helm with swept-back glider winglets & crystal visor
HELMET_ADEPT_AIR = [
    "..OO........OO..",
    ".OAAO......OAAO.",
    ".OAPAO....OAPAO.",
    "..OAPGOO..GPAO..",
    "...OAGGGGGGAO...",
    "..OAGPVVVVPGAO..",
    "..OAPVVVVVVPAO..",
    "..OAPVVVVVVPAO..",
    "..OAP.C..C.PAO..",
    "..OAP......PAO..",
    "..OAPPO..OPPAO..",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# --- TIER 4: VETERAN WARRIOR ---
# Fire Veteran: Imperial Fire Army battle helm (pointed crest, neck curtain drape, crimson cheekplates)
HELMET_VET_FIRE = [
    ".......AA.......",
    "......OAAO......",
    ".....OAGPAO.....",
    "....OAGPPPAO....",
    "...OAGPPPPPAO...",
    "..OAGPPPPPPAO...",
    "..OAPPTTTTPPO...",
    "..OAP.C..C.PO...",
    "..OAP.C..C.PO...",
    "..OAPSSSSSSPO...",
    "..OAPSSSSSSPO...",
    "..OAPPTTTTPPO...",
    "..OAPPPPPPPPO...",
    "..OSSSSSSSSSO...",
    "...OOOOOOOOO....",
    "................"
]

# Water Veteran: Deep-sea warrior kabuto with sea-scale neck curtain & coral horn spikes
HELMET_VET_WATER = [
    "..OO........OO..",
    ".OAAO......OAAO.",
    ".OAPAO.OO.OAPAO.",
    "..OAPGOGGGPAO...",
    "..OAGPPPPPPGAO..",
    "..OAGPTTTPGAO...",
    "..OAPPTTTTPPO...",
    "..OAP.C..C.PO...",
    "..OAP.C..C.PO...",
    "..OAPTTTTTTPO...",
    "..OAPTTTTTTPO...",
    "..OAPPPPPPPPO...",
    "..OSSSSSSSSSO...",
    "...OOOOOOOOO....",
    "................",
    "................"
]

# Earth Veteran: Heavy infantry fortress helm with rectangular brow-guard & iron boulder ear-guards
HELMET_VET_EARTH = [
    ".....OOOOOO.....",
    "...OOAAAAAAOO...",
    "..OAGPPPPPPGAO..",
    "..OAGPTTTTPGAO..",
    ".OOAGPPPPPPGAOO.",
    ".OAPAAAAAAAAAPO.",
    ".OAP..C..C..APO.",
    ".OAP..C..C..APO.",
    ".OAPAAAAAAAAAPO.",
    ".OAP..OOOO..APO.",
    "..OAPPPPPPPAPO..",
    "..OAPPPPPPPAPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# Air Veteran: Sky Temple battle cowl with flowing prayer veil & meditation bead circlet
HELMET_VET_AIR = [
    "......OOOO......",
    "....OOGGGGOO....",
    "...OGGGGGGGGO...",
    "..OGGGGGGGGGGO..",
    "..OGAAAAAAAAAGGO",
    "..OGABBAABBAAGGO",
    "..OP..C..C..PPO.",
    "..OP..C..C..PPO.",
    "..OPAAAAAAAAAPO.",
    "..OPSSSSSSSSPO..",
    "..OPSSSSSSSSPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# --- TIER 5: GRAND MASTER ---
# Fire Master: Ornate Fire Lord officer helm with flared gilded winglets & glowing ruby visor
HELMET_MAS_FIRE = [
    ".OO..........OO.",
    ".OAAO......OAAO.",
    ".OAAPO....OPA AO",
    "..OAGPOOOPGAO...",
    "...OAGPTTPGAO...",
    "..OAGPTTTTPGAO..",
    "..OAPAAAAAAPAO..",
    "..OAP.C..C.PAO..",
    "..OAP.C..C.PAO..",
    "..OAP.VVVV.PAO..",
    "..OAPPPPPPPPAO..",
    "..OAPPTTTTPPAO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# Water Master: High Chieftain whale-spirit greathelm with curving pearl tusks & wave pauldrons
HELMET_MAS_WATER = [
    "...OO......OO...",
    "..OAAO....OAAO..",
    "..OAPAO..OAPAO..",
    "..OAPAO..OAPAO..",
    "..OAGPPPPPPGAO..",
    "..OAGPNTTNPGAAO.",
    "..OAPTTTTTTPPAO.",
    "..OAP.C..C.PAAO.",
    "..OAP.C..C.PAAO.",
    "..OAP......PAO..",
    "..OAPPPPPPPPAO..",
    "...OPPSSSSPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Earth Master: Earth Monarch royal guard helm with monolithic jade horns & fortress pauldrons
HELMET_MAS_EARTH = [
    ".OO..........OO.",
    ".OAAO......OAAO.",
    ".OAPAO....OAPAO.",
    "..OAPAO..OAPAO..",
    "..OAGPPPPPPGAO..",
    "..OAGPTTTTPGAO..",
    "..OAPAAAAAAPAO..",
    "..OAP.C..C.PAO..",
    "..OAP.C..C.PAO..",
    "..OAPTTTTTTPAO..",
    "..OAPPPPPPPPAO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................"
]

# Air Master: High Monk spiritual cowl with floating nimbus ring & gilded cloud pauldrons
HELMET_MAS_AIR = [
    "......AAAA......",
    "....AA....AA....",
    "...AO.OOOO.OA...",
    "..AOGGGGGGGGOA..",
    "..AOGGTTTTGGOA..",
    "...OGGAAAA GGO...",
    "..OP..C..C..PO..",
    "..OP..C..C..PO..",
    "..OP...VV...PO..",
    "..OPPP....PPPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................"
]

# --- TIER 6: ASCENDED MYTHIC ---
# Fire Mythic: Mythic volcanic dragon helm with twin smoking horns & molten runic visor
HELMET_MYTH_FIRE = [
    ".OO..........OO.",
    ".OAAO......OAAO.",
    ".OAPAO....OAPAO.",
    "..OAPAO..OAPAO..",
    "...OAGPTTPGAO...",
    "..OAGPTTTTPGAO..",
    "..OAPTVVVVTPAO..",
    "..OAPTVVVVTPAO..",
    "..OAP.VVVV.PAO..",
    "..OAPTTTTTTPAO..",
    "..OAPPPPPPPPAO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................"
]

# Water Mythic: Mythic Leviathan crest tiara with dual water-serpent horns & glowing oceanic pearl
HELMET_MYTH_WATER = [
    "...OO......OO...",
    "..OTTO....OTTO..",
    "..OTAPO..OPATO..",
    "...OTAPGGNATO...",
    "...OAGPPPPAAGO..",
    "..OAGPPTTPPAAGO.",
    "..OPPPTTTTPPPPO.",
    "..OPP.C..C.PPPO.",
    "..OPP.C..C.PPPO.",
    "..OPP......PPPO.",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................"
]

# Earth Mythic: Mythic mountain titan helm with quadruple emerald horns & obsidian bastions
HELMET_MYTH_EARTH = [
    "OO..OO....OO..OO",
    "OAAOAAO..OAAOAAO",
    "OAPAAPAO.OAPAAPO",
    ".OAGPPPPAAPPPGO.",
    ".OAGPPTTTTPPGO..",
    ".OAGPPAAAAPPGO..",
    "..OPP.C..C.PPO..",
    "..OPP.C..C.PPO..",
    "..OPPTTTTTTPPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
    "................"
]

# Air Mythic: Mythic celestial sky crown with quadruple wind plumage & glowing Avatar forehead arrow
HELMET_MYTH_AIR = [
    "..OO........OO..",
    ".OTTO......OTTO.",
    ".OTAPO.OO.OPATO.",
    "..OAGPPTTPGAO...",
    "..OAGPTVVTGAO...",
    "..OAGPVVVVPGAO..",
    "..OPP..VV..PPO..",
    "..OPP.C..C.PPO..",
    "..OPP.C..C.PPO..",
    "..OPPTTTTTTPPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................"
]

# --- TIER 7: LEGENDARY SOVEREIGN ---
# Fire Sovereign: Grand Golden Dragon Horn Crown, Dragon-Maw Warplate, Dragon Claws
HELMET_SOV_FIRE = [
    ".OO..........OO.",
    ".OAG........GAO.",
    ".OAPG......GPAO.",
    "..OAPG.OO.GPAO..",
    "...OAPGOOGPAO...",
    "..OOOAPTTPAOOO..",
    ".OAGPPTTTTPGAO..",
    ".OAPPTAAAAATPPO.",
    ".OAPPOOOOOOPPAO.",
    ".OAPPO.OO.OPPAO.",
    "..OPP......PPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# Water Sovereign: Ocean Spirit Tiara & Moon Pearl, Leviathan Manta Mantle
HELMET_SOV_WATER = [
    "...OO......OO...",
    "..OTTO....OTTO..",
    "..OTAGO..OGATO..",
    "...OTAPGGNATO...",
    "...OAGPPPPAAGO..",
    "..OAGPPTTPPAAGO.",
    "..OPPPTTTTPPPPO.",
    "..OPPPAAAAPPPO..",
    "..OPPOOOOOOPPO..",
    "..OP..OOOO..PO..",
    "..OPP......PPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# Earth Sovereign: Titan Bedrock Mountain Horns, Fortress Bastion
HELMET_SOV_EARTH = [
    ".OOOO......OOOO.",
    ".OGAPO....OPAGO.",
    ".OGAPO.OO.OPAGO.",
    "..OGAPOAAOPAGO..",
    "..OGAPPTTPAPGO..",
    "..OGPPTTTTPPGO..",
    ".OGPPPAAAAPPPGO.",
    ".OGPPOOOOOOPPGO.",
    ".OPPO..OO..OPPO.",
    ".OPPO..OO..OPPO.",
    "..OPP......PPO..",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# Air Sovereign: Celestial Cloud Nimbus with glowing cyan Avatar arrow
HELMET_SOV_AIR = [
    "...OO......OO...",
    "..OTTO.OO.OTTO..",
    ".OTTAPOAAOPATTO.",
    ".OTAGPPTTPPAATO.",
    "..OAGPPTTTPAAGO.",
    "..OGPPTTTTPPPGO.",
    "..OPP..VV..PPPO.",
    "..OPP..VV..PPPO.",
    "..OPP...V...PPO.",
    "..OPP...V...PPO.",
    "..OPP..VV..PPPO.",
    "..OPPPPPPPPPPO..",
    "...OSSSSSSSSO...",
    "....OOOOOOOO....",
    "................",
    "................"
]

# ==============================================================================
# 2. PIXEL TEMPLATES: CHESTPLATES (Evolving Pauldrons & Cuirass)
# ==============================================================================

# Initiate: Soft cloth tunic with rope belt, draped cloth shoulders
CHEST_INITIATE = [
    "................",
    "...OO......OO...",
    "..OGGO....OGGO..",
    ".OGGGGO..OGGGGO.",
    ".OGGGGGGGGGGGGO.",
    ".OGGGGGGGGGGGGO.",
    ".OGGGGGGGGGGGGO.",
    "..OGGGGGGGGGGO..",
    "..OGGGGGGGGGGO..",
    "..OGGGOOOOGGGO..",
    "...OGGTTTTGGO...",
    "...OGGGGGGGGO...",
    "....OGGGGGGO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Apprentice: Quilted scout vest with shoulder guards & nation trims
CHEST_APPRENTICE = [
    "................",
    "..OOO......OOO..",
    ".OAGGO....OGGAO.",
    ".OAGPPO..OPPGAO.",
    "OAGGGGGGGGGGGAO.",
    "OAGGPPTTTPPGGAO.",
    ".OPPPTTTTTTPPO..",
    "..OPPPPPPPPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPTTTTPPO...",
    "...OPPTTTTPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Adept: Studded adventurer vest with metal pectoral plates & shoulder studs
CHEST_ADEPT = [
    "................",
    "..OOO......OOO..",
    ".OAGGO....OGGAO.",
    ".OAGPPO..OPPGAO.",
    "OAGPPPPPPPPPPGAO",
    "OAGPPPAAAAPPGAO.",
    ".OPPPAAAAAAPPPO.",
    "..OPPPPPPPPPPO..",
    "..OPPPPPPPPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Veteran: Imperial segmented warplate, solid steel breastplate & layered pauldrons
CHEST_VETERAN = [
    "................",
    ".OOOO......OOOO.",
    "OAGGGO....OGGGAO",
    "OAGGPPO..OPPGGAO",
    "OAGPPPPPPPPPPGAO",
    ".OAGPPTTTPPGGAO.",
    "..OPPTTTTTTAPPO.",
    "..OPPAAAAAAPPO..",
    "..OPPPPPPPPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPTTTTPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Master: Knightly plated cuirass with ornate wide pauldrons & flowing tabard
CHEST_MASTER = [
    "................",
    ".OOOO......OOOO.",
    "OAGGGO....OGGGAO",
    "OAGGPPO..OPPGGAO",
    "OAGPPPPPPPPPPGAO",
    ".OAGPPAAAAPPGAO.",
    "..OPPAAAAAAPPO..",
    "..OPPPTTTTPPPO..",
    "..OPPPPPPPPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Mythic: Netherite warplate infused with glowing elemental veins & spikes
CHEST_MYTHIC = [
    "................",
    ".OOOO......OOOO.",
    "OTAGGO....OGGATO",
    "OTAGPPO..OPPGATO",
    "OTAGPPPPPPPPGATO",
    ".OAGPTTTTTTPGAO.",
    "..OPPTTVVTTPPO..",
    "..OPPTTVVTTPPO..",
    "..OPPTTTTTTPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPTTTTPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Sovereign Fire: Dragon-Maw Warplate
CHEST_SOV_FIRE = [
    ".OO..........OO.",
    ".OAGO......OGAO.",
    "OAGPPO....OPPGAO",
    "OAGPPPO..OPPPGAO",
    "OAGPPPPPPPPPPGAO",
    ".OAGPPAATTAPGAO.",
    ".OAPPTAAAAATPPO.",
    "..OPPTTAATTAPPO.",
    "..OPPPAAAAPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Sovereign Water: Leviathan Manta Mantle
CHEST_SOV_WATER = [
    "................",
    ".OOO........OOO.",
    "OAGGO......OGGAO",
    "OTAGPPO..OPPGATO",
    "OTAGPPPPPPPPGATO",
    ".OTAGPAAAAPGATO.",
    "..OTPAATTTAPPO..",
    "..OPPAATTTAPPO..",
    "..OPPPAAAAPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Sovereign Earth: Titan Fortress Bastion
CHEST_SOV_EARTH = [
    "................",
    "OOOO........OOOO",
    "OAGAPO....OPAGAO",
    "OAGAPPO..OPPAGAO",
    "OAGAPPPPPPPPAGAO",
    ".OAGPPAAAAPPGAO.",
    "..OPPAAAAAAPPO..",
    "..OPPPAATTAPPO..",
    "..OPPPAATTAPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# Sovereign Air: Winged Zephyr Mantle
CHEST_SOV_AIR = [
    "................",
    ".OO..........OO.",
    ".OTTO......OTTO.",
    ".OTAPPO..OPPAT..",
    "OTAGPPPPPPPPGATO",
    ".OTAGPAAAAPGATO.",
    "..OTPAATTTAPTO..",
    "..OPPAATTTAPPO..",
    "..OPPPTTTTPPPO..",
    "..OPPPOOOOPPPO..",
    "...OPPSSSSPPO...",
    "...OPPPPPPPPO...",
    "....OSSSSSSO....",
    ".....OOOOOO.....",
    "................",
    "................"
]

# ==============================================================================
# 3. PIXEL TEMPLATES: LEGGINGS (Evolving Trousers & Plated Greaves)
# ==============================================================================

# Initiate: Loose cloth monk trousers with soft knee folds
LEGS_INITIATE = [
    "................",
    "..OOOOOOOOOOOO..",
    ".OGGGGGGGGGGGGO.",
    ".OGGGOOOOOOGGGO.",
    ".OGGG.OOOO.GGGO.",
    ".OGGG......GGGO.",
    ".OGGG......GGGO.",
    ".OGGG......GGGO.",
    ".OGTT......TTGO.",
    ".OGGG......GGGO.",
    ".OGGG......GGGO.",
    ".OGGG......GGGO.",
    "..OGO......OGO..",
    "..OOO......OOO..",
    "................",
    "................"
]

# Apprentice: Fitted travel pants with leather knee wraps & straps
LEGS_APPRENTICE = [
    "................",
    "..OOOOOOOOOOOO..",
    ".OAGGGGGGGGGGAO.",
    ".OAGPPOOOOPPGAO.",
    ".OAGP.OOOO.PGAO.",
    ".OPPP......PPPO.",
    ".OPPP......PPPO.",
    ".OPAA......AAPO.",
    ".OPTT......TTPO.",
    ".OPPP......PPPO.",
    ".OPPP......PPPO.",
    ".OPSS......SSPO.",
    "..OOO......OOO..",
    "................",
    "................",
    "................"
]

# Adept: Reinforced combat pants with leather thigh guards & metal knee caps
LEGS_ADEPT = [
    "................",
    "..OOOOOOOOOOOO..",
    ".OAGGPPPPPPGGAO.",
    ".OAGPPOOOOPPGAO.",
    ".OAGP.OOOO.PGAO.",
    ".OPPP......PPPO.",
    ".OPPP......PPPO.",
    ".OPPP......PPPO.",
    ".OPAA......AAPO.",
    ".OPPP......PPPO.",
    ".OPPP......PPPO.",
    ".OPSS......SSPO.",
    "..OOO......OOO..",
    "................",
    "................",
    "................"
]

# Veteran: Heavy plate-reinforced soldier greaves with articulated thigh lames
LEGS_VETERAN = [
    "................",
    ".OOOOOOOOOOOOOO.",
    "OAGGPPPPPPPPGGAO",
    "OAGPPOOOOOOPPGAO",
    "OAGPP.OOOO.PPGAO",
    "OPPPP......PPPPO",
    "OPPTT......TTPPO",
    "OPPAA......AAPPO",
    "OPPAA......AAPPO",
    "OPPPP......PPPPO",
    "OPPSS......SSPPO",
    "OPPSS......SSPPO",
    ".OOOO......OOOO.",
    "................",
    "................",
    "................"
]

# Master: Knightly plated greaves with gilded engravings & gem knee guards
LEGS_MASTER = [
    "................",
    ".OOOOOOOOOOOOOO.",
    "OAGGPPPPPPPPGGAO",
    "OAGPPOOOOOOPPGAO",
    "OAGPP.OOOO.PPGAO",
    "OPPPP......PPPPO",
    "OPPPP......PPPPO",
    "OPPAA......AAPPO",
    "OPPAA......AAPPO",
    "OPPPP......PPPPO",
    "OPPSS......SSPPO",
    "OPPSS......SSPPO",
    ".OOOO......OOOO.",
    "................",
    "................",
    "................"
]

# Mythic: Netherite runed greaves with glowing elemental channels
LEGS_MYTHIC = [
    "................",
    "OOOOOOOOOOOOOOOO",
    "OAGPPTTTTTTPGGAO",
    "OAGPPOOOOOOPPGAO",
    "OAPPP.OOOO.PPPAO",
    "OAPTT......TTPAO",
    "OAPVV......VVPAO",
    "OAPTT......TTPAO",
    "OAPAA......AAPAO",
    "OAPPP......PPPAO",
    "OAPSS......SSPAO",
    "OAPSS......SSPAO",
    ".OOOO......OOOO.",
    "................",
    "................",
    "................"
]

# Sovereign: Sovereign Ornate Greaves (elemental side ridges, glowing knee emblems)
LEGS_SOVEREIGN = [
    "................",
    "OOOOOOOOOOOOOOOO",
    "OAGPPAATTAPPGGAO",
    "OAGPPOOOOOOPPGAO",
    "OAPPP.OOOO.PPPAO",
    "OAPPP......PPPAO",
    "OAPAA......AAPAO",
    "OAPTT......TTPAO",
    "OAPTT......TTPAO",
    "OAPPP......PPPAO",
    "OAPSS......SSPAO",
    "OAPSS......SSPAO",
    ".OOOO......OOOO.",
    "................",
    "................",
    "................"
]

# ==============================================================================
# 4. PIXEL TEMPLATES: BOOTS (Evolving Footwear)
# ==============================================================================

# Initiate: Soft cloth wraps / simple monk sandals
BOOTS_INITIATE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOO......OOO..",
    ".OGGGO....OGGGO.",
    ".OGGGO....OGGGO.",
    ".OGGGO....OGGGO.",
    ".OGGGGO..OGGGGO.",
    "OGGGGGGOOGGGGGGO",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Apprentice: Leather travel boots with copper buckle & calf wrap
BOOTS_APPRENTICE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOOO....OOOO..",
    ".OAGGO....OGGAO.",
    ".OAGGO....OGGAO.",
    ".OASSO....OSSAO.",
    ".OAPPO....OPPAO.",
    ".OAPPPPO.OPPPPAO",
    "OAGGGGGGOOGGGGGG",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Adept: Adventurer combat boots with metal toe caps & ankle straps
BOOTS_ADEPT = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOOO....OOOO..",
    ".OAPPO....OPPAO.",
    ".OAPPO....OPPAO.",
    ".OASSO....OSSAO.",
    ".OAPPO....OPPAO.",
    ".OAPPPPO.OPPPPAO",
    "OAPPPPPGAAPPPPPG",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Veteran: Segmented iron sabatons with armored shin guards
BOOTS_VETERAN = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOOO....OOOO..",
    ".OAPPPO..OPPPAO.",
    ".OAPPPO..OPPPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPPPO..OPPPAO.",
    ".OAPPPPOOPPPPAO.",
    "OAPPPPPGAAPPPPPG",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Master: Knightly plated sabatons with gilded ankle shields
BOOTS_MASTER = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOOO....OOOO..",
    ".OAPPPO..OPPPAO.",
    ".OAPPPO..OPPPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPPPO..OPPPAO.",
    ".OAPPPPOOPPPPAO.",
    "OAPPPPPGAAPPPPPG",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Mythic: Netherite warboots with runed elemental spurs & glowing soles
BOOTS_MYTHIC = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OO........OO..",
    ".OAAO......OAAO.",
    ".OAPPO....OPPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPVPO..OPVPAO.",
    ".OAPTTPO.OPTPAO.",
    ".OAPPPPAAAPPPPAO",
    "OAPPPPAAAAPPPPAO",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Sovereign Fire: Dragon Claw Spiked Sabatons
BOOTS_SOV_FIRE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OO........OO..",
    ".OAAO......OAAO.",
    ".OAPPO....OPPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPPTPO.OPTPAO.",
    ".OAPPPPAAAPPPPAO",
    "OAPPPPAAAAPPPPAO",
    "OAAPAAOAOAAPAAOA",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Sovereign Water: Finned Tidal Boots
BOOTS_SOV_WATER = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".OO..........OO.",
    "OTTO........OTTO",
    ".OAPPO....OPPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPAPO..OPAPAO.",
    ".OAPPTPO.OPTPAO.",
    ".OAPPPPAAAPPPPAO",
    "OAPPPPAAAAPPPPAO",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Sovereign Earth: Titan Bedrock Stompers
BOOTS_SOV_EARTH = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "OOOO........OOOO",
    "OAPPO......OPPAO",
    "OAPPO......OPPAO",
    "OAPAPO....OPAPAO",
    "OAPAPO....OPAPAO",
    "OAPPAPOOOOAPPAPO",
    "OAPPPPPGAAPPPPPG",
    "OAPPPPPGAAPPPPPG",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# Sovereign Air: Hermes Winged Cloud Boots
BOOTS_SOV_AIR = [
    "................",
    "................",
    "................",
    "................",
    "OO............OO",
    "OTTO........OTTO",
    ".OTAPO....OPATO.",
    "..OAPPO..OPPAO..",
    "..OAPAPOOAPAPO..",
    "..OAPAPOOAPAPO..",
    "..OAPPTPOOPTPAO.",
    ".OAPPPPAAAPPPAO.",
    "OAPPPPPGAAPPPPPG",
    "OASSSSSSOASSSSSS",
    "OOOOOOOOOOOOOOOO",
    "................"
]

# ==============================================================================
# TEMPLATE SELECTOR
# ==============================================================================
def get_template(nation, tier, piece):
    if piece == "helmet":
        if tier == "initiate":
            return HELMET_INITIATE
        elif tier == "apprentice":
            if nation == "fire": return HELMET_APP_FIRE
            if nation == "water": return HELMET_APP_WATER
            if nation == "earth": return HELMET_APP_EARTH
            if nation == "air": return HELMET_APP_AIR
        elif tier == "adept":
            if nation == "fire": return HELMET_ADEPT_FIRE
            if nation == "water": return HELMET_ADEPT_WATER
            if nation == "earth": return HELMET_ADEPT_EARTH
            if nation == "air": return HELMET_ADEPT_AIR
        elif tier == "veteran":
            if nation == "fire": return HELMET_VET_FIRE
            if nation == "water": return HELMET_VET_WATER
            if nation == "earth": return HELMET_VET_EARTH
            if nation == "air": return HELMET_VET_AIR
        elif tier == "master":
            if nation == "fire": return HELMET_MAS_FIRE
            if nation == "water": return HELMET_MAS_WATER
            if nation == "earth": return HELMET_MAS_EARTH
            if nation == "air": return HELMET_MAS_AIR
        elif tier == "mythic":
            if nation == "fire": return HELMET_MYTH_FIRE
            if nation == "water": return HELMET_MYTH_WATER
            if nation == "earth": return HELMET_MYTH_EARTH
            if nation == "air": return HELMET_MYTH_AIR
        elif tier == "sovereign":
            if nation == "fire": return HELMET_SOV_FIRE
            if nation == "water": return HELMET_SOV_WATER
            if nation == "earth": return HELMET_SOV_EARTH
            if nation == "air": return HELMET_SOV_AIR

    elif piece == "chestplate":
        if tier == "initiate": return CHEST_INITIATE
        elif tier == "apprentice": return CHEST_APPRENTICE
        elif tier == "adept": return CHEST_ADEPT
        elif tier == "veteran": return CHEST_VETERAN
        elif tier == "master": return CHEST_MASTER
        elif tier == "mythic": return CHEST_MYTHIC
        elif tier == "sovereign":
            if nation == "fire": return CHEST_SOV_FIRE
            if nation == "water": return CHEST_SOV_WATER
            if nation == "earth": return CHEST_SOV_EARTH
            if nation == "air": return CHEST_SOV_AIR

    elif piece == "leggings":
        if tier == "initiate": return LEGS_INITIATE
        elif tier == "apprentice": return LEGS_APPRENTICE
        elif tier == "adept": return LEGS_ADEPT
        elif tier == "veteran": return LEGS_VETERAN
        elif tier == "master": return LEGS_MASTER
        elif tier == "mythic": return LEGS_MYTHIC
        elif tier == "sovereign": return LEGS_SOVEREIGN

    elif piece == "boots":
        if tier == "initiate": return BOOTS_INITIATE
        elif tier == "apprentice": return BOOTS_APPRENTICE
        elif tier == "adept": return BOOTS_ADEPT
        elif tier == "veteran": return BOOTS_VETERAN
        elif tier == "master": return BOOTS_MASTER
        elif tier == "mythic": return BOOTS_MYTHIC
        elif tier == "sovereign":
            if nation == "fire": return BOOTS_SOV_FIRE
            if nation == "water": return BOOTS_SOV_WATER
            if nation == "earth": return BOOTS_SOV_EARTH
            if nation == "air": return BOOTS_SOV_AIR

    return HELMET_INITIATE

def render_item(template, pal):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    pixels = img.load()

    color_map = {
        "O": pal["outline"],
        "S": pal["shadow"],
        "P": pal["primary"],
        "G": pal["primary"],
        "A": pal["accent"],
        "M": pal["glint"],
        "T": pal["trim"],
        "N": (255, 255, 255, 255),
        "B": pal.get("secondary", pal["primary"]),
        "C": pal.get("visor", (20, 20, 20, 255)),
        "V": pal.get("glow", (255, 255, 255, 255))
    }

    for y in range(16):
        row = template[y]
        for x in range(16):
            ch = row[x]
            if ch != ".":
                pixels[x, y] = color_map.get(ch, pal["primary"])
    return img

def create_equipment_layers(nation, pal):
    layer1 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    layer2 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(layer1)
    d2 = ImageDraw.Draw(layer2)

    c_prim = pal["primary"]
    c_sec = pal["secondary"]
    c_acc = pal["accent"]

    # Layer 1: Helmet & Chestplate
    d1.rectangle([(0, 0), (31, 15)], fill=c_prim)
    d1.rectangle([(4, 4), (12, 12)], fill=c_sec)
    d1.rectangle([(16, 16), (39, 31)], fill=c_prim)
    d1.rectangle([(20, 20), (36, 28)], fill=c_acc)
    d1.rectangle([(40, 16), (55, 31)], fill=c_sec)
    d1.rectangle([(0, 16), (15, 31)], fill=c_prim)

    # Layer 2: Leggings
    d2.rectangle([(0, 0), (15, 15)], fill=c_prim)
    d2.rectangle([(16, 16), (39, 31)], fill=c_prim)
    d2.rectangle([(22, 18), (34, 28)], fill=c_sec)
    d2.rectangle([(0, 16), (15, 31)], fill=c_prim)
    d2.rectangle([(40, 16), (55, 31)], fill=c_acc)

    return layer1, layer2

def main():
    print("Generating 7-Tier Avatar Armor textures for Minecraft 1.21.1...")
    count = 0
    for nat in NATIONS:
        for t in TIERS:
            pal = PALETTES[(nat, t)]
            for p in PIECES:
                tpl = get_template(nat, t, p)
                img = render_item(tpl, pal)
                filename = f"{nat}_{t}_{p}.png"
                img.save(os.path.join(ITEM_TEX_DIR, filename), "PNG")
                count += 1

                # Legacy aliases for compatibility
                if t == "initiate":
                    img.save(os.path.join(ITEM_TEX_DIR, f"{nat}_basic_{p}.png"), "PNG")
                elif t == "sovereign":
                    img.save(os.path.join(ITEM_TEX_DIR, f"{nat}_legendary_{p}.png"), "PNG")
                    img.save(os.path.join(ITEM_TEX_DIR, f"{nat}_{p}.png"), "PNG")
                    nation_full = {"fire": "fire_nation", "water": "water_tribe", "earth": "earth_kingdom", "air": "air_nomad"}[nat]
                    img.save(os.path.join(ITEM_TEX_DIR, f"{nation_full}_{p}.png"), "PNG")

        # Entity Equipment Textures (from Sovereign tier)
        sov_pal = PALETTES[(nat, "sovereign")]
        l1, l2 = create_equipment_layers(nat, sov_pal)
        l1.save(os.path.join(ENTITY_EQUIP_DIR, f"{nat}_layer_1.png"), "PNG")
        l2.save(os.path.join(ENTITY_EQUIP_DIR, f"{nat}_layer_2.png"), "PNG")

    print(f"Successfully generated {count} textures and entity equipment layers.")

if __name__ == "__main__":
    main()
