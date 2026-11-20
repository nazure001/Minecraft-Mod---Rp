import os
import json
import math
from PIL import Image, ImageDraw

ROOT = r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets\avatar_elements"
TEXTURE_DIR = os.path.join(ROOT, "textures", "vfx")
MODEL_DIR = os.path.join(ROOT, "models", "vfx")
os.makedirs(TEXTURE_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE TEXTURES (128x128 RGBA)
# ---------------------------------------------------------

# Texture 1: martial_shockwave.png
def make_shockwave_texture():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2

    # Draw expanding concentric energy ripple rings
    for r in range(58, 10, -1):
        alpha = int(255 * (1.0 - math.pow(r / 60.0, 1.8)))
        # Outer golden-amber ring
        if r > 45:
            color = (255, 200, 80, int(alpha * 0.85))
        elif r > 30:
            color = (255, 240, 160, int(alpha * 0.95))
        else:
            color = (255, 255, 255, int(alpha * 0.9))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    
    # Inner energy core glow
    for r in range(15, 0, -1):
        alpha = int(220 * (1.0 - r / 15.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 240, alpha))
    
    # 8-direction burst lines
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        x1 = cx + math.cos(rad) * 20
        y1 = cy + math.sin(rad) * 20
        x2 = cx + math.cos(rad) * 56
        y2 = cy + math.sin(rad) * 56
        draw.line([x1, y1, x2, y2], fill=(255, 255, 220, 180), width=3)

    out_path = os.path.join(TEXTURE_DIR, "martial_shockwave.png")
    img.save(out_path)
    print("Saved:", out_path)

# Texture 2: hitstop_flash.png
def make_hitstop_texture():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2

    # 4-point impact star flash
    for w in range(16, 0, -2):
        alpha = int(255 * (1.0 - (w / 18.0) * 0.4))
        # Horizontal & vertical diamond spikes
        points_cross = [
            (cx, cy - 60), (cx + w, cy),
            (cx, cy + 60), (cx - w, cy)
        ]
        draw.polygon(points_cross, fill=(255, 245, 180, alpha))
        
        points_cross_h = [
            (cx - 60, cy), (cx, cy + w),
            (cx + 60, cy), (cx, cy - w)
        ]
        draw.polygon(points_cross_h, fill=(255, 245, 180, alpha))

    # Diagonal smaller spikes
    for w in range(10, 0, -2):
        alpha = int(200 * (1.0 - (w / 12.0) * 0.4))
        p_diag1 = [
            (cx - 40, cy - 40), (cx + w, cy - w),
            (cx + 40, cy + 40), (cx - w, cy + w)
        ]
        draw.polygon(p_diag1, fill=(255, 200, 100, alpha))
        p_diag2 = [
            (cx + 40, cy - 40), (cx + w, cy + w),
            (cx - 40, cy + 40), (cx - w, cy - w)
        ]
        draw.polygon(p_diag2, fill=(255, 200, 100, alpha))

    # Bright central spark
    for r in range(18, 0, -2):
        alpha = int(255 * (1.0 - r / 20.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))

    out_path = os.path.join(TEXTURE_DIR, "hitstop_flash.png")
    img.save(out_path)
    print("Saved:", out_path)

# Texture 3: dive_kick_trail.png
def make_dive_kick_texture():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Vertical aerodynamic streak cone
    # From top (narrow) to bottom (wide plume)
    for y in range(0, size):
        progress = y / float(size)
        spread = int(4 + progress * 50)
        alpha = int(240 * (1.0 - math.pow(progress, 0.7)))
        x_left = 64 - spread
        x_right = 64 + spread
        # Gradient from white core to cyan/air border
        for x in range(x_left, x_right):
            dist_center = abs(x - 64) / float(spread + 1)
            core_alpha = int(alpha * (1.0 - math.pow(dist_center, 1.5)))
            if core_alpha <= 0:
                continue
            r = int(200 + 55 * (1.0 - dist_center))
            g = int(240 + 15 * (1.0 - dist_center))
            b = 255
            img.putpixel((x, y), (r, g, b, core_alpha))

    out_path = os.path.join(TEXTURE_DIR, "dive_kick_trail.png")
    img.save(out_path)
    print("Saved:", out_path)

# ---------------------------------------------------------
# 2. GENERATE 3D JSON MODELS
# ---------------------------------------------------------

def make_shockwave_model():
    model = {
        "credit": "Avatar Elements Mod - Martial Shockwave (Fabric 1.21.1)",
        "texture_size": [64, 64],
        "textures": {
            "texture": "avatar_elements:vfx/martial_shockwave",
            "particle": "avatar_elements:vfx/martial_shockwave"
        },
        "elements": [
            {
                "name": "shockwave_center_plane",
                "from": [0.0, 7.9, 0.0],
                "to": [16.0, 8.1, 16.0],
                "rotation": { "origin": [8.0, 8.0, 8.0], "axis": "y", "angle": 0.0 },
                "faces": {
                    "up":   { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "down": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            },
            {
                "name": "shockwave_diag_plane",
                "from": [0.0, 7.9, 0.0],
                "to": [16.0, 8.1, 16.0],
                "rotation": { "origin": [8.0, 8.0, 8.0], "axis": "y", "angle": 45.0 },
                "faces": {
                    "up":   { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "down": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            }
        ]
    }
    out_path = os.path.join(MODEL_DIR, "martial_shockwave.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    print("Saved:", out_path)

def make_hitstop_model():
    model = {
        "credit": "Avatar Elements Mod - Hitstop Flash Impact (Fabric 1.21.1)",
        "texture_size": [64, 64],
        "textures": {
            "texture": "avatar_elements:vfx/hitstop_flash",
            "particle": "avatar_elements:vfx/hitstop_flash"
        },
        "elements": [
            {
                "name": "flash_plane_front",
                "from": [0.0, 0.0, 7.9],
                "to": [16.0, 16.0, 8.1],
                "rotation": { "origin": [8.0, 8.0, 8.0], "axis": "y", "angle": 0.0 },
                "faces": {
                    "north": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "south": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            },
            {
                "name": "flash_plane_side",
                "from": [7.9, 0.0, 0.0],
                "to": [8.1, 16.0, 16.0],
                "rotation": { "origin": [8.0, 8.0, 8.0], "axis": "y", "angle": 0.0 },
                "faces": {
                    "east": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "west": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            }
        ]
    }
    out_path = os.path.join(MODEL_DIR, "hitstop_flash.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    print("Saved:", out_path)

def make_dive_kick_model():
    model = {
        "credit": "Avatar Elements Mod - Dive Kick Trail (Fabric 1.21.1)",
        "texture_size": [64, 64],
        "textures": {
            "texture": "avatar_elements:vfx/dive_kick_trail",
            "particle": "avatar_elements:vfx/dive_kick_trail"
        },
        "elements": [
            {
                "name": "trail_vertical_1",
                "from": [0.0, 0.0, 7.9],
                "to": [16.0, 32.0, 8.1],
                "rotation": { "origin": [8.0, 16.0, 8.0], "axis": "y", "angle": 0.0 },
                "faces": {
                    "north": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "south": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            },
            {
                "name": "trail_vertical_2",
                "from": [7.9, 0.0, 0.0],
                "to": [8.1, 32.0, 16.0],
                "rotation": { "origin": [8.0, 16.0, 8.0], "axis": "y", "angle": 0.0 },
                "faces": {
                    "east": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "west": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            },
            {
                "name": "trail_diag_1",
                "from": [0.0, 0.0, 7.9],
                "to": [16.0, 32.0, 8.1],
                "rotation": { "origin": [8.0, 16.0, 8.0], "axis": "y", "angle": 45.0 },
                "faces": {
                    "north": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" },
                    "south": { "uv": [0.0, 0.0, 16.0, 16.0], "texture": "#texture" }
                }
            }
        ]
    }
    out_path = os.path.join(MODEL_DIR, "dive_kick_trail.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    print("Saved:", out_path)

if __name__ == "__main__":
    make_shockwave_texture()
    make_hitstop_texture()
    make_dive_kick_texture()
    make_shockwave_model()
    make_hitstop_model()
    make_dive_kick_model()
    print("All VFX assets generated successfully!")
