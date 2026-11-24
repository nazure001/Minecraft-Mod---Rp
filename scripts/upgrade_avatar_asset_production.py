import json
import math
import os
import shutil
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

REPO_ROOT = Path("d:/repo/Minecraft Mod & Rp")
BUNDLE_ROOT = REPO_ROOT / "Avatar_Elements_Production_Bundle_v3"
RES = BUNDLE_ROOT / "src/main/resources/assets/avatar_elements"
MC_RES = BUNDLE_ROOT / "src/main/resources/assets/minecraft"
JAVA_CLIENT = BUNDLE_ROOT / "src/client/java/com/avatarmod/elements/client/vfx"
JAVA_MAIN = BUNDLE_ROOT / "src/main/java/com/avatarmod/elements/registry"


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict):
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_text(path: Path, text: str):
    ensure_dir(path.parent)
    path.write_text(text.strip() + "\n", encoding="utf-8")


# ==============================================================================
# 1. ANIME-STYLE CEL-SHADED PARTICLES (32 TYPES, 128 UNBAKED FRAMES)
# Discrete 3-Tone Bands: Core (Hot/Highlight), Mid (Saturated Tone), Edge (Shadow/Border)
# ==============================================================================
PARTICLES_V3 = {
    # FIRE & SUB-BENDING
    "fire_ember":          {"core": (255, 255, 200), "mid": (255, 120, 20),  "edge": (180, 30, 5),   "shape": "ember",     "opaque": False},
    "fire_arc_slash":      {"core": (255, 255, 220), "mid": (255, 90, 15),   "edge": (160, 20, 5),   "shape": "arc",       "opaque": False},
    "blue_flame":          {"core": (240, 255, 255), "mid": (40, 160, 255),  "edge": (15, 60, 210),  "shape": "flame",     "opaque": False},
    "fire_comet":          {"core": (255, 250, 180), "mid": (255, 80, 10),   "edge": (150, 20, 5),   "shape": "orb",       "opaque": False},
    "fire_shockwave":      {"core": (255, 240, 160), "mid": (255, 110, 25),  "edge": (170, 35, 10),  "shape": "ring",      "opaque": False},
    "ozai_meteor":         {"core": (255, 255, 210), "mid": (255, 60, 0),    "edge": (120, 15, 0),   "shape": "orb",       "opaque": False},
    "combustion_charge":   {"core": (255, 255, 255), "mid": (255, 40, 10),   "edge": (140, 10, 0),   "shape": "cross",     "opaque": False},

    # AIR & SUB-BENDING
    "air_ring":            {"core": (255, 255, 255), "mid": (190, 240, 255), "edge": (130, 210, 240), "shape": "ring",      "opaque": False},
    "air_gust_swirl":      {"core": (255, 255, 255), "mid": (180, 235, 252), "edge": (120, 200, 230), "shape": "swirl",     "opaque": False},
    "air_tornado_wisp":    {"core": (250, 255, 255), "mid": (170, 230, 250), "edge": (110, 195, 225), "shape": "swirl",     "opaque": False},
    "air_pressure_burst":  {"core": (255, 255, 255), "mid": (160, 225, 245), "edge": (100, 190, 220), "shape": "ring",      "opaque": False},
    "air_flight_trail":    {"core": (255, 255, 255), "mid": (205, 245, 255), "edge": (150, 220, 245), "shape": "swirl",     "opaque": False},

    # WATER & SUB-BENDING
    "water_droplet":       {"core": (240, 252, 255), "mid": (50, 160, 255),  "edge": (20, 95, 210),  "shape": "droplet",   "opaque": False},
    "water_whip_splash":   {"core": (250, 255, 255), "mid": (40, 150, 255),  "edge": (15, 80, 195),  "shape": "splash",    "opaque": False},
    "water_healing_aura":  {"core": (230, 255, 245), "mid": (70, 240, 190),  "edge": (25, 175, 135), "shape": "orb",       "opaque": False},
    "ice_shard":           {"core": (255, 255, 255), "mid": (150, 230, 255), "edge": (80, 180, 235), "shape": "faceted",   "opaque": False},
    "ice_burst":           {"core": (255, 255, 255), "mid": (135, 220, 255), "edge": (70, 170, 225), "shape": "ring",      "opaque": False},
    "plant_vine_chi":      {"core": (235, 255, 220), "mid": (85, 210, 75),   "edge": (35, 140, 30),  "shape": "swirl",     "opaque": False},

    # EARTH & SUB-BENDING
    "earth_chunk":         {"core": (185, 150, 105), "mid": (125, 95, 58),   "edge": (75, 55, 32),   "shape": "blocky",    "opaque": True},
    "earth_stomp_dust":    {"core": (205, 175, 135), "mid": (145, 115, 75),  "edge": (90, 70, 42),   "shape": "cloud",     "opaque": True},
    "earth_seismic_wave":  {"core": (220, 190, 140), "mid": (140, 105, 65),  "edge": (80, 60, 35),   "shape": "ring",      "opaque": False},
    "metal_spark":         {"core": (255, 255, 255), "mid": (210, 220, 235), "edge": (135, 145, 160), "shape": "cross",     "opaque": False},
    "lava_spark":          {"core": (255, 245, 140), "mid": (255, 100, 15),  "edge": (150, 30, 10),  "shape": "ember",     "opaque": False},
    "lava_splash":         {"core": (255, 235, 110), "mid": (245, 80, 10),   "edge": (140, 25, 5),   "shape": "splash",    "opaque": False},

    # LIGHTNING, SPIRIT & AVATAR
    "lightning_arc":       {"core": (255, 255, 255), "mid": (150, 215, 255), "edge": (95, 125, 255), "shape": "zigzag",    "opaque": False},
    "lightning_branch":    {"core": (255, 255, 255), "mid": (130, 200, 255), "edge": (85, 110, 250), "shape": "zigzag",    "opaque": False},
    "healing_mote":        {"core": (230, 255, 245), "mid": (85, 240, 190),  "edge": (30, 175, 130), "shape": "orb",       "opaque": False},
    "spirit_mote":         {"core": (250, 235, 255), "mid": (185, 125, 255), "edge": (125, 60, 220), "shape": "orb",       "opaque": False},
    "vaatu_void_energy":   {"core": (240, 200, 255), "mid": (140, 35, 220),  "edge": (55, 10, 95),   "shape": "swirl",     "opaque": False},
    "avatar_chi":          {"core": (255, 255, 255), "mid": (130, 240, 255), "edge": (70, 180, 250), "shape": "orb",       "opaque": False},
    "avatar_state_chi":    {"core": (255, 255, 255), "mid": (255, 225, 130), "edge": (100, 225, 255), "shape": "ring",      "opaque": False},
    "blood_chi_filament":  {"core": (255, 200, 200), "mid": (200, 25, 25),   "edge": (110, 10, 10),  "shape": "zigzag",    "opaque": False},
}


def render_anime_particle_frame(name, spec, frame_idx):
    """
    Renders 16x16 cel-shaded frame adhering to /anime-style:
    - 2-3 discrete tonal steps (Constant color breaks)
    - Clean silhouettes
    - Frame age scaling
    """
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    core, mid, edge = spec["core"], spec["mid"], spec["edge"]
    shape = spec["shape"]

    scale = 1.0 - (frame_idx * 0.15)
    alpha = max(0.2, 1.0 - (frame_idx * 0.18))

    cx, cy = 7.5, 7.5
    for y in range(16):
        for x in range(16):
            dx = (x - cx) / (6.2 * scale)
            dy = (y - cy) / (6.2 * scale)
            r = math.hypot(dx, dy)

            dist = 999.0
            if shape == "arc":
                angle = math.atan2(dy, dx)
                dist = abs(r - 0.7) * 2.2 if -math.pi * 0.6 <= angle <= math.pi * 0.6 else 999.0
            elif shape == "ring":
                ring_r = 0.5 + (frame_idx * 0.12)
                dist = abs(r - ring_r) * 3.0
            elif shape == "swirl":
                spiral_phase = math.atan2(dy, dx) / (2.0 * math.pi)
                dist = abs(r - (0.4 + spiral_phase * 0.3)) * 2.4
            elif shape == "droplet":
                dist = math.hypot(dx * 1.1, dy - (0.3 if dy > 0 else dy * 1.8))
            elif shape == "faceted":
                dist = max(abs(dx) + abs(dy) * 0.8, abs(dy) + abs(dx) * 0.8)
            elif shape == "blocky":
                dist = max(abs(dx), abs(dy)) * 1.1
            elif shape == "zigzag":
                zig = math.sin(dy * 4.0) * 0.35
                dist = abs(dx - zig) * 2.5
            elif shape == "cross":
                dist = min(max(abs(dx), abs(dy) * 3.5), max(abs(dy), abs(dx) * 3.5))
            else: # orb / ember / splash / flame / cloud
                dist = r

            if dist <= 1.0:
                # 3-Tone Anime Cel Break (Strict Constant Steps)
                if dist < 0.32:
                    col = core
                    a = int(255 * alpha)
                elif dist < 0.70:
                    col = mid
                    a = int(220 * alpha)
                else:
                    col = edge
                    a = int(180 * alpha)
                px[x, y] = (col[0], col[1], col[2], a if not spec["opaque"] else 255)

    return img


def generate_all_particles():
    tex_dir = RES / "textures/particle"
    part_dir = RES / "particles"
    ensure_dir(tex_dir)
    ensure_dir(part_dir)

    for name, spec in PARTICLES_V3.items():
        frames = []
        for f in range(4):
            img = render_anime_particle_frame(name, spec, f)
            frame_name = f"{name}_{f}"
            img.save(tex_dir / f"{frame_name}.png")
            frames.append(f"avatar_elements:{frame_name}")

        write_json(part_dir / f"{name}.json", {"textures": frames})
    print(f"Generated {len(PARTICLES_V3)} anime particle definitions ({len(PARTICLES_V3) * 4} frames).")


# ==============================================================================
# 2. VFX RIBBONS (15 SEAMLESS 128x32 STRIPS)
# ==============================================================================
RIBBONS_V3 = {
    "fire_ribbon":          ((255, 250, 180), (255, 110, 20), (180, 25, 5)),
    "blue_flame_ribbon":    ((240, 255, 255), (50, 170, 255), (15, 65, 215)),
    "water_ribbon":         ((230, 252, 255), (45, 155, 255), (15, 90, 205)),
    "ice_ribbon":           ((250, 255, 255), (145, 225, 255),(75, 175, 230)),
    "air_ribbon":           ((250, 255, 255), (195, 240, 255),(145, 215, 240)),
    "air_vortex_ribbon":    ((245, 255, 255), (180, 235, 252),(125, 200, 230)),
    "earth_energy_ribbon":  ((210, 185, 130), (140, 105, 60), (85, 60, 35)),
    "seismic_ribbon":       ((225, 195, 145), (145, 110, 68), (88, 62, 36)),
    "lava_ribbon":          ((255, 240, 130), (245, 85, 10),  (145, 25, 5)),
    "metal_ribbon":         ((255, 255, 255), (215, 225, 240),(140, 150, 165)),
    "lightning_ribbon":     ((255, 255, 255), (145, 210, 255),(90, 120, 255)),
    "spirit_ribbon":        ((250, 235, 255), (175, 110, 255),(110, 50, 205)),
    "vaatu_ribbon":         ((240, 200, 255), (145, 40, 225), (60, 15, 100)),
    "avatar_state_ribbon":  ((255, 255, 255), (255, 225, 140),(90, 220, 255)),
    "blood_ribbon":         ((255, 210, 210), (210, 30, 30),  (115, 15, 15)),
}


def generate_all_ribbons():
    vfx_dir = RES / "textures/vfx"
    ensure_dir(vfx_dir)

    for name, (core, mid, edge) in RIBBONS_V3.items():
        img = Image.new("RGBA", (128, 32), (0, 0, 0, 0))
        px = img.load()
        for x in range(128):
            wave = math.sin((x / 128.0) * math.pi * 4.0) * 3.5
            cy = 15.5 + wave
            for y in range(32):
                d = abs(y - cy) / 10.0
                if d <= 1.0:
                    if d < 0.28:
                        c, a = core, 250
                    elif d < 0.65:
                        c, a = mid, 215
                    else:
                        c, a = edge, 140
                    px[x, y] = (c[0], c[1], c[2], a)
        img.save(vfx_dir / f"{name}.png")
    print(f"Generated {len(RIBBONS_V3)} VFX ribbon textures (128x32).")


# ==============================================================================
# 3. ANIME-STYLE GUI SKILL ICONS (32x32) & RPG ATTRIBUTES
# ==============================================================================
SKILL_ICONS_V3 = {
    # FIRE
    "fire_jab":          {"color": (255, 95, 20),   "symbol": "flame"},
    "flame_sweep":       {"color": (255, 130, 25),  "symbol": "arc"},
    "fire_blast":        {"color": (255, 65, 10),   "symbol": "burst"},
    "fire_jet":          {"color": (255, 160, 40),  "symbol": "thruster"},
    "fire_guard":        {"color": (230, 50, 15),   "symbol": "shield"},
    "fire_comet":        {"color": (255, 80, 10),   "symbol": "meteor"},
    "ozai_meteor":       {"color": (255, 45, 0),    "symbol": "meteor"},
    "blue_flame":        {"color": (40, 165, 255),  "symbol": "flame"},
    "combustion_charge": {"color": (255, 30, 10),   "symbol": "cross"},
    "lightning":         {"color": (120, 195, 255), "symbol": "bolt"},
    "lightning_branch":  {"color": (100, 180, 255), "symbol": "bolt"},

    # AIR
    "air_palm":          {"color": (185, 235, 250), "symbol": "palm"},
    "air_blast":         {"color": (160, 225, 245), "symbol": "ring"},
    "air_vortex":        {"color": (170, 230, 252), "symbol": "swirl"},
    "air_tornado_wisp":  {"color": (150, 220, 245), "symbol": "swirl"},
    "air_flight_trail":  {"color": (200, 240, 255), "symbol": "wing"},
    "air_pressure_burst":{"color": (140, 215, 240), "symbol": "ring"},

    # WATER
    "water_whip":        {"color": (40, 150, 255),  "symbol": "whip"},
    "water_whip_splash": {"color": (30, 140, 245),  "symbol": "splash"},
    "water_healing_aura":{"color": (70, 240, 190),  "symbol": "cross"},
    "healing":           {"color": (65, 235, 180),  "symbol": "cross"},
    "ice_wall":          {"color": (145, 230, 255), "symbol": "barrier"},
    "ice_burst":         {"color": (130, 220, 255), "symbol": "burst"},
    "plant_vine_chi":    {"color": (80, 210, 70),   "symbol": "swirl"},

    # EARTH
    "earth_boulder":     {"color": (145, 105, 60),  "symbol": "rock"},
    "boulder_launch":    {"color": (135, 95, 55),   "symbol": "meteor"},
    "earth_pillar":      {"color": (120, 85, 48),   "symbol": "pillar"},
    "earth_stomp_dust":  {"color": (160, 125, 80),  "symbol": "ring"},
    "earth_seismic_wave":{"color": (150, 115, 70),  "symbol": "ring"},
    "metal_guard":       {"color": (180, 190, 205), "symbol": "shield"},
    "metal_spark":       {"color": (210, 220, 235), "symbol": "cross"},
    "lava_burst":        {"color": (255, 85, 15),   "symbol": "burst"},
    "lava_splash":       {"color": (245, 75, 10),   "symbol": "splash"},

    # SPIRIT & AVATAR
    "spirit_projection": {"color": (175, 115, 255), "symbol": "eye"},
    "vaatu_void_energy": {"color": (135, 30, 215),  "symbol": "swirl"},
    "avatar_state":      {"color": (115, 230, 255), "symbol": "avatar"},
    "avatar_state_chi":  {"color": (255, 230, 140), "symbol": "avatar"},
}

RPG_ATTRIBUTES = {
    "agility":    {"color": (120, 230, 255), "name": "Agility"},
    "chi_focus":  {"color": (255, 225, 110), "name": "Chi Focus"},
    "vigor":      {"color": (245, 75, 75),   "name": "Vigor"},
    "mastery":    {"color": (180, 110, 255), "name": "Elemental Mastery"},
    "precision":  {"color": (90, 240, 160),  "name": "Precision"},
}

MOB_EFFECTS_V3 = {
    "burning":       (255, 95, 15),
    "chilled":       (130, 220, 255),
    "stagger":       (150, 115, 70),
    "chi_severance": (165, 90, 245),
    "healing_chi":   (75, 235, 185),
}


def draw_anime_symbol(draw, symbol, col):
    """Draws iconic anime-style minimalist elemental shapes on 32x32 canvas."""
    if symbol == "flame":
        draw.polygon([(16, 6), (22, 16), (19, 26), (13, 26), (10, 16)], fill=col)
        draw.polygon([(16, 12), (19, 18), (17, 24), (15, 24), (13, 18)], fill=(255, 255, 220))
    elif symbol == "arc":
        draw.arc([7, 7, 25, 25], start=-45, end=135, fill=col, width=4)
    elif symbol == "ring":
        draw.ellipse([8, 8, 24, 24], outline=col, width=3)
        draw.ellipse([13, 13, 19, 19], fill=col)
    elif symbol == "swirl":
        draw.arc([6, 6, 26, 26], start=0, end=270, fill=col, width=3)
        draw.arc([11, 11, 21, 21], start=90, end=360, fill=(255, 255, 255), width=2)
    elif symbol == "bolt":
        draw.polygon([(18, 5), (10, 17), (16, 17), (14, 27), (23, 14), (17, 14)], fill=col)
    elif symbol == "rock":
        draw.polygon([(16, 7), (24, 12), (22, 24), (10, 24), (8, 12)], fill=col)
        draw.polygon([(16, 10), (21, 14), (19, 21), (13, 21), (11, 14)], fill=(col[0] + 30, col[1] + 30, col[2] + 20))
    elif symbol == "pillar":
        draw.rectangle([11, 7, 21, 25], fill=col)
        draw.line([(16, 7), (16, 25)], fill=(col[0] + 40, col[1] + 40, col[2] + 30), width=2)
    elif symbol == "shield":
        draw.polygon([(16, 5), (25, 10), (22, 23), (16, 27), (10, 23), (7, 10)], fill=col)
        draw.polygon([(16, 9), (21, 13), (19, 21), (16, 23), (13, 21), (11, 13)], fill=(255, 255, 255, 180))
    elif symbol == "whip":
        draw.arc([6, 6, 26, 26], start=45, end=240, fill=col, width=4)
    elif symbol == "avatar":
        draw.ellipse([8, 8, 24, 24], outline=(255, 255, 255), width=2)
        draw.polygon([(16, 9), (23, 16), (16, 23), (9, 16)], fill=col)
    else: # orb / cross / burst / palm / eye / etc.
        draw.ellipse([9, 9, 23, 23], fill=col)
        draw.ellipse([13, 13, 19, 19], fill=(255, 255, 255, 220))


def generate_all_icons():
    skill_dir = RES / "textures/gui/skills"
    attr_dir = RES / "textures/gui/attributes"
    eff_dir = RES / "textures/mob_effect"
    ensure_dir(skill_dir)
    ensure_dir(attr_dir)
    ensure_dir(eff_dir)

    # 32x32 Anime Cel Skill Icons
    for name, data in SKILL_ICONS_V3.items():
        col = data["color"]
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # 1px Contrast Outer Outline + Darkened Inner Plate
        draw.rounded_rectangle([1, 1, 30, 30], radius=5, fill=(18, 16, 15, 235), outline=(col[0], col[1], col[2], 255), width=2)
        # Inner cel glyph
        draw_anime_symbol(draw, data["symbol"], col)
        img.save(skill_dir / f"{name}.png")

    # RPG Attribute Icons (32x32)
    for name, data in RPG_ATTRIBUTES.items():
        col = data["color"]
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([1, 1, 30, 30], radius=6, fill=(25, 24, 30, 240), outline=(col[0], col[1], col[2], 255), width=2)
        draw.ellipse([8, 8, 24, 24], fill=(col[0], col[1], col[2], 220))
        draw.ellipse([12, 12, 20, 20], fill=(255, 255, 255, 240))
        img.save(attr_dir / f"{name}.png")

    # 18x18 Mob Effects
    for name, rgb in MOB_EFFECTS_V3.items():
        img = Image.new("RGBA", (18, 18), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([1, 1, 16, 16], fill=(16, 16, 20, 225), outline=(rgb[0], rgb[1], rgb[2], 255), width=1)
        draw.ellipse([4, 4, 13, 13], fill=(rgb[0], rgb[1], rgb[2], 240))
        img.save(eff_dir / f"{name}.png")

    print(f"Generated {len(SKILL_ICONS_V3)} skill icons, {len(RPG_ATTRIBUTES)} RPG attribute icons, {len(MOB_EFFECTS_V3)} mob effect icons.")


# ==============================================================================
# 4. CANONICAL 16 WEAPONS SUITE: 64x64 CEL ATLAS & JAVA 1.21.1 JSON MODELS
# Legal Bounds [-16, 32], Legal Angles [-45, -22.5, 0, 22.5, 45], Grip Pivot (0,0,0)
# ==============================================================================
CANONICAL_WEAPONS = {
    "dual_swords": {
        "q0": (210, 220, 230), "q1": (220, 180, 60),  "q2": (170, 35, 35),  "q3": (120, 40, 30),
        "cmd": 1701, "name_en": "Zuko Dual Dao Broadswords", "name_id": "Pedang Kembar Dao Zuko"
    },
    "earth_hammer": {
        "q0": (75, 80, 85),    "q1": (135, 140, 145), "q2": (120, 80, 48),  "q3": (50, 185, 115),
        "cmd": 3701, "name_en": "Kyoshi Earthbender Warhammer", "name_id": "Palu Perang Tanah Kyoshi"
    },
    "war_fan": {
        "q0": (45, 165, 100),  "q1": (230, 190, 65),  "q2": (100, 70, 45),  "q3": (195, 45, 45),
        "cmd": 4701, "name_en": "Kyoshi Warrior War Fan", "name_id": "Kipas Tempur Prajurit Kyoshi"
    },
    "water_spear": {
        "q0": (160, 240, 255), "q1": (240, 235, 220), "q2": (45, 90, 160),  "q3": (140, 135, 125),
        "cmd": 2701, "name_en": "Water Tribe Harpoon Spear", "name_id": "Tombak Harpun Suku Air"
    },
    "air_staff": {
        "q0": (175, 120, 70),  "q1": (225, 180, 80),  "q2": (220, 90, 45),  "q3": (240, 248, 255),
        "cmd": 4702, "name_en": "Air Nomad Glider Staff", "name_id": "Tongkat Glider Pengembara Udara"
    },
    "space_sword": {
        "q0": (35, 35, 40),    "q1": (200, 205, 215), "q2": (55, 60, 65),   "q3": (160, 165, 175),
        "cmd": 1702, "name_en": "Sokka Meteorite Space Sword", "name_id": "Pedang Meteorit Hitam Sokka"
    },
    "piandao_jian": {
        "q0": (225, 230, 235), "q1": (235, 200, 75),  "q2": (130, 30, 30),  "q3": (250, 250, 250),
        "cmd": 1703, "name_en": "Master Piandao Steel Jian", "name_id": "Pedang Lurus Jian Master Piandao"
    },
    "sokka_boomerang": {
        "q0": (165, 125, 80),  "q1": (215, 220, 230), "q2": (115, 80, 50),  "q3": (50, 100, 175),
        "cmd": 2702, "name_en": "Water Tribe Bladed Boomerang", "name_id": "Bumerang Tempur Suku Air"
    },
    "hook_swords": {
        "q0": (210, 215, 225), "q1": (190, 140, 50),  "q2": (140, 40, 35),  "q3": (95, 30, 25),
        "cmd": 1704, "name_en": "Jet Twin Hook Swords", "name_id": "Sepasang Pedang Berkait Jet"
    },
    "daili_rock_glove": {
        "q0": (95, 100, 105),  "q1": (65, 70, 75),    "q2": (135, 140, 145), "q3": (45, 170, 105),
        "cmd": 3702, "name_en": "Dai Li Earthbending Rock Glove", "name_id": "Sarung Tangan Batu Dai Li"
    },
    "equalist_shock_gauntlet": {
        "q0": (195, 135, 70),  "q1": (100, 190, 255), "q2": (50, 45, 55),   "q3": (235, 225, 120),
        "cmd": 1705, "name_en": "Equalist Electrified Shock Gauntlet", "name_id": "Sarung Tangan Listrik Equalist"
    },
}


def generate_canonical_weapons():
    tex_dir = RES / "textures/item"
    model_dir = RES / "models/item"
    mc_item_dir = MC_RES / "models/item"
    ensure_dir(tex_dir)
    ensure_dir(model_dir)
    ensure_dir(mc_item_dir)

    overrides = []

    for name, data in CANONICAL_WEAPONS.items():
        q0, q1, q2, q3 = data["q0"], data["q1"], data["q2"], data["q3"]
        cmd = data["cmd"]

        # 64x64 Cel-Shaded 4-Quadrant Pixel Atlas with Shading Variation
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        # Quadrant 0: Main Blade/Head
        draw.rectangle([0, 0, 31, 31], fill=q0)
        draw.rectangle([4, 4, 27, 27], fill=(min(255, q0[0] + 25), min(255, q0[1] + 25), min(255, q0[2] + 25)))
        # Quadrant 1: Metal Fittings & Guard
        draw.rectangle([32, 0, 63, 31], fill=q1)
        draw.rectangle([36, 4, 59, 27], fill=(min(255, q1[0] + 25), min(255, q1[1] + 25), min(255, q1[2] + 25)))
        # Quadrant 2: Grip & Haft
        draw.rectangle([0, 32, 31, 63], fill=q2)
        draw.rectangle([4, 36, 27, 59], fill=(min(255, q2[0] + 20), min(255, q2[1] + 20), min(255, q2[2] + 20)))
        # Quadrant 3: Ornaments, Tassels & Gems
        draw.rectangle([32, 32, 63, 63], fill=q3)
        draw.rectangle([36, 36, 59, 59], fill=(min(255, q3[0] + 30), min(255, q3[1] + 30), min(255, q3[2] + 30)))
        img.save(tex_dir / f"{name}.png")

        # Java 1.21.1 Multi-Cube Item Model (Legal Bounds [-16, 32], Legal Angles)
        model = {
            "credit": "Avatar Elements Canonical 3D Suite (Fabric 1.21.1)",
            "texture_size": [64, 64],
            "textures": {
                "0": f"avatar_elements:item/{name}",
                "particle": f"avatar_elements:item/{name}",
            },
            "elements": [
                {
                    "name": "grip_handle",
                    "from": [7.0, 1.0, 7.0],
                    "to": [9.0, 10.0, 9.0],
                    "faces": {
                        "north": {"uv": [0, 8, 4, 16], "texture": "#0"},
                        "east":  {"uv": [0, 8, 4, 16], "texture": "#0"},
                        "south": {"uv": [0, 8, 4, 16], "texture": "#0"},
                        "west":  {"uv": [0, 8, 4, 16], "texture": "#0"},
                        "up":    {"uv": [8, 0, 12, 4], "texture": "#0"},
                        "down":  {"uv": [8, 0, 12, 4], "texture": "#0"},
                    },
                },
                {
                    "name": "guard_fitting",
                    "from": [5.0, 10.0, 6.0],
                    "to": [11.0, 12.0, 10.0],
                    "faces": {
                        "north": {"uv": [8, 0, 16, 4], "texture": "#0"},
                        "east":  {"uv": [8, 0, 16, 4], "texture": "#0"},
                        "south": {"uv": [8, 0, 16, 4], "texture": "#0"},
                        "west":  {"uv": [8, 0, 16, 4], "texture": "#0"},
                        "up":    {"uv": [8, 0, 16, 4], "texture": "#0"},
                        "down":  {"uv": [8, 0, 16, 4], "texture": "#0"},
                    },
                },
                {
                    "name": "blade_body",
                    "from": [6.5, 12.0, 7.5],
                    "to": [9.5, 30.5, 8.5],
                    "faces": {
                        "north": {"uv": [0, 0, 8, 8], "texture": "#0"},
                        "east":  {"uv": [0, 0, 8, 8], "texture": "#0"},
                        "south": {"uv": [0, 0, 8, 8], "texture": "#0"},
                        "west":  {"uv": [0, 0, 8, 8], "texture": "#0"},
                        "up":    {"uv": [8, 8, 16, 16], "texture": "#0"},
                        "down":  {"uv": [8, 8, 16, 16], "texture": "#0"},
                    },
                },
            ],
            "display": {
                "thirdperson_righthand": {"rotation": [0, -90, 0], "translation": [0, 1.5, 1.0], "scale": [0.92, 0.92, 0.92]},
                "thirdperson_lefthand":  {"rotation": [0, 90, 0],  "translation": [0, 1.5, 1.0], "scale": [0.92, 0.92, 0.92]},
                "firstperson_righthand": {"rotation": [0, -90, 18], "translation": [1.2, 2.0, 0.5], "scale": [0.8, 0.8, 0.8]},
                "firstperson_lefthand":  {"rotation": [0, 90, -18], "translation": [1.2, 2.0, 0.5], "scale": [0.8, 0.8, 0.8]},
                "gui": {"rotation": [30, 45, -35], "translation": [0, -3.0, 0], "scale": [0.55, 0.55, 0.55]},
            },
        }
        write_json(model_dir / f"{name}.json", model)

        overrides.append({"predicate": {"custom_model_data": cmd}, "model": f"avatar_elements:item/{name}"})

    # Vanilla iron_sword.json Predicates Override
    write_json(
        mc_item_dir / "iron_sword.json",
        {
            "parent": "minecraft:item/handheld",
            "textures": {"layer0": "minecraft:item/iron_sword"},
            "overrides": overrides,
        },
    )
    print(f"Generated {len(CANONICAL_WEAPONS)} canonical 3D weapon models & texture atlases.")


# ==============================================================================
# 5. AUDIO & LOCALIZATION
# ==============================================================================
def generate_audio_and_localization():
    sounds = {
        "fire.jab":       {"subtitle": "subtitles.avatar_elements.fire.jab",       "sounds": [{"name": "avatar_elements:fire_jab", "attenuation_distance": 16}]},
        "air.blast":      {"subtitle": "subtitles.avatar_elements.air.blast",      "sounds": [{"name": "avatar_elements:air_blast", "attenuation_distance": 18}]},
        "water.whip":     {"subtitle": "subtitles.avatar_elements.water.whip",     "sounds": [{"name": "avatar_elements:water_whip", "attenuation_distance": 16}]},
        "earth.impact":   {"subtitle": "subtitles.avatar_elements.earth.impact",   "sounds": [{"name": "avatar_elements:earth_impact", "attenuation_distance": 24}]},
        "lightning.cast": {"subtitle": "subtitles.avatar_elements.lightning.cast", "sounds": [{"name": "avatar_elements:lightning_cast", "attenuation_distance": 28}]},
        "healing.chime":  {"subtitle": "subtitles.avatar_elements.healing.chime",  "sounds": [{"name": "avatar_elements:healing_chime", "attenuation_distance": 14}]},
    }
    write_json(RES / "sounds.json", sounds)

    en_us = {
        "subtitles.avatar_elements.fire.jab": "Fire Jab whooshes",
        "subtitles.avatar_elements.air.blast": "Air Blast bursts",
        "subtitles.avatar_elements.water.whip": "Water Whip cracks",
        "subtitles.avatar_elements.earth.impact": "Earth impact rumbles",
        "subtitles.avatar_elements.lightning.cast": "Lightning crackles",
        "subtitles.avatar_elements.healing.chime": "Healing chi chimes",
    }
    id_id = {
        "subtitles.avatar_elements.fire.jab": "Pukulan Api menderu",
        "subtitles.avatar_elements.air.blast": "Ledakan Angin berhembus",
        "subtitles.avatar_elements.water.whip": "Cambuk Air menyabet",
        "subtitles.avatar_elements.earth.impact": "Benturan Tanah bergemuruh",
        "subtitles.avatar_elements.lightning.cast": "Petir menyambar",
        "subtitles.avatar_elements.healing.chime": "Chi penyembuh berdenting",
    }

    for name, data in CANONICAL_WEAPONS.items():
        en_us[f"item.avatar_elements.{name}"] = data["name_en"]
        id_id[f"item.avatar_elements.{name}"] = data["name_id"]

    for name, data in RPG_ATTRIBUTES.items():
        en_us[f"attribute.avatar_elements.{name}"] = data["name"]
        id_id[f"attribute.avatar_elements.{name}"] = data["name"]

    write_json(RES / "lang/en_us.json", en_us)
    write_json(RES / "lang/id_id.json", id_id)
    print("Generated sounds.json and lang files (en_us, id_id).")


# ==============================================================================
# 6. BLENDER MASTER SUITE SCRIPT (BLENDER 4.x SCRIPTING PIPELINE)
# Implements /blender-director, /blender-modeler, /animation, and /anime-style
# ==============================================================================
BLENDER_SCRIPT_CONTENT = '''"""
Blender Master 3D Suite - Avatar Elements
Adheres strictly to /blender-director, /blender-modeler, /animation, and /anime-style skills.
"""
import bpy
import math

def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    col_project = bpy.data.collections.new("COL_Project")
    bpy.context.scene.collection.children.link(col_project)
    
    col_ref = bpy.data.collections.new("COL_Reference")
    col_blockout = bpy.data.collections.new("COL_Blockout")
    col_geo = bpy.data.collections.new("COL_Geo")
    col_collision = bpy.data.collections.new("COL_Collision")
    col_export = bpy.data.collections.new("COL_Export")
    
    for c in [col_ref, col_blockout, col_geo, col_collision, col_export]:
        col_project.children.link(c)
        
    return {"project": col_project, "geo": col_geo, "collision": col_collision, "export": col_export}

def create_anime_toon_material(name, base_color, shadow_color, specular_tint=(1,1,1,1)):
    """Creates a 2-tone Anime Toon Cel Shader with hard shadow breaks."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    s2rgb = nodes.new(type='ShaderNodeShaderToRGB')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    
    # Constant interpolation for crisp anime breaks
    color_ramp.color_ramp.interpolation = 'CONSTANT'
    color_ramp.color_ramp.elements[0].position = 0.45
    color_ramp.color_ramp.elements[0].color = shadow_color
    color_ramp.color_ramp.elements[1].position = 0.46
    color_ramp.color_ramp.elements[1].color = base_color
    
    links.new(diffuse.outputs['BSDF'], s2rgb.inputs['Shader'])
    links.new(s2rgb.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], output.inputs['Surface'])
    
    return mat

def build_weapon_mesh(col_geo, name="SM_Dual_Swords"):
    u = 0.0625 # 1 Minecraft unit = 1/16 meter
    
    # Grip (Origin at 0,0,0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 4.5 * u), scale=(1.2 * u, 1.2 * u, 9 * u))
    grip = bpy.context.active_object
    grip.name = f"{name}_Grip"
    
    # Guard
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 9.5 * u), scale=(4.0 * u, 2.5 * u, 1.0 * u))
    guard = bpy.context.active_object
    guard.name = f"{name}_Guard"
    
    # Blade with Bevel Modifier (Non-destructive)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 20.0 * u), scale=(2.4 * u, 0.8 * u, 20.0 * u))
    blade = bpy.context.active_object
    blade.name = f"{name}_Blade"
    
    bevel = blade.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.015
    bevel.segments = 2
    
    # Add Locators
    loc_tip = bpy.data.objects.new(f"{name}_locator_trail_end", None)
    loc_tip.location = (0, 0, 30.0 * u)
    col_geo.objects.link(loc_tip)
    
    loc_base = bpy.data.objects.new(f"{name}_locator_trail_begin", None)
    loc_base.location = (0, 0, 10.0 * u)
    col_geo.objects.link(loc_base)

def build_combat_animation():
    """Sets up combat swing action keyframes on active object."""
    obj = bpy.context.active_object
    if not obj:
        return
    obj.animation_data_create()
    action = bpy.data.actions.new(name="AN_Combat_Slash_Arc")
    obj.animation_data.action = action
    
    # Frame 1: Anticipation / Windup
    obj.rotation_euler = (0, -math.radians(45), math.radians(25))
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # Frame 6: Active Strike Arc
    obj.rotation_euler = (0, math.radians(75), -math.radians(40))
    obj.keyframe_insert(data_path="rotation_euler", frame=6)
    
    # Frame 12: Recovery Pose
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=12)

if __name__ == "__main__":
    cols = setup_scene()
    toon_mat = create_anime_toon_material("M_Anime_Blade", (0.85, 0.90, 0.95, 1.0), (0.25, 0.30, 0.40, 1.0))
    build_weapon_mesh(cols["geo"], "SM_Dual_Swords")
    print("Blender Master Scene and Weapon Suite successfully initialized.")
'''


def generate_blender_suite():
    tools_dir = BUNDLE_ROOT / "tools/blender"
    ensure_dir(tools_dir)
    write_text(tools_dir / "blender_avatar_master_suite.py", BLENDER_SCRIPT_CONTENT)
    print("Generated blender_avatar_master_suite.py conforming to /blender-modeler & /anime-style.")


# ==============================================================================
# 7. FABRIC 1.21.1 COMPLETE JAVA SOURCES
# ==============================================================================
def generate_java_sources():
    ensure_dir(JAVA_MAIN)
    ensure_dir(JAVA_CLIENT)

    # 1. AvatarParticles.java
    particle_fields = "\n".join([f'    public static final SimpleParticleType {k.upper()} = register("{k}");' for k in PARTICLES_V3.keys()])
    avatar_particles_code = f"""package com.avatarmod.elements.registry;

import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

public final class AvatarParticles {{
    public static final String MOD_ID = "avatar_elements";

{particle_fields}

    private AvatarParticles() {{}}

    private static SimpleParticleType register(String name) {{
        return Registry.register(
            Registries.PARTICLE_TYPE,
            Identifier.of(MOD_ID, name),
            FabricParticleTypes.simple(false)
        );
    }}

    public static void init() {{}}
}}
"""
    write_text(JAVA_MAIN / "AvatarParticles.java", avatar_particles_code)

    # 2. ElementalParticleClientRegistry.java
    registry_calls = []
    for k, spec in PARTICLES_V3.items():
        sheet = "ParticleTextureSheet.PARTICLE_SHEET_OPAQUE" if spec["opaque"] else "ParticleTextureSheet.PARTICLE_SHEET_TRANSLUCENT"
        gravity = "0.35f" if spec["shape"] == "blocky" else ("-0.04f" if "ember" in k or "flame" in k else "0.00f")
        damping = "0.92f" if spec["shape"] == "blocky" else "0.94f"
        registry_calls.append(f"        register(AvatarParticles.{k.upper()}, {sheet}, 16, 0.20f, {gravity}, {damping});")

    calls_block = "\n".join(registry_calls)
    client_registry_code = f"""package com.avatarmod.elements.client.vfx;

import com.avatarmod.elements.registry.AvatarParticles;
import net.fabricmc.api.EnvType;
import net.fabricmc.api.Environment;
import net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry;
import net.minecraft.client.particle.ParticleTextureSheet;
import net.minecraft.client.particle.SpriteBillboardParticle;
import net.minecraft.client.particle.SpriteProvider;
import net.minecraft.client.world.ClientWorld;

@Environment(EnvType.CLIENT)
public final class ElementalParticleClientRegistry {{
    private ElementalParticleClientRegistry() {{}}

    public static void registerAll() {{
{calls_block}
    }}

    private static void register(
        net.minecraft.particle.SimpleParticleType type,
        ParticleTextureSheet sheet,
        int maxAge,
        float scale,
        float gravityStrength,
        float damping
    ) {{
        ParticleFactoryRegistry.getInstance().register(type, sprites ->
            (effect, world, x, y, z, vx, vy, vz) ->
                new ElementalParticle(world, x, y, z, vx, vy, vz, sprites, sheet, maxAge, scale, gravityStrength, damping)
        );
    }}

    private static final class ElementalParticle extends SpriteBillboardParticle {{
        private final SpriteProvider sprites;
        private final ParticleTextureSheet sheet;
        private final float damping;

        private ElementalParticle(
            ClientWorld world,
            double x, double y, double z,
            double vx, double vy, double vz,
            SpriteProvider sprites,
            ParticleTextureSheet sheet,
            int maxAge,
            float scale,
            float gravityStrength,
            float damping
        ) {{
            super(world, x, y, z, vx, vy, vz);
            this.sprites = sprites;
            this.sheet = sheet;
            this.maxAge = maxAge;
            this.scale = scale;
            this.gravityStrength = gravityStrength;
            this.damping = damping;
            this.velocityX = vx;
            this.velocityY = vy;
            this.velocityZ = vz;
            this.setSpriteForAge(sprites);
        }}

        @Override
        public void tick() {{
            super.tick();
            if (!this.dead) {{
                this.setSpriteForAge(this.sprites);
                this.velocityX *= this.damping;
                this.velocityY *= this.damping;
                this.velocityZ *= this.damping;
            }}
        }}

        @Override
        public ParticleTextureSheet getType() {{
            return this.sheet;
        }}
    }}
}}
"""
    write_text(JAVA_CLIENT / "ElementalParticleClientRegistry.java", client_registry_code)
    print("Generated full Java registration and client particle factory.")


# ==============================================================================
# 8. COPY SOUNDS & RIBBONS FROM V2 & SYNC TO ART-SOURCE
# ==============================================================================
def sync_with_v2_and_art_source():
    v2_zip_path = REPO_ROOT / "Avatar_Elements_Asset_Production_v2.zip"
    if v2_zip_path.exists():
        with zipfile.ZipFile(v2_zip_path, "r") as zf:
            for item in zf.namelist():
                if item.endswith(".ogg"):
                    dest = RES / "sounds" / Path(item).name
                    ensure_dir(dest.parent)
                    dest.write_bytes(zf.read(item))
                elif item.endswith(".obj"):
                    dest = BUNDLE_ROOT / "vfx_mesh" / Path(item).name
                    ensure_dir(dest.parent)
                    dest.write_bytes(zf.read(item))
        print("Copied audio SFX and OBJ ribbons from V2 zip.")

    # Sync into art-source/
    art_source_vfx = REPO_ROOT / "art-source/asset_pack_t2_vfx/assets/avatar_elements"
    if art_source_vfx.parent.exists():
        for src_dir, dst_dir in [
            (RES / "textures/particle", art_source_vfx / "textures/particle"),
            (RES / "particles", art_source_vfx / "particles"),
            (RES / "textures/vfx", art_source_vfx / "textures/vfx"),
            (RES / "textures/gui/skills", art_source_vfx / "textures/gui/skills"),
            (RES / "textures/mob_effect", art_source_vfx / "textures/mob_effect"),
        ]:
            if src_dir.exists():
                ensure_dir(dst_dir)
                for f in src_dir.glob("*.png"):
                    shutil.copy2(f, dst_dir / f.name)
                for f in src_dir.glob("*.json"):
                    shutil.copy2(f, dst_dir / f.name)
        print("Synchronized upgraded assets into art-source/asset_pack_t2_vfx/.")


# ==============================================================================
# 9. ZIP BUNDLE V3
# ==============================================================================
def create_zip_v3():
    zip_path = REPO_ROOT / "Avatar_Elements_Asset_Production_v3.zip"
    write_text(
        BUNDLE_ROOT / "README_V3.md",
        """# Avatar Elements Asset Production v3 (Definitive Edition)
Upgraded with Blender Director, Blender Modeler, Animation, and Anime Style principles:
- 32 Anime-style Cel-shaded Particle Types (128 unbaked 16x16 frames with 3-tone discrete breaks).
- 15 Seamless 128x32 VFX Ribbon Textures.
- 37+ Anime Cel Skill Icons & 5 RPG Attribute Icons (32x32).
- 11 Canonical 3D Weapons Suite (64x64 Cel-shaded 4-Quadrant Atlases & Java 1.21.1 JSON Models).
- Complete Fabric 1.21.1 Java Registries (AvatarParticles & ElementalParticleClientRegistry with setSpriteForAge).
- Blender Master Suite Python Script (`tools/blender/blender_avatar_master_suite.py`).
- Audio SFX and sounds.json with English & Indonesian localization.
""",
    )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(BUNDLE_ROOT.rglob("*")):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(BUNDLE_ROOT))
    print(f"Created final deliverable: {zip_path.resolve()} ({zip_path.stat().st_size} bytes)")


if __name__ == "__main__":
    generate_all_particles()
    generate_all_ribbons()
    generate_all_icons()
    generate_canonical_weapons()
    generate_audio_and_localization()
    generate_blender_suite()
    generate_java_sources()
    sync_with_v2_and_art_source()
    create_zip_v3()
