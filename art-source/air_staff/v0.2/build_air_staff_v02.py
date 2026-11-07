import os
import json
import base64
import math
from PIL import Image

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff\v0.2"
os.makedirs(out_dir, exist_ok=True)

# 1. TEXTURE v0.2 (Pure Organic Wood + Linen Wrap, NO BRASS/METAL ORNAMENTS)
tex_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
pixels = tex_img.load()

# (0, 0) to (16, 16): Shaft wood texture & natural grain
for y in range(0, 16):
    for x in range(0, 16):
        grain = (x * 3 + y * 7) % 5
        if grain == 0:
            c = (93, 59, 35, 255) # shadow
        elif grain in (1, 2):
            c = (166, 114, 68, 255) # midtone
        elif grain == 3:
            c = (198, 139, 89, 255) # light
        else:
            c = (138, 90, 54, 255) # base
        pixels[x, y] = c

# (16, 0) to (32, 16): Grip linen wrap
for y in range(0, 16):
    for x in range(16, 32):
        wrap = (x + y * 2) % 4
        if wrap == 0:
            c = (140, 128, 109, 255) # wrap shadow
        elif wrap == 1:
            c = (184, 174, 156, 255) # mid
        elif wrap == 2:
            c = (234, 230, 223, 255) # highlight
        else:
            c = (213, 206, 191, 255) # base
        pixels[x, y] = c

# (0, 16) to (16, 32): End caps / hardened dark wood
for y in range(16, 32):
    for x in range(0, 16):
        pattern = (x + y) % 3
        if pattern == 0:
            c = (67, 48, 34, 255) # dark
        elif pattern == 1:
            c = (92, 67, 50, 255) # mid
        else:
            c = (120, 88, 64, 255) # rim highlight
        pixels[x, y] = c

# (16, 16) to (32, 32): Wood knots / natural grain variations (NO BRASS)
for y in range(16, 32):
    for x in range(16, 32):
        dist_knot = math.sqrt((x - 24)**2 + (y - 24)**2)
        if dist_knot < 3.0:
            c = (62, 39, 27, 255) # knot core
        elif dist_knot < 6.0:
            c = (92, 62, 44, 255) # knot ring
        else:
            c = (125, 84, 55, 255) # dark grain
        pixels[x, y] = c

tex_path = os.path.join(out_dir, "air_staff_v02.png")
tex_img.save(tex_path, "PNG")
print("Saved texture to:", tex_path)

# 2. DEFINISI ELEMEN MODEL (5 KUBUS)
raw_elements = [
    {
        "name": "lower_cap",
        "uuid": "c3a1f2e0-1111-4000-8000-000000000001",
        "from": [7.0, -7.0, 7.0],
        "to": [9.0, -6.0, 9.0],
        "faces_bb_32px": {
            "north": [0.0, 16.0, 2.0, 17.0],
            "east":  [2.0, 16.0, 4.0, 17.0],
            "south": [4.0, 16.0, 6.0, 17.0],
            "west":  [6.0, 16.0, 8.0, 17.0],
            "up":    [0.0, 17.0, 2.0, 19.0],
            "down":  [2.0, 17.0, 4.0, 19.0]
        }
    },
    {
        "name": "lower_shaft",
        "uuid": "c3a1f2e0-1111-4000-8000-000000000002",
        "from": [7.25, -6.0, 7.25],
        "to": [8.75, 5.0, 8.75],
        "faces_bb_32px": {
            "north": [0.0, 0.0, 1.5, 11.0],
            "east":  [2.0, 0.0, 3.5, 11.0],
            "south": [4.0, 0.0, 5.5, 11.0],
            "west":  [6.0, 0.0, 7.5, 11.0],
            "up":    [0.0, 0.0, 1.5, 1.5],
            "down":  [0.0, 0.0, 1.5, 1.5]
        }
    },
    {
        "name": "grip_wrap",
        "uuid": "c3a1f2e0-1111-4000-8000-000000000003",
        "from": [7.0, 5.0, 7.0],
        "to": [9.0, 11.0, 9.0],
        "faces_bb_32px": {
            "north": [16.0, 0.0, 18.0, 6.0],
            "east":  [18.0, 0.0, 20.0, 6.0],
            "south": [20.0, 0.0, 22.0, 6.0],
            "west":  [22.0, 0.0, 24.0, 6.0],
            "up":    [16.0, 6.0, 18.0, 8.0],
            "down":  [18.0, 6.0, 20.0, 8.0]
        }
    },
    {
        "name": "upper_shaft",
        "uuid": "c3a1f2e0-1111-4000-8000-000000000004",
        "from": [7.25, 11.0, 7.25],
        "to": [8.75, 22.0, 8.75],
        "faces_bb_32px": {
            "north": [8.0, 0.0, 9.5, 11.0],
            "east":  [10.0, 0.0, 11.5, 11.0],
            "south": [12.0, 0.0, 13.5, 11.0],
            "west":  [14.0, 0.0, 15.5, 11.0],
            "up":    [8.0, 0.0, 9.5, 1.5],
            "down":  [8.0, 0.0, 9.5, 1.5]
        }
    },
    {
        "name": "upper_cap",
        "uuid": "c3a1f2e0-1111-4000-8000-000000000005",
        "from": [7.0, 22.0, 7.0],
        "to": [9.0, 23.0, 9.0],
        "faces_bb_32px": {
            "north": [8.0, 16.0, 10.0, 17.0],
            "east":  [10.0, 16.0, 12.0, 17.0],
            "south": [12.0, 16.0, 14.0, 17.0],
            "west":  [14.0, 16.0, 16.0, 17.0],
            "up":    [8.0, 17.0, 10.0, 19.0],
            "down":  [10.0, 17.0, 12.0, 19.0]
        }
    }
]

# Display Slots standar 1.21.1
display_slots = {
    "thirdperson_righthand": {
        "rotation": [0, -90, 55],
        "translation": [0.0, 4.0, 0.5],
        "scale": [0.85, 0.85, 0.85]
    },
    "thirdperson_lefthand": {
        "rotation": [0, 90, -55],
        "translation": [0.0, 4.0, 0.5],
        "scale": [0.85, 0.85, 0.85]
    },
    "firstperson_righthand": {
        "rotation": [0, -90, 25],
        "translation": [1.13, 3.2, 1.13],
        "scale": [0.68, 0.68, 0.68]
    },
    "firstperson_lefthand": {
        "rotation": [0, 90, -25],
        "translation": [1.13, 3.2, 1.13],
        "scale": [0.68, 0.68, 0.68]
    },
    "ground": {
        "rotation": [0, 0, 0],
        "translation": [0.0, 3.0, 0.0],
        "scale": [0.5, 0.5, 0.5]
    },
    "gui": {
        "rotation": [0, 0, -45],
        "translation": [0.0, 0.0, 0.0],
        "scale": [0.55, 0.55, 0.55]
    },
    "fixed": {
        "rotation": [0, 180, 0],
        "translation": [0.0, 0.0, 0.0],
        "scale": [0.7, 0.7, 0.7]
    }
}

# 3. GENERATE BLOCKBENCH .bbmodel (FORMAT: java_block)
with open(tex_path, "rb") as f:
    tex_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

bb_elements = []
outliner_uuids = []

for el in raw_elements:
    outliner_uuids.append(el["uuid"])
    faces_dict = {}
    for side, uv in el["faces_bb_32px"].items():
        faces_dict[side] = {
            "uv": uv,
            "texture": 0
        }
    bb_elements.append({
        "name": el["name"],
        "box_uv": False,
        "type": "cube",
        "uuid": el["uuid"],
        "from": el["from"],
        "to": el["to"],
        "origin": [8.0, 8.0, 8.0],
        "color": 4,
        "faces": faces_dict
    })

bbmodel = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730975000,
        "model_format": "java_block",
        "box_uv": False
    },
    "name": "air_staff",
    "model_identifier": "avatar_elements:air_staff",
    "resolution": {"width": 32, "height": 32},
    "elements": bb_elements,
    "outliner": outliner_uuids,
    "textures": [
        {
            "path": "air_staff_v02.png",
            "name": "air_staff_v02",
            "folder": "item",
            "namespace": "avatar_elements",
            "id": "0",
            "particle": False,
            "render_mode": "default",
            "visible": True,
            "mode": "bitmap",
            "saved": True,
            "uuid": "c3a1f2e0-1111-4000-8000-000000000000",
            "source": tex_b64
        }
    ],
    "display": display_slots
}

bbmodel_path = os.path.join(out_dir, "air_staff.bbmodel")
with open(bbmodel_path, "w", encoding="utf-8") as f:
    json.dump(bbmodel, f, indent=2)
print("Saved Blockbench .bbmodel (java_block format) to:", bbmodel_path)

# 4. GENERATE MINECRAFT JAVA ITEM MODEL JSON (air_staff.json)
# Konversi UV: Pixel 32px -> Normalisasi Java Block/Item 0..16 (UV_java = UV_bb * 16.0 / 32.0 = UV_bb * 0.5)
java_elements = []
for el in raw_elements:
    faces_json = {}
    for side, uv in el["faces_bb_32px"].items():
        # Konversi UV ke ruang 0..16
        uv_converted = [round(c * 0.5, 4) for c in uv]
        faces_json[side] = {
            "uv": uv_converted,
            "texture": "#0"
        }
    java_elements.append({
        "name": el["name"],
        "from": el["from"],
        "to": el["to"],
        "faces": faces_json
    })

java_model = {
    "credit": "Air Staff Prototype v0.2 for Avatar: Elements (Minecraft 1.21.1)",
    "textures": {
        "0": "avatar_elements:item/air_staff",
        "particle": "avatar_elements:item/air_staff"
    },
    "elements": java_elements,
    "display": display_slots
}

json_path = os.path.join(out_dir, "air_staff.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(java_model, f, indent=2)
print("Saved Java Item Model JSON to:", json_path)
