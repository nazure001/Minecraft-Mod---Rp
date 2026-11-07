import os
import json
import base64
import math
from PIL import Image, ImageDraw, ImageFont

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff"
os.makedirs(out_dir, exist_ok=True)

# 1. GENERATE TEXTURE (32x32 pixel art texture)
tex_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
pixels = tex_img.load()

# (0, 0) to (16, 16): Shaft wood texture & gradients
for y in range(0, 16):
    for x in range(0, 16):
        grain = (x * 3 + y * 7) % 5
        if grain == 0:
            c = (93, 59, 35, 255) # dark shadow
        elif grain in (1, 2):
            c = (166, 114, 68, 255) # mid
        elif grain == 3:
            c = (198, 139, 89, 255) # light
        else:
            c = (138, 90, 54, 255) # base
        pixels[x, y] = c

# (16, 0) to (32, 16): Grip linen cloth texture
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

# (0, 16) to (16, 32): End caps / dark reinforced wood
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

# (16, 16) to (32, 32): Brass ring accent / collar
for y in range(16, 32):
    for x in range(16, 32):
        if y in (16, 17, 30, 31) or x in (16, 17, 30, 31):
            pixels[x, y] = (153, 122, 21, 255)
        else:
            pixels[x, y] = (212, 175, 55, 255)

tex_path = os.path.join(out_dir, "air_staff.png")
tex_img.save(tex_path, "PNG")
print("Saved texture to:", tex_path)

# 2. GENERATE JAVA ITEM MODEL JSON
java_model = {
    "credit": "Air Staff Prototype v0.1 for Avatar: Elements (Minecraft 1.21.1)",
    "texture_size": [32, 32],
    "textures": {
        "0": "avatar:item/air_staff",
        "particle": "avatar:item/air_staff"
    },
    "elements": [
        {
            "name": "lower_cap",
            "from": [7.0, -7.0, 7.0],
            "to": [9.0, -6.0, 9.0],
            "faces": {
                "north": {"uv": [0, 16, 2, 17], "texture": "#0"},
                "east":  {"uv": [2, 16, 4, 17], "texture": "#0"},
                "south": {"uv": [4, 16, 6, 17], "texture": "#0"},
                "west":  {"uv": [6, 16, 8, 17], "texture": "#0"},
                "up":    {"uv": [0, 17, 2, 19], "texture": "#0"},
                "down":  {"uv": [2, 17, 4, 19], "texture": "#0"}
            }
        },
        {
            "name": "lower_shaft",
            "from": [7.25, -6.0, 7.25],
            "to": [8.75, 5.0, 8.75],
            "faces": {
                "north": {"uv": [0, 0, 1.5, 11], "texture": "#0"},
                "east":  {"uv": [2, 0, 3.5, 11], "texture": "#0"},
                "south": {"uv": [4, 0, 5.5, 11], "texture": "#0"},
                "west":  {"uv": [6, 0, 7.5, 11], "texture": "#0"},
                "up":    {"uv": [0, 0, 1.5, 1.5], "texture": "#0"},
                "down":  {"uv": [0, 0, 1.5, 1.5], "texture": "#0"}
            }
        },
        {
            "name": "grip_wrap",
            "from": [7.0, 5.0, 7.0],
            "to": [9.0, 11.0, 9.0],
            "faces": {
                "north": {"uv": [16, 0, 18, 6], "texture": "#0"},
                "east":  {"uv": [18, 0, 20, 6], "texture": "#0"},
                "south": {"uv": [20, 0, 22, 6], "texture": "#0"},
                "west":  {"uv": [22, 0, 24, 6], "texture": "#0"},
                "up":    {"uv": [16, 6, 18, 8], "texture": "#0"},
                "down":  {"uv": [18, 6, 20, 8], "texture": "#0"}
            }
        },
        {
            "name": "upper_shaft",
            "from": [7.25, 11.0, 7.25],
            "to": [8.75, 22.0, 8.75],
            "faces": {
                "north": {"uv": [8, 0, 9.5, 11], "texture": "#0"},
                "east":  {"uv": [10, 0, 11.5, 11], "texture": "#0"},
                "south": {"uv": [12, 0, 13.5, 11], "texture": "#0"},
                "west":  {"uv": [14, 0, 15.5, 11], "texture": "#0"},
                "up":    {"uv": [8, 0, 9.5, 1.5], "texture": "#0"},
                "down":  {"uv": [8, 0, 9.5, 1.5], "texture": "#0"}
            }
        },
        {
            "name": "upper_cap",
            "from": [7.0, 22.0, 7.0],
            "to": [9.0, 23.0, 9.0],
            "faces": {
                "north": {"uv": [8, 16, 10, 17], "texture": "#0"},
                "east":  {"uv": [10, 16, 12, 17], "texture": "#0"},
                "south": {"uv": [12, 16, 14, 17], "texture": "#0"},
                "west":  {"uv": [14, 16, 16, 17], "texture": "#0"},
                "up":    {"uv": [8, 17, 10, 19], "texture": "#0"},
                "down":  {"uv": [10, 17, 12, 19], "texture": "#0"}
            }
        }
    ],
    "display": {
        "thirdperson_righthand": {
            "rotation": [0, -90, 55],
            "translation": [0, 4.0, 0.5],
            "scale": [0.85, 0.85, 0.85]
        },
        "thirdperson_lefthand": {
            "rotation": [0, 90, -55],
            "translation": [0, 4.0, 0.5],
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
            "translation": [0, 3.0, 0],
            "scale": [0.5, 0.5, 0.5]
        },
        "gui": {
            "rotation": [0, 0, -45],
            "translation": [0, 0, 0],
            "scale": [0.55, 0.55, 0.55]
        },
        "fixed": {
            "rotation": [0, 180, 0],
            "translation": [0, 0, 0],
            "scale": [0.7, 0.7, 0.7]
        }
    }
}

json_path = os.path.join(out_dir, "air_staff.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(java_model, f, indent=2)
print("Saved Java item model to:", json_path)

# 3. GENERATE BLOCKBENCH .bbmodel PROJECT FILE
with open(tex_path, "rb") as f:
    tex_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

bbmodel = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730970000,
        "model_format": "free",
        "box_uv": False
    },
    "name": "air_staff",
    "model_identifier": "avatar:air_staff",
    "resolution": {"width": 32, "height": 32},
    "elements": [
        {
            "name": el["name"],
            "box_uv": False,
            "type": "cube",
            "from": el["from"],
            "to": el["to"],
            "origin": [8.0, 8.0, 8.0],
            "color": 4,
            "faces": {
                side: {
                    "uv": f["uv"],
                    "texture": 0
                } for side, f in el["faces"].items()
            }
        } for el in java_model["elements"]
    ],
    "outliner": [
        el["name"] for el in java_model["elements"]
    ],
    "textures": [
        {
            "path": "air_staff.png",
            "name": "air_staff",
            "folder": "item",
            "namespace": "avatar",
            "id": "0",
            "particle": False,
            "render_mode": "default",
            "visible": True,
            "mode": "bitmap",
            "saved": True,
            "uuid": "a7b3c2d1-e4f5-6789-0123-abcdef456789",
            "source": tex_b64
        }
    ],
    "display": java_model["display"]
}

bbmodel_path = os.path.join(out_dir, "air_staff.bbmodel")
with open(bbmodel_path, "w", encoding="utf-8") as f:
    json.dump(bbmodel, f, indent=2)
print("Saved Blockbench .bbmodel to:", bbmodel_path)
