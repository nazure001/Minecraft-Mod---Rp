import os
import json
import math
from PIL import Image, ImageDraw

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
SHOWCASE_DIR = os.path.join(REPO_ROOT, "art-source", "showcase")
MOD_MODELS_DIR = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "models", "entity")
MOD_TEX_DIR = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity")
ARTIFACT_DIR = r"C:\Users\USER\.gemini\antigravity\brain\3da0aa46-232f-4896-9819-483a61eed335"

# -----------------------------------------------------------------------------
# 3D ISOMETRIC HIERARCHICAL RIG RENDERER
# -----------------------------------------------------------------------------

def project_iso(x, y, z, cx, cy, scale):
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    px = cx + (x - z) * scale * cos30
    py = cy - y * scale + (x + z) * scale * sin30
    return (px, py)

def rotate_point(p, rot, pivot):
    # p and pivot are (x, y, z); rot is (rx, ry, rz) in degrees
    x, y, z = p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2]
    
    rad_x = math.radians(rot[0])
    rad_y = math.radians(rot[1])
    rad_z = math.radians(rot[2])

    # Rotation X
    y1 = y * math.cos(rad_x) - z * math.sin(rad_x)
    z1 = y * math.sin(rad_x) + z * math.cos(rad_x)
    x1 = x
    
    # Rotation Y
    x2 = x1 * math.cos(rad_y) + z1 * math.sin(rad_y)
    z2 = -x1 * math.sin(rad_y) + z1 * math.cos(rad_y)
    y2 = y1

    # Rotation Z
    x3 = x2 * math.cos(rad_z) - y2 * math.sin(rad_z)
    y3 = x2 * math.sin(rad_z) + y2 * math.cos(rad_z)
    z3 = z2

    return (x3 + pivot[0], y3 + pivot[1], z3 + pivot[2])

def render_transformed_cube(draw, tex_pix, tex_w, tex_h, cube_pts, uv_rect, cx, cy, scale):
    # cube_pts: list of 8 corners [c000, c100, c110, c010, c001, c101, c111, c011]
    p_2d = [project_iso(pt[0], pt[1], pt[2], cx, cy, scale) for pt in cube_pts]

    # Sample UV
    ux, uy = int(uv_rect[0]) % tex_w, int(uv_rect[1]) % tex_h
    base_color = tex_pix[ux, uy]
    if len(base_color) == 4 and base_color[3] == 0:
        base_color = (180, 150, 130, 255)

    def shade(col, factor):
        return (int(min(255, col[0] * factor)), int(min(255, col[1] * factor)), int(min(255, col[2] * factor)), 255)

    # Faces:
    # Top face (p010, p110, p111, p011)
    draw.polygon([p_2d[3], p_2d[2], p_2d[6], p_2d[7]], fill=shade(base_color, 1.05), outline=shade(base_color, 0.70))
    # South face (p001, p101, p111, p011)
    draw.polygon([p_2d[4], p_2d[5], p_2d[6], p_2d[7]], fill=shade(base_color, 0.85), outline=shade(base_color, 0.60))
    # East face (p100, p101, p111, p110)
    draw.polygon([p_2d[1], p_2d[5], p_2d[6], p_2d[2]], fill=shade(base_color, 0.70), outline=shade(base_color, 0.50))


def render_geo_showcase(mob_id, title, category, element, geo_file, tex_file, scale=12.0, cy_offset=0, rot_view=25):
    with open(geo_file, "r", encoding="utf-8") as f:
        gdata = json.load(f)
    
    geom = gdata.get("minecraft:geometry", [{}])[0]
    tex_w = geom.get("description", {}).get("texture_width", 256)
    tex_h = geom.get("description", {}).get("texture_height", 256)
    bones = geom.get("bones", [])
    
    tex_img = Image.open(tex_file).convert("RGBA")
    tex_pix = tex_img.load()

    W, H = 1200, 800
    canvas = Image.new("RGBA", (W, H), (18, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)

    # Header
    draw.rectangle([0, 0, W, 80], fill=(26, 32, 42, 255))
    draw.line([0, 80, W, 80], fill=(55, 68, 88, 255), width=2)
    draw.text((40, 18), "AVATAR: ELEMENTS — ARTICULATED 3D KINEMATIC SHOWCASE", fill=(245, 248, 255, 255))
    draw.text((40, 44), f"Target: {title} | Kategori: {category} | Rig: {len(bones)} Articulated Bones | Format: GeckoLib 1.12.0", fill=(160, 175, 195, 255))

    # Left: Texture & Spec Card
    draw.rectangle([40, 110, 310, 750], fill=(24, 28, 36, 255), outline=(48, 56, 72, 255), width=2)
    draw.text((55, 125), "ATLAS TEKSTUR RESMI", fill=(240, 200, 80, 255))
    draw.text((55, 145), f"Resolusi: {tex_w}x{tex_h} Pixel Art", fill=(160, 170, 185, 255))
    
    tex_preview = tex_img.resize((230, 230), Image.NEAREST)
    canvas.paste(tex_preview, (60, 175))

    draw.text((55, 425), "FITUR KINEMATIKA & POSE", fill=(100, 220, 140, 255))
    draw.text((55, 450), f"• Total Bones: {len(bones)} Tulang Sendi", fill=(210, 215, 225, 255))
    draw.text((55, 470), "• Hierarki Bersarang (Parent-Child)", fill=(210, 215, 225, 255))
    draw.text((55, 490), "• Natural Resting Posture (Luwes)", fill=(210, 215, 225, 255))
    draw.text((55, 510), "• Paha, Betis & Telapak Berotot", fill=(210, 215, 225, 255))
    draw.text((55, 530), "• Multi-Segment Spine & Ekor", fill=(210, 215, 225, 255))
    draw.text((55, 550), "• Siklus Animasi Idle/Walk/Attack", fill=(210, 215, 225, 255))

    # Right: 3D Viewport
    draw.rectangle([330, 110, 1160, 750], fill=(14, 18, 24, 255), outline=(55, 70, 92, 255), width=2)
    draw.text((350, 125), f"VIEWPORT 3D KINEMATIK — {title.upper()}", fill=(230, 235, 245, 255))
    draw.text((350, 148), f"Geometri multi-sendi dengan pose natural dinamis (bukan T-Pose siku-siku)", fill=(130, 145, 165, 255))

    cx = 745
    cy = 480 + cy_offset

    # Ground Shadow
    shadow_pts = [
        project_iso(-35, 0, -35, cx, cy, scale),
        project_iso(35, 0, -35, cx, cy, scale),
        project_iso(35, 0, 35, cx, cy, scale),
        project_iso(-35, 0, 35, cx, cy, scale)
    ]
    draw.polygon(shadow_pts, fill=(10, 12, 16, 255))

    # Collect and transform all cubes
    transformed_cubes = []
    
    # Simple global model rotation
    def global_rot(p):
        rad = math.radians(rot_view)
        rx = p[0] * math.cos(rad) + p[2] * math.sin(rad)
        rz = -p[0] * math.sin(rad) + p[2] * math.cos(rad)
        return (rx, p[1], rz)

    for b in bones:
        b_rot = b.get("rotation", [0, 0, 0])
        b_pivot = b.get("pivot", [0, 0, 0])
        for c in b.get("cubes", []):
            ox, oy, oz = c.get("origin", [0, 0, 0])
            sx, sy, sz = c.get("size", [1, 1, 1])
            uv = c.get("uv", [0, 0])

            # 8 corners
            raw_pts = [
                (ox, oy, oz), (ox + sx, oy, oz), (ox + sx, oy + sy, oz), (ox, oy + sy, oz),
                (ox, oy, oz + sz), (ox + sx, oy, oz + sz), (ox + sx, oy + sy, oz + sz), (ox, oy + sy, oz + sz)
            ]
            # Apply bone rotation around pivot
            rotated_pts = [rotate_point(pt, b_rot, b_pivot) for pt in raw_pts]
            # Apply global view rotation
            final_pts = [global_rot(pt) for pt in rotated_pts]

            # Compute depth for painter's algorithm
            avg_depth = sum(pt[0] + pt[2] for pt in final_pts) / 8.0 - (sum(pt[1] for pt in final_pts) / 8.0) * 0.1
            transformed_cubes.append((avg_depth, final_pts, uv))

    # Sort by depth
    transformed_cubes.sort(key=lambda x: x[0])

    for depth, pts, uv in transformed_cubes:
        render_transformed_cube(draw, tex_pix, tex_w, tex_h, pts, uv, cx, cy, scale)

    # Save to art-source/showcase and artifact directory
    out_path_repo = os.path.join(SHOWCASE_DIR, f"mockup_{mob_id}.png")
    canvas.save(out_path_repo, format="PNG")
    
    out_path_art = os.path.join(ARTIFACT_DIR, f"mockup_{mob_id}.png")
    canvas.save(out_path_art, format="PNG")
    print(f"Generated Articulated Showcase for {mob_id} -> {out_path_repo}")


def execute_renders():
    print("="*70)
    print("RENDERING ARTICULATED 3D ISOMETRIC SHOWCASE PREVIEWS")
    print("="*70)

    # 1. Flying Bison (71 Bones, 512x512 Texture)
    bison_geo = os.path.join(MOD_MODELS_DIR, "flying_bison.geo.json")
    bison_tex = os.path.join(MOD_TEX_DIR, "pet", "flying_bison.png")
    render_geo_showcase("flying_bison", "Flying Bison (Sky Bison / Appa)", "Pet / Mount", "Air (Nomad Companion)", bison_geo, bison_tex, scale=3.6, cy_offset=-40, rot_view=20)

    # 2. Platypus Bear (21 Bones, 256x256 Texture)
    platypus_geo = os.path.join(MOD_MODELS_DIR, "platypus_bear.geo.json")
    platypus_tex = os.path.join(MOD_TEX_DIR, "mobs", "platypus_bear.png")
    render_geo_showcase("platypus_bear", "Platypus Bear (Beruang Berparuh)", "Wild Creature / Mob", "Earth Kingdom Fauna", platypus_geo, platypus_tex, scale=12.0, cy_offset=10, rot_view=25)

    # 3. Phoenix King Ozai (22 Bones, 256x256 Texture)
    ozai_geo = os.path.join(MOD_MODELS_DIR, "phoenix_king_ozai.geo.json")
    ozai_tex = os.path.join(MOD_TEX_DIR, "boss", "phoenix_king_ozai.png")
    render_geo_showcase("phoenix_king_ozai", "Phoenix King Ozai (Raja Api Ozai)", "Prime Boss", "Fire / Lightning (Sozin Comet)", ozai_geo, ozai_tex, scale=15.0, cy_offset=40, rot_view=20)

    print("\n" + "="*70)
    print("ALL ARTICULATED SHOWCASE RENDERS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    execute_renders()
