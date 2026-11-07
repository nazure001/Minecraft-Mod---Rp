import os
import json

base_rp = r"d:\repo\avatar-armor-resourcepack"
hw_dir = os.path.join(base_rp, "assets", "avatar", "models", "item", "headwear")
os.makedirs(hw_dir, exist_ok=True)

nations = ["fire", "water", "earth", "air"]
tiers = ["initiate", "apprentice", "adept", "veteran", "master", "mythic", "sovereign"]

# Common display settings so it fits the player's head and renders cleanly in inventory
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

def make_box(from_coords, to_coords, rot=None):
    box = {
        "from": from_coords,
        "to": to_coords,
        "faces": {
            "north": {"uv": [0, 0, 16, 16], "texture": "#0"},
            "east": {"uv": [0, 0, 16, 16], "texture": "#0"},
            "south": {"uv": [0, 0, 16, 16], "texture": "#0"},
            "west": {"uv": [0, 0, 16, 16], "texture": "#0"},
            "up": {"uv": [0, 0, 16, 16], "texture": "#0"},
            "down": {"uv": [0, 0, 16, 16], "texture": "#0"}
        }
    }
    if rot:
        box["rotation"] = rot
    return box

def get_elements_for(nat, tier):
    elems = []
    
    # Base head circlet / band around the player head (head is X:4..12, Y:0..8, Z:4..12)
    # Headband
    elems.append(make_box([3.8, 4.5, 3.8], [12.2, 7.5, 12.2]))

    # --- TIER 1: INITIATE (Soft cloth cowl wrapping neck and back of head) ---
    if tier == "initiate":
        # Hood top
        elems.append(make_box([3.6, 7.5, 3.6], [12.4, 8.8, 12.4]))
        # Back drape
        elems.append(make_box([3.6, 0.5, 11.5], [12.4, 7.5, 12.8]))
        # Side flaps
        elems.append(make_box([3.2, 1.0, 4.0], [4.2, 7.5, 12.0]))
        elems.append(make_box([11.8, 1.0, 4.0], [12.8, 7.5, 12.0]))

    # --- TIER 2: APPRENTICE (Iconic Avatar Headwear) ---
    elif tier == "apprentice":
        if nat == "fire":
            # Half-face ninja mask
            elems.append(make_box([4.2, 0.8, 3.2], [11.8, 4.2, 4.4]))
            # Flame Topknot ponytail
            elems.append(make_box([7.0, 8.5, 9.0], [9.0, 12.0, 11.0], {"origin": [8, 8.5, 10], "axis": "x", "angle": -22.5}))
        elif nat == "water":
            # Wolf Headpiece: Wolf snout
            elems.append(make_box([5.5, 5.0, 2.2], [10.5, 7.5, 4.0]))
            # Left wolf ear
            elems.append(make_box([3.5, 8.2, 6.0], [5.5, 11.2, 8.0], {"origin": [4.5, 8, 7], "axis": "z", "angle": 22.5}))
            # Right wolf ear
            elems.append(make_box([10.5, 8.2, 6.0], [12.5, 11.2, 8.0], {"origin": [11.5, 8, 7], "axis": "z", "angle": -22.5}))
        elif nat == "earth":
            # Conical Dai Li bamboo hat (sloping wide brim)
            elems.append(make_box([0.5, 7.0, 0.5], [15.5, 8.0, 15.5]))
            # Cone peak
            elems.append(make_box([5.0, 8.0, 5.0], [11.0, 10.5, 11.0]))
            elems.append(make_box([6.5, 10.5, 6.5], [9.5, 12.5, 9.5]))
        elif nat == "air":
            # Flight Goggles around eyes
            elems.append(make_box([4.0, 3.5, 2.8], [7.5, 5.8, 4.2]))
            elems.append(make_box([8.5, 3.5, 2.8], [12.0, 5.8, 4.2]))
            # Goggle bridge
            elems.append(make_box([7.5, 4.2, 3.0], [8.5, 5.2, 3.8]))
            # Fleece ear-cups
            elems.append(make_box([2.8, 2.5, 6.0], [4.0, 6.0, 9.5]))
            elems.append(make_box([12.0, 2.5, 6.0], [13.2, 6.0, 9.5]))

    # --- TIER 3: ADEPT (Crested Light Battle Helm) ---
    elif tier == "adept":
        # Brow guard
        elems.append(make_box([4.0, 6.5, 3.0], [12.0, 8.5, 4.2]))
        if nat == "fire":
            # Pointed forehead flame spike
            elems.append(make_box([7.0, 8.5, 3.0], [9.0, 11.5, 4.5]))
            # Cheek guards
            elems.append(make_box([3.5, 1.5, 3.5], [4.5, 6.5, 6.0]))
            elems.append(make_box([11.5, 1.5, 3.5], [12.5, 6.5, 6.0]))
        elif nat == "water":
            # Double whalebone curved crests
            elems.append(make_box([2.8, 7.5, 5.0], [4.2, 11.5, 7.0], {"origin": [3.5, 7.5, 6], "axis": "z", "angle": 22.5}))
            elems.append(make_box([11.8, 7.5, 5.0], [13.2, 11.5, 7.0], {"origin": [12.5, 7.5, 6], "axis": "z", "angle": -22.5}))
        elif nat == "earth":
            # Angular jade forehead crest
            elems.append(make_box([6.0, 7.8, 2.5], [10.0, 10.5, 4.2]))
            # Ear shields
            elems.append(make_box([2.8, 2.0, 5.5], [4.0, 7.0, 10.0]))
            elems.append(make_box([12.0, 2.0, 5.5], [13.2, 7.0, 10.0]))
        elif nat == "air":
            # Swept-back glider wings
            elems.append(make_box([2.0, 6.0, 6.0], [4.0, 8.5, 12.0], {"origin": [3, 7, 9], "axis": "y", "angle": -22.5}))
            elems.append(make_box([12.0, 6.0, 6.0], [14.0, 8.5, 12.0], {"origin": [13, 7, 9], "axis": "y", "angle": 22.5}))

    # --- TIER 4: VETERAN WARRIOR (Heavy Battleplate & Drapes) ---
    elif tier == "veteran":
        # Solid helmet dome
        elems.append(make_box([3.5, 7.5, 3.5], [12.5, 9.0, 12.5]))
        # Neck curtain drape
        elems.append(make_box([3.2, 0.0, 11.8], [12.8, 7.5, 13.0]))
        if nat == "fire":
            # Imperial helmet pointed peak
            elems.append(make_box([6.5, 9.0, 5.0], [9.5, 13.5, 8.0]))
        elif nat == "water":
            # Dorsal fin crest
            elems.append(make_box([7.2, 8.5, 3.5], [8.8, 12.5, 11.5]))
        elif nat == "earth":
            # Heavy fortress rectangular crown
            elems.append(make_box([4.5, 9.0, 4.5], [11.5, 11.5, 11.5]))
        elif nat == "air":
            # Prayer veil & bead ring
            elems.append(make_box([3.0, 6.5, 3.0], [13.0, 8.5, 13.0]))

    # --- TIER 5: GRAND MASTER (Ornate Gilded Battle Crests) ---
    elif tier == "master":
        elems.append(make_box([3.2, 7.5, 3.2], [12.8, 9.2, 12.8]))
        if nat == "fire":
            # Officer golden flame wings
            elems.append(make_box([1.8, 7.5, 5.0], [3.8, 13.0, 7.5], {"origin": [2.8, 7.5, 6], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 7.5, 5.0], [14.2, 13.0, 7.5], {"origin": [13.2, 7.5, 6], "axis": "z", "angle": -22.5}))
            elems.append(make_box([6.5, 9.0, 3.0], [9.5, 13.0, 5.5]))
        elif nat == "water":
            # Chieftain whale tusks
            elems.append(make_box([2.0, 6.5, 3.0], [4.0, 12.5, 5.5], {"origin": [3, 6.5, 4], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.0, 6.5, 3.0], [14.0, 12.5, 5.5], {"origin": [13, 6.5, 4], "axis": "z", "angle": -22.5}))
        elif nat == "earth":
            # Monolithic jade horns
            elems.append(make_box([3.0, 8.5, 4.0], [5.5, 14.0, 6.5]))
            elems.append(make_box([10.5, 8.5, 4.0], [13.0, 14.0, 6.5]))
        elif nat == "air":
            # Floating golden nimbus halo
            elems.append(make_box([2.5, 11.0, 2.5], [13.5, 12.0, 13.5]))

    # --- TIER 6: ASCENDED MYTHIC (Elemental Horns & Runic Wings) ---
    elif tier == "mythic":
        elems.append(make_box([3.0, 7.5, 3.0], [13.0, 9.5, 13.0]))
        if nat == "fire":
            # Volcanic dragon horns
            elems.append(make_box([2.0, 8.0, 8.0], [4.2, 15.0, 10.5], {"origin": [3, 8, 9], "axis": "x", "angle": -22.5}))
            elems.append(make_box([11.8, 8.0, 8.0], [14.0, 15.0, 10.5], {"origin": [13, 8, 9], "axis": "x", "angle": -22.5}))
        elif nat == "water":
            # Leviathan serpent tiara
            elems.append(make_box([1.5, 7.5, 4.0], [3.8, 14.5, 7.0], {"origin": [2.5, 7.5, 5.5], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 7.5, 4.0], [14.5, 14.5, 7.0], {"origin": [13.5, 7.5, 5.5], "axis": "z", "angle": -22.5}))
        elif nat == "earth":
            # Quadruple mountain titan horns
            elems.append(make_box([2.0, 8.0, 3.0], [4.5, 14.5, 5.5]))
            elems.append(make_box([11.5, 8.0, 3.0], [14.0, 14.5, 5.5]))
            elems.append(make_box([2.0, 8.0, 9.0], [4.5, 13.5, 11.5]))
            elems.append(make_box([11.5, 8.0, 9.0], [14.0, 13.5, 11.5]))
        elif nat == "air":
            # Quadruple wind plumage
            elems.append(make_box([6.5, 9.0, 2.5], [9.5, 15.0, 4.5]))
            elems.append(make_box([2.0, 8.5, 7.0], [3.8, 14.0, 9.5], {"origin": [3, 8.5, 8], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 8.5, 7.0], [14.0, 14.0, 9.5], {"origin": [13, 8.5, 8], "axis": "z", "angle": -22.5}))

    # --- TIER 7: LEGENDARY SOVEREIGN (Grand Sovereign Godplate & 3D Crowns) ---
    elif tier == "sovereign":
        # Base royal circlet
        elems.append(make_box([3.0, 7.5, 3.0], [13.0, 9.5, 13.0]))
        
        if nat == "fire":
            # Grand 3D Dragon Horns (massive curving horns!)
            elems.append(make_box([1.5, 8.0, 7.0], [4.0, 16.5, 10.0], {"origin": [2.5, 8, 8.5], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.0, 8.0, 7.0], [14.5, 16.5, 10.0], {"origin": [13.5, 8, 8.5], "axis": "z", "angle": -22.5}))
            # Crown spikes (front, center, sides)
            elems.append(make_box([7.0, 9.5, 2.0], [9.0, 14.0, 3.8]))
            elems.append(make_box([4.5, 9.5, 2.5], [6.0, 12.5, 3.8]))
            elems.append(make_box([10.0, 9.5, 2.5], [11.5, 12.5, 3.8]))
        elif nat == "water":
            # Ocean Spirit Tiara: Rising wave horns
            elems.append(make_box([1.5, 7.5, 3.5], [3.8, 16.0, 6.5], {"origin": [2.5, 7.5, 5], "axis": "z", "angle": 22.5}))
            elems.append(make_box([12.2, 7.5, 3.5], [14.5, 16.0, 6.5], {"origin": [13.5, 7.5, 5], "axis": "z", "angle": -22.5}))
            # Floating Moon Pearl
            elems.append(make_box([7.0, 11.5, 1.8], [9.0, 13.5, 3.8]))
        elif nat == "earth":
            # Titan Bedrock Horns (Massive monolith block horns)
            elems.append(make_box([1.0, 8.0, 4.0], [4.5, 16.5, 8.5]))
            elems.append(make_box([11.5, 8.0, 4.0], [15.0, 16.5, 8.5]))
            # Central fortress crest
            elems.append(make_box([5.5, 9.5, 2.0], [10.5, 14.0, 4.0]))
        elif nat == "air":
            # Full 3D Floating Nimbus Halo (hovering above head!)
            elems.append(make_box([1.5, 12.5, 1.5], [14.5, 13.8, 14.5]))
            # Floating Avatar forehead gem
            elems.append(make_box([7.0, 9.0, 2.0], [9.0, 12.0, 3.5]))
            # Hermes winged plumes
            elems.append(make_box([0.5, 8.0, 7.0], [2.5, 15.0, 9.5], {"origin": [1.5, 8, 8], "axis": "z", "angle": 22.5}))
            elems.append(make_box([13.5, 8.0, 7.0], [15.5, 15.0, 9.5], {"origin": [14.5, 8, 8], "axis": "z", "angle": -22.5}))

    return elems

def generate_all():
    count = 0
    for nat in nations:
        for t in tiers:
            tex_name = f"{nat}_{t}_helmet"
            model_data = {
                "credit": "Avatar Armor 3D Headwear (1.21.1)",
                "texture_size": [16, 16],
                "textures": {
                    "0": f"avatar:item/{tex_name}",
                    "particle": f"avatar:item/{tex_name}"
                },
                "elements": get_elements_for(nat, t),
                "display": DISPLAY_SETTINGS
            }

            fname = f"{nat}_{t}.json"
            out_path = os.path.join(hw_dir, fname)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(model_data, f, indent=2)
            count += 1

    print(f"Generated {count} custom 3D headwear JSON models in {hw_dir}!")

if __name__ == "__main__":
    generate_all()
