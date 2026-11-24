import os
import json
import math
import random
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
SHOWCASE_DIR = os.path.join(REPO_ROOT, "art-source", "showcase")
TEXTURES_DIR = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity")
os.makedirs(SHOWCASE_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. TEXTURE ATLAS PAINTERS (128x128 RGBA)
# -----------------------------------------------------------------------------

def create_flying_bison_texture():
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pix = img.load()
    
    # Base Fur Colors
    c_fur_light = (244, 238, 222, 255)
    c_fur_mid   = (232, 223, 199, 255)
    c_fur_dark  = (213, 200, 168, 255)
    c_fur_shade = (185, 172, 142, 255)
    c_belly     = (220, 212, 190, 255)
    
    # Arrow & Marking Colors (Air Nomad Brown Chevron)
    c_arrow     = (99, 72, 50, 255)
    c_arrow_d   = (70, 50, 34, 255)
    c_arrow_l   = (125, 92, 65, 255)
    
    # Horn Colors
    c_horn      = (65, 50, 40, 255)
    c_horn_l    = (95, 75, 60, 255)
    c_horn_d    = (45, 35, 28, 255)
    
    # Nose & Claws
    c_nose      = (55, 45, 45, 255)
    c_nostril   = (25, 20, 20, 255)
    c_claws     = (75, 70, 68, 255)
    
    # Harness & Saddle (Burgundy & Brass)
    c_leather   = (122, 32, 33, 255)
    c_leather_d = (88, 22, 23, 255)
    c_brass     = (224, 168, 56, 255)

    # 1. Head Region (UV: x=0..48, y=0..40)
    for y in range(0, 40):
        for x in range(0, 48):
            noise = (math.sin(x * 0.8) + math.cos(y * 0.8)) * 0.5
            base_col = c_fur_light if noise > 0.2 else (c_fur_mid if noise > -0.2 else c_fur_dark)
            pix[x, y] = base_col
            
    # Forehead Arrow on Head top/front
    for y in range(6, 26):
        w = int(2 + (26 - y) * 0.5) # Arrow widens towards rear
        for x in range(24 - w, 24 + w):
            pix[x, y] = c_arrow if (x + y) % 2 == 0 else c_arrow_d
    # Arrow tip
    draw.polygon([(24, 28), (21, 24), (27, 24)], fill=c_arrow)

    # Eyes & Cheeks
    pix[14, 20] = (30, 25, 25, 255)
    pix[15, 20] = (200, 190, 180, 255) # catchlight
    pix[33, 20] = (30, 25, 25, 255)
    pix[32, 20] = (200, 190, 180, 255)

    # 2. Snout Region (UV: x=48..80, y=0..24)
    draw.rectangle([48, 0, 80, 24], fill=c_fur_dark)
    # Nose pad
    draw.rectangle([58, 6, 70, 16], fill=c_nose)
    draw.rectangle([60, 10, 62, 14], fill=c_nostril)
    draw.rectangle([66, 10, 68, 14], fill=c_nostril)
    # Fur tufts around mouth
    for x in range(48, 80, 2):
        pix[x, 22] = c_fur_light

    # 3. Horns (UV: x=80..112, y=0..32)
    for y in range(0, 32):
        for x in range(80, 112):
            ring = int((y + x * 0.3) % 4)
            col = c_horn_l if ring == 0 else (c_horn if ring < 3 else c_horn_d)
            pix[x, y] = col

    # 4. Body Main (UV: x=0..64, y=40..100)
    for y in range(40, 100):
        for x in range(0, 64):
            # Gradient: back darker, belly lighter
            grad = (y - 40) / 60.0
            r = int(c_fur_light[0] * (1 - grad * 0.15))
            g = int(c_fur_light[1] * (1 - grad * 0.18))
            b = int(c_fur_light[2] * (1 - grad * 0.22))
            # Fur stipple noise
            if (x * 7 + y * 13) % 5 == 0:
                r -= 8; g -= 8; b -= 8
            pix[x, y] = (r, g, b, 255)
            
    # Dorsal Spine Arrow Stripe down back
    for y in range(40, 95):
        for x in range(28, 36):
            pix[x, y] = c_arrow if (x + y) % 3 != 0 else c_arrow_d

    # 5. Tail (Beaver paddle with chevron bands) (UV: x=64..100, y=40..80)
    draw.rectangle([64, 40, 100, 80], fill=c_fur_mid)
    # Chevron stripe bands on tail
    for y in range(44, 76, 8):
        draw.polygon([(82, y), (70, y + 6), (74, y + 6), (82, y + 2), (90, y + 6), (94, y + 6)], fill=c_arrow)

    # 6. Legs (6 legs) (UV: x=0..64, y=100..128)
    for y in range(100, 128):
        for x in range(0, 64):
            pix[x, y] = c_fur_mid if (x + y) % 3 != 0 else c_fur_shade
    # Claws at bottom
    draw.rectangle([0, 124, 64, 127], fill=c_claws)

    # 7. Saddle & Harness (UV: x=64..128, y=80..128)
    draw.rectangle([64, 80, 128, 128], fill=c_leather)
    for x in range(64, 128, 6):
        draw.rectangle([x, 82, x + 2, 126], fill=c_leather_d)
    # Brass buckles
    for y in range(86, 126, 12):
        draw.rectangle([70, y, 76, y + 4], fill=c_brass)
        draw.rectangle([116, y, 122, y + 4], fill=c_brass)

    return img


def create_platypus_bear_texture():
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    pix = img.load()
    draw = ImageDraw.Draw(img)
    
    # Bear Fur Colors
    c_fur_dark  = (68, 40, 24, 255)
    c_fur_mid   = (90, 56, 37, 255)
    c_fur_light = (112, 71, 48, 255)
    c_chest     = (138, 96, 64, 255)
    
    # Leathery Platypus Duck-Bill Colors (Deep Olive-Teal)
    c_bill_base = (47, 82, 74, 255)
    c_bill_mid  = (59, 101, 91, 255)
    c_bill_dark = (31, 56, 50, 255)
    c_bill_edge = (74, 124, 112, 255)
    
    # Scales / Tail Colors
    c_scale_d   = (40, 24, 14, 255)
    c_scale_l   = (58, 36, 24, 255)
    c_claw      = (220, 208, 186, 255)

    # 1. Bear Head (UV: 0..48, 0..40)
    for y in range(0, 40):
        for x in range(0, 48):
            noise = (math.sin(x * 0.9) * math.cos(y * 0.7)) * 0.5
            col = c_fur_light if noise > 0.15 else (c_fur_mid if noise > -0.15 else c_fur_dark)
            pix[x, y] = col
    # Intense small bear eyes
    pix[14, 16] = (20, 15, 12, 255); pix[15, 16] = (180, 140, 60, 255)
    pix[33, 16] = (20, 15, 12, 255); pix[32, 16] = (180, 140, 60, 255)
    # Rounded Ears
    draw.rectangle([6, 2, 14, 10], fill=c_fur_dark)
    draw.rectangle([8, 4, 12, 8], fill=(50, 30, 18, 255))
    draw.rectangle([34, 2, 42, 10], fill=c_fur_dark)
    draw.rectangle([36, 4, 40, 8], fill=(50, 30, 18, 255))

    # 2. Platypus Bill (UV: 48..88, 0..32)
    for y in range(0, 32):
        for x in range(48, 88):
            leathery = (math.sin(x * 1.2) + math.sin(y * 1.5)) * 0.4
            bcol = c_bill_mid if leathery > 0.1 else (c_bill_base if leathery > -0.1 else c_bill_dark)
            pix[x, y] = bcol
    # Dark bill border & nostrils
    draw.rectangle([48, 0, 88, 2], fill=c_bill_dark)
    draw.rectangle([48, 30, 88, 31], fill=c_bill_edge)
    draw.rectangle([60, 12, 64, 18], fill=c_bill_dark)
    draw.rectangle([72, 12, 76, 18], fill=c_bill_dark)

    # 3. Heavy Bear Torso & Shoulder Mane (UV: 0..64, 40..100)
    for y in range(40, 100):
        for x in range(0, 64):
            # Shoulder mane thicker on top
            is_mane = y < 65
            base = c_fur_dark if is_mane else c_fur_mid
            # Chest patch in front center
            is_chest = (20 <= x <= 44) and (60 <= y <= 85)
            if is_chest:
                pix[x, y] = c_chest if (x + y) % 3 != 0 else c_fur_light
            else:
                fur_jitter = (x * 11 + y * 7) % 7
                r = base[0] + (fur_jitter - 3) * 3
                g = base[1] + (fur_jitter - 3) * 3
                b = base[2] + (fur_jitter - 3) * 3
                pix[x, y] = (r, g, b, 255)

    # 4. Platypus Flat Beaver Tail (UV: 64..104, 40..80)
    for y in range(40, 80):
        for x in range(64, 104):
            # Crosshatch leathery scales
            scale_grid = (x // 3 + y // 3) % 2 == 0
            pix[x, y] = c_scale_l if scale_grid else c_scale_d

    # 5. Bear Paws & Claws (UV: 0..64, 100..128)
    draw.rectangle([0, 100, 64, 122], fill=c_fur_dark)
    # Long curved digging claws
    for x in range(4, 60, 6):
        draw.rectangle([x, 122, x + 2, 127], fill=c_claw)

    return img


def create_phoenix_king_ozai_textures():
    # Diffuse Albedo
    albedo = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_pix = albedo.load()
    a_draw = ImageDraw.Draw(albedo)
    
    # Emissive Glow Map (OptiFine / Iris / Sodium)
    glow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    g_pix = glow.load()
    
    # Palette
    c_skin_base = (245, 214, 184, 255)
    c_skin_shad = (226, 184, 146, 255)
    c_hair_dark = (26, 24, 28, 255)
    c_hair_mid  = (40, 36, 42, 255)
    
    c_robe_crimson = (158, 26, 26, 255)
    c_robe_dark    = (125, 18, 18, 255)
    c_robe_bright  = (191, 36, 36, 255)
    c_tunic_black  = (32, 30, 35, 255)
    
    c_gold_bright  = (243, 202, 62, 255)
    c_gold_mid     = (212, 175, 55, 255)
    c_gold_dark    = (140, 109, 20, 255)
    
    # Glowing Eye / Flame Chi
    c_glow_eye     = (255, 210, 42, 255)
    c_glow_white   = (255, 255, 240, 255)

    # 1. Head & Face (UV: 0..32, 0..32)
    for y in range(0, 32):
        for x in range(0, 32):
            a_pix[x, y] = c_skin_base if (x + y) % 4 != 0 else c_skin_shad
    # Facial Features: Goatee, Stern Mouth, Eyebrows
    a_draw.rectangle([10, 24, 22, 29], fill=c_hair_dark) # Goatee
    a_draw.line([(12, 22), (20, 22)], fill=(120, 70, 60, 255), width=1) # Mouth
    a_draw.line([(8, 13), (14, 14)], fill=c_hair_dark, width=2) # Left Eyebrow
    a_draw.line([(18, 14), (24, 13)], fill=c_hair_dark, width=2) # Right Eyebrow
    # Searing Amber Chi Eyes
    a_pix[10, 16] = c_glow_eye; a_pix[11, 16] = c_glow_white
    a_pix[21, 16] = c_glow_eye; a_pix[22, 16] = c_glow_white
    # Eye Glow in emissive map
    g_pix[10, 16] = (255, 255, 255, 255); g_pix[11, 16] = (255, 255, 255, 255)
    g_pix[21, 16] = (255, 255, 255, 255); g_pix[22, 16] = (255, 255, 255, 255)

    # 2. Golden Fire Lord Crown & Hair Topknot (UV: 32..64, 0..32)
    a_draw.rectangle([32, 0, 64, 32], fill=c_hair_dark)
    # Golden Crown Crest (Flame Trident)
    a_draw.rectangle([40, 4, 56, 16], fill=c_gold_mid)
    a_draw.polygon([(48, 0), (44, 6), (52, 6)], fill=c_gold_bright) # Center spike
    a_draw.polygon([(42, 2), (40, 6), (44, 6)], fill=c_gold_bright) # Left spike
    a_draw.polygon([(54, 2), (52, 6), (56, 6)], fill=c_gold_bright) # Right spike
    # Crown Gem Glow
    a_pix[48, 8] = (255, 50, 50, 255)
    g_pix[48, 8] = (255, 255, 255, 255)

    # 3. Imperial Dragon Robes Torso (UV: 0..64, 32..80)
    for y in range(32, 80):
        for x in range(0, 64):
            # Center under-tunic black
            if 26 <= x <= 38:
                a_pix[x, y] = c_tunic_black if (x + y) % 3 != 0 else (45, 42, 50, 255)
            else:
                # Crimson outer robes with shading
                col = c_robe_bright if (y % 4 == 0) else (c_robe_crimson if x % 2 == 0 else c_robe_dark)
                a_pix[x, y] = col
    # Gold Embroidered Robe Edges
    a_draw.rectangle([24, 32, 26, 80], fill=c_gold_bright)
    a_draw.rectangle([38, 32, 40, 80], fill=c_gold_bright)
    # Imperial Dragon Crest on Chest
    a_draw.ellipse([27, 44, 37, 54], outline=c_gold_bright, fill=c_gold_dark, width=1)
    a_pix[32, 49] = (255, 220, 100, 255)
    g_pix[32, 49] = (200, 200, 200, 255) # Soft glow on dragon medallion

    # 4. Flaring Golden Pauldrons (UV: 64..96, 32..64)
    for y in range(32, 64):
        for x in range(64, 96):
            sh = int(c_gold_mid[0] * (1.0 - (y - 32) * 0.01))
            a_pix[x, y] = (sh, int(sh * 0.82), int(sh * 0.25), 255)
    # Sharp layered edges
    for y in range(36, 64, 8):
        a_draw.line([(64, y), (96, y)], fill=c_gold_bright, width=2)

    # 5. Robe Lower / Skirt (UV: 0..64, 80..128)
    for y in range(80, 128):
        for x in range(0, 64):
            grad = (y - 80) / 48.0
            r = int(c_robe_crimson[0] * (1.0 - grad * 0.3))
            g = int(c_robe_crimson[1] * (1.0 - grad * 0.3))
            b = int(c_robe_crimson[2] * (1.0 - grad * 0.3))
            a_pix[x, y] = (r, g, b, 255)
    # Gold hem border
    a_draw.rectangle([0, 122, 64, 126], fill=c_gold_bright)

    # 6. Arms & Bracers (UV: 64..128, 64..128)
    a_draw.rectangle([64, 64, 128, 100], fill=c_robe_crimson)
    # Gold Bracers with Fire Chi Emitters
    a_draw.rectangle([64, 100, 128, 120], fill=c_gold_mid)
    for x in range(68, 128, 16):
        a_draw.rectangle([x, 104, x + 6, 116], fill=(255, 120, 20, 255))
        g_pix[x + 1, 110] = (255, 255, 255, 255)
        g_pix[x + 2, 110] = (255, 255, 255, 255)

    return albedo, glow


# -----------------------------------------------------------------------------
# 2. SOFTWARE 3D ISOMETRIC RENDERER
# -----------------------------------------------------------------------------

def project_iso(x, y, z, cx, cy, scale):
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    px = cx + (x - z) * scale * cos30
    py = cy - y * scale + (x + z) * scale * sin30
    return (px, py)

def render_cube(draw, tex_pix, tex_w, tex_h, origin, size, uv_rect, cx, cy, scale, rot_y=0):
    ox, oy, oz = origin
    sx, sy, sz = size
    
    # Simple Y rotation around local center
    def rot(x, y, z):
        if rot_y == 0: return x, y, z
        rad = math.radians(rot_y)
        rx = x * math.cos(rad) + z * math.sin(rad)
        rz = -x * math.sin(rad) + z * math.cos(rad)
        return rx, y, rz

    # Corners
    c000 = rot(ox, oy, oz)
    c100 = rot(ox + sx, oy, oz)
    c110 = rot(ox + sx, oy + sy, oz)
    c010 = rot(ox, oy + sy, oz)
    c001 = rot(ox, oy, oz + sz)
    c101 = rot(ox + sx, oy, oz + sz)
    c111 = rot(ox + sx, oy + sy, oz + sz)
    c011 = rot(ox, oy + sy, oz + sz)
    
    # Project to 2D
    p000 = project_iso(c000[0], c000[1], c000[2], cx, cy, scale)
    p100 = project_iso(c100[0], c100[1], c100[2], cx, cy, scale)
    p110 = project_iso(c110[0], c110[1], c110[2], cx, cy, scale)
    p010 = project_iso(c010[0], c010[1], c010[2], cx, cy, scale)
    p001 = project_iso(c001[0], c001[1], c001[2], cx, cy, scale)
    p101 = project_iso(c101[0], c101[1], c101[2], cx, cy, scale)
    p111 = project_iso(c111[0], c111[1], c111[2], cx, cy, scale)
    p011 = project_iso(c011[0], c011[1], c011[2], cx, cy, scale)

    # Sample color from UV rect center
    ux0, uy0, ux1, uy1 = uv_rect
    tx = int((ux0 + ux1) * 0.5) % tex_w
    ty = int((uy0 + uy1) * 0.5) % tex_h
    base_color = tex_pix[tx, ty]
    if len(base_color) == 4 and base_color[3] == 0:
        base_color = (180, 160, 140, 255)

    def shade(col, factor):
        return (int(col[0] * factor), int(col[1] * factor), int(col[2] * factor), 255)

    # Draw visible faces in isometric projection (Top, South, East)
    # 1. Top face (Up) -> Factor 1.05
    draw.polygon([p010, p110, p111, p011], fill=shade(base_color, 1.05), outline=shade(base_color, 0.75))
    # 2. South face (Front-Left) -> Factor 0.85
    draw.polygon([p001, p101, p111, p011], fill=shade(base_color, 0.85), outline=shade(base_color, 0.65))
    # 3. East face (Front-Right) -> Factor 0.70
    draw.polygon([p100, p101, p111, p110], fill=shade(base_color, 0.70), outline=shade(base_color, 0.55))


def render_mob_showcase(mob_name, title, category, element, cubes, tex_img, old_tex_img, glow_img=None):
    W, H = 1200, 800
    canvas = Image.new("RGBA", (W, H), (20, 24, 30, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Header Banner
    draw.rectangle([0, 0, W, 80], fill=(28, 34, 44, 255))
    draw.line([0, 80, W, 80], fill=(60, 72, 92, 255), width=2)
    
    draw.text((40, 18), f"AVATAR: ELEMENTS — 3D MOB MOCKUP SHOWCASE", fill=(240, 242, 248, 255))
    draw.text((40, 44), f"Target: {title} | Kategori: {category} | Elemen: {element} | Format: Minecraft Java 1.21.1 / GeckoLib", fill=(160, 175, 195, 255))
    
    # 1. Left Panel: Before vs After Textures
    # Before Placeholder Box
    draw.rectangle([40, 110, 280, 420], fill=(26, 30, 38, 255), outline=(50, 58, 74, 255), width=2)
    draw.text((50, 120), "SEBELUM (Placeholder)", fill=(220, 100, 100, 255))
    draw.text((50, 138), "Hanya 5 warna flat (476 bytes)", fill=(140, 150, 165, 255))
    old_resized = old_tex_img.resize((200, 200), Image.NEAREST)
    canvas.paste(old_resized, (60, 170))
    
    # After Rich Texture Box
    draw.rectangle([40, 440, 280, 750], fill=(26, 30, 38, 255), outline=(50, 58, 74, 255), width=2)
    draw.text((50, 450), "SESUDAH (Rich AAA Cel-Shaded)", fill=(100, 220, 140, 255))
    draw.text((50, 468), "Multi-tone, shading, ambient AO", fill=(140, 150, 165, 255))
    new_resized = tex_img.resize((200, 200), Image.NEAREST)
    canvas.paste(new_resized, (60, 500))

    # 2. Center/Right: 3D Viewport
    draw.rectangle([300, 110, 1160, 750], fill=(16, 20, 26, 255), outline=(60, 75, 98, 255), width=2)
    
    # Viewport Title
    draw.text((320, 125), f"VIEWPORT 3D ISOMETRIK — {title.upper()}", fill=(230, 235, 245, 255))
    draw.text((320, 148), f"Model multi-kubus anatomi penuh dengan tekstur kaya & pencahayaan terarah", fill=(120, 135, 155, 255))
    
    # Ground Grid & Contact Shadow
    cx = 720
    cy = 470
    scale = 10.5 if "Bison" in title else (16.0 if "Platypus" in title else 17.5)
    
    # Ground Shadow Polygon
    shadow_pts = [
        project_iso(-30, 0, -30, cx, cy, scale),
        project_iso(30, 0, -30, cx, cy, scale),
        project_iso(30, 0, 30, cx, cy, scale),
        project_iso(-30, 0, 30, cx, cy, scale)
    ]
    draw.polygon(shadow_pts, fill=(12, 14, 18, 255))
    
    # Sort cubes by isometric depth (Z-sorting: x + z ascending)
    def cube_depth(c):
        ox, oy, oz = c["origin"]
        sx, sy, sz = c["size"]
        return (ox + sx * 0.5) + (oz + sz * 0.5) - (oy + sy * 0.5) * 0.1

    sorted_cubes = sorted(cubes, key=cube_depth)
    tex_pix = tex_img.load()
    
    # Render 3D Cubes
    for c in sorted_cubes:
        render_cube(draw, tex_pix, 128, 128, c["origin"], c["size"], c["uv"], cx, cy, scale, rot_y=25)

    # 3. Spec / Callout Box in Bottom Right
    draw.rectangle([820, 560, 1140, 730], fill=(22, 28, 38, 230), outline=(70, 85, 110, 255), width=2)
    draw.text((835, 570), "SPESIFIKASI VISUAL KANONIKAL", fill=(240, 200, 80, 255))
    if "Bison" in title:
        draw.text((835, 595), "• 6 Kaki Anatomi + Ekor Beaver Lebar", fill=(200, 205, 215, 255))
        draw.text((835, 615), "• Tanda Panah Cokelat Chevron Pengembara", fill=(200, 205, 215, 255))
        draw.text((835, 635), "• Tanduk Melengkung Cokelat Tua Berulir", fill=(200, 205, 215, 255))
        draw.text((835, 655), "• Sadel Kayu Tradisional & Pelana Merah", fill=(200, 205, 215, 255))
        draw.text((835, 675), "• Bulu Cream Bertekstur Shaggy Lembut", fill=(200, 205, 215, 255))
    elif "Platypus" in title:
        draw.text((835, 595), "• Paruh Bebek Platypus Teal Leathery", fill=(200, 205, 215, 255))
        draw.text((835, 615), "• Tubuh Beruang Grizzly Raksasa Berbulu", fill=(200, 205, 215, 255))
        draw.text((835, 635), "• Ekor Pipih Lebar Bersisik Cokelat Tua", fill=(200, 205, 215, 255))
        draw.text((835, 655), "• 4 Kaki Berotot + Cakar Tajam Gading", fill=(200, 205, 215, 255))
        draw.text((835, 675), "• Mantel Bulu Pundak Berlapis Gelap", fill=(200, 205, 215, 255))
    else:
        draw.text((835, 595), "• Mahkota Api Topknot Emas Kekaisaran", fill=(200, 205, 215, 255))
        draw.text((835, 615), "• Jubah Sutra Sutera Scarlet & Bordir Emas", fill=(200, 205, 215, 255))
        draw.text((835, 635), "• Pauldron Pundak Bertingkat Runcing", fill=(200, 205, 215, 255))
        draw.text((835, 655), "• Bracer Pergelangan Tangan Api Berkilau", fill=(200, 205, 215, 255))
        draw.text((835, 675), "• Peta Emissive Glow Map untuk Mata Chi", fill=(200, 205, 215, 255))

    out_path = os.path.join(SHOWCASE_DIR, f"mockup_{mob_name}.png")
    canvas.save(out_path, format="PNG")
    print(f"Saved showcase mockup: {out_path}")
    return out_path


# -----------------------------------------------------------------------------
# 3. MAIN WORKFLOW EXECUTION
# -----------------------------------------------------------------------------

def execute_all():
    print("="*70)
    print("GENERATING AAA MOB TEXTURES & 3D ISOMETRIC MOCKUPS")
    print("="*70)

    # 1. Flying Bison (Pet/Mount)
    bison_cubes = [
        {"origin": [-12, 10, -18], "size": [24, 16, 36], "uv": [0, 40, 64, 96]}, # body
        {"origin": [-9, 14, -30], "size": [18, 14, 14], "uv": [0, 0, 48, 40]},   # head
        {"origin": [-7, 14, -35], "size": [14, 8, 6], "uv": [48, 0, 80, 24]},     # snout
        {"origin": [9, 23, -24], "size": [4, 4, 6], "uv": [80, 0, 112, 32]},      # horn left base
        {"origin": [11, 27, -27], "size": [3, 9, 4], "uv": [80, 0, 112, 32]},     # horn left tip
        {"origin": [-13, 23, -24], "size": [4, 4, 6], "uv": [80, 0, 112, 32]},    # horn right base
        {"origin": [-14, 27, -27], "size": [3, 9, 4], "uv": [80, 0, 112, 32]},    # horn right tip
        {"origin": [9, 17, -19], "size": [3, 4, 3], "uv": [0, 10, 10, 20]},       # ear left
        {"origin": [-12, 17, -19], "size": [3, 4, 3], "uv": [0, 10, 10, 20]},      # ear right
        {"origin": [8, 0, -15], "size": [5, 10, 6], "uv": [0, 100, 20, 128]},     # leg FL
        {"origin": [-13, 0, -15], "size": [5, 10, 6], "uv": [0, 100, 20, 128]},    # leg FR
        {"origin": [8, 0, -2], "size": [5, 10, 6], "uv": [20, 100, 40, 128]},     # leg ML
        {"origin": [-13, 0, -2], "size": [5, 10, 6], "uv": [20, 100, 40, 128]},    # leg MR
        {"origin": [8, 0, 11], "size": [5, 10, 6], "uv": [40, 100, 60, 128]},     # leg BL
        {"origin": [-13, 0, 11], "size": [5, 10, 6], "uv": [40, 100, 60, 128]},    # leg BR
        {"origin": [-9, 15, 18], "size": [18, 4, 22], "uv": [64, 40, 100, 80]},  # beaver tail
        {"origin": [-11, 26, -6], "size": [22, 5, 20], "uv": [64, 80, 128, 128]} # saddle
    ]
    bison_tex = create_flying_bison_texture()
    old_bison_path = os.path.join(TEXTURES_DIR, "pet", "flying_bison.png")
    old_bison_tex = Image.open(old_bison_path)
    # Save new texture
    bison_tex.save(old_bison_path)
    render_mob_showcase("flying_bison", "Flying Bison (Sky Bison / Appa)", "Pet / Mount", "Air (Nomad Companion)", bison_cubes, bison_tex, old_bison_tex)

    # 2. Platypus Bear (Wild Mob)
    platypus_cubes = [
        {"origin": [-8, 7, -11], "size": [16, 14, 22], "uv": [0, 40, 64, 95]},   # body
        {"origin": [-9, 14, -12], "size": [18, 8, 14], "uv": [0, 40, 64, 65]},    # shoulder mantle
        {"origin": [-5.5, 14, -19], "size": [11, 10, 9], "uv": [0, 0, 48, 40]},   # bear head
        {"origin": [-5, 14, -26], "size": [10, 3.5, 8], "uv": [48, 0, 88, 32]},   # platypus bill snout
        {"origin": [4, 22, -14], "size": [3, 3, 2], "uv": [6, 2, 14, 10]},       # ear left
        {"origin": [-7, 22, -14], "size": [3, 3, 2], "uv": [34, 2, 42, 10]},      # ear right
        {"origin": [5, 0, -9], "size": [4.5, 8, 5], "uv": [0, 100, 32, 128]},     # leg FL
        {"origin": [-9.5, 0, -9], "size": [4.5, 8, 5], "uv": [0, 100, 32, 128]},  # leg FR
        {"origin": [5, 0, 5], "size": [4.5, 8, 5], "uv": [32, 100, 64, 128]},     # leg BL
        {"origin": [-9.5, 0, 5], "size": [4.5, 8, 5], "uv": [32, 100, 64, 128]},  # leg BR
        {"origin": [-5.5, 10, 11], "size": [11, 3.5, 13], "uv": [64, 40, 104, 80]}# platypus tail
    ]
    platypus_tex = create_platypus_bear_texture()
    old_platypus_path = os.path.join(TEXTURES_DIR, "mobs", "platypus_bear.png")
    old_platypus_tex = Image.open(old_platypus_path)
    platypus_tex.save(old_platypus_path)
    render_mob_showcase("platypus_bear", "Platypus Bear (Beruang Berparuh)", "Wild Creature / Mob", "Earth Kingdom Fauna", platypus_cubes, platypus_tex, old_platypus_tex)

    # 3. Phoenix King Ozai (Boss)
    ozai_cubes = [
        {"origin": [-3.5, 23, -3.5], "size": [7, 8, 7], "uv": [0, 0, 32, 32]},       # head
        {"origin": [-1.5, 31, -1.5], "size": [3, 3.5, 3], "uv": [32, 0, 64, 32]},    # topknot
        {"origin": [-2, 32, -2.5], "size": [4, 6, 2], "uv": [40, 4, 56, 16]},        # crown crest
        {"origin": [-4, 11, -2.5], "size": [8, 12, 5], "uv": [0, 32, 64, 80]},       # torso upper
        {"origin": [-4.5, 0, -3], "size": [9, 12, 6], "uv": [0, 80, 64, 128]},       # lower imperial robe
        {"origin": [4, 19, -3.5], "size": [4, 4.5, 7], "uv": [64, 32, 96, 64]},      # pauldron left
        {"origin": [-8, 19, -3.5], "size": [4, 4.5, 7], "uv": [64, 32, 96, 64]},     # pauldron right
        {"origin": [4, 10, -2], "size": [3, 11, 4], "uv": [64, 64, 128, 128]},       # arm left + bracer
        {"origin": [-7, 10, -2], "size": [3, 11, 4], "uv": [64, 64, 128, 128]},      # arm right + bracer
        {"origin": [0.5, 0, -2], "size": [3.5, 11, 4], "uv": [0, 80, 32, 128]},      # leg left
        {"origin": [-4, 0, -2], "size": [3.5, 11, 4], "uv": [32, 80, 64, 128]}       # leg right
    ]
    ozai_tex, ozai_glow = create_phoenix_king_ozai_textures()
    old_ozai_path = os.path.join(TEXTURES_DIR, "boss", "phoenix_king_ozai.png")
    old_ozai_tex = Image.open(old_ozai_path)
    ozai_tex.save(old_ozai_path)
    
    ozai_glow_path = os.path.join(TEXTURES_DIR, "boss", "phoenix_king_ozai_glow.png")
    ozai_glow.save(ozai_glow_path)
    
    render_mob_showcase("phoenix_king_ozai", "Phoenix King Ozai (Raja Api Ozai)", "Prime Boss", "Fire / Lightning (Sozin Comet)", ozai_cubes, ozai_tex, old_ozai_tex, ozai_glow)

    print("\n" + "="*70)
    print("ALL MOCKUPS AND TEXTURES SUCCESSFULLY GENERATED!")
    print("="*70)

if __name__ == "__main__":
    execute_all()
