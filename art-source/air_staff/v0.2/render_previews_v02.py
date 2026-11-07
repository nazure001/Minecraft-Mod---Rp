import os
import json
import math
from PIL import Image, ImageDraw

out_dir = r"D:\repo\Minecraft Mod & Rp\art-source\air_staff\v0.2"
tex_path = os.path.join(out_dir, "air_staff_v02.png")
json_path = os.path.join(out_dir, "air_staff.json")

# 1. LOAD ASSETS DIRECTLY FROM SOURCE FILES
with open(json_path, "r", encoding="utf-8") as f:
    model_json = json.load(f)

display_slots = model_json.get("display", {})
elements_json = model_json.get("elements", [])

tex_img = Image.open(tex_path).convert("RGBA")
tex_pix = tex_img.load()

# ==============================================================================
# PREVIEW 1: MODEL GEOMETRY & TEXTURE PREVIEW (preview_model_v02.png)
# ==============================================================================
W, H = 1000, 750
img = Image.new("RGBA", (W, H), (24, 26, 32, 255))
draw = ImageDraw.Draw(img)

# Title & Metadata
draw.text((40, 25), "AIR NOMAD STAFF (TONGKAT UDARA) — PREVIEW MODEL ISOMETRIK v0.2", fill=(240, 240, 245, 255))
draw.text((40, 50), "Input: air_staff.json (Minecraft 1.21.1) & air_staff_v02.png (32x32 RGBA)", fill=(140, 150, 170, 255))
draw.text((40, 70), "Status Visual: MENUNGGU REVIEW (Sampling piksel murni dari tekstur dan geometri JSON)", fill=(230, 180, 80, 255))

# Viewport Box
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

# Ground Shadow
shadow_pts = [project(6.0, -8.5, 6.0), project(10.0, -8.5, 6.0), project(10.0, -8.5, 10.0), project(6.0, -8.5, 10.0)]
draw.polygon(shadow_pts, fill=(20, 22, 28, 200))

# Textured Face Rendering: sample pixels directly from air_staff_v02.png using JSON UV (converted 0..16 to 0..32)
def render_textured_face(face_type, from_pt, to_pt, uv_json, brightness):
    x0, y0, z0 = from_pt
    x1, y1, z1 = to_pt
    # Convert JSON normalized UV (0..16) to texture pixel space (0..32)
    u0 = uv_json[0] * 2.0
    v0 = uv_json[1] * 2.0
    u1 = uv_json[2] * 2.0
    v1 = uv_json[3] * 2.0
    
    du = int(round(abs(u1 - u0)))
    dv = int(round(abs(v1 - v0)))
    if du <= 0: du = 1
    if dv <= 0: dv = 1
    
    u_min = min(u0, u1)
    v_min = min(v0, v1)
    
    if face_type == "up":
        # y = y1, x from x0..x1, z from z0..z1
        for ix in range(du):
            for iz in range(dv):
                tx = int(u_min + ix) % 32
                ty = int(v_min + iz) % 32
                r, g, b, a = tex_pix[tx, ty]
                cr = int(r * brightness)
                cg = int(g * brightness)
                cb = int(b * brightness)
                
                wx0 = x0 + (x1 - x0) * (ix / du)
                wx1 = x0 + (x1 - x0) * ((ix + 1) / du)
                wz0 = z0 + (z1 - z0) * (iz / dv)
                wz1 = z0 + (z1 - z0) * ((iz + 1) / dv)
                
                p0 = project(wx0, y1, wz0)
                p1 = project(wx1, y1, wz0)
                p2 = project(wx1, y1, wz1)
                p3 = project(wx0, y1, wz1)
                draw.polygon([p0, p1, p2, p3], fill=(cr, cg, cb, a))
                
    elif face_type == "south":
        # z = z1, x from x0..x1, y from y0..y1
        for ix in range(du):
            for iy in range(dv):
                tx = int(u_min + ix) % 32
                ty = int(v_min + iy) % 32
                r, g, b, a = tex_pix[tx, ty]
                cr = int(r * brightness)
                cg = int(g * brightness)
                cb = int(b * brightness)
                
                wx0 = x0 + (x1 - x0) * (ix / du)
                wx1 = x0 + (x1 - x0) * ((ix + 1) / du)
                wy1 = y1 - (y1 - y0) * (iy / dv)
                wy0 = y1 - (y1 - y0) * ((iy + 1) / dv)
                
                p0 = project(wx0, wy0, z1)
                p1 = project(wx1, wy0, z1)
                p2 = project(wx1, wy1, z1)
                p3 = project(wx0, wy1, z1)
                draw.polygon([p0, p1, p2, p3], fill=(cr, cg, cb, a))
                
    elif face_type == "east":
        # x = x1, z from z1..z0, y from y0..y1
        for iz in range(du):
            for iy in range(dv):
                tx = int(u_min + iz) % 32
                ty = int(v_min + iy) % 32
                r, g, b, a = tex_pix[tx, ty]
                cr = int(r * brightness)
                cg = int(g * brightness)
                cb = int(b * brightness)
                
                wz0 = z0 + (z1 - z0) * (iz / du)
                wz1 = z0 + (z1 - z0) * ((iz + 1) / du)
                wy1 = y1 - (y1 - y0) * (iy / dv)
                wy0 = y1 - (y1 - y0) * ((iy + 1) / dv)
                
                p0 = project(x1, wy0, wz0)
                p1 = project(x1, wy0, wz1)
                p2 = project(x1, wy1, wz1)
                p3 = project(x1, wy1, wz0)
                draw.polygon([p0, p1, p2, p3], fill=(cr, cg, cb, a))

# Render each element directly from air_staff.json
for el in elements_json:
    f_pt = el["from"]
    t_pt = el["to"]
    faces = el["faces"]
    
    # 1. South face (front-left in iso)
    if "south" in faces:
        render_textured_face("south", f_pt, t_pt, faces["south"]["uv"], 0.85)
    # 2. East face (front-right in iso)
    if "east" in faces:
        render_textured_face("east", f_pt, t_pt, faces["east"]["uv"], 0.70)
    # 3. Up face (top in iso)
    if "up" in faces:
        render_textured_face("up", f_pt, t_pt, faces["up"]["uv"], 1.00)

# Wireframe silhouette for crisp edges (sampled strictly from JSON geometry)
for el in elements_json:
    x0, y0, z0 = el["from"]
    x1, y1, z1 = el["to"]
    draw.line([project(x0, y1, z0), project(x1, y1, z0)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x1, y1, z0), project(x1, y1, z1)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x1, y1, z1), project(x0, y1, z1)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x0, y1, z1), project(x0, y1, z0)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x1, y0, z1), project(x1, y1, z1)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x0, y0, z1), project(x1, y0, z1)], fill=(30, 25, 20, 160), width=1)
    draw.line([project(x1, y0, z0), project(x1, y0, z1)], fill=(30, 25, 20, 160), width=1)

# Annotations (Strictly honest, no gameplay claims)
p_piv = project(8.0, 8.0, 8.0)
draw.ellipse([(p_piv[0]-5, p_piv[1]-5), (p_piv[0]+5, p_piv[1]+5)], fill=(255, 70, 70, 255), outline=(255, 255, 255, 255))
draw.line([(p_piv[0]+5, p_piv[1]), (p_piv[0]+45, p_piv[1])], fill=(255, 100, 100, 255), width=2)
draw.text((p_piv[0]+50, p_piv[1]-8), "Pivot Model [8.0, 8.0, 8.0] (Pusat rotasi matematis; posisi genggaman MENUNGGU REVIEW)", fill=(255, 160, 160, 255))

dim_top = project(4.0, 23.0, 8.0)
dim_bot = project(4.0, -7.0, 8.0)
draw.line([dim_top, dim_bot], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_top[0]-8, dim_top[1]), (dim_top[0]+8, dim_top[1])], fill=(100, 130, 180, 255), width=2)
draw.line([(dim_bot[0]-8, dim_bot[1]), (dim_bot[0]+8, dim_bot[1])], fill=(100, 130, 180, 255), width=2)
draw.text((dim_top[0]-145, (dim_top[1]+dim_bot[1])//2 - 16), "Panjang Model: 30 Units", fill=(140, 175, 230, 255))
draw.text((dim_top[0]-145, (dim_top[1]+dim_bot[1])//2 + 2), "(Skala visual dimodulasi display transform)", fill=(110, 140, 180, 255))

# Right panel: Texture & UV mapping
draw.rectangle([(650, 105), (960, 420)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 120), "ASSET TEKSTUR AKTUAL (32x32 PNG)", fill=(240, 240, 245, 255))
tex_scaled = tex_img.resize((224, 224), Image.NEAREST)
img.paste(tex_scaled, (670, 150), tex_scaled)
draw.rectangle([(670, 150), (894, 374)], outline=(80, 90, 115, 255), width=1)
draw.text((670, 385), "4 Kuadran: Batang | Grip Linen | Tutup Kayu | Serat Kayu", fill=(130, 140, 160, 255))

# Technical Specs Panel
draw.rectangle([(650, 440), (960, 710)], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
draw.text((670, 455), "AUDIT SPESIFIKASI MODEL v0.2", fill=(240, 240, 245, 255))

specs = [
    ("Format File JSON:", "Minecraft Java Item Model (1.21.1)"),
    ("Model Identifier:", "avatar_elements:item/air_staff"),
    ("Total Elemen:", f"{len(elements_json)} Kubus dibaca dari JSON"),
    ("Rentang UV JSON:", "0.0 s/d 12.0 (Lolos batas 16.0)"),
    ("Panjang Model:", "30 Unit Model Grid (Y: -7 s/d +23)"),
    ("Tebal Poros Batang:", "1.5 x 1.5 Unit"),
    ("Tebal Grip Wrap:", "2.0 x 2.0 Unit (Panjang 6 Unit)"),
    ("Palet Tekstur:", "Kayu Ash Alami + Linen Krem"),
    ("Status Evaluasi Visual:", "MENUNGGU REVIEW ASET"),
    ("Status Runtime Game:", "BELUM DIMUAT DALAM RUNTIME")
]

y_pos = 482
for label, val in specs:
    draw.text((665, y_pos), label, fill=(140, 150, 170, 255))
    draw.text((800, y_pos), val, fill=(220, 225, 235, 255))
    y_pos += 21

preview_v02_path = os.path.join(out_dir, "preview_model_v02.png")
img.save(preview_v02_path, "PNG")
print("Saved revised model preview (direct from air_staff.json) to:", preview_v02_path)

# ==============================================================================
# PREVIEW 2: DISPLAY TRANSFORMS DIAGRAM (preview_transforms_v02.png)
# ==============================================================================
W2, H2 = 1000, 750
img2 = Image.new("RGBA", (W2, H2), (24, 26, 32, 255))
draw2 = ImageDraw.Draw(img2)

draw2.text((40, 20), "AIR STAFF — DIAGRAM TRANSFORMASI DISPLAY v0.2 (MINECRAFT 1.21.1)", fill=(240, 240, 245, 255))
draw2.text((40, 45), "DIAGRAM SKEMATIK PARAMETER (Bukan hasil render in-game; status: MENUNGGU REVIEW)", fill=(230, 180, 80, 255))
draw2.text((40, 65), "Slot display sesuai standar 1.21.1: ground dan fixed dipisahkan karena memiliki transform berbeda", fill=(140, 150, 170, 255))

panels = [
    {
        "title": "thirdperson_righthand",
        "rect": (40, 95, 480, 240),
        "rot": str(display_slots.get("thirdperson_righthand", {}).get("rotation")),
        "trans": str(display_slots.get("thirdperson_righthand", {}).get("translation")),
        "scale": str(display_slots.get("thirdperson_righthand", {}).get("scale")),
        "desc": "Diagram skematik genggaman tangan kanan pihak ketiga. Orientasi rotasi 55 deg. Skala 0.85x.",
        "angle": 55
    },
    {
        "title": "thirdperson_lefthand",
        "rect": (510, 95, 950, 240),
        "rot": str(display_slots.get("thirdperson_lefthand", {}).get("rotation")),
        "trans": str(display_slots.get("thirdperson_lefthand", {}).get("translation")),
        "scale": str(display_slots.get("thirdperson_lefthand", {}).get("scale")),
        "desc": "Diagram skematik genggaman tangan kiri pihak ketiga (cermin). Orientasi rotasi -55 deg. Skala 0.85x.",
        "angle": -55
    },
    {
        "title": "firstperson_righthand",
        "rect": (40, 255, 480, 400),
        "rot": str(display_slots.get("firstperson_righthand", {}).get("rotation")),
        "trans": str(display_slots.get("firstperson_righthand", {}).get("translation")),
        "scale": str(display_slots.get("firstperson_righthand", {}).get("scale")),
        "desc": "Diagram tampilan orang pertama kanan. Kemiringan 25 deg di tepi kanan agar tidak menghalangi FOV.",
        "angle": 25
    },
    {
        "title": "gui (Inventory / Hotbar)",
        "rect": (510, 255, 950, 400),
        "rot": str(display_slots.get("gui", {}).get("rotation")),
        "trans": str(display_slots.get("gui", {}).get("translation")),
        "scale": str(display_slots.get("gui", {}).get("scale")),
        "desc": "Diagram tampilan slot inventaris/hotbar. Rotasi -45 deg diagonal standar ikon item Minecraft.",
        "angle": -45
    },
    {
        "title": "ground (Item Jatuh di Blok)",
        "rect": (40, 415, 480, 560),
        "rot": str(display_slots.get("ground", {}).get("rotation")),
        "trans": str(display_slots.get("ground", {}).get("translation")),
        "scale": str(display_slots.get("ground", {}).get("scale")),
        "desc": "Item mengambang di atas tanah: rotasi [0, 0, 0], translasi vertikal Y=+3.0, skala 0.5x.",
        "angle": 0
    },
    {
        "title": "fixed (Item Frame / Dinding)",
        "rect": (510, 415, 950, 560),
        "rot": str(display_slots.get("fixed", {}).get("rotation")),
        "trans": str(display_slots.get("fixed", {}).get("translation")),
        "scale": str(display_slots.get("fixed", {}).get("scale")),
        "desc": "Item pada bingkai item frame: rotasi Y=180 deg menghadap depan bingkai, skala 0.7x.",
        "angle": 90
    }
]

for p in panels:
    x0, y0, x1, y1 = p["rect"]
    draw2.rectangle([x0, y0, x1, y1], fill=(32, 35, 44, 255), outline=(50, 56, 72, 255), width=2)
    draw2.text((x0 + 15, y0 + 12), p["title"].upper(), fill=(240, 210, 120, 255))
    
    # Schematic indicator
    mcx = x0 + 65
    mcy = y0 + 80
    rad = math.radians(p["angle"] + 90)
    slen = 40
    sx0 = mcx - slen * math.cos(rad)
    sy0 = mcy - slen * math.sin(rad)
    sx1 = mcx + slen * math.cos(rad)
    sy1 = mcy + slen * math.sin(rad)
    
    draw2.line([(sx0, sy0), (sx1, sy1)], fill=(166, 114, 68, 255), width=4)
    gx0 = mcx - 8 * math.cos(rad)
    gy0 = mcy - 8 * math.sin(rad)
    gx1 = mcx + 8 * math.cos(rad)
    gy1 = mcy + 8 * math.sin(rad)
    draw2.line([(gx0, gy0), (gx1, gy1)], fill=(213, 206, 191, 255), width=6)
    
    draw2.text((x0 + 140, y0 + 35), f"Rotation:    {p['rot']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 140, y0 + 55), f"Translation: {p['trans']}", fill=(180, 190, 210, 255))
    draw2.text((x0 + 140, y0 + 75), f"Scale:       {p['scale']}", fill=(180, 190, 210, 255))
    
    draw2.text((x0 + 140, y0 + 100), "Catatan:", fill=(140, 150, 170, 255))
    draw2.text((x0 + 195, y0 + 100), p["desc"], fill=(210, 215, 225, 255))

# Bottom warning banner
draw2.rectangle([(40, 580), (950, 720)], fill=(36, 32, 28, 255), outline=(180, 130, 60, 255), width=1)
draw2.text((60, 595), "STATUS EVALUASI VISUAL: MENUNGGU REVIEW ASET", fill=(240, 190, 80, 255))
draw2.text((60, 620), "- Parameter rotasi, translasi, dan skala di atas dibaca langsung dari air_staff.json.", fill=(200, 205, 215, 255))
draw2.text((60, 642), "- Diagram ini adalah diagram skematik parameter, BUKAN screenshot render dalam game.", fill=(200, 205, 215, 255))
draw2.text((60, 664), "- Posisi genggaman tangan aktual (hand-grip offset) dan kenyamanan sudut pandang kamera", fill=(200, 205, 215, 255))
draw2.text((60, 686), "  BELUM DIVERIFIKASI RUNTIME dan berstatus MENUNGGU REVIEW pada tahap peninjauan aset.", fill=(200, 205, 215, 255))

preview_trans_path = os.path.join(out_dir, "preview_transforms_v02.png")
img2.save(preview_trans_path, "PNG")
print("Saved revised display transforms diagram to:", preview_trans_path)
