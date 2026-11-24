import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

REPO_ROOT = Path(r"d:\repo\Minecraft Mod & Rp")
STAGING_DIR = REPO_ROOT / "art-source/Avatar_Elements_Missing_Assets_Staging"
ASSETS_DIR = STAGING_DIR / "assets/avatar_elements"
ZIP_OUT = REPO_ROOT / "Avatar_Elements_Missing_Bestiary_And_Armor_ZIP.zip"


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_json(p: Path, payload: dict):
    ensure_dir(p.parent)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# (id, category, primary_rgb, secondary_rgb, accent_rgb, has_glow, scale_mult)
MOBS_SPEC = [
    # 1. Fauna ternak/liar (mobs)
    ("turtle_duck",           "mobs", (65, 165, 85),   (95, 78, 55),    (235, 200, 75),  False, 0.75),
    ("ostrich_horse",         "mobs", (185, 145, 95),  (120, 85, 55),   (240, 225, 195), False, 1.15),
    ("koala_sheep",           "mobs", (145, 150, 158), (225, 220, 210), (75, 70, 68),    False, 0.95),
    ("platypus_bear",         "mobs", (110, 75, 48),   (65, 45, 30),    (220, 165, 65),  False, 1.25),
    ("otter_penguin",         "mobs", (55, 65, 85),    (235, 240, 245), (140, 195, 225), False, 0.90),
    ("boar_q_pine",           "mobs", (95, 65, 45),    (55, 40, 30),    (235, 225, 195), False, 1.10),
    ("hog_monkey",            "mobs", (155, 105, 75),  (105, 70, 50),   (225, 130, 120), False, 0.85),
    ("rabbi_roo",             "mobs", (175, 135, 95),  (230, 215, 190), (95, 65, 45),    False, 0.75),
    ("tigerdillo",            "mobs", (210, 125, 45),  (65, 42, 28),    (245, 225, 185), False, 1.05),

    # 2. Monster rimba (mobs)
    ("shirshu",               "mobs", (42, 46, 56),    (24, 26, 34),    (165, 185, 210), False, 1.65),
    ("canyon_crawler",        "mobs", (165, 95, 55),   (110, 58, 32),   (225, 145, 75),  False, 1.35),
    ("catgator",              "mobs", (68, 92, 62),    (42, 58, 40),    (195, 205, 150), False, 1.30),
    ("sand_shark",            "mobs", (215, 185, 125), (175, 142, 88),  (245, 225, 175), False, 1.40),
    ("buzzard_wasp",          "mobs", (175, 125, 45),  (38, 34, 30),    (235, 175, 55),  False, 1.20),
    ("wolfbat",               "mobs", (45, 42, 52),    (28, 26, 34),    (185, 45, 55),   True,  1.10),
    ("eel_hound",             "mobs", (55, 115, 125),  (35, 75, 85),    (215, 235, 185), False, 1.25),

    # 3. Humanoid Factions (mobs)
    ("fire_nation_spearman",  "mobs", (155, 28, 24),   (42, 38, 38),    (225, 175, 55),  False, 1.00),
    ("dai_li_agent",          "mobs", (48, 92, 62),    (28, 32, 30),    (210, 175, 70),  False, 1.00),
    ("equalist_chi_blocker",  "mobs", (36, 38, 46),    (72, 28, 36),    (215, 195, 165), False, 0.98),
    ("swamp_waterbender",     "mobs", (52, 88, 66),    (32, 54, 42),    (120, 175, 145), False, 1.02),

    # 4. Custom Pet / Mount (pet)
    ("flying_bison",          "pet",  (145, 102, 62),  (235, 225, 205), (95, 65, 42),    False, 2.40),
    ("winged_lemur",          "pet",  (225, 215, 195), (140, 110, 85),  (245, 165, 95),  False, 0.65),
    ("polar_bear_dog",        "pet",  (238, 244, 248), (185, 205, 220), (55, 85, 125),   False, 1.55),
    ("komodo_rhino",          "pet",  (125, 55, 42),   (78, 36, 30),    (215, 155, 65),  False, 1.70),

    # 5. Bosses: Mini-Boss, Roaming Sub-Boss & Prime Boss (boss)
    ("phoenix_king_ozai",     "boss", (185, 25, 18),   (255, 145, 25),  (255, 235, 120), True,  1.45),
    ("vaatu_spirit_titan",    "boss", (45, 18, 72),    (155, 25, 45),   (195, 85, 255),  True,  2.20),
    ("combustion_man",        "boss", (145, 65, 42),   (62, 32, 24),    (255, 155, 45),  True,  1.30),
    ("general_fong",          "boss", (62, 108, 68),   (45, 42, 36),    (215, 175, 65),  False, 1.15),
    ("hama_puppetmaster",     "boss", (75, 115, 145),  (45, 62, 82),    (165, 225, 255), True,  1.00),
    ("the_boulder",           "boss", (115, 88, 58),   (75, 58, 38),    (95, 175, 115),  False, 1.40),
    ("hei_bai_corrupted",     "boss", (32, 30, 36),    (18, 16, 20),    (220, 45, 45),   True,  1.80),
]

ARMOR_SETS = {
    "kyoshi_armor":        ((38, 128, 72),  (215, 175, 55), (235, 230, 215)),
    "fire_nation_plate":   ((155, 26, 22),  (220, 170, 50), (35, 32, 32)),
    "earth_kingdom_armor": ((62, 112, 66),  (135, 102, 58), (210, 175, 65)),
}


def build_mob_assets():
    geo_dir = STAGING_DIR / "models/entity"
    ensure_dir(geo_dir)

    for mob_id, category, c1, c2, c3, has_glow, scale_mult in MOBS_SPEC:
        tex_dir = ASSETS_DIR / f"textures/entity/{category}"
        ensure_dir(tex_dir)

        # 128x128 entity texture with layered shading
        img = Image.new("RGBA", (128, 128), (c1[0], c1[1], c1[2], 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 63, 63], fill=(c1[0], c1[1], c1[2], 255))
        draw.rectangle([64, 0, 127, 63], fill=(c2[0], c2[1], c2[2], 255))
        draw.rectangle([0, 64, 127, 127], fill=(c1[0], c1[1], c1[2], 255))
        # Eyes / facial markings
        draw.rectangle([12, 12, 51, 24], fill=(c3[0], c3[1], c3[2], 255))
        draw.rectangle([76, 12, 115, 24], fill=(c3[0], c3[1], c3[2], 255))
        # Shading gradient bands
        draw.rectangle([0, 60, 127, 63], fill=(int(c1[0]*0.8), int(c1[1]*0.8), int(c1[2]*0.8), 255))
        draw.rectangle([0, 124, 127, 127], fill=(int(c1[0]*0.75), int(c1[1]*0.75), int(c1[2]*0.75), 255))
        img.save(tex_dir / f"{mob_id}.png")

        if has_glow:
            glow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            gdraw = ImageDraw.Draw(glow)
            gdraw.rectangle([14, 14, 49, 22], fill=(c3[0], c3[1], c3[2], 255))
            gdraw.rectangle([78, 14, 113, 22], fill=(c3[0], c3[1], c3[2], 255))
            glow.save(tex_dir / f"{mob_id}_glow.png")

        # Blockbench Bedrock template .geo.json
        h = 16.0 * scale_mult
        w = 10.0 * scale_mult
        geo = {
            "format_version": "1.12.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": f"geometry.avatar_elements.{mob_id}",
                        "texture_width": 128,
                        "texture_height": 128,
                        "visible_bounds_width": max(2.0, 2.0 * scale_mult),
                        "visible_bounds_height": max(3.0, 2.5 * scale_mult),
                        "visible_bounds_offset": [0.0, max(1.2, 1.1 * scale_mult), 0.0],
                    },
                    "bones": [
                        {
                            "name": "root",
                            "pivot": [0.0, 0.0, 0.0],
                            "cubes": [
                                {
                                    "origin": [-w * 0.5, 0.0, -w * 0.5],
                                    "size": [w, h, w],
                                    "uv": [0, 0],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        write_json(geo_dir / f"{mob_id}.geo.json", geo)


def build_armor_assets():
    armor_tex_dir = ASSETS_DIR / "textures/models/armor"
    item_tex_dir = ASSETS_DIR / "textures/item"
    ensure_dir(armor_tex_dir)
    ensure_dir(item_tex_dir)

    for set_name, (main_c, trim_c, detail_c) in ARMOR_SETS.items():
        # --- LAYER 1: Helmet, Chestplate, Boots ---
        img1 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
        d1 = ImageDraw.Draw(img1)
        # Helmet area: (0,0) to (32, 16)
        d1.rectangle([0, 0, 31, 15], fill=(main_c[0], main_c[1], main_c[2], 255))
        d1.rectangle([8, 8, 23, 11], fill=(trim_c[0], trim_c[1], trim_c[2], 255))
        # Chestplate body: (16, 16) to (40, 31)
        d1.rectangle([16, 16, 39, 31], fill=(main_c[0], main_c[1], main_c[2], 255))
        d1.rectangle([20, 20, 35, 27], fill=(detail_c[0], detail_c[1], detail_c[2], 255))
        # Arms / Sleeves: (40, 16) to (63, 31)
        d1.rectangle([40, 16, 63, 31], fill=(main_c[0], main_c[1], main_c[2], 255))
        # Boots (lower legs): (0, 16) to (15, 31)
        d1.rectangle([0, 16, 15, 31], fill=(trim_c[0], trim_c[1], trim_c[2], 255))
        img1.save(armor_tex_dir / f"{set_name}_layer_1.png")

        # --- LAYER 2: Leggings only (Head & Body must be transparent!) ---
        img2 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
        d2 = ImageDraw.Draw(img2)
        # Waistband: (16, 16) to (39, 23)
        d2.rectangle([16, 16, 39, 23], fill=(trim_c[0], trim_c[1], trim_c[2], 255))
        # Thighs / Upper legs: (0, 16) to (15, 31)
        d2.rectangle([0, 16, 15, 31], fill=(main_c[0], main_c[1], main_c[2], 255))
        img2.save(armor_tex_dir / f"{set_name}_layer_2.png")

        # --- Item Icons (16x16) for Inventory & Hotbar ---
        pieces = [
            ("helmet", [3, 2, 12, 11], trim_c),
            ("chestplate", [2, 2, 13, 14], main_c),
            ("leggings", [3, 2, 12, 14], main_c),
            ("boots", [2, 4, 13, 14], trim_c),
        ]
        for piece_name, rect, color in pieces:
            icon = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            idraw = ImageDraw.Draw(icon)
            idraw.rectangle(rect, fill=(color[0], color[1], color[2], 255), outline=(30, 25, 25, 255))
            icon.save(item_tex_dir / f"{set_name}_{piece_name}.png")


def build_zip():
    ensure_dir(ZIP_OUT.parent)
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(STAGING_DIR.rglob("*")):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(STAGING_DIR))
    print(f"ZIP Kurasi Bersih berhasil dibuat: {ZIP_OUT.resolve()}")


if __name__ == "__main__":
    build_mob_assets()
    build_armor_assets()
    build_zip()
