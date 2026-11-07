#!/usr/bin/env python3
"""
Avatar Armor Resource Pack - 7-Tier Evolution Comparison Sheet Generator
Renders a high-resolution grid comparison of all 4 Nations x 7 Tiers (112 pieces).
"""

import os
from PIL import Image, ImageDraw, ImageFont

def make_evolution_sheet():
    base_dir = r"d:\repo\avatar-armor-resourcepack"
    tex_dir = os.path.join(base_dir, "assets", "avatar", "textures", "item")
    out_file = os.path.join(base_dir, "evolution_comparison.png")

    brain_dirs = [
        r"C:\Users\USER\.gemini\antigravity\brain\dbff834a-f1b1-4485-9c66-111e74e9f43a",
        r"C:\Users\USER\.gemini\antigravity\brain\e65e5fce-91cb-4b69-a64c-039879037539"
    ]

    nations = [
        ("fire", "🔥 Fire Nation", (239, 68, 68), "Terracotta → Lacquer → Dragon God"),
        ("water", "🌊 Water Tribe", (56, 189, 248), "Tundra Wool → Scales → Ocean Spirit"),
        ("earth", "🪨 Earth Kingdom", (74, 222, 128), "Hempen Cloth → Bamboo → Bedrock Titan"),
        ("air", "💨 Air Nomad", (250, 204, 21), "Saffron Robes → Goggles → Avatar Nimbus")
    ]

    tiers = [
        ("initiate", "Tier I: Initiate\n(Cloth / Hoodie / Wraps)"),
        ("apprentice", "Tier II: Apprentice\n(Mask / Goggles / Pelt)"),
        ("adept", "Tier III: Adept\n(Reinforced Battle Gear)"),
        ("veteran", "Tier IV: Veteran\n(Imperial Warplate)"),
        ("master", "Tier V: Master\n(Gilded Plated Armor)"),
        ("mythic", "Tier VI: Mythic\n(Netherite Runed Warplate)"),
        ("sovereign", "Tier VII: Sovereign\n(Grand Avatar Godplate)")
    ]

    pieces = ["helmet", "chestplate", "leggings", "boots"]

    slot_size = 48
    icon_size = 42
    pad = (slot_size - icon_size) // 2

    # Dimensions
    start_x = 210
    col_w = 148
    W = start_x + len(tiers) * col_w + 30
    row_h = 145
    start_y = 150
    H = start_y + len(nations) * row_h + 30

    img = Image.new("RGBA", (W, H), (15, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
    f_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12)
    f_header = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 11)
    f_nation = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 13)
    f_sub_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 9)

    # Background grid lines
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(20, 23, 31, 255), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(20, 23, 31, 255), width=1)

    # Header
    draw.rounded_rectangle([(20, 16), (W - 20, 80)], radius=8, fill=(21, 24, 33), outline=(45, 52, 69), width=1)
    draw.text((36, 24), "7-TIER VISUAL EVOLUTION MATRIX — INITIATE TO SOVEREIGN", fill=(255, 215, 0), font=f_title)
    draw.text((38, 54), "All 4 Nations progress through equal vanilla bases (Leather → Chain → Iron → Iron+ → Diamond → Netherite → Godplate) with custom pixel art.", fill=(160, 175, 200), font=f_sub)

    # Column Headers (Tiers)
    y_tier_head = 94
    for t_idx, (t_key, t_label) in enumerate(tiers):
        tx = start_x + t_idx * col_w
        is_sov = (t_key == "sovereign")
        is_myth = (t_key == "mythic")
        border_c = (255, 215, 0) if is_sov else ((192, 132, 252) if is_myth else (60, 70, 90))
        bg_c = (38, 30, 20) if is_sov else ((28, 24, 38) if is_myth else (25, 29, 39))

        draw.rounded_rectangle([(tx, y_tier_head), (tx + col_w - 8, y_tier_head + 42)], radius=6, fill=bg_c, outline=border_c, width=1)
        lines = t_label.split("\n")
        h_color = (255, 215, 0) if is_sov else ((216, 180, 254) if is_myth else (180, 195, 220))
        draw.text((tx + 6, y_tier_head + 4), lines[0], fill=h_color, font=f_header)
        draw.text((tx + 6, y_tier_head + 22), lines[1], fill=(130, 145, 170), font=f_sub_small)

    # Rows (Nations)
    for n_idx, (nat_key, nat_name, nat_color, nat_desc) in enumerate(nations):
        ry = start_y + n_idx * row_h

        # Nation label card on left
        draw.rounded_rectangle([(20, ry), (198, ry + row_h - 12)], radius=8, fill=(22, 26, 36), outline=nat_color, width=1)
        draw.text((28, ry + 16), nat_name, fill=nat_color, font=f_nation)
        draw.text((28, ry + 42), f"Archetype Progression:\n• {nat_desc}\n• 28 Custom Pieces\n• Scaled Attributes", fill=(140, 155, 180), font=f_sub_small)

        # 7 Tiers for this nation
        for t_idx, (t_key, _) in enumerate(tiers):
            tx = start_x + t_idx * col_w
            is_sov = (t_key == "sovereign")
            is_myth = (t_key == "mythic")

            card_fill = (35, 28, 18) if is_sov else ((28, 22, 38) if is_myth else (20, 23, 31))
            card_border = (255, 215, 0) if is_sov else ((192, 132, 252) if is_myth else (45, 52, 69))
            draw.rounded_rectangle([(tx, ry), (tx + col_w - 8, ry + row_h - 12)], radius=8, fill=card_fill, outline=card_border, width=2 if is_sov else 1)

            # 4 Pieces 2x2 grid
            for p_idx, piece in enumerate(pieces):
                gx = tx + 14 + (p_idx % 2) * (slot_size + 12)
                gy = ry + 14 + (p_idx // 2) * (slot_size + 8)

                # Slot background
                draw.rectangle([(gx, gy), (gx + slot_size, gy + slot_size)], fill=(12, 14, 18), outline=(50, 58, 75), width=1)

                tex_file = os.path.join(tex_dir, f"{nat_key}_{t_key}_{piece}.png")
                if os.path.exists(tex_file):
                    t_img = Image.open(tex_file).convert("RGBA").resize((icon_size, icon_size), Image.NEAREST)
                    img.paste(t_img, (gx + pad, gy + pad), t_img)

    img.save(out_file, "PNG")
    for b_dir in brain_dirs:
        if os.path.exists(b_dir):
            img.save(os.path.join(b_dir, "evolution_comparison.png"), "PNG")

    print(f"Evolution comparison sheet successfully generated: {out_file} ({W}x{H})")

if __name__ == "__main__":
    make_evolution_sheet()
