import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff"

# Load texture
tex_path = os.path.join(out_dir, "air_staff.png")
tex = Image.open(tex_path).convert("RGBA")

# -------------------------------------------------------------
# 1. RENDER 3D ISOMETRIC / ORTHOGRAPHIC MODEL PREVIEW
# -------------------------------------------------------------
W, H = 1000, 750
img = Image.new("RGBA", (W, H), (24, 26, 32, 255))
draw = ImageDraw.Draw(img)

# Title & Info
draw.text((40, 30), "AIR NOMAD STAFF (TONGKAT UDARA) — MODEL PREVIEW v0.1", fill=(240, 240, 245, 255))
draw.text((40, 55), "Source: air_staff.bbmodel | Minecraft 1.21.1 Java Model: air_staff.json | Texture: 32x32 PNG", fill=(140, 150, 170, 255))
draw.text((40, 75), "Brief Rule: Traditional Straight Wooden Staff | No Glider | No Excess Ornaments", fill=(210, 175, 100, 255))

# Draw Grid / Canvas for model
draw.rectangle([(40, 110), (620, 700)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)

# Isometric projection math:
# Project 3D coordinate (x, y, z) relative to pivot (8, 8, 8)
# iso_x = cx + (x - z) * scale * cos(30 deg)
# iso_y = cy - (y - 8) * scale + (x + z - 16) * scale * sin(30 deg)
cx = 330
cy = 405
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
    
    # 8 vertices
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
    
    # Top face (Y = y1)
    draw.polygon([v['p010'], v['p110'], v['p111'], v['p011']], fill=top_color, outline=outline_color)
    # Left face (Z = z1)
    draw.polygon([v['p001'], v['p101'], v['p111'], v['p011']], fill=left_color, outline=outline_color)
    # Right face (X = x1)
    draw.polygon([v['p100'], v['p101'], v['p111'], v['p110']], fill=right_color, outline=outline_color)

# Draw ground shadow
shadow_pts = [
    project(6.0, -8.5, 6.0),
    project(10.0, -8.5, 6.0),
    project(10.0, -8.5, 10.0),
    project(6.0, -8.5, 10.0)
]
draw.polygon(shadow_pts, fill=(20, 22, 28, 200))

# 1. Lower Cap [7, -7, 7] to [9, -6, 9]
draw_cube([7.0, -7.0, 7.0], [9.0, -6.0, 9.0], 
          top_color=(100, 75, 55, 255), left_color=(75, 54, 38, 255), right_color=(55, 40, 28, 255), outline_color=(40, 30, 20, 255))

# 2. Lower Shaft [7.25, -6.0, 7.25] to [8.75, 5.0, 8.75]
draw_cube([7.25, -6.0, 7.25], [8.75, 5.0, 8.75],
          top_color=(198, 139, 89, 255), left_color=(150, 102, 60, 255), right_color=(115, 76, 44, 255), outline_color=(70, 45, 25, 255))

# 3. Grip Linen Cloth [7.0, 5.0, 7.0] to [9.0, 11.0, 9.0]
draw_cube([7.0, 5.0, 7.0], [9.0, 11.0, 9.0],
          top_color=(234, 230, 223, 255), left_color=(205, 198, 185, 255), right_color=(165, 155, 140, 255), outline_color=(100, 92, 80, 255))

# Draw wrap stripes on grip
for wy in range(6, 11, 2):
    p_l0 = project(7.0, wy, 9.0)
    p_l1 = project(9.0, wy, 9.0)
    p_r0 = project(9.0, wy, 7.0)
    draw.line([p_l0, p_l1], fill=(135, 125, 110, 255), width=2)
    draw.line([p_l1, p_r0], fill=(115, 105, 90, 255), width=2)

# 4. Upper Shaft [7.25, 11.0, 7.25] to [8.75, 22.0, 8.75]
draw_cube([7.25, 11.0, 7.25], [8.75, 22.0, 8.75],
          top_color=(198, 139, 89, 255), left_color=(150, 102, 60, 255), right_color=(115, 76, 44, 255), outline_color=(70, 45, 25, 255))

# 5. Upper Cap [7.0, 22.0, 7.0] to [9.0, 23.0, 9.0]
draw_cube([7.0, 22.0, 7.0], [9.0, 23.0, 9.0],
          top_color=(110, 85, 62, 255), left_color=(85, 62, 45, 255), right_color=(60, 44, 32, 255), outline_color=(40, 30, 20, 255))

# Annotation pointers on model
# Pivot point marker
p_piv = project(8.0, 8.0, 8.0)
draw.ellipse([(p_piv[0]-5, p_piv[1]-5), (p_piv[0]+5, p_piv[1]+5)], fill=(255, 70, 70, 255), outline=(255, 255, 255, 255))
draw.line([(p_piv[0]+5, p_piv[1]), (p_piv[0]+45, p_piv[1])], fill=(255, 100, 100, 255), width=2)
draw.text((p_piv[0]+50, p_piv[1]-8), "Center Pivot [8.0, 8.0, 8.0] (Hand Grip Point)", fill=(255, 150, 150, 255))

# Top Cap Annotation
p_top = project(8.0, 23.0, 8.0)
draw.line([(p_top[0]+5, p_top[1]), (p_top[0]+50, p_top[1]-20)], fill=(200, 180, 130, 255), width=2)
draw.text((p_top[0]+55, p_top[1]-28), "Upper Reinforced Cap (Y: +23.0, 2x2x1)", fill=(230, 210, 160, 255))

# Shaft Annotation
p_shaft = project(8.75, 16.5, 8.0)
draw.line([(p_shaft[0]+5, p_shaft[1]), (p_shaft[0]+45, p_shaft[1])], fill=(200, 150, 100, 255), width=2)
draw.text((p_shaft[0]+50, p_shaft[1]-8), "Shaft: Slender Ash Wood (1.5x1.5x11)", fill=(220, 180, 140, 255))

# Grip Annotation
p_grip = project(7.0, 8.0, 8.0)
draw.line([(p_grip[0]-5, p_grip[1]), (p_grip[0]-50, p_grip[1])], fill=(230, 230, 230, 255), width=2)
draw.text((p_grip[0]-190, p_grip[1]-8), "Linen Cloth Wrap (2x2x6)", fill=(240, 240, 240, 255))

# Bottom Cap Annotation
p_bot = project(8.0, -7.0, 8.0)
draw.line([(p_bot[0]+5, p_bot[1]), (p_bot[0]+50, p_bot[1]+20)], fill=(200, 180, 130, 255), width=2)
draw.text((p_bot[0]+55, p_bot[1]+12), "Lower Reinforced Cap (Y: -7.0, 2x2x1)", fill=(230, 210, 160, 255))

# Dimension bar on left
dim_top = project(4.0, 23.0, 8.0)
dim_bot = project(4.0, -7.0, 8.0)
draw.line([dim_top, dim_bot], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_top[0]-8, dim_top[1]), (dim_top[0]+8, dim_top[1])], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_bot[0]-8, dim_bot[1]), (dim_bot[0]+8, dim_bot[1])], fill=(100, 130, 180, 255), width=2)
draw.text((dim_top[0]-95, (dim_top[1]+dim_bot[1])//2 - 8), "Total: 30 Units (1.875m)", fill=(140, 175, 230, 255))

# -------------------------------------------------------------
# RIGHT SIDE: TEXTURE & SPECIFICATION INSETS
# -------------------------------------------------------------
# Texture preview panel
draw.rectangle([(650, 110), (960, 420)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 125), "TEXTURE UV MAP (32x32 PNG)", fill=(240, 240, 245, 255))

# Upscale 32x32 texture to 224x224 (7x nearest neighbor)
tex_scaled = tex.resize((224, 224), Image.NEAREST)
img.paste(tex_scaled, (670, 155), tex_scaled)
draw.rectangle([(670, 155), (894, 379)], outline=(80, 90, 115, 255), width=1)

draw.text((670, 390), "4 Quadrants: Wood Shaft | Linen Wrap | End Caps | Brass Accent", fill=(130, 140, 160, 255))

# Specs panel below
draw.rectangle([(650, 440), (960, 700)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 455), "MODEL SPECIFICATIONS", fill=(240, 240, 245, 255))

specs = [
    ("Target Platform:", "Minecraft Java Edition 1.21.1"),
    ("Item Slot:", "Mainhand & Offhand Weapon"),
    ("Model Type:", "Blockbench Free / Handheld 3D"),
    ("Total Elements:", "5 Cubes (Shafts + Grip + Caps)"),
    ("Total Length:", "30.0 Pixels / Units"),
    ("Shaft Caliber:", "1.5 x 1.5 Pixels (Slender)"),
    ("Grip Caliber:", "2.0 x 2.0 Pixels (6.0 Length)"),
    ("Glider/Wing Status:", "EXCLUDED (Strict Brief)"),
    ("Ornaments:", "NONE (Strict Brief Clean Design)")
]

y_pos = 485
for label, val in specs:
    draw.text((670, y_pos), label, fill=(140, 150, 170, 255))
    draw.text((800, y_pos), val, fill=(220, 225, 235, 255))
    y_pos += 22

preview_path = os.path.join(out_dir, "preview_model.png")
img.save(preview_path, "PNG")
print("Saved model preview render to:", preview_path)

# -------------------------------------------------------------
# 2. RENDER ITEM TRANSFORMS PREVIEW
# -------------------------------------------------------------
W2, H2 = 1000, 600
img2 = Image.new("RGBA", (W2, H2), (24, 26, 32, 255))
draw2 = ImageDraw.Draw(img2)

draw2.text((40, 30), "AIR STAFF — ITEM DISPLAY TRANSFORMS MATRIX (1.21.1)", fill=(240, 240, 245, 255))
draw2.text((40, 55), "Evaluates Handheld Alignment: thirdperson, firstperson, gui, ground, fixed", fill=(140, 150, 170, 255))

panels = [
    {
        "title": "thirdperson_righthand",
        "rect": (40, 95, 480, 320),
        "rot": "[0, -90, 55]",
        "trans": "[0.0, 4.0, 0.5]",
        "scale": "[0.85, 0.85, 0.85]",
        "desc": "Held firmly at center grip, staff tilted 55 deg back ready for martial arts strike / parry.",
        "angle": 55
    },
    {
        "title": "firstperson_righthand",
        "rect": (510, 95, 950, 320),
        "rot": "[0, -90, 25]",
        "trans": "[1.13, 3.2, 1.13]",
        "scale": "[0.68, 0.68, 0.68]",
        "desc": "Staff held diagonally on the right screen edge without obstructing player crosshair / sightline.",
        "angle": 25
    },
    {
        "title": "gui (Inventory / Hotbar)",
        "rect": (40, 340, 480, 565),
        "rot": "[0, 0, -45]",
        "trans": "[0.0, 0.0, 0.0]",
        "scale": "[0.55, 0.55, 0.55]",
        "desc": "Tilted 45 deg diagonally from top-left to bottom-right, standard Minecraft weapon GUI standard.",
        "angle": -45
    },
    {
        "title": "ground / fixed",
        "rect": (510, 340, 950, 565),
        "rot": "[0, 0, 0]",
        "trans": "[0.0, 3.0, 0.0]",
        "scale": "[0.5, 0.5, 0.5]",
        "desc": "Drops vertically onto ground with bottom cap resting cleanly above floor level.",
        "angle": 0
    }
]

for p in panels:
    x0, y0, x1, y1 = p["rect"]
    draw2.rectangle([x0, y0, x1, y1], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
    draw2.text((x0 + 15, y0 + 15), p["title"].upper(), fill=(240, 210, 120, 255))
    
    # Schematic stick drawing illustrating rotation
    mcx = x0 + 80
    mcy = y0 + 130
    rad = math.radians(p["angle"] + 90)
    slen = 60
    sx0 = mcx - slen * math.cos(rad)
    sy0 = mcy - slen * math.sin(rad)
    sx1 = mcx + slen * math.cos(rad)
    sy1 = mcy + slen * math.sin(rad)
    
    # Draw stick
    draw2.line([(sx0, sy0), (sx1, sy1)], fill=(166, 114, 68, 255), width=6)
    # Draw grip
    gx0 = mcx - 12 * math.cos(rad)
    gy0 = mcy - 12 * math.sin(rad)
    gx1 = mcx + 12 * math.cos(rad)
    gy1 = mcy + 12 * math.sin(rad)
    draw2.line([(gx0, gy0), (gx1, gy1)], fill=(234, 230, 223, 255), width=8)
    # Draw caps
    draw2.ellipse([(sx0-4, sy0-4), (sx0+4, sy0+4)], fill=(67, 48, 34, 255))
    draw2.ellipse([(sx1-4, sy1-4), (sx1+4, sy1+4)], fill=(67, 48, 34, 255))
    
    # Transform coordinates
    draw2.text((x0 + 170, y0 + 45), f"Rotation:    {p['rot']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 170, y0 + 70), f"Translation: {p['trans']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 170, y0 + 95), f"Scale:       {p['scale']}", fill=(180, 190, 210, 255))
    
    draw2.text((x0 + 170, y0 + 135), "Visual Result:", fill=(140, 150, 170, 255))
    # Word wrap description
    words = p["desc"].split(" ")
    line1 = ""
    line2 = ""
    for w in words:
        if len(line1 + " " + w) < 38:
            line1 += (" " if line1 else "") + w
        else:
            line2 += (" " if line2 else "") + w
    draw2.text((x0 + 170, y0 + 158), line1, fill=(220, 225, 235, 255))
    if line2:
        draw2.text((x0 + 170, y0 + 180), line2, fill=(220, 225, 235, 255))

preview_trans_path = os.path.join(out_dir, "preview_transforms.png")
img2.save(preview_trans_path, "PNG")
print("Saved transforms preview render to:", preview_trans_path)
