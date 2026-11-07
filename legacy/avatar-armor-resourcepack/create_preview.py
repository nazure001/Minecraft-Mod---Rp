#!/usr/bin/env python3
"""
Avatar Armor Resource Pack - Comprehensive 7-Tier Preview Sheet Generator (Minecraft 1.21.1)
Renders a showcase poster of all 4 Nations x 7 Tiers (112 pieces) with lore, catalysts & abilities.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def make_preview():
    base_dir = r"d:\repo\avatar-armor-resourcepack"
    tex_dir = os.path.join(base_dir, "assets", "avatar", "textures", "item")
    pack_icon_path = os.path.join(base_dir, "pack.png")
    out_rp = os.path.join(base_dir, "preview.png")

    brain_dirs = [
        r"C:\Users\USER\.gemini\antigravity\brain\dbff834a-f1b1-4485-9c66-111e74e9f43a",
        r"C:\Users\USER\.gemini\antigravity\brain\e65e5fce-91cb-4b69-a64c-039879037539"
    ]

    # Dimensions
    W, H = 1620, 1260
    canvas = Image.new("RGBA", (W, H), (15, 17, 23, 255))
    draw = ImageDraw.Draw(canvas)

    NATION_CODES = {"fire": 1, "water": 2, "earth": 3, "air": 4}

    # Fonts
    font_dir = r"C:\Windows\Fonts"
    f_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 28)
    f_sub = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 13)
    f_badge = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 11)
    f_col_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 18)
    f_col_sub = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 10)
    f_tier_name = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 11)
    f_tier_mat = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 10)
    f_tier_bonus = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 9)
    f_footer_h = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 12)
    f_footer_p = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 10)

    # Background grid
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(22, 26, 35, 255), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(22, 26, 35, 255), width=1)

    # Header Panel (Y: 18 to 98)
    draw.rounded_rectangle([(24, 18), (W - 24, 98)], radius=10, fill=(21, 24, 33, 250), outline=(45, 52, 69, 255), width=1)

    # Pack Icon
    if os.path.exists(pack_icon_path):
        p_icon = Image.open(pack_icon_path).convert("RGBA").resize((64, 64), Image.NEAREST)
        canvas.paste(p_icon, (38, 26), p_icon)
        draw.rounded_rectangle([(37, 25), (103, 91)], radius=6, outline=(218, 165, 32, 220), width=2)

    # Title & Subtitle
    draw.text((120, 26), "AVATAR: THE LAST AIRBENDER — 7-TIER ELEMENTAL ARMOR", fill=(255, 215, 0), font=f_title)
    draw.text((122, 64), "Minecraft Java 1.21.1 Datapack & Resource Pack  •  4 Nations  •  7 Tiers (Initiate → Sovereign)  •  100% Equal Progression Across All Nations", fill=(175, 185, 205), font=f_sub)

    # Version Badge
    badge_x = W - 200
    draw.rounded_rectangle([(badge_x, 34), (W - 40, 76)], radius=8, fill=(28, 55, 42), outline=(52, 199, 89), width=1)
    draw.text((badge_x + 14, 40), "MC JAVA 1.21.1", fill=(74, 222, 128), font=f_badge)
    draw.text((badge_x + 14, 56), "SURVIVAL READY", fill=(200, 240, 210), font=f_badge)

    # Nation Data
    nations = [
        {
            "id": "fire",
            "name": "🔥 FIRE NATION",
            "motto": "Strength, Fire Immunity & Burning Sunfire",
            "accent": (239, 68, 68),
            "accent_dark": (65, 18, 18),
            "tiers": [
                ("Tier I: Initiate", "Leather Base  •  Blaze Powder", "Fire Res I + Speed", "fire_initiate"),
                ("Tier II: Apprentice", "Chain Base  •  Magma Cream", "Fire Res I + Speed I + Strength I", "fire_apprentice"),
                ("Tier III: Adept", "Iron Base  •  Blaze Rod", "Fire Res + Str I + Spd I + Haste I", "fire_adept"),
                ("Tier IV: Veteran", "Iron Reinf.  •  Crying Obsidian", "Fire Res + Str II + Spd I + Haste I", "fire_veteran"),
                ("Tier V: Master", "Diamond Base  •  Magma Block", "Fire Res + Str II + Spd II + Haste I", "fire_master"),
                ("Tier VI: Mythic", "Netherite Base  •  Dragon Breath", "Fire Res + Str II + Spd II + Haste II + Regen I", "fire_mythic"),
                ("Tier VII: Sovereign", "Dragon Godplate  •  Nether Star", "Fire Immunity + Str III + Spd II + Haste II + Res II + Regen I", "fire_sovereign"),
            ]
        },
        {
            "id": "water",
            "name": "🌊 WATER TRIBE",
            "motto": "Resilience, Ocean Grace & Infinite Breath",
            "accent": (56, 189, 248),
            "accent_dark": (15, 45, 65),
            "tiers": [
                ("Tier I: Initiate", "Leather Base  •  Prismarine Shard", "Water Breathing I", "water_initiate"),
                ("Tier II: Apprentice", "Chain Base  •  Prismarine Crystal", "Water Breathing + Dolphin's Grace I", "water_apprentice"),
                ("Tier III: Adept", "Iron Base  •  Lapis Lazuli", "Water Breath + Dolphin + Regen I", "water_adept"),
                ("Tier IV: Veteran", "Iron Reinf.  •  Dark Prismarine", "Water Breath + Dolphin + Regen I + Res I", "water_veteran"),
                ("Tier V: Master", "Diamond Base  •  Heart of Sea", "Water Breath + Dolphin + Regen II + Res I + Health I", "water_master"),
                ("Tier VI: Mythic", "Netherite Base  •  Nautilus Shell", "Water Breath + Dolphin + Regen II + Res II + Health II", "water_mythic"),
                ("Tier VII: Sovereign", "Ocean Spirit  •  Nether Star", "Water Breath + Dolphin + Conduit + Regen II + Res II + Health IV", "water_sovereign"),
            ]
        },
        {
            "id": "earth",
            "name": "🪨 EARTH KINGDOM",
            "motto": "Immovable Defense, Haste & Earth Tremors",
            "accent": (74, 222, 128),
            "accent_dark": (18, 55, 28),
            "tiers": [
                ("Tier I: Initiate", "Leather Base  •  Clay Ball", "Resistance I", "earth_initiate"),
                ("Tier II: Apprentice", "Chain Base  •  Bamboo", "Resistance I + Haste I", "earth_apprentice"),
                ("Tier III: Adept", "Iron Base  •  Amethyst Shard", "Resistance I + Haste I + Absorption I", "earth_adept"),
                ("Tier IV: Veteran", "Iron Reinf.  •  Emerald Ingot", "Resistance II + Haste II", "earth_veteran"),
                ("Tier V: Master", "Diamond Base  •  Emerald Block", "Resistance II + Haste II + Strength I + Health I", "earth_master"),
                ("Tier VI: Mythic", "Netherite Base  •  Obsidian", "Resistance III + Haste II + Strength II + Health II", "earth_mythic"),
                ("Tier VII: Sovereign", "Mountain Titan  •  Nether Star", "Resistance III + Haste III + Strength II + Health IV", "earth_sovereign"),
            ]
        },
        {
            "id": "air",
            "name": "💨 AIR NOMAD",
            "motto": "Agility, Gliding & Spiritual Ascension",
            "accent": (250, 204, 21),
            "accent_dark": (65, 52, 15),
            "tiers": [
                ("Tier I: Initiate", "Leather Base  •  Feather", "Speed I + Jump Boost I", "air_initiate"),
                ("Tier II: Apprentice", "Chain Base  •  Rabbit Hide", "Speed I + Jump Boost I + Slow Falling", "air_apprentice"),
                ("Tier III: Adept", "Iron Base  •  Phantom Membrane", "Speed II + Jump Boost II + Slow Falling", "air_adept"),
                ("Tier IV: Veteran", "Iron Reinf.  •  White Wool", "Speed II + Jump Boost II + Slow Falling + Haste I", "air_veteran"),
                ("Tier V: Master", "Diamond Base  •  Wind Charge", "Speed III + Jump Boost II + Slow Falling + Haste II", "air_master"),
                ("Tier VI: Mythic", "Netherite Base  •  Breeze Rod", "Speed III + Jump Boost III + Slow Falling + Haste II + Regen I", "air_mythic"),
                ("Tier VII: Sovereign", "Avatar Nimbus  •  Nether Star", "Speed IV + Jump Boost III + Slow Falling + Haste III + Regen II", "air_sovereign"),
            ]
        }
    ]

    pieces = ["helmet", "chestplate", "leggings", "boots"]
    col_w = 376
    gap = 14
    start_x = 24
    top_y = 110
    col_h = 1040

    slot_size = 38
    icon_size = 32
    pad = (slot_size - icon_size) // 2

    for col_idx, nat in enumerate(nations):
        cx = start_x + col_idx * (col_w + gap)

        # Column Background Card
        draw.rounded_rectangle([(cx, top_y), (cx + col_w, top_y + col_h)], radius=10, fill=(20, 23, 31, 245), outline=nat["accent"], width=1)

        # Column Header banner
        draw.rounded_rectangle([(cx, top_y), (cx + col_w, top_y + 54)], radius=10, fill=nat["accent_dark"], outline=None)
        draw.text((cx + 14, top_y + 8), nat["name"], fill=nat["accent"], font=f_col_title)
        draw.text((cx + 14, top_y + 32), nat["motto"], fill=(200, 215, 235), font=f_col_sub)

        # 7 Tiers inside this nation column
        card_y = top_y + 64
        t_card_h = 132

        for t_idx, (t_name, t_mat, t_bonus, t_key) in enumerate(nat["tiers"]):
            is_sov = (t_idx == 6)
            is_myth = (t_idx == 5)

            c_bg = (34, 26, 16) if is_sov else ((26, 22, 34) if is_myth else (16, 18, 25))
            c_border = (255, 215, 0) if is_sov else ((192, 132, 252) if is_myth else (40, 48, 64))

            cy = card_y + t_idx * (t_card_h + 6)
            draw.rounded_rectangle([(cx + 10, cy), (cx + col_w - 10, cy + t_card_h)], radius=6, fill=c_bg, outline=c_border, width=2 if is_sov else 1)

            # Tier Name & Material
            name_c = (255, 215, 0) if is_sov else ((216, 180, 254) if is_myth else (235, 240, 250))
            draw.text((cx + 18, cy + 6), t_name, fill=name_c, font=f_tier_name)
            draw.text((cx + 18, cy + 22), t_mat, fill=(150, 165, 185), font=f_tier_mat)

            # 4 Piece Icons
            icons_y = cy + 40
            for p_idx, p_name in enumerate(pieces):
                ix = cx + 18 + p_idx * (slot_size + 8)

                # Slot background
                draw.rectangle([(ix, icons_y), (ix + slot_size, icons_y + slot_size)], fill=(10, 12, 16), outline=(50, 58, 75), width=1)

                tex_file = os.path.join(tex_dir, f"{nat['id']}_{t_key.split('_')[1]}_{p_name}.png")
                if os.path.exists(tex_file):
                    icon_img = Image.open(tex_file).convert("RGBA").resize((icon_size, icon_size), Image.NEAREST)
                    canvas.paste(icon_img, (ix + pad, icons_y + pad), icon_img)

            # Set Bonus Text
            bonus_c = (255, 215, 0) if is_sov else ((216, 180, 254) if is_myth else nat["accent"])
            draw.text((cx + 18, cy + 86), "✨ " + t_bonus, fill=bonus_c, font=f_tier_bonus)
            draw.text((cx + 18, cy + 104), f"Custom Model Data: {NATION_CODES[nat['id']]}000..  •  Attribute Scaled", fill=(120, 135, 155), font=f_tier_mat)

    # Footer Info Bar (Y: 1165 to 1245)
    draw.rounded_rectangle([(24, 1165), (W - 24, 1245)], radius=10, fill=(21, 24, 33, 250), outline=(45, 52, 69, 255), width=1)
    draw.text((38, 1175), "SURVIVAL CRAFTING & PROGRESSION WORKFLOW", fill=(255, 215, 0), font=f_footer_h)
    draw.text((38, 1198), "1. Start with Leather piece + Catalyst 1  •  2. Upgrade with Copper + Catalyst 2  •  3. Upgrade with Iron + Catalyst 3  •  4. Upgrade with Iron Block + Catalyst 4", fill=(180, 190, 210), font=f_footer_p)
    draw.text((38, 1218), "5. Upgrade with Diamond Block + Catalyst 5  •  6. Upgrade with Netherite Ingot + Catalyst 6  •  7. Ascend to Sovereign with Nether Star + Totem of Undying", fill=(140, 155, 175), font=f_footer_p)

    canvas.save(out_rp, "PNG")
    for b_dir in brain_dirs:
        if os.path.exists(b_dir):
            canvas.save(os.path.join(b_dir, "preview.png"), "PNG")
            canvas.save(os.path.join(b_dir, "preview_avatar_armor.png"), "PNG")

    print(f"Preview sheet successfully generated: {out_rp} ({W}x{H})")

if __name__ == "__main__":
    make_preview()
