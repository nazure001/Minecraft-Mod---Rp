import os
import json
from PIL import Image, ImageDraw

out_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. TEXTURE GENERATION
# -------------------------------------------------------------

# A. Earth Boulder Texture (32x32)
# Palettes: Stone strata, slate core, mossy fissures, jade crystal
boulder_tex = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
b_pix = boulder_tex.load()

# (0, 0) - (16, 16): Primary stone & granite strata
for y in range(0, 16):
    for x in range(0, 16):
        noise = (x * 7 + y * 13 + (x ^ y)) % 7
        if noise == 0:
            c = (55, 52, 49, 255) # deep slate shadow
        elif noise in (1, 2):
            c = (86, 81, 75, 255) # dark stone
        elif noise in (3, 4):
            c = (122, 116, 108, 255) # midtone stone
        elif noise == 5:
            c = (158, 151, 142, 255) # sunlit stone highlight
        else:
            c = (70, 85, 60, 255) # earthen moss patch
        b_pix[x, y] = c

# (16, 0) - (32, 16): Chiseled rock bevels & dark fracture seams
for y in range(0, 16):
    for x in range(16, 32):
        seam = (x + y * 3) % 5
        if seam == 0:
            c = (38, 35, 33, 255) # fracture crack
        elif seam in (1, 2):
            c = (99, 93, 87, 255) # bevel mid
        else:
            c = (140, 133, 124, 255) # bevel edge highlight
        b_pix[x, y] = c

# (0, 16) - (16, 32): Earthen bedrock & dirt rim
for y in range(16, 32):
    for x in range(0, 16):
        dirt = (x * 5 + y * 11) % 4
        if dirt == 0:
            c = (78, 54, 38, 255) # loam dark
        elif dirt == 1:
            c = (107, 76, 54, 255) # earth mid
        elif dirt == 2:
            c = (135, 98, 70, 255) # clay light
        else:
            c = (60, 42, 30, 255) # root shadow
        b_pix[x, y] = c

# (16, 16) - (32, 32): Earth Kingdom jade crystal inclusion
for y in range(16, 32):
    for x in range(16, 32):
        dist = abs(x - 24) + abs(y - 24)
        if dist <= 2:
            b_pix[x, y] = (140, 235, 170, 255) # jade inner glint
        elif dist <= 5:
            b_pix[x, y] = (50, 170, 95, 255) # rich jade green
        else:
            b_pix[x, y] = (30, 110, 60, 255) # deep jade shadow

boulder_tex_path = os.path.join(out_dir, "earth_boulder.png")
boulder_tex.save(boulder_tex_path, "PNG")
print("Generated Earth Boulder texture:", boulder_tex_path)


# B. Water Whip Texture (32x32)
water_tex = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
w_pix = water_tex.load()

# Flowing water gradient with translucency
for y in range(0, 32):
    for x in range(0, 32):
        wave = (x * 4 + y * 2 + (x * y) % 5) % 8
        if wave == 0:
            w_pix[x, y] = (255, 255, 255, 230) # crest foam
        elif wave in (1, 2):
            w_pix[x, y] = (120, 220, 255, 210) # light aqua surface
        elif wave in (3, 4, 5):
            w_pix[x, y] = (40, 150, 230, 195) # vibrant stream
        else:
            w_pix[x, y] = (15, 80, 180, 220) # deep core water

water_tex_path = os.path.join(out_dir, "water_whip.png")
water_tex.save(water_tex_path, "PNG")
print("Generated Water Whip texture:", water_tex_path)


# C. Avatar Relic 3D Texture (32x32)
relic_tex = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
r_pix = relic_tex.load()

# (0, 0) - (16, 16): Ornate Antique Gold Framework
for y in range(0, 16):
    for x in range(0, 16):
        rim = (x + y) % 4
        if rim == 0:
            r_pix[x, y] = (150, 110, 30, 255) # gold shadow
        elif rim in (1, 2):
            r_pix[x, y] = (220, 175, 55, 255) # polished gold
        else:
            r_pix[x, y] = (255, 235, 130, 255) # gold highlight

# (16, 0) - (32, 16): Four Nations Gems
# Top-left: Fire (Red), Top-right: Water (Blue), Bottom-left: Earth (Green), Bottom-right: Air (White/Gold)
for y in range(0, 8):
    for x in range(16, 24):
        r_pix[x, y] = (235, 50, 40, 255) # Fire ruby
for y in range(0, 8):
    for x in range(24, 32):
        r_pix[x, y] = (40, 140, 245, 255) # Water sapphire
for y in range(8, 16):
    for x in range(16, 24):
        r_pix[x, y] = (50, 200, 90, 255) # Earth emerald
for y in range(8, 16):
    for x in range(24, 32):
        r_pix[x, y] = (240, 230, 190, 255) # Air topaz

# (0, 16) - (32, 32): Glowing Chi Energy Core
for y in range(16, 32):
    for x in range(0, 32):
        d = ((x - 16)**2 + (y - 24)**2)**0.5
        if d <= 3:
            r_pix[x, y] = (255, 255, 255, 255) # pure energy white
        elif d <= 7:
            r_pix[x, y] = (160, 240, 255, 240) # cyan chi glow
        elif d <= 11:
            r_pix[x, y] = (80, 170, 255, 200) # deep chi blue
        else:
            r_pix[x, y] = (40, 60, 110, 180) # outer aura edge

relic_tex_path = os.path.join(out_dir, "avatar_relic_3d.png")
relic_tex.save(relic_tex_path, "PNG")
print("Generated Avatar Relic 3D texture:", relic_tex_path)


# -------------------------------------------------------------
# 2. JAVA 1.21.1 JSON MODELS
# -------------------------------------------------------------

# Model 1: Earth Boulder
earth_boulder_model = {
    "credit": "Avatar Elemental Skills - Earth Boulder (Minecraft 1.21.1)",
    "texture_size": [32, 32],
    "textures": {
        "0": "avatar_skills:item/earth_boulder",
        "particle": "avatar_skills:item/earth_boulder"
    },
    "elements": [
        # Central monolith core
        {
            "name": "core_boulder",
            "from": [3.0, 3.0, 3.0],
            "to": [13.0, 13.0, 13.0],
            "faces": {
                "north": {"uv": [0, 0, 10, 10], "texture": "#0"},
                "east":  {"uv": [0, 0, 10, 10], "texture": "#0"},
                "south": {"uv": [0, 0, 10, 10], "texture": "#0"},
                "west":  {"uv": [0, 0, 10, 10], "texture": "#0"},
                "up":    {"uv": [0, 0, 10, 10], "texture": "#0"},
                "down":  {"uv": [0, 0, 10, 10], "texture": "#0"}
            }
        },
        # Top stepped facet
        {
            "name": "top_crag",
            "from": [5.0, 13.0, 4.0],
            "to": [11.0, 16.0, 12.0],
            "faces": {
                "north": {"uv": [16, 0, 22, 3], "texture": "#0"},
                "east":  {"uv": [16, 0, 24, 3], "texture": "#0"},
                "south": {"uv": [16, 0, 22, 3], "texture": "#0"},
                "west":  {"uv": [16, 0, 24, 3], "texture": "#0"},
                "up":    {"uv": [16, 0, 22, 8], "texture": "#0"},
                "down":  {"uv": [16, 0, 22, 8], "texture": "#0"}
            }
        },
        # Bottom anchor wedge
        {
            "name": "bottom_wedge",
            "from": [4.0, 0.0, 5.0],
            "to": [12.0, 3.0, 11.0],
            "faces": {
                "north": {"uv": [0, 16, 8, 19], "texture": "#0"},
                "east":  {"uv": [0, 16, 6, 19], "texture": "#0"},
                "south": {"uv": [0, 16, 8, 19], "texture": "#0"},
                "west":  {"uv": [0, 16, 6, 19], "texture": "#0"},
                "up":    {"uv": [0, 16, 8, 22], "texture": "#0"},
                "down":  {"uv": [0, 16, 8, 22], "texture": "#0"}
            }
        },
        # Right jagged protrusion
        {
            "name": "right_shear",
            "from": [13.0, 5.0, 4.0],
            "to": [15.5, 11.0, 12.0],
            "rotation": {"origin": [13.0, 8.0, 8.0], "axis": "z", "angle": -22.5},
            "faces": {
                "north": {"uv": [16, 0, 19, 6], "texture": "#0"},
                "east":  {"uv": [16, 0, 24, 6], "texture": "#0"},
                "south": {"uv": [16, 0, 19, 6], "texture": "#0"},
                "west":  {"uv": [16, 0, 24, 6], "texture": "#0"},
                "up":    {"uv": [16, 0, 19, 8], "texture": "#0"},
                "down":  {"uv": [16, 0, 19, 8], "texture": "#0"}
            }
        },
        # Left jade crystal vein
        {
            "name": "jade_vein",
            "from": [1.0, 4.0, 5.0],
            "to": [3.0, 12.0, 11.0],
            "rotation": {"origin": [3.0, 8.0, 8.0], "axis": "y", "angle": 22.5},
            "faces": {
                "north": {"uv": [16, 16, 18, 24], "texture": "#0"},
                "east":  {"uv": [16, 16, 22, 24], "texture": "#0"},
                "south": {"uv": [16, 16, 18, 24], "texture": "#0"},
                "west":  {"uv": [16, 16, 22, 24], "texture": "#0"},
                "up":    {"uv": [16, 16, 18, 22], "texture": "#0"},
                "down":  {"uv": [16, 16, 18, 22], "texture": "#0"}
            }
        }
    ],
    "display": {
        "thirdperson_righthand": {
            "rotation": [45, 0, 0],
            "translation": [0, 3, -1],
            "scale": [0.65, 0.65, 0.65]
        },
        "firstperson_righthand": {
            "rotation": [15, 30, -5],
            "translation": [2.5, 4.0, 1.0],
            "scale": [0.75, 0.75, 0.75]
        },
        "gui": {
            "rotation": [30, 225, 0],
            "translation": [0, 0, 0],
            "scale": [0.75, 0.75, 0.75]
        },
        "ground": {
            "rotation": [0, 0, 0],
            "translation": [0, 2, 0],
            "scale": [0.6, 0.6, 0.6]
        },
        "fixed": {
            "rotation": [0, 0, 0],
            "translation": [0, 0, 0],
            "scale": [0.8, 0.8, 0.8]
        }
    }
}

boulder_json_path = os.path.join(out_dir, "earth_boulder.json")
with open(boulder_json_path, "w", encoding="utf-8") as f:
    json.dump(earth_boulder_model, f, indent=2)
print("Generated Earth Boulder JSON model:", boulder_json_path)


# Model 2: Water Whip
water_whip_model = {
    "credit": "Avatar Elemental Skills - Water Whip Tendril (Minecraft 1.21.1)",
    "texture_size": [32, 32],
    "textures": {
        "0": "avatar_skills:item/water_whip",
        "particle": "avatar_skills:item/water_whip"
    },
    "elements": [
        # Segment 1: Grip node
        {
            "name": "water_grip",
            "from": [7.0, 0.0, 7.0],
            "to": [9.0, 5.0, 9.0],
            "faces": {
                "north": {"uv": [0, 0, 2, 5], "texture": "#0"},
                "east":  {"uv": [0, 0, 2, 5], "texture": "#0"},
                "south": {"uv": [0, 0, 2, 5], "texture": "#0"},
                "west":  {"uv": [0, 0, 2, 5], "texture": "#0"},
                "up":    {"uv": [0, 0, 2, 2], "texture": "#0"},
                "down":  {"uv": [0, 0, 2, 2], "texture": "#0"}
            }
        },
        # Segment 2: Rising arc
        {
            "name": "water_arc_1",
            "from": [6.5, 4.5, 6.0],
            "to": [9.5, 10.5, 9.0],
            "rotation": {"origin": [8.0, 5.0, 8.0], "axis": "x", "angle": -22.5},
            "faces": {
                "north": {"uv": [2, 0, 5, 6], "texture": "#0"},
                "east":  {"uv": [2, 0, 5, 6], "texture": "#0"},
                "south": {"uv": [2, 0, 5, 6], "texture": "#0"},
                "west":  {"uv": [2, 0, 5, 6], "texture": "#0"},
                "up":    {"uv": [2, 0, 5, 3], "texture": "#0"},
                "down":  {"uv": [2, 0, 5, 3], "texture": "#0"}
            }
        },
        # Segment 3: Crest whip strike
        {
            "name": "water_crest",
            "from": [6.0, 9.0, 3.0],
            "to": [10.0, 14.0, 7.0],
            "rotation": {"origin": [8.0, 10.0, 5.0], "axis": "x", "angle": -45.0},
            "faces": {
                "north": {"uv": [6, 0, 10, 5], "texture": "#0"},
                "east":  {"uv": [6, 0, 10, 5], "texture": "#0"},
                "south": {"uv": [6, 0, 10, 5], "texture": "#0"},
                "west":  {"uv": [6, 0, 10, 5], "texture": "#0"},
                "up":    {"uv": [6, 0, 10, 4], "texture": "#0"},
                "down":  {"uv": [6, 0, 10, 4], "texture": "#0"}
            }
        },
        # Segment 4: Fluid tip lashing forward
        {
            "name": "water_tip",
            "from": [7.0, 11.0, -3.0],
            "to": [9.0, 13.0, 4.0],
            "rotation": {"origin": [8.0, 12.0, 1.0], "axis": "y", "angle": 22.5},
            "faces": {
                "north": {"uv": [10, 0, 12, 2], "texture": "#0"},
                "east":  {"uv": [10, 0, 17, 2], "texture": "#0"},
                "south": {"uv": [10, 0, 12, 2], "texture": "#0"},
                "west":  {"uv": [10, 0, 17, 2], "texture": "#0"},
                "up":    {"uv": [10, 0, 12, 7], "texture": "#0"},
                "down":  {"uv": [10, 0, 12, 7], "texture": "#0"}
            }
        },
        # Swirling droplet ring
        {
            "name": "splash_droplet",
            "from": [4.0, 8.0, 6.0],
            "to": [6.0, 10.0, 8.0],
            "faces": {
                "north": {"uv": [0, 8, 2, 10], "texture": "#0"},
                "east":  {"uv": [0, 8, 2, 10], "texture": "#0"},
                "south": {"uv": [0, 8, 2, 10], "texture": "#0"},
                "west":  {"uv": [0, 8, 2, 10], "texture": "#0"},
                "up":    {"uv": [0, 8, 2, 10], "texture": "#0"},
                "down":  {"uv": [0, 8, 2, 10], "texture": "#0"}
            }
        }
    ],
    "display": {
        "thirdperson_righthand": {
            "rotation": [60, -45, 0],
            "translation": [0, 4, 3],
            "scale": [0.85, 0.85, 0.85]
        },
        "firstperson_righthand": {
            "rotation": [10, -20, 10],
            "translation": [1.5, 3.5, -2.0],
            "scale": [0.9, 0.9, 0.9]
        },
        "gui": {
            "rotation": [25, 135, 0],
            "translation": [0, 1, 0],
            "scale": [0.8, 0.8, 0.8]
        }
    }
}

water_whip_json_path = os.path.join(out_dir, "water_whip.json")
with open(water_whip_json_path, "w", encoding="utf-8") as f:
    json.dump(water_whip_model, f, indent=2)
print("Generated Water Whip JSON model:", water_whip_json_path)


# Model 3: Avatar Relic 3D Catalyst
avatar_relic_3d_model = {
    "credit": "Avatar Elemental Skills - 3D Relic Catalyst (Minecraft 1.21.1)",
    "texture_size": [32, 32],
    "textures": {
        "0": "avatar_skills:item/avatar_relic_3d",
        "particle": "avatar_skills:item/avatar_relic_3d"
    },
    "elements": [
        # Central glowing Chi Core
        {
            "name": "chi_core",
            "from": [5.5, 5.5, 5.5],
            "to": [10.5, 10.5, 10.5],
            "faces": {
                "north": {"uv": [0, 16, 5, 21], "texture": "#0"},
                "east":  {"uv": [0, 16, 5, 21], "texture": "#0"},
                "south": {"uv": [0, 16, 5, 21], "texture": "#0"},
                "west":  {"uv": [0, 16, 5, 21], "texture": "#0"},
                "up":    {"uv": [0, 16, 5, 21], "texture": "#0"},
                "down":  {"uv": [0, 16, 5, 21], "texture": "#0"}
            }
        },
        # Outer Gold Frame Ring - North/South Bars
        {
            "name": "gold_ring_n",
            "from": [3.5, 7.0, 3.5],
            "to": [12.5, 9.0, 4.5],
            "faces": {
                "north": {"uv": [0, 0, 9, 2], "texture": "#0"},
                "east":  {"uv": [0, 0, 1, 2], "texture": "#0"},
                "south": {"uv": [0, 0, 9, 2], "texture": "#0"},
                "west":  {"uv": [0, 0, 1, 2], "texture": "#0"},
                "up":    {"uv": [0, 0, 9, 1], "texture": "#0"},
                "down":  {"uv": [0, 0, 9, 1], "texture": "#0"}
            }
        },
        {
            "name": "gold_ring_s",
            "from": [3.5, 7.0, 11.5],
            "to": [12.5, 9.0, 12.5],
            "faces": {
                "north": {"uv": [0, 0, 9, 2], "texture": "#0"},
                "east":  {"uv": [0, 0, 1, 2], "texture": "#0"},
                "south": {"uv": [0, 0, 9, 2], "texture": "#0"},
                "west":  {"uv": [0, 0, 1, 2], "texture": "#0"},
                "up":    {"uv": [0, 0, 9, 1], "texture": "#0"},
                "down":  {"uv": [0, 0, 9, 1], "texture": "#0"}
            }
        },
        # Outer Gold Frame Ring - East/West Bars
        {
            "name": "gold_ring_w",
            "from": [3.5, 7.0, 4.5],
            "to": [4.5, 9.0, 11.5],
            "faces": {
                "north": {"uv": [0, 0, 1, 2], "texture": "#0"},
                "east":  {"uv": [0, 0, 7, 2], "texture": "#0"},
                "south": {"uv": [0, 0, 1, 2], "texture": "#0"},
                "west":  {"uv": [0, 0, 7, 2], "texture": "#0"},
                "up":    {"uv": [0, 0, 1, 7], "texture": "#0"},
                "down":  {"uv": [0, 0, 1, 7], "texture": "#0"}
            }
        },
        {
            "name": "gold_ring_e",
            "from": [11.5, 7.0, 4.5],
            "to": [12.5, 9.0, 11.5],
            "faces": {
                "north": {"uv": [0, 0, 1, 2], "texture": "#0"},
                "east":  {"uv": [0, 0, 7, 2], "texture": "#0"},
                "south": {"uv": [0, 0, 1, 2], "texture": "#0"},
                "west":  {"uv": [0, 0, 7, 2], "texture": "#0"},
                "up":    {"uv": [0, 0, 1, 7], "texture": "#0"},
                "down":  {"uv": [0, 0, 1, 7], "texture": "#0"}
            }
        },
        # 4 Corner Elemental Catalysts (Fire, Water, Earth, Air)
        {
            "name": "gem_fire",
            "from": [2.5, 7.0, 2.5],
            "to": [4.5, 9.0, 4.5],
            "faces": {
                "north": {"uv": [16, 0, 18, 2], "texture": "#0"},
                "east":  {"uv": [16, 0, 18, 2], "texture": "#0"},
                "south": {"uv": [16, 0, 18, 2], "texture": "#0"},
                "west":  {"uv": [16, 0, 18, 2], "texture": "#0"},
                "up":    {"uv": [16, 0, 18, 2], "texture": "#0"},
                "down":  {"uv": [16, 0, 18, 2], "texture": "#0"}
            }
        },
        {
            "name": "gem_water",
            "from": [11.5, 7.0, 2.5],
            "to": [13.5, 9.0, 4.5],
            "faces": {
                "north": {"uv": [24, 0, 26, 2], "texture": "#0"},
                "east":  {"uv": [24, 0, 26, 2], "texture": "#0"},
                "south": {"uv": [24, 0, 26, 2], "texture": "#0"},
                "west":  {"uv": [24, 0, 26, 2], "texture": "#0"},
                "up":    {"uv": [24, 0, 26, 2], "texture": "#0"},
                "down":  {"uv": [24, 0, 26, 2], "texture": "#0"}
            }
        },
        {
            "name": "gem_earth",
            "from": [2.5, 7.0, 11.5],
            "to": [4.5, 9.0, 13.5],
            "faces": {
                "north": {"uv": [16, 8, 18, 10], "texture": "#0"},
                "east":  {"uv": [16, 8, 18, 10], "texture": "#0"},
                "south": {"uv": [16, 8, 18, 10], "texture": "#0"},
                "west":  {"uv": [16, 8, 18, 10], "texture": "#0"},
                "up":    {"uv": [16, 8, 18, 10], "texture": "#0"},
                "down":  {"uv": [16, 8, 18, 10], "texture": "#0"}
            }
        },
        {
            "name": "gem_air",
            "from": [11.5, 7.0, 11.5],
            "to": [13.5, 9.0, 13.5],
            "faces": {
                "north": {"uv": [24, 8, 26, 10], "texture": "#0"},
                "east":  {"uv": [24, 8, 26, 10], "texture": "#0"},
                "south": {"uv": [24, 8, 26, 10], "texture": "#0"},
                "west":  {"uv": [24, 8, 26, 10], "texture": "#0"},
                "up":    {"uv": [24, 8, 26, 10], "texture": "#0"},
                "down":  {"uv": [24, 8, 26, 10], "texture": "#0"}
            }
        }
    ],
    "display": {
        "thirdperson_righthand": {
            "rotation": [45, 45, 0],
            "translation": [0, 3, 1],
            "scale": [0.65, 0.65, 0.65]
        },
        "firstperson_righthand": {
            "rotation": [15, 45, 0],
            "translation": [2.0, 3.5, 0.5],
            "scale": [0.75, 0.75, 0.75]
        },
        "gui": {
            "rotation": [30, 225, 0],
            "translation": [0, 0, 0],
            "scale": [0.8, 0.8, 0.8]
        },
        "ground": {
            "rotation": [0, 0, 0],
            "translation": [0, 2, 0],
            "scale": [0.6, 0.6, 0.6]
        }
    }
}

relic_json_path = os.path.join(out_dir, "avatar_relic_3d.json")
with open(relic_json_path, "w", encoding="utf-8") as f:
    json.dump(avatar_relic_3d_model, f, indent=2)
print("Generated Avatar Relic 3D JSON model:", relic_json_path)


# -------------------------------------------------------------
# 3. DEPLOY TO RESOURCE PACK
# -------------------------------------------------------------
rp_item_models = r"D:\repo\Minecraft Mod & Rp\avatar-skill-resourcepack\assets\avatar_skills\models\item"
rp_item_textures = r"D:\repo\Minecraft Mod & Rp\avatar-skill-resourcepack\assets\avatar_skills\textures\item"

if os.path.exists(rp_item_models) and os.path.exists(rp_item_textures):
    import shutil
    # Copy models
    shutil.copy2(boulder_json_path, os.path.join(rp_item_models, "earth_boulder.json"))
    shutil.copy2(water_whip_json_path, os.path.join(rp_item_models, "water_whip.json"))
    shutil.copy2(relic_json_path, os.path.join(rp_item_models, "avatar_relic_3d.json"))
    # Also update avatar_relic.json to point to 3D model!
    with open(os.path.join(rp_item_models, "avatar_relic.json"), "w", encoding="utf-8") as f:
        json.dump({"parent": "avatar_skills:item/avatar_relic_3d"}, f, indent=2)

    # Copy textures
    shutil.copy2(boulder_tex_path, os.path.join(rp_item_textures, "earth_boulder.png"))
    shutil.copy2(water_tex_path, os.path.join(rp_item_textures, "water_whip.png"))
    shutil.copy2(relic_tex_path, os.path.join(rp_item_textures, "avatar_relic_3d.png"))
    print("Successfully deployed 3D skill models & textures directly to avatar-skill-resourcepack!")
