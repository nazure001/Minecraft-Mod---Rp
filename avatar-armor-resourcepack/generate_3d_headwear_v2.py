import os
import json
from PIL import Image, ImageDraw

base_rp = r"d:\repo\avatar-armor-resourcepack"
models_dir = os.path.join(base_rp, "assets", "avatar", "models", "item", "headwear")
tex_dir = os.path.join(base_rp, "assets", "avatar", "textures", "item", "headwear")
os.makedirs(models_dir, exist_ok=True)
os.makedirs(tex_dir, exist_ok=True)

nations = ["fire", "water", "earth", "air"]
tiers = ["initiate", "apprentice", "adept", "veteran", "master", "mythic", "sovereign"]

# Palette definitions: (base, trim, gem, horn)
# Each has 4 colors for subtle shading within its 8x8 quadrant
PALETTES = {
    "fire": {
        "base": [(28, 12, 12), (45, 18, 18), (62, 24, 24), (80, 30, 30)],      # Dark volcanic crimson/steel
        "trim": [(212, 155, 0), (255, 174, 0), (255, 215, 0), (255, 235, 120)], # Imperial gold
        "gem":  [(180, 20, 0), (240, 60, 10), (255, 120, 20), (255, 220, 50)],   # Blazing sun ruby/fire
        "horn": [(20, 15, 15), (40, 25, 25), (70, 35, 35), (110, 45, 45)]       # Dragon obsidian horn
    },
    "water": {
        "base": [(11, 29, 58), (20, 50, 92), (31, 72, 126), (45, 95, 160)],     # Deep ocean navy
        "trim": [(127, 169, 200), (165, 205, 230), (208, 231, 249), (240, 248, 255)], # Glacier silver
        "gem":  [(0, 180, 220), (0, 225, 255), (120, 245, 255), (255, 255, 255)], # Moon sapphire & pearl
        "horn": [(197, 179, 142), (226, 214, 181), (244, 238, 219), (255, 250, 240)] # Carved whale ivory
    },
    "earth": {
        "base": [(31, 36, 26), (47, 56, 39), (64, 77, 53), (85, 100, 70)],     # Heavy bronze ironstone
        "trim": [(147, 116, 36), (194, 155, 56), (223, 183, 79), (245, 210, 120)], # Regal brass
        "gem":  [(2, 60, 40), (5, 150, 105), (16, 185, 129), (52, 211, 153)],    # Imperial emerald/jade
        "horn": [(31, 41, 55), (55, 65, 81), (75, 85, 99), (107, 114, 128)]     # Bedrock granite monolith
    },
    "air": {
        "base": [(138, 75, 22), (180, 101, 31), (217, 119, 36), (240, 145, 60)], # Monk saffron cloth
        "trim": [(217, 140, 20), (245, 158, 11), (251, 191, 36), (254, 243, 199)], # Golden silk
        "gem":  [(14, 116, 144), (56, 189, 248), (125, 211, 252), (224, 242, 254)], # Sky diamond
        "horn": [(203, 213, 225), (226, 232, 240), (241, 245, 249), (255, 255, 255)] # Falcon plumage/wings
    }
}

UV_ZONES = {
    "base": [0, 0, 8, 8],
    "trim": [8, 0, 16, 8],
    "gem":  [0, 8, 8, 16],
    "horn": [8, 8, 16, 16]
}

def create_texture(nat, tier):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    pal = PALETTES[nat]

    # Fill base quadrant (0,0 to 7,7)
    for y in range(8):
        for x in range(8):
            c = pal["base"][(x + y) % 4]
            draw.point((x, y), fill=c + (255,))

    # Fill trim quadrant (8,0 to 15,7)
    for y in range(8):
        for x in range(8, 16):
            c = pal["trim"][(x + y) % 4]
            draw.point((x, y), fill=c + (255,))

    # Fill gem quadrant (0,8 to 7,15)
    for y in range(8, 16):
        for x in range(8):
            c = pal["gem"][(x + y) % 4]
            draw.point((x, y), fill=c + (255,))

    # Fill horn quadrant (8,8 to 15,15)
    for y in range(8, 16):
        for x in range(8, 16):
            c = pal["horn"][(x + y) % 4]
            draw.point((x, y), fill=c + (255,))

    fname = f"{nat}_{tier}.png"
    out_path = os.path.join(tex_dir, fname)
    img.save(out_path)
    return f"avatar:item/headwear/{nat}_{tier}"

DISPLAY_SETTINGS = {
    "head": {
        "translation": [0, -1.75, 0],
        "rotation": [0, 0, 0],
        "scale": [1.02, 1.02, 1.02]
    },
    "gui": {
        "translation": [0, -1, 0],
        "rotation": [20, 135, 0],
        "scale": [0.65, 0.65, 0.65]
    },
    "ground": {
        "translation": [0, 2, 0],
        "scale": [0.5, 0.5, 0.5]
    },
    "fixed": {
        "scale": [0.5, 0.5, 0.5]
    },
    "thirdperson_righthand": {
        "rotation": [75, 45, 0],
        "translation": [0, 2.5, 0],
        "scale": [0.375, 0.375, 0.375]
    },
    "firstperson_righthand": {
        "rotation": [0, 45, 0],
        "scale": [0.4, 0.4, 0.4]
    }
}

def make_box(from_coords, to_coords, zone="base", rot=None):
    uv = UV_ZONES.get(zone, [0, 0, 8, 8])
    box = {
        "from": from_coords,
        "to": to_coords,
        "faces": {
            "north": {"uv": uv, "texture": "#0"},
            "east": {"uv": uv, "texture": "#0"},
            "south": {"uv": uv, "texture": "#0"},
            "west": {"uv": uv, "texture": "#0"},
            "up": {"uv": uv, "texture": "#0"},
            "down": {"uv": uv, "texture": "#0"}
        }
    }
    if rot:
        box["rotation"] = rot
    return box

def get_elements_for(nat, tier):
    elems = []
    
    # Base circlet band around head (head is X:4..12, Y:0..8, Z:4..12)
    elems.append(make_box([3.8, 4.5, 3.8], [12.2, 7.5, 12.2], zone="base"))
    elems.append(make_box([3.7, 5.0, 3.7], [12.3, 6.5, 12.3], zone="trim"))

    # =========================================================================
    # TIER 1: INITIATE (Soft cloth cowl wrapping neck and head)
    # =========================================================================
    if tier == "initiate":
        elems.append(make_box([3.6, 7.5, 3.6], [12.4, 8.8, 12.4], zone="base")) # Hood top
        elems.append(make_box([3.6, 0.5, 11.5], [12.4, 7.5, 12.8], zone="base")) # Back drape
        elems.append(make_box([3.2, 1.0, 4.0], [4.2, 7.5, 12.0], zone="base"))   # Side flap L
        elems.append(make_box([11.8, 1.0, 4.0], [12.8, 7.5, 12.0], zone="base")) # Side flap R

    # =========================================================================
    # TIER 2: APPRENTICE (Iconic Cultural Avatar Headwear)
    # =========================================================================
    elif tier == "apprentice":
        if nat == "fire":
            # Half-face ninja mask + Fire Nation Topknot ponytail
            elems.append(make_box([4.2, 0.8, 3.2], [11.8, 4.2, 4.4], zone="base"))
            elems.append(make_box([6.5, 7.8, 9.0], [9.5, 9.5, 11.0], zone="trim")) # Gold topknot pin
            elems.append(make_box([7.0, 9.5, 9.5], [9.0, 13.0, 11.5], zone="horn", rot={"origin": [8, 9.5, 10.5], "axis": "x", "angle": -22.5})) # Hair
        elif nat == "water":
            # Wolf Headpiece: Wolf snout + ears
            elems.append(make_box([5.5, 5.0, 2.0], [10.5, 7.5, 4.0], zone="horn")) # Wolf snout
            elems.append(make_box([3.5, 8.2, 6.0], [5.5, 11.5, 8.0], zone="horn", rot={"origin": [4.5, 8, 7], "axis": "z", "angle": 22.5}))
            elems.append(make_box([10.5, 8.2, 6.0], [12.5, 11.5, 8.0], zone="horn", rot={"origin": [11.5, 8, 7], "axis": "z", "angle": -22.5}))
            elems.append(make_box([7.0, 6.8, 1.8], [9.0, 8.2, 3.5], zone="gem")) # Nose pearl
        elif nat == "earth":
            # Conical Dai Li bamboo hat (wide sloping brim + peaked center)
            elems.append(make_box([0.0, 7.0, 0.0], [16.0, 8.0, 16.0], zone="horn")) # Wide brim
            elems.append(make_box([4.5, 8.0, 4.5], [11.5, 10.5, 11.5], zone="base")) # Middle tier
            elems.append(make_box([6.5, 10.5, 6.5], [9.5, 13.0, 9.5], zone="gem"))   # Jade pinnacle
        elif nat == "air":
            # Flight Goggles with twin circular lenses + earcups
            elems.append(make_box([4.0, 3.5, 2.8], [7.5, 5.8, 4.2], zone="gem")) # Left lens
            elems.append(make_box([8.5, 3.5, 2.8], [12.0, 5.8, 4.2], zone="gem")) # Right lens
            elems.append(make_box([7.5, 4.2, 3.0], [8.5, 5.2, 3.8], zone="trim")) # Goggle bridge
            elems.append(make_box([2.8, 2.5, 6.0], [4.0, 6.0, 9.5], zone="horn")) # Fleece ear L
            elems.append(make_box([12.0, 2.5, 6.0], [13.2, 6.0, 9.5], zone="horn")) # Fleece ear R

    # =========================================================================
    # TIER 3: ADEPT (Crested Light Battle Helm)
    # =========================================================================
    elif tier == "adept":
        elems.append(make_box([4.0, 6.5, 3.0], [12.0, 8.5, 4.2], zone="trim")) # Forehead brow guard
        if nat == "fire":
            elems.append(make_box([7.0, 8.5, 2.8], [9.0, 12.0, 4.5], zone="gem")) # Flame spike
            elems.append(make_box([3.5, 1.5, 3.5], [4.5, 6.5, 6.0], zone="base")) # Cheek guard L
            elems.append(make_box([11.5, 1.5, 3.5], [12.5, 6.5, 6.0], zone="base")) # Cheek guard R
        elif nat == "water":
            # Twin whalebone curved horn crests
            elems.append(make_box([2.8, 7.5, 5.0], [4.2, 12.0, 7.0], zone="horn", rot={"origin": [3.5, 7.5, 6], "axis": "z", "angle": 22.5}))
            elems.append(make_box([11.8, 7.5, 5.0], [13.2, 12.0, 7.0], zone="horn", rot={"origin": [12.5, 7.5, 6], "axis": "z", "angle": -22.5}))
            elems.append(make_box([7.0, 7.2, 2.8], [9.0, 9.0, 4.2], zone="gem")) # Center sapphire
        elif nat == "earth":
            elems.append(make_box([6.0, 7.8, 2.5], [10.0, 11.0, 4.2], zone="gem")) # Jade brow spike
            elems.append(make_box([2.5, 2.0, 5.5], [4.0, 7.0, 10.0], zone="base"))  # Ear shields
            elems.append(make_box([12.0, 2.0, 5.5], [13.5, 7.0, 10.0], zone="base"))
        elif nat == "air":
            elems.append(make_box([1.8, 6.0, 6.0], [3.8, 9.0, 12.5], zone="horn", rot={"origin": [3, 7, 9], "axis": "y", "angle": -22.5})) # Glider wings L
            elems.append(make_box([12.2, 6.0, 6.0], [14.2, 9.0, 12.5], zone="horn", rot={"origin": [13, 7, 9], "axis": "y", "angle": 22.5})) # Glider wings R
            elems.append(make_box([7.0, 8.0, 2.8], [9.0, 10.5, 4.2], zone="gem")) # Aero gem

    # =========================================================================
    # TIER 4: VETERAN (Heavy Battleplate & Drapes)
    # =========================================================================
    elif tier == "veteran":
        elems.append(make_box([3.5, 7.5, 3.5], [12.5, 9.0, 12.5], zone="base")) # Helmet dome
        elems.append(make_box([3.2, 0.0, 11.8], [12.8, 7.5, 13.0], zone="base")) # Neck curtain
        if nat == "fire":
            elems.append(make_box([6.5, 9.0, 4.5], [9.5, 14.0, 7.5], zone="trim")) # Pointed spire
            elems.append(make_box([7.0, 12.5, 5.0], [9.0, 16.0, 7.0], zone="gem")) # Red plume
        elif nat == "water":
            elems.append(make_box([7.0, 8.5, 3.5], [9.0, 13.0, 11.5], zone="horn")) # Dorsal fin crest
            elems.append(make_box([6.5, 9.0, 2.8], [9.5, 11.5, 4.5], zone="gem"))
        elif nat == "earth":
            elems.append(make_box([4.0, 9.0, 4.0], [12.0, 12.0, 12.0], zone="horn")) # Heavy fortress crest
            elems.append(make_box([3.0, 3.0, 2.5], [13.0, 5.5, 4.0], zone="base"))   # Visor plate
        elif nat == "air":
            elems.append(make_box([2.8, 6.5, 2.8], [13.2, 8.5, 13.2], zone="trim")) # Bead ring
            elems.append(make_box([6.5, 8.5, 2.5], [9.5, 12.5, 4.0], zone="gem"))

    # =========================================================================
    # TIER 5: MASTER (Ornate Gilded Battle Crests)
    # =========================================================================
    elif tier == "master":
        elems.append(make_box([3.2, 7.5, 3.2], [12.8, 9.2, 12.8], zone="base"))
        if nat == "fire":
            # Radiant golden flame wings + ruby spire
            elems.append(make_box([1.8, 7.5, 5.0], [3.8, 14.0, 7.5], zone="trim", rot={"origin": [2.8, 7.5, 6], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 7.5, 5.0], [14.2, 14.0, 7.5], zone="trim", rot={"origin": [13.2, 7.5, 6], "axis": "z", "angle": -22.5}))
            elems.append(make_box([6.5, 9.0, 2.5], [9.5, 14.0, 5.0], zone="gem")) # Ruby spire
        elif nat == "water":
            # Chieftain walrus tusks + pearl tiara
            elems.append(make_box([1.8, 6.0, 3.0], [3.8, 13.5, 5.5], zone="horn", rot={"origin": [2.8, 6.0, 4], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 6.0, 3.0], [14.2, 13.5, 5.5], zone="horn", rot={"origin": [13.2, 6.0, 4], "axis": "z", "angle": -22.5}))
            elems.append(make_box([6.5, 9.5, 2.2], [9.5, 12.5, 4.0], zone="gem")) # Water pearl
        elif nat == "earth":
            # Monolithic jade horns
            elems.append(make_box([2.8, 8.5, 4.0], [5.5, 14.5, 6.5], zone="gem"))
            elems.append(make_box([10.5, 8.5, 4.0], [13.2, 14.5, 6.5], zone="gem"))
            elems.append(make_box([5.5, 9.0, 2.5], [10.5, 12.5, 4.5], zone="trim"))
        elif nat == "air":
            # Floating golden nimbus halo hovering above head!
            elems.append(make_box([2.0, 11.5, 2.0], [14.0, 12.8, 14.0], zone="trim"))
            elems.append(make_box([6.8, 8.5, 2.5], [9.2, 11.5, 4.0], zone="gem"))

    # =========================================================================
    # TIER 6: MYTHIC (Elemental Horns & Runic Wings)
    # =========================================================================
    elif tier == "mythic":
        elems.append(make_box([3.0, 7.5, 3.0], [13.0, 9.5, 13.0], zone="base"))
        if nat == "fire":
            # Volcanic dragon horns curved backwards
            elems.append(make_box([1.8, 8.0, 8.0], [4.2, 15.5, 11.0], zone="horn", rot={"origin": [3, 8, 9.5], "axis": "x", "angle": -22.5}))
            elems.append(make_box([11.8, 8.0, 8.0], [14.2, 15.5, 11.0], zone="horn", rot={"origin": [13, 8, 9.5], "axis": "x", "angle": -22.5}))
            elems.append(make_box([6.5, 9.5, 2.2], [9.5, 14.5, 4.5], zone="gem")) # Central flame crest
        elif nat == "water":
            # Leviathan serpent crown
            elems.append(make_box([1.5, 7.5, 4.0], [4.0, 15.0, 7.0], zone="horn", rot={"origin": [2.5, 7.5, 5.5], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.0, 7.5, 4.0], [14.5, 15.0, 7.0], zone="horn", rot={"origin": [13.5, 7.5, 5.5], "axis": "z", "angle": -22.5}))
            elems.append(make_box([6.5, 10.0, 2.0], [9.5, 13.5, 4.0], zone="gem")) # Leviathan pearl
        elif nat == "earth":
            # Quadruple mountain titan horns
            elems.append(make_box([1.8, 8.0, 3.0], [4.5, 15.0, 5.5], zone="horn"))
            elems.append(make_box([11.5, 8.0, 3.0], [14.2, 15.0, 5.5], zone="horn"))
            elems.append(make_box([1.8, 8.0, 9.0], [4.5, 14.0, 11.5], zone="horn"))
            elems.append(make_box([11.5, 8.0, 9.0], [14.2, 14.0, 11.5], zone="horn"))
            elems.append(make_box([5.5, 9.5, 2.2], [10.5, 13.5, 4.2], zone="gem"))
        elif nat == "air":
            # Quadruple wind plumage
            elems.append(make_box([6.5, 9.0, 2.5], [9.5, 15.5, 4.5], zone="gem"))
            elems.append(make_box([1.8, 8.5, 7.0], [3.8, 14.5, 9.5], zone="horn", rot={"origin": [2.8, 8.5, 8], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 8.5, 7.0], [14.2, 14.5, 9.5], zone="horn", rot={"origin": [13.2, 8.5, 8], "axis": "z", "angle": -22.5}))

    # =========================================================================
    # TIER 7: SOVEREIGN (Grand Sovereign Godplate & 3D Crowns)
    # =========================================================================
    elif tier == "sovereign":
        elems.append(make_box([3.0, 7.5, 3.0], [13.0, 9.5, 13.0], zone="base"))
        if nat == "fire":
            # Grand 3D Dragon Horns (massive curving horns!)
            elems.append(make_box([1.2, 8.0, 7.0], [4.0, 17.0, 10.5], zone="horn", rot={"origin": [2.5, 8, 8.5], "axis": "z", "angle": 25.0}))
            elems.append(make_box([12.0, 8.0, 7.0], [14.8, 17.0, 10.5], zone="horn", rot={"origin": [13.5, 8, 8.5], "axis": "z", "angle": -25.0}))
            # 5-spire golden Dragon Crown
            elems.append(make_box([6.8, 9.5, 1.8], [9.2, 15.0, 3.8], zone="gem"))  # Center sun ruby spire
            elems.append(make_box([4.2, 9.5, 2.2], [6.0, 13.5, 3.8], zone="trim")) # Left mid spire
            elems.append(make_box([10.0, 9.5, 2.2], [11.8, 13.5, 3.8], zone="trim")) # Right mid spire
            elems.append(make_box([2.2, 9.5, 3.0], [3.8, 12.0, 4.5], zone="trim")) # Left outer spire
            elems.append(make_box([12.2, 9.5, 3.0], [13.8, 12.0, 4.5], zone="trim")) # Right outer spire
        elif nat == "water":
            # Ocean Spirit Tiara: Rising wave horns + floating moon pearl
            elems.append(make_box([1.2, 7.5, 3.5], [3.8, 17.0, 6.8], zone="horn", rot={"origin": [2.5, 7.5, 5], "axis": "z", "angle": 25.0}))
            elems.append(make_box([12.2, 7.5, 3.5], [14.8, 17.0, 6.8], zone="horn", rot={"origin": [13.5, 7.5, 5], "axis": "z", "angle": -25.0}))
            # Floating Moon Pearl
            elems.append(make_box([6.8, 12.0, 1.5], [9.2, 14.5, 3.8], zone="gem"))
            elems.append(make_box([5.0, 9.5, 2.0], [11.0, 12.0, 4.0], zone="trim"))
        elif nat == "earth":
            # Titan Bedrock Horns (Massive monolith block horns)
            elems.append(make_box([0.8, 8.0, 4.0], [4.5, 17.5, 8.5], zone="horn"))
            elems.append(make_box([11.5, 8.0, 4.0], [15.2, 17.5, 8.5], zone="horn"))
            # Central fortress crest + emerald core
            elems.append(make_box([5.0, 9.5, 1.8], [11.0, 14.5, 4.0], zone="trim"))
            elems.append(make_box([6.5, 10.5, 1.5], [9.5, 13.5, 3.0], zone="gem"))
        elif nat == "air":
            # Full 3D Floating Nimbus Halo (hovering above head!)
            elems.append(make_box([1.0, 13.0, 1.0], [15.0, 14.5, 15.0], zone="trim"))
            # Hermes winged plumes
            elems.append(make_box([0.5, 8.0, 7.0], [2.5, 16.0, 10.0], zone="horn", rot={"origin": [1.5, 8, 8.5], "axis": "z", "angle": 25.0}))
            elems.append(make_box([13.5, 8.0, 7.0], [15.5, 16.0, 10.0], zone="horn", rot={"origin": [14.5, 8, 8.5], "axis": "z", "angle": -25.0}))
            # Floating Avatar forehead gem
            elems.append(make_box([6.8, 9.5, 1.8], [9.2, 12.8, 3.5], zone="gem"))

    return elems

def generate_all():
    count = 0
    for nat in nations:
        for t in tiers:
            tex_ref = create_texture(nat, t)
            model_data = {
                "credit": "Avatar Armor 3D Headwear (1.21.1)",
                "texture_size": [16, 16],
                "textures": {
                    "0": tex_ref,
                    "particle": tex_ref
                },
                "elements": get_elements_for(nat, t),
                "display": DISPLAY_SETTINGS
            }

            fname = f"{nat}_{t}.json"
            out_path = os.path.join(models_dir, fname)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(model_data, f, indent=2)
            count += 1

    print(f"Successfully generated {count} 3D headwear models and textures!")

if __name__ == "__main__":
    generate_all()
