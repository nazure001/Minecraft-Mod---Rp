import os
import json
import base64
import math
from PIL import Image, ImageDraw

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff\v0.2"
os.makedirs(out_dir, exist_ok=True)

# 1. TEXTURE v0.2 (Pure Organic Wood + Linen Wrap, NO BRASS/METAL ORNAMENTS)
tex_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
pixels = tex_img.load()

# Palette:
# Shaft wood: #8A5A36, #A67244, #C68B59, #DFAB7A, #5D3B23
# Grip cloth: #EAE6DF, #D5CEBF, #B8AE9C, #8C806D
# End caps: #5C4332, #433022, #785840
# Dark wood accent / knots (replacing brass): #3E271B, #4D3224, #5C3E2C

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
print("Saved revised texture to:", tex_path)

# 2. JAVA ITEM MODEL JSON v0.2
# Namespace matches D009: avatar_elements
java_model = {
    "credit": "Air Staff Prototype v0.2 for Avatar: Elements (Minecraft 1.21.1)",
    "texture_size": [32, 32],
    "textures": {
        "0": "avatar_elements:item/air_staff",
        "particle": "avatar_elements:item/air_staff"
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
print("Saved revised Java item model to:", json_path)

# 3. BLOCKBENCH .bbmodel PROJECT FILE v0.2
with open(tex_path, "rb") as f:
    tex_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

bbmodel = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730975000,
        "model_format": "free",
        "box_uv": False
    },
    "name": "air_staff",
    "model_identifier": "avatar_elements:air_staff",
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
            "uuid": "b8c4d3e2-f5a6-7890-1234-bcdef5678901",
            "source": tex_b64
        }
    ],
    "display": java_model["display"]
}

bbmodel_path = os.path.join(out_dir, "air_staff.bbmodel")
with open(bbmodel_path, "w", encoding="utf-8") as f:
    json.dump(bbmodel, f, indent=2)
print("Saved revised Blockbench .bbmodel to:", bbmodel_path)

# 4. RENDER VISUAL PREVIEWS v0.2 (NO METRIC ASSUMPTIONS)
W, H = 1000, 750
img = Image.new("RGBA", (W, H), (24, 26, 32, 255))
draw = ImageDraw.Draw(img)

draw.text((40, 25), "AIR NOMAD STAFF (TONGKAT UDARA) — REVISED MODEL PREVIEW v0.2", fill=(240, 240, 245, 255))
draw.text((40, 50), "Format: Minecraft 1.21.1 Java Model JSON & Blockbench 4.10 | Texture: 32x32 PNG", fill=(140, 150, 170, 255))
draw.text((40, 70), "Brief Compliance: 100% Organic Ash Wood + Linen Wrap | Zero Glider | Zero Metal Ornaments", fill=(210, 175, 100, 255))

draw.rectangle([(40, 105), (620, 710)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)

cx = 330
cy = 415
scale = 13.5
cos30 = math.cos(math.radians(30))
sin30 = math.sin(math.radians(30))

def project(x, y, z):
    dx = x - 8.0
    dz = z - 8.0
    dy = y - 8.0
    px = cx + (dx - dz) * scale * cos30
    py = cy - dy * scale + (dx + dz) * scale * sin30
    return (px, py)

def draw_cube(from_pt, to_pt, top_color, left_color, right_color, outline_color):
    x0, y0, z0 = from_pt
    x1, y1, z1 = to_pt
    v = {
        'p000': project(x0, y0, z0),
        'p100': project(x1, y0, z0),
        'p101': project(x1, y0, z1),
        'p001': project(x0, y0, z1),
        'p010': project(x0, y1, z0),
        'p110': project(x1, y1, z0),
        'p111': project(x1, y1, z1),
        'p011': project(x0, y1, z1)
    }
    draw.polygon([v['p010'], v['p110'], v['p111'], v['p011']], fill=top_color, outline=outline_color)
    draw.polygon([v['p001'], v['p101'], v['p111'], v['p011']], fill=left_color, outline=outline_color)
    draw.polygon([v['p100'], v['p101'], v['p111'], v['p110']], fill=right_color, outline=outline_color)

# Ground shadow
shadow_pts = [project(6.0, -8.5, 6.0), project(10.0, -8.5, 6.0), project(10.0, -8.5, 10.0), project(6.0, -8.5, 10.0)]
draw.polygon(shadow_pts, fill=(20, 22, 28, 200))

# 1. Lower Cap [7, -7, 7] to [9, -6, 9]
draw_cube([7.0, -7.0, 7.0], [9.0, -6.0, 9.0], (100, 75, 55, 255), (75, 54, 38, 255), (55, 40, 28, 255), (40, 30, 20, 255))
# 2. Lower Shaft [7.25, -6.0, 7.25] to [8.75, 5.0, 8.75]
draw_cube([7.25, -6.0, 7.25], [8.75, 5.0, 8.75], (198, 139, 89, 255), (150, 102, 60, 255), (115, 76, 44, 255), (70, 45, 25, 255))
# 3. Grip Linen Cloth [7.0, 5.0, 7.0] to [9.0, 11.0, 9.0]
draw_cube([7.0, 5.0, 7.0], [9.0, 11.0, 9.0], (234, 230, 223, 255), (205, 198, 185, 255), (165, 155, 140, 255), (100, 92, 80, 255))
for wy in range(6, 11, 2):
    p_l0 = project(7.0, wy, 9.0)
    p_l1 = project(9.0, wy, 9.0)
    p_r0 = project(9.0, wy, 7.0)
    draw.line([p_l0, p_l1], fill=(135, 125, 110, 255), width=2)
    draw.line([p_l1, p_r0], fill=(115, 105, 90, 255), width=2)
# 4. Upper Shaft [7.25, 11.0, 7.25] to [8.75, 22.0, 8.75]
draw_cube([7.25, 11.0, 7.25], [8.75, 22.0, 8.75], (198, 139, 89, 255), (150, 102, 60, 255), (115, 76, 44, 255), (70, 45, 25, 255))
# 5. Upper Cap [7.0, 22.0, 7.0] to [9.0, 23.0, 9.0]
draw_cube([7.0, 22.0, 7.0], [9.0, 23.0, 9.0], (110, 85, 62, 255), (85, 62, 45, 255), (60, 44, 32, 255), (40, 30, 20, 255))

# Anotasi Model Units (Bukan meter)
p_piv = project(8.0, 8.0, 8.0)
draw.ellipse([(p_piv[0]-5, p_piv[1]-5), (p_piv[0]+5, p_piv[1]+5)], fill=(255, 70, 70, 255), outline=(255, 255, 255, 255))
draw.line([(p_piv[0]+5, p_piv[1]), (p_piv[0]+45, p_piv[1])], fill=(255, 100, 100, 255), width=2)
draw.text((p_piv[0]+50, p_piv[1]-8), "Center Pivot [8.0, 8.0, 8.0] (Hand Grip Point)", fill=(255, 150, 150, 255))

dim_top = project(4.0, 23.0, 8.0)
dim_bot = project(4.0, -7.0, 8.0)
draw.line([dim_top, dim_bot], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_top[0]-8, dim_top[1]), (dim_top[0]+8, dim_top[1])], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_bot[0]-8, dim_bot[1]), (dim_bot[0]+8, dim_bot[1])], fill=(100, 130, 180, 255), width=2)
draw.text((dim_top[0]-145, (dim_top[1]+dim_bot[1])//2 - 16), "Panjang Model: 30 Units", fill=(140, 175, 230, 255))
draw.text((dim_top[0]-145, (dim_top[1]+dim_bot[1])//2 + 2), "(Skala visual dimodulasi display transform)", fill=(110, 140, 180, 255))

# Right panel: UV map
draw.rectangle([(650, 105), (960, 420)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 120), "REVISED TEXTURE UV MAP (32x32 PNG)", fill=(240, 240, 245, 255))
tex_scaled = tex_img.resize((224, 224), Image.NEAREST)
img.paste(tex_scaled, (670, 150), tex_scaled)
draw.rectangle([(670, 150), (894, 374)], outline=(80, 90, 115, 255), width=1)
draw.text((670, 385), "4 Kuadran: Batang Kayu | Kain Linen | Ujung Kayu | Aksen Serat", fill=(130, 140, 160, 255))

# Specs panel
draw.rectangle([(650, 440), (960, 710)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 455), "SPESIFIKASI TEKNIS MODEL v0.2", fill=(240, 240, 245, 255))

specs = [
    ("Target Platform:", "Minecraft Java Edition 1.21.1"),
    ("Namespace Resmi:", "avatar_elements (sesuai D009)"),
    ("Model Identifier:", "avatar_elements:air_staff"),
    ("Total Elemen:", "5 Kubus (Batang + Grip + Ujung)"),
    ("Panjang Model:", "30 Unit Model Grid (Y: -7 s/d +23)"),
    ("Tebal Poros Batang:", "1.5 x 1.5 Unit"),
    ("Tebal Balutan Grip:", "2.0 x 2.0 Unit (Panjang 6 Unit)"),
    ("Palet Tekstur:", "Kayu Ash Alami + Kain Linen Krem"),
    ("Ornamen Logam/Glider:", "DIHAPUS (100% Sesuai Brief Sederhana)")
]

y_pos = 485
for label, val in specs:
    draw.text((670, y_pos), label, fill=(140, 150, 170, 255))
    draw.text((810, y_pos), val, fill=(220, 225, 235, 255))
    y_pos += 22

preview_v02_path = os.path.join(out_dir, "preview_model_v02.png")
img.save(preview_v02_path, "PNG")
print("Saved revised model preview render to:", preview_v02_path)
