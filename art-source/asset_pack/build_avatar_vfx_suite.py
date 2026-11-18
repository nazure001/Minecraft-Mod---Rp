"""
Avatar Elements Mod - Complete 3D VFX & Asset Production Suite
Authors: Antigravity IDE (3D Technical Art Lead)
Standards: blender-skills (vfx-fx, procedural-modeling, materials) + Blockbench 4.10 Spec

Produces:
1. Elemental Charge Orbs Suite (Fire, Water, Earth, Air)
   - SM_Charge_Orb_Quad: .bbmodel, .obj, .mtl, .geo.json, .json, atlas texture, pulse/spin animation
2. Captured Earth Shards & Earth Armor Overlay
   - SM_Captured_Shards & SM_Earth_Armor_Plates: .bbmodel, .obj, .mtl, .geo.json, .json, textures, orbit animation
3. Air Vortex Funnel
   - SM_Air_Vortex_Funnel: .bbmodel, .obj, .mtl, .geo.json, .json, texture, tornado spin animation
4. Water Whip Segmented Stream
   - SM_Water_Whip_Segmented: .bbmodel, .obj, .mtl, .geo.json, .json, texture, wave animation
5. Boulder Launch Megalith
   - SM_Boulder_Launch_Megalith: .bbmodel, .obj, .mtl, .geo.json, .json, texture
6. Multi-angle 3D Previews & Turntable GIFs
7. Complete Handoff Specifications for Claude Code
"""

import os
import sys
import math
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
ASSET_PACK_DIR = os.path.join(REPO_ROOT, "art-source", "asset_pack")
MODELS_DIR = os.path.join(ASSET_PACK_DIR, "models")
BBMODELS_DIR = os.path.join(MODELS_DIR, "bbmodel")
MESHES_VFX_DIR = os.path.join(ASSET_PACK_DIR, "meshes", "vfx")
ANIMATIONS_DIR = os.path.join(ASSET_PACK_DIR, "animations")
TEXTURES_VFX_DIR = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "vfx")
PREVIEWS_DIR = os.path.join(ASSET_PACK_DIR, "previews")
DOCS_DIR = os.path.join(ASSET_PACK_DIR, "docs")

for d in [MODELS_DIR, BBMODELS_DIR, MESHES_VFX_DIR, ANIMATIONS_DIR, TEXTURES_VFX_DIR, PREVIEWS_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

SCALE_FACTOR = 0.0625 # 1 Blockbench unit = 1/16 meter

# Helper: Point rotation
def rotate_pt(pt, origin, axis, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    x, y, z = pt[0] - origin[0], pt[1] - origin[1], pt[2] - origin[2]
    if axis == "x":
        ny = y * cos_a - z * sin_a
        nz = y * sin_a + z * cos_a
        return (x + origin[0], ny + origin[1], nz + origin[2])
    elif axis == "y":
        nx = x * cos_a + z * sin_a
        nz = -x * sin_a + z * cos_a
        return (nx + origin[0], y + origin[1], nz + origin[2])
    elif axis == "z":
        nx = x * cos_a - y * sin_a
        ny = x * sin_a + y * cos_a
        return (nx + origin[0], ny + origin[1], z + origin[2])
    return pt

# Universal Exporter: Exports elements to .bbmodel, .obj, .mtl, .geo.json, .json
def export_asset_package(asset_id, asset_name, elements, texture_img, animations=None, custom_outliner=None, pivot_desc="Center Contact"):
    print(f"\n==========================================")
    print(f"--> Exporting Asset: {asset_id} ({asset_name})")
    print(f"==========================================")
    
    # 1. Save Texture
    tex_filename = f"{asset_id}.png"
    tex_path = os.path.join(TEXTURES_VFX_DIR, tex_filename)
    texture_img.save(tex_path, "PNG")
    # Also save in models and meshes for direct preview
    texture_img.save(os.path.join(MODELS_DIR, tex_filename), "PNG")
    texture_img.save(os.path.join(MESHES_VFX_DIR, tex_filename), "PNG")
    
    # Base64 for bbmodel
    buf = BytesIO()
    texture_img.save(buf, format="PNG")
    tex_b64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
    
    # 2. Blockbench .bbmodel
    import uuid
    bb_elements = []
    outliner = custom_outliner if custom_outliner else [{"name": "root", "origin": [0, 0, 0], "children": []}]
    root_group = outliner[0]["children"]
    
    w, h = texture_img.size
    
    for elem in elements:
        elem_uuid = str(uuid.uuid4())
        u0, v0, u1, v1 = elem.get("uv", [0, 0, 16, 16])
        faces = {}
        for f in ["north", "east", "south", "west", "up", "down"]:
            faces[f] = {"uv": [u0, v0, u1, v1], "texture": 0}
            
        bb_elem = {
            "name": elem["name"],
            "box_uv": False,
            "from": elem["from"],
            "to": elem["to"],
            "faces": faces,
            "uuid": elem_uuid
        }
        if "rotation" in elem:
            rot = elem["rotation"]
            bb_elem["rotation"] = [
                rot["angle"] if rot["axis"] == "x" else 0,
                rot["angle"] if rot["axis"] == "y" else 0,
                rot["angle"] if rot["axis"] == "z" else 0
            ]
            bb_elem["origin"] = rot["origin"]
        else:
            bb_elem["origin"] = [0, 0, 0]
            
        bb_elements.append(bb_elem)
        root_group.append(elem_uuid)
        
    bbmodel_data = {
        "meta": {"format_version": "4.10", "model_format": "bedrock", "box_uv": False},
        "name": asset_id,
        "model_identifier": f"geometry.{asset_id}",
        "resolution": {"width": w, "height": h},
        "elements": bb_elements,
        "outliner": outliner,
        "textures": [
            {
                "path": tex_filename,
                "name": tex_filename,
                "folder": "textures/vfx",
                "namespace": "avatar_elements",
                "id": "0",
                "particle": False,
                "render_mode": "default",
                "visible": True,
                "mode": "bitmap",
                "saved": True,
                "uuid": str(uuid.uuid4()),
                "source": tex_b64
            }
        ],
        "animations": animations if animations else []
    }
    
    bb_path = os.path.join(BBMODELS_DIR, f"{asset_id}.bbmodel")
    with open(bb_path, "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)
    with open(os.path.join(MESHES_VFX_DIR, f"{asset_id}.bbmodel"), "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)
    print(f"  [OK] Saved Blockbench Project: {bb_path}")
    
    # 3. Wavefront OBJ & MTL
    mtl_path = os.path.join(MESHES_VFX_DIR, f"{asset_id}.mtl")
    with open(mtl_path, "w", encoding="utf-8") as f:
        f.write(f"# Avatar Elements Material: {asset_id}\n")
        f.write(f"newmtl {asset_id}_mat\n")
        f.write("Kd 1.0 1.0 1.0\n")
        f.write("Ks 0.2 0.2 0.2\n")
        f.write("Ns 20.0\n")
        f.write("d 1.0\n")
        f.write(f"map_Kd {tex_filename}\n")
        
    obj_path = os.path.join(MESHES_VFX_DIR, f"{asset_id}.obj")
    vertices = []
    texcoords = []
    normals = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
    mesh_faces = []
    
    for elem in elements:
        f_x, f_y, f_z = elem["from"]
        t_x, t_y, t_z = elem["to"]
        raw_corners = [
            (f_x, f_y, f_z), (t_x, f_y, f_z), (t_x, t_y, f_z), (f_x, t_y, f_z),
            (f_x, f_y, t_z), (t_x, f_y, t_z), (t_x, t_y, t_z), (f_x, t_y, t_z)
        ]
        rot = elem.get("rotation")
        corners = [rotate_pt(pt, rot["origin"], rot["axis"], rot["angle"]) for pt in raw_corners] if rot else raw_corners
        scaled_corners = [(c[0] * SCALE_FACTOR, c[1] * SCALE_FACTOR, c[2] * SCALE_FACTOR) for c in corners]
        
        v_base = len(vertices) + 1
        for sc in scaled_corners:
            vertices.append(sc)
            
        u0, v0, u1, v1 = elem.get("uv", [0, 0, 16, 16])
        u0_f = u0 / float(w)
        v0_f = 1.0 - (v0 / float(h))
        u1_f = u1 / float(w)
        v1_f = 1.0 - (v1 / float(h))
        
        vt_base = len(texcoords) + 1
        texcoords.extend([(u0_f, v0_f), (u1_f, v0_f), (u1_f, v1_f), (u0_f, v1_f)])
        
        mesh_faces.append(((v_base+0, vt_base+0, 2), (v_base+3, vt_base+3, 2), (v_base+2, vt_base+2, 2), (v_base+1, vt_base+1, 2)))
        mesh_faces.append(((v_base+5, vt_base+0, 1), (v_base+6, vt_base+3, 1), (v_base+7, vt_base+2, 1), (v_base+4, vt_base+1, 1)))
        mesh_faces.append(((v_base+4, vt_base+0, 4), (v_base+7, vt_base+3, 4), (v_base+3, vt_base+2, 4), (v_base+0, vt_base+1, 4)))
        mesh_faces.append(((v_base+1, vt_base+0, 3), (v_base+2, vt_base+3, 3), (v_base+6, vt_base+2, 3), (v_base+5, vt_base+1, 3)))
        mesh_faces.append(((v_base+3, vt_base+0, 5), (v_base+7, vt_base+3, 5), (v_base+6, vt_base+2, 5), (v_base+2, vt_base+1, 5)))
        mesh_faces.append(((v_base+0, vt_base+0, 6), (v_base+1, vt_base+3, 6), (v_base+5, vt_base+2, 6), (v_base+4, vt_base+1, 6)))
        
    with open(obj_path, "w", encoding="utf-8") as f:
        f.write(f"# Avatar Elements 3D VFX Mesh: {asset_id}\n")
        f.write(f"# Pivot: {pivot_desc} | Units: Metric (1.0 = 1 meter)\n")
        f.write(f"mtllib {asset_id}.mtl\n")
        f.write(f"o {asset_name}\n")
        for v in vertices:
            f.write(f"v {v[0]:.5f} {v[1]:.5f} {v[2]:.5f}\n")
        for vt in texcoords:
            f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
        for vn in normals:
            f.write(f"vn {vn[0]:.1f} {vn[1]:.1f} {vn[2]:.1f}\n")
        f.write(f"usemtl {asset_id}_mat\n")
        f.write("s 1\n")
        for face in mesh_faces:
            f.write(f"f {face[0][0]}/{face[0][1]}/{face[0][2]} {face[1][0]}/{face[1][1]}/{face[1][2]} {face[2][0]}/{face[2][1]}/{face[2][2]} {face[3][0]}/{face[3][1]}/{face[3][2]}\n")
    print(f"  [OK] Saved Wavefront OBJ: {obj_path}")
    
    # 4. Bedrock geo.json
    geo_cubes = []
    for elem in elements:
        s_x = elem["to"][0] - elem["from"][0]
        s_y = elem["to"][1] - elem["from"][1]
        s_z = elem["to"][2] - elem["from"][2]
        u0, v0, u1, v1 = elem.get("uv", [0, 0, 16, 16])
        cube = {"origin": elem["from"], "size": [s_x, s_y, s_z], "uv": [u0, v0]}
        if "rotation" in elem:
            rot = elem["rotation"]
            cube["pivot"] = rot["origin"]
            cube["rotation"] = [
                rot["angle"] if rot["axis"] == "x" else 0,
                rot["angle"] if rot["axis"] == "y" else 0,
                rot["angle"] if rot["axis"] == "z" else 0
            ]
        geo_cubes.append(cube)
        
    geo_data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": f"geometry.{asset_id}",
                    "texture_width": w,
                    "texture_height": h,
                    "visible_bounds_width": 3,
                    "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 1, 0]
                },
                "bones": [{"name": "root", "pivot": [0, 0, 0], "cubes": geo_cubes}]
            }
        ]
    }
    geo_path = os.path.join(MODELS_DIR, f"{asset_id}.geo.json")
    with open(geo_path, "w", encoding="utf-8") as f:
        json.dump(geo_data, f, indent=2)
    print(f"  [OK] Saved Bedrock Geo: {geo_path}")
    
    # 5. Java Display Model .json
    java_elements = []
    for elem in elements:
        j_from = [elem["from"][0] + 8.0, elem["from"][1] + 8.0, elem["from"][2] + 8.0]
        j_to   = [elem["to"][0] + 8.0,   elem["to"][1] + 8.0,   elem["to"][2] + 8.0]
        u0, v0, u1, v1 = elem.get("uv", [0, 0, 16, 16])
        faces = {}
        for f in ["north", "east", "south", "west", "up", "down"]:
            faces[f] = {"uv": [u0 / 4.0, v0 / 4.0, u1 / 4.0, v1 / 4.0], "texture": "#texture"}
        j_elem = {"name": elem["name"], "from": j_from, "to": j_to, "faces": faces}
        if "rotation" in elem:
            rot = elem["rotation"]
            j_elem["rotation"] = {
                "origin": [rot["origin"][0] + 8.0, rot["origin"][1] + 8.0, rot["origin"][2] + 8.0],
                "axis": rot["axis"],
                "angle": rot["angle"]
            }
        java_elements.append(j_elem)
        
    java_data = {
        "credit": f"Avatar Elements Mod - {asset_name} (Fabric 1.21.1)",
        "texture_size": [w, h],
        "textures": {
            "texture": f"avatar_elements:textures/vfx/{asset_id}",
            "particle": f"avatar_elements:textures/vfx/{asset_id}"
        },
        "elements": java_elements,
        "display": {
            "ground": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
            "fixed":  {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
            "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.65, 0.65, 0.65]},
            "firstperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.75, 0.75, 0.75]}
        }
    }
    java_path = os.path.join(MODELS_DIR, f"{asset_id}.json")
    with open(java_path, "w", encoding="utf-8") as f:
        json.dump(java_data, f, indent=2)
    # Also in assets item models
    with open(os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "models", "item", f"{asset_id}.json"), "w", encoding="utf-8") as f:
        json.dump(java_data, f, indent=2)
    print(f"  [OK] Saved Java Display Model: {java_path}")
    
    # 6. Render 3D Preview (Isometric & Turntable GIF)
    preview_sub = os.path.join(PREVIEWS_DIR, asset_id)
    os.makedirs(preview_sub, exist_ok=True)
    
    def project_v(v, yaw_deg, pitch_deg, scale, cx, cy):
        x, y, z = v
        yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
        x1 = x * math.cos(yaw) + z * math.sin(yaw)
        z1 = -x * math.sin(yaw) + z * math.cos(yaw)
        y2 = y * math.cos(pitch) - z1 * math.sin(pitch)
        x2 = x1
        z2 = y * math.sin(pitch) + z1 * math.cos(pitch)
        return (cx + x2 * scale, cy - y2 * scale, z2)
        
    def render_one(yaw, pitch, w_px=320, h_px=320, sc=90, cx=160, cy=160, col_base=(160, 160, 160)):
        im = Image.new("RGBA", (w_px, h_px), (20, 22, 26, 255))
        d = ImageDraw.Draw(im)
        quads = []
        l_dir = (-0.577, 0.577, 0.577)
        for face in mesh_faces:
            p0 = vertices[face[0][0] - 1]
            p1 = vertices[face[1][0] - 1]
            p2 = vertices[face[2][0] - 1]
            p3 = vertices[face[3][0] - 1]
            v01 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            v03 = (p3[0] - p0[0], p3[1] - p0[1], p3[2] - p0[2])
            nx = v01[1] * v03[2] - v01[2] * v03[1]
            ny = v01[2] * v03[0] - v01[0] * v03[2]
            nz = v01[0] * v03[1] - v01[1] * v03[0]
            nl = math.sqrt(nx*nx + ny*ny + nz*nz)
            nx, ny, nz = (nx/nl, ny/nl, nz/nl) if nl > 1e-6 else (0, 1, 0)
            dot = max(0.2, nx * l_dir[0] + ny * l_dir[1] + nz * l_dir[2])
            inte = 0.4 + 0.6 * dot
            c_fill = (min(255, int(col_base[0] * inte)), min(255, int(col_base[1] * inte)), min(255, int(col_base[2] * inte)), 255)
            c_edge = (max(0, int(c_fill[0] * 0.4)), max(0, int(c_fill[1] * 0.4)), max(0, int(c_fill[2] * 0.4)), 255)
            
            pr0 = project_v(p0, yaw, pitch, sc, cx, cy)
            pr1 = project_v(p1, yaw, pitch, sc, cx, cy)
            pr2 = project_v(p2, yaw, pitch, sc, cx, cy)
            pr3 = project_v(p3, yaw, pitch, sc, cx, cy)
            ad = (pr0[2] + pr1[2] + pr2[2] + pr3[2]) / 4.0
            quads.append((ad, [(pr0[0], pr0[1]), (pr1[0], pr1[1]), (pr2[0], pr2[1]), (pr3[0], pr3[1])], c_fill, c_edge))
            
        quads.sort(key=lambda q: q[0])
        for q in quads:
            d.polygon(q[1], fill=q[2], outline=q[3])
        return im

    # Choose primary color tint based on asset theme
    if "fire" in asset_id:
        t_col = (235, 120, 30)
    elif "water" in asset_id:
        t_col = (50, 160, 240)
    elif "earth" in asset_id or "boulder" in asset_id or "armor" in asset_id:
        t_col = (130, 115, 95)
    elif "air" in asset_id:
        t_col = (200, 230, 240)
    else:
        t_col = (180, 180, 180)
        
    iso_img = render_one(45, 25, 400, 400, 130, 200, 200, t_col)
    iso_img.save(os.path.join(preview_sub, f"{asset_id}_isometric.png"))
    
    # Turntable 360 GIF
    gif_frames = []
    for deg in range(0, 360, 15):
        gif_frames.append(render_one(deg, 20, 256, 256, 85, 128, 128, t_col))
    gif_frames[0].save(os.path.join(preview_sub, f"{asset_id}_turntable.gif"), save_all=True, append_images=gif_frames[1:], duration=60, loop=0)
    print(f"  [OK] Saved 3D Previews: {preview_sub}")
    return bb_path, obj_path


# =============================================================
# ASSET 1: ELEMENTAL CHARGE ORBS (4 ELEMENTS)
# =============================================================
print("\n>>> BUILDING ASSET SUITE 1: ELEMENTAL CHARGE ORBS (FIRE, WATER, EARTH, AIR)")

# Texture Atlas 64x64: 4 quadrants for 4 elements
orb_tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
orb_pix = orb_tex.load()

# Q0 [0..32, 0..32]: Fire Plasma Core (Solar flare, orange, yellow core)
for y in range(0, 32):
    for x in range(0, 32):
        d = math.sqrt((x - 16)**2 + (y - 16)**2)
        if d <= 4:
            c = (255, 255, 220, 255) # White hot core
        elif d <= 9:
            c = (255, 180, 40, 245)  # Solar yellow-orange
        elif d <= 14:
            c = (235, 75, 15, 220)   # Blazing red flare
        else:
            c = (140, 20, 5, 0)
        orb_pix[x, y] = c

# Q1 [32..64, 0..32]: Water Fluid Swirl (Aqua, cyan glow, deep ocean)
for y in range(0, 32):
    for x in range(32, 64):
        lx, ly = x - 32, y
        d = math.sqrt((lx - 16)**2 + (ly - 16)**2)
        swirl = (lx * 3 + ly * 5) % 6
        if d <= 5:
            c = (210, 245, 255, 230) # Core foam crest
        elif d <= 10:
            c = (60, 190, 245, 210)  # Cyan vortex
        elif d <= 14:
            c = (20, 100, 210, 180)  # Deep water
        else:
            c = (0, 0, 0, 0)
        orb_pix[x, y] = c

# Q2 [0..32, 32..64]: Earth Geode (Slate core, granite shell, emerald jade glint)
for y in range(32, 64):
    for x in range(0, 32):
        lx, ly = x, y - 32
        d = math.sqrt((lx - 16)**2 + (ly - 16)**2)
        if d <= 5:
            c = (120, 240, 160, 255) # Jade inner crystal
        elif d <= 10:
            c = (110, 102, 92, 255)  # Chiseled granite
        elif d <= 14:
            c = (65, 58, 50, 255)    # Basalt crust
        else:
            c = (0, 0, 0, 0)
        orb_pix[x, y] = c

# Q3 [32..64, 32..64]: Air Vortex (Translucent white, sky teal, aerodynamic rings)
for y in range(32, 64):
    for x in range(32, 64):
        lx, ly = x - 32, y - 32
        d = math.sqrt((lx - 16)**2 + (ly - 16)**2)
        ring = (lx + ly * 2) % 4
        if d <= 6:
            c = (255, 255, 255, 240) # Dense air center
        elif d <= 11:
            c = (215, 240, 250, 190) # Slipstream pale teal
        elif d <= 15:
            c = (180, 215, 235, 140) # Outer gust
        else:
            c = (0, 0, 0, 0)
        orb_pix[x, y] = c

# Geometry: Concentric Multi-Ring Elemental Sphere (Pivot at Knuckle 0,0,0)
orb_elements = [
    # Inner Plasma/Matter Core (8-sided faceted sphere)
    {"name": "core_sphere", "from": [-3.0, -3.0, -3.0], "to": [3.0, 3.0, 3.0], "uv": [0, 0, 16, 16]},
    {"name": "core_facet_x", "from": [-2.5, -2.5, -2.5], "to": [2.5, 2.5, 2.5], "rotation": {"origin": [0,0,0], "axis": "x", "angle": 45.0}, "uv": [0, 0, 16, 16]},
    {"name": "core_facet_y", "from": [-2.5, -2.5, -2.5], "to": [2.5, 2.5, 2.5], "rotation": {"origin": [0,0,0], "axis": "y", "angle": 45.0}, "uv": [0, 0, 16, 16]},
    {"name": "core_facet_z", "from": [-2.5, -2.5, -2.5], "to": [2.5, 2.5, 2.5], "rotation": {"origin": [0,0,0], "axis": "z", "angle": 45.0}, "uv": [0, 0, 16, 16]},
    
    # Outer Orbital Corona Shell
    {"name": "corona_ring_horizontal", "from": [-5.5, -0.6, -5.5], "to": [5.5, 0.6, 5.5], "rotation": {"origin": [0,0,0], "axis": "y", "angle": 25.0}, "uv": [16, 0, 32, 16]},
    {"name": "corona_ring_inclined",   "from": [-5.5, -0.6, -5.5], "to": [5.5, 0.6, 5.5], "rotation": {"origin": [0,0,0], "axis": "x", "angle": 35.0}, "uv": [16, 0, 32, 16]},
    {"name": "corona_ring_perpendicular", "from": [-5.5, -0.6, -5.5], "to": [5.5, 0.6, 5.5], "rotation": {"origin": [0,0,0], "axis": "z", "angle": 55.0}, "uv": [16, 0, 32, 16]},
    
    # 4 Orbiting Elemental Catalyst Shards
    {"name": "shard_north", "from": [-1.0, 4.0, -1.0], "to": [1.0, 6.0, 1.0], "rotation": {"origin": [0,0,0], "axis": "x", "angle": 15.0}, "uv": [0, 32, 16, 48]},
    {"name": "shard_south", "from": [-1.0, -6.0, -1.0], "to": [1.0, -4.0, 1.0], "rotation": {"origin": [0,0,0], "axis": "x", "angle": -15.0}, "uv": [0, 32, 16, 48]},
    {"name": "shard_east",  "from": [4.0, -1.0, -1.0], "to": [6.0, 1.0, 1.0], "rotation": {"origin": [0,0,0], "axis": "z", "angle": 15.0}, "uv": [32, 32, 48, 48]},
    {"name": "shard_west",  "from": [-6.0, -1.0, -1.0], "to": [-4.0, 1.0, 1.0], "rotation": {"origin": [0,0,0], "axis": "z", "angle": -15.0}, "uv": [32, 32, 48, 48]}
]

# Continuous 360 Spin & Breathing Pulse Animation (0.8s loop)
orb_anims = [
    {
        "name": "orb_idle_spin",
        "loop": "loop",
        "length": 0.8,
        "animators": {
            "root": {
                "rotation": {
                    "0.0": [0, 0, 0],
                    "0.4": [180, 180, 0],
                    "0.8": [360, 360, 0]
                },
                "scale": {
                    "0.0": [1.0, 1.0, 1.0],
                    "0.2": [1.15, 1.15, 1.15],
                    "0.4": [0.95, 0.95, 0.95],
                    "0.6": [1.1, 1.1, 1.1],
                    "0.8": [1.0, 1.0, 1.0]
                }
            }
        }
    }
]

export_asset_package("charge_orb_elemental", "Elemental Charge Orb", orb_elements, orb_tex, orb_anims, pivot_desc="Knuckle Pivot (0,0,0)")


# =============================================================
# ASSET 2: CAPTURED SHARDS & EARTH ARMOR OVERLAY
# =============================================================
print("\n>>> BUILDING ASSET SUITE 2: CAPTURED SHARDS & EARTH ARMOR OVERLAY")

# Texture 64x64 for Earth Armor
armor_tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
armor_pix = armor_tex.load()
for y in range(0, 64):
    for x in range(0, 64):
        border = min(x % 16, 15 - (x % 16), y % 16, 15 - (y % 16))
        grain = (x * 7 + y * 11) % 5
        if border <= 1:
            c = (55, 48, 42, 255) # Chiseled stone edge
        elif border <= 3:
            c = (88, 80, 72, 255) # Bevel midtone
        elif (x + y) % 11 == 0:
            c = (40, 140, 75, 255) # Embedded jade vein
        else:
            c = (125, 118, 108, 255) if grain <= 2 else (145, 138, 126, 255)
        armor_pix[x, y] = c

# A. Captured Shards (4 Orbiting Rock Plates around Player Body)
captured_shards_elements = [
    # Shard Front-Right
    {"name": "shard_fr", "from": [ 9.0, 6.0, -10.0], "to": [14.0, 14.0, -8.0], "rotation": {"origin": [ 11.5, 10.0, -9.0], "axis": "y", "angle": -30.0}, "uv": [0, 0, 16, 16]},
    # Shard Front-Left
    {"name": "shard_fl", "from": [-14.0, 8.0, -10.0], "to": [ -9.0, 16.0, -8.0], "rotation": {"origin": [-11.5, 12.0, -9.0], "axis": "y", "angle": 30.0}, "uv": [0, 0, 16, 16]},
    # Shard Back-Right
    {"name": "shard_br", "from": [ 9.0, 10.0,  8.0], "to": [14.0, 18.0, 10.0], "rotation": {"origin": [ 11.5, 14.0,  9.0], "axis": "y", "angle": 35.0}, "uv": [16, 0, 32, 16]},
    # Shard Back-Left
    {"name": "shard_bl", "from": [-14.0, 5.0,  8.0], "to": [ -9.0, 13.0, 10.0], "rotation": {"origin": [-11.5,  9.0,  9.0], "axis": "y", "angle": -35.0}, "uv": [16, 0, 32, 16]},
    # Central Hovering Kinetic Catalyst
    {"name": "kinetic_core", "from": [-2.0, 9.0, -11.0], "to": [2.0, 13.0, -9.0], "rotation": {"origin": [0, 11, -10], "axis": "z", "angle": 45.0}, "uv": [32, 0, 48, 16]}
]

captured_anims = [
    {
        "name": "orbit_defensive",
        "loop": "loop",
        "length": 1.2,
        "animators": {
            "root": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [0, 180, 0], "1.2": [0, 360, 0]},
                "position": {"0.0": [0, 0, 0], "0.3": [0, 1.5, 0], "0.6": [0, 0, 0], "0.9": [0, -1.5, 0], "1.2": [0, 0, 0]}
            }
        }
    }
]
export_asset_package("captured_earth_shards", "Captured Earth Shards", captured_shards_elements, armor_tex, captured_anims, pivot_desc="Body Center (0, 12, 0)")

# B. Earth Armor Overlay Plates (Chest, Pauldrons, Bracers)
earth_armor_elements = [
    # Chestplate Heavy Slab
    {"name": "chest_slab_main", "from": [-5.5, 12.0, -3.8], "to": [5.5, 23.0, -2.0], "uv": [0, 0, 24, 24]},
    {"name": "chest_ridge_v",   "from": [-1.2, 13.0, -4.5], "to": [1.2, 22.0, -3.5], "uv": [24, 0, 32, 24]},
    # Right Shoulder Pauldron
    {"name": "pauldron_right",  "from": [4.5, 20.0, -3.0],  "to": [9.5, 25.5, 3.0],  "rotation": {"origin": [4.5, 20.0, 0], "axis": "z", "angle": -18.0}, "uv": [32, 0, 48, 16]},
    # Left Shoulder Pauldron
    {"name": "pauldron_left",   "from": [-9.5, 20.0, -3.0], "to": [-4.5, 25.5, 3.0], "rotation": {"origin": [-4.5, 20.0, 0], "axis": "z", "angle": 18.0}, "uv": [32, 0, 48, 16]},
    # Right Forearm Guard (Gauntlet)
    {"name": "gauntlet_right",  "from": [4.2, 11.0, -2.8],  "to": [8.8, 17.5, 2.8],  "uv": [0, 32, 16, 48]},
    # Left Forearm Guard (Gauntlet)
    {"name": "gauntlet_left",   "from": [-8.8, 11.0, -2.8], "to": [-4.2, 17.5, 2.8], "uv": [0, 32, 16, 48]},
    # Back Bedrock Plate
    {"name": "back_slab",       "from": [-5.0, 12.0, 2.0],   "to": [5.0, 22.5, 3.8],  "uv": [16, 32, 32, 48]}
]
export_asset_package("earth_armor_overlay", "Earth Armor Overlay", earth_armor_elements, armor_tex, pivot_desc="Player Center (0, 0, 0)")


# =============================================================
# ASSET 3: AIR VORTEX HELICAL FUNNEL
# =============================================================
print("\n>>> BUILDING ASSET SUITE 3: AIR VORTEX HELICAL FUNNEL")

vortex_tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
v_pix = vortex_tex.load()
for y in range(0, 64):
    for x in range(0, 64):
        spiral = (x * 4 + y * 8) % 32
        alpha = int(140 + 100 * math.sin(y * 0.2))
        c = (235, 248, 255, max(80, min(240, alpha))) if spiral < 12 else (180, 220, 245, 110)
        v_pix[x, y] = c

# Stacked Expanding Helical Vortex Rings
vortex_elements = [
    # Ground Suction Eye (Tier 0)
    {"name": "vortex_eye_base", "from": [-3.0, 0.0, -3.0], "to": [3.0, 3.0, 3.0], "uv": [0, 0, 16, 16]},
    # Tier 1 Funnel Ring
    {"name": "funnel_tier_1",   "from": [-5.0, 3.0, -5.0], "to": [5.0, 8.0, 5.0], "rotation": {"origin": [0, 5.5, 0], "axis": "y", "angle": 30.0}, "uv": [0, 16, 32, 32]},
    # Tier 2 Funnel Ring
    {"name": "funnel_tier_2",   "from": [-7.5, 8.0, -7.5], "to": [7.5, 15.0, 7.5], "rotation": {"origin": [0, 11.5, 0], "axis": "y", "angle": 60.0}, "uv": [0, 16, 32, 32]},
    # Tier 3 Funnel Ring
    {"name": "funnel_tier_3",   "from": [-10.5, 15.0, -10.5], "to": [10.5, 24.0, 10.5], "rotation": {"origin": [0, 19.5, 0], "axis": "y", "angle": 90.0}, "uv": [32, 0, 64, 32]},
    # Tier 4 Top Funnel Canopy
    {"name": "funnel_canopy",   "from": [-14.0, 24.0, -14.0], "to": [14.0, 34.0, 14.0], "rotation": {"origin": [0, 29.0, 0], "axis": "y", "angle": 120.0}, "uv": [32, 0, 64, 32]},
    # Helical Outer Slipstream Ribbons
    {"name": "ribbon_swirl_a",  "from": [-12.0, 6.0, -2.0], "to": [-9.0, 26.0, 2.0], "rotation": {"origin": [0, 16, 0], "axis": "y", "angle": 45.0}, "uv": [0, 32, 32, 64]},
    {"name": "ribbon_swirl_b",  "from": [ 9.0, 10.0, -2.0], "to": [12.0, 30.0, 2.0], "rotation": {"origin": [0, 20, 0], "axis": "y", "angle": -45.0}, "uv": [0, 32, 32, 64]}
]

vortex_anims = [
    {
        "name": "tornado_spin",
        "loop": "loop",
        "length": 0.5,
        "animators": {
            "root": {"rotation": {"0.0": [0, 0, 0], "0.25": [0, 180, 0], "0.5": [0, 360, 0]}}
        }
    }
]
export_asset_package("air_vortex_funnel", "Air Vortex Funnel", vortex_elements, vortex_tex, vortex_anims, pivot_desc="Ground Contact (0, 0, 0)")


# =============================================================
# ASSET 4: WATER WHIP SEGMENTED STREAM
# =============================================================
print("\n>>> BUILDING ASSET SUITE 4: WATER WHIP SEGMENTED STREAM")

whip_tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
w_pix = whip_tex.load()
for y in range(0, 64):
    for x in range(0, 64):
        wave = (x * 3 + y * 6) % 7
        if wave <= 1:
            c = (255, 255, 255, 230) # Crest foam
        elif wave <= 3:
            c = (120, 220, 255, 210) # Light aqua surface
        elif wave <= 5:
            c = (40, 150, 235, 190)  # Stream body
        else:
            c = (15, 80, 185, 220)   # Deep water core
        w_pix[x, y] = c

# Articulated Fluid Whip Segments (Extends along Z axis from hand at 0,0,0)
whip_elements = [
    {"name": "segment_0_handle", "from": [-1.2, -1.2,  0.0], "to": [1.2, 1.2,  6.0], "uv": [0, 0, 16, 16]},
    {"name": "segment_1_shaft",  "from": [-1.5, -1.5,  5.0], "to": [1.5, 1.5, 13.0], "rotation": {"origin": [0, 0,  5], "axis": "y", "angle":  10.0}, "uv": [0, 0, 16, 16]},
    {"name": "segment_2_bend",   "from": [-1.4, -1.4, 12.0], "to": [1.4, 1.4, 21.0], "rotation": {"origin": [0, 0, 12], "axis": "y", "angle": -15.0}, "uv": [16, 0, 32, 16]},
    {"name": "segment_3_loop",   "from": [-1.2, -1.2, 20.0], "to": [1.2, 1.2, 30.0], "rotation": {"origin": [0, 0, 20], "axis": "x", "angle":  12.0}, "uv": [16, 0, 32, 16]},
    {"name": "segment_4_arc",    "from": [-1.0, -1.0, 29.0], "to": [1.0, 1.0, 40.0], "rotation": {"origin": [0, 0, 29], "axis": "y", "angle":  20.0}, "uv": [0, 16, 16, 32]},
    {"name": "segment_5_lash",   "from": [-0.8, -0.8, 39.0], "to": [0.8, 0.8, 50.0], "rotation": {"origin": [0, 0, 39], "axis": "x", "angle": -18.0}, "uv": [0, 16, 16, 32]},
    {"name": "segment_6_tip",    "from": [-0.5, -0.5, 49.0], "to": [0.5, 0.5, 60.0], "rotation": {"origin": [0, 0, 49], "axis": "y", "angle": -25.0}, "uv": [16, 16, 32, 32]}
]

whip_anims = [
    {
        "name": "whip_strike_wave",
        "loop": "once",
        "length": 0.45,
        "animators": {
            "root": {"rotation": {"0.0": [25, 0, 0], "0.18": [-45, 0, 0], "0.45": [0, 0, 0]}}
        }
    }
]
export_asset_package("water_whip_stream", "Water Whip Stream", whip_elements, whip_tex, whip_anims, pivot_desc="Hand Origin (0, 0, 0)")


# =============================================================
# ASSET 5: BOULDER LAUNCH MEGALITH
# =============================================================
print("\n>>> BUILDING ASSET SUITE 5: BOULDER LAUNCH MEGALITH")

boulder_tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
b_pix = boulder_tex.load()
for y in range(0, 64):
    for x in range(0, 64):
        edge = (x * 9 + y * 13) % 7
        if edge == 0:
            c = (42, 38, 34, 255) # Fracture seam
        elif edge <= 2:
            c = (82, 76, 70, 255) # Dark rock
        elif edge <= 4:
            c = (118, 112, 104, 255) # Mid granite
        elif (x + y * 2) % 17 == 0:
            c = (45, 175, 90, 255) # Ba Sing Se Jade vein
        else:
            c = (162, 155, 144, 255) # Highlight facet
        b_pix[x, y] = c

# Heavy Multi-Faceted Megalith Projectile
boulder_elements = [
    # Monolith Core Block
    {"name": "core_boulder", "from": [-7.0, -7.0, -7.0], "to": [7.0, 7.0, 7.0], "uv": [0, 0, 32, 32]},
    # Beveled Shear Facets
    {"name": "facet_bevel_x", "from": [-6.0, -6.0, -6.0], "to": [6.0, 6.0, 6.0], "rotation": {"origin": [0,0,0], "axis": "x", "angle": 45.0}, "uv": [0, 0, 32, 32]},
    {"name": "facet_bevel_y", "from": [-6.0, -6.0, -6.0], "to": [6.0, 6.0, 6.0], "rotation": {"origin": [0,0,0], "axis": "y", "angle": 45.0}, "uv": [0, 0, 32, 32]},
    {"name": "facet_bevel_z", "from": [-6.0, -6.0, -6.0], "to": [6.0, 6.0, 6.0], "rotation": {"origin": [0,0,0], "axis": "z", "angle": 45.0}, "uv": [0, 0, 32, 32]},
    # Jagged Protruding Crags
    {"name": "crag_top",   "from": [-4.0, 7.0, -4.0],  "to": [4.0, 10.5, 4.0], "uv": [32, 0, 64, 32]},
    {"name": "crag_right", "from": [7.0, -4.0, -4.0],  "to": [10.5, 4.0, 4.0], "uv": [32, 0, 64, 32]},
    {"name": "crag_front", "from": [-4.0, -4.0, 7.0],  "to": [4.0, 4.0, 10.5], "uv": [0, 32, 32, 64]},
    # Jade Crystal Ridge Inclusion
    {"name": "jade_ridge", "from": [-8.0, -2.0, -3.0], "to": [-6.5, 5.0, 3.0], "rotation": {"origin": [-7.25, 1.5, 0], "axis": "z", "angle": 22.5}, "uv": [32, 32, 64, 64]}
]

boulder_anims = [
    {
        "name": "projectile_tumble",
        "loop": "loop",
        "length": 0.6,
        "animators": {
            "root": {"rotation": {"0.0": [0, 0, 0], "0.3": [180, 90, 0], "0.6": [360, 180, 0]}}
        }
    }
]
export_asset_package("boulder_launch_megalith", "Boulder Launch Megalith", boulder_elements, boulder_tex, boulder_anims, pivot_desc="Center of Mass (0, 0, 0)")

print("\n=======================================================")
print("ALL 5 AVATAR 3D ASSET SUITES PRODUCED & EXPORTED SUCCESSFULLY!")
print("=======================================================")
