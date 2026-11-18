"""
Avatar Elements Mod - Canonical Weapons 3D Blockbench Suite Builder (Tahap 4)
Author: Antigravity IDE (3D Technical Art Specialist)
Target: Fabric 1.21.1 Client & Resource Pack
Literature: ATLA / LOK Canon, "Weaponry in the World of Avatar"

Generates 4 Production-Ready 3D Canonical Weapons:
1. SM_Dual_Swords (Zuko Dao Broadswords)
2. SM_Earth_Hammer (Kyoshi Earthbender Warhammer)
3. SM_War_Fan (Kyoshi Warriors War Fan)
4. SM_Water_Spear (Water Tribe Harpoon Spear)

Standard Requirements:
- Metric scale: 1 Blockbench unit = 1/16 meter (0.0625m).
- Origin / pivot point strictly at hand grip point (0, 0, 0).
- 64x64 cel-shaded texture atlas for each weapon.
- Formats exported:
  * .bbmodel (Blockbench 4.10 project with embedded texture and locators)
  * .geo.json (Bedrock 1.12.0 geometry)
  * .json (Minecraft Java 1.21.1 display item model, coordinates within [-16, 32])
  * .obj and .mtl (Wavefront 3D mesh, metric 1.0 = 1m)
  * Previews: isometric PNG, turntable GIF, front/side renders in previews/
"""

import os
import sys
import math
import json
import base64
import uuid
from io import BytesIO
from PIL import Image, ImageDraw

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
ASSET_PACK_DIR = os.path.join(REPO_ROOT, "art-source", "asset_pack")
MODELS_DIR = os.path.join(ASSET_PACK_DIR, "models")
BBMODELS_DIR = os.path.join(MODELS_DIR, "bbmodel")
BBMODELS_WEAPONS_DIR = os.path.join(BBMODELS_DIR, "weapons")
MESHES_WEAPONS_DIR = os.path.join(ASSET_PACK_DIR, "meshes", "weapons")
MESHES_VFX_DIR = os.path.join(ASSET_PACK_DIR, "meshes", "vfx")
TEXTURES_WEAPONS_DIR = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "weapons")
TEXTURES_ITEM_DIR = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "item")
TEXTURES_VFX_DIR = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "vfx")
ITEM_MODELS_DIR = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "models", "item")
PREVIEWS_DIR = os.path.join(ASSET_PACK_DIR, "previews")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
ASSET_DOCS_DIR = os.path.join(ASSET_PACK_DIR, "docs")

for d in [
    MODELS_DIR, BBMODELS_DIR, BBMODELS_WEAPONS_DIR,
    MESHES_WEAPONS_DIR, MESHES_VFX_DIR,
    TEXTURES_WEAPONS_DIR, TEXTURES_ITEM_DIR, TEXTURES_VFX_DIR,
    ITEM_MODELS_DIR, PREVIEWS_DIR, DOCS_DIR, ASSET_DOCS_DIR
]:
    os.makedirs(d, exist_ok=True)

SCALE_FACTOR = 0.0625  # 1 unit = 1/16 meter

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

# =============================================================
# EXPORTER FUNCTION
# =============================================================
def export_weapon(
    asset_id,
    legacy_ids,
    asset_title,
    elements,
    texture_img,
    locators=None,
    display_override=None,
    custom_preview_tint=(220, 200, 180)
):
    print(f"\n=======================================================")
    print(f"--> Exporting Weapon Asset: {asset_id} ({asset_title})")
    print(f"=======================================================")

    tex_filename = f"{asset_id}.png"
    w, h = texture_img.size

    # Save textures across relevant asset paths
    tex_paths = [
        os.path.join(TEXTURES_WEAPONS_DIR, tex_filename),
        os.path.join(TEXTURES_ITEM_DIR, tex_filename),
        os.path.join(TEXTURES_VFX_DIR, tex_filename),
        os.path.join(MODELS_DIR, tex_filename),
        os.path.join(MESHES_WEAPONS_DIR, tex_filename),
        os.path.join(MESHES_VFX_DIR, tex_filename),
    ]
    for p in tex_paths:
        texture_img.save(p, "PNG")
    print(f"  [OK] Textures saved (size {w}x{h}).")

    # Base64 for BBModel
    buf = BytesIO()
    texture_img.save(buf, format="PNG")
    tex_b64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    # 1. Blockbench .bbmodel
    bb_elements = []
    root_group_children = []

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
        root_group_children.append(elem_uuid)

    tex_uuid = str(uuid.uuid4())
    bbmodel_data = {
        "meta": {"format_version": "4.10", "model_format": "bedrock", "box_uv": False},
        "name": asset_id,
        "model_identifier": f"geometry.{asset_id}",
        "resolution": {"width": w, "height": h},
        "elements": bb_elements,
        "outliner": [
            {
                "name": "weapon_root",
                "origin": [0, 0, 0],
                "children": root_group_children
            }
        ],
        "textures": [
            {
                "path": f"textures/weapons/{tex_filename}",
                "name": tex_filename,
                "folder": "textures/weapons",
                "namespace": "avatar_elements",
                "id": "0",
                "particle": False,
                "render_mode": "default",
                "visible": True,
                "mode": "bitmap",
                "saved": True,
                "uuid": tex_uuid,
                "source": tex_b64
            }
        ],
        "locators": locators if locators else {
            "trail_begin": [0.0, 2.0, 0.0],
            "trail_end": [0.0, 22.0, 0.0],
            "imbue_emitter": [0.0, 12.0, 0.0]
        }
    }

    bb_primary_path = os.path.join(BBMODELS_DIR, f"{asset_id}.bbmodel")
    bb_weapons_path = os.path.join(BBMODELS_WEAPONS_DIR, f"{asset_id}.bbmodel")
    with open(bb_primary_path, "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)
    with open(bb_weapons_path, "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)

    # Also update legacy weapon file if present
    for leg in legacy_ids:
        leg_path = os.path.join(BBMODELS_WEAPONS_DIR, f"{leg}.bbmodel")
        with open(leg_path, "w", encoding="utf-8") as f:
            json.dump(bbmodel_data, f, indent=2)
    print(f"  [OK] Saved Blockbench .bbmodel: {bb_primary_path}")

    # 2. Bedrock .geo.json
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
                    "visible_bounds_width": 2,
                    "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 0.75, 0]
                },
                "bones": [
                    {
                        "name": "weapon_root",
                        "pivot": [0, 0, 0],
                        "cubes": geo_cubes,
                        "locators": locators if locators else {
                            "trail_begin": [0.0, 2.0, 0.0],
                            "trail_end": [0.0, 22.0, 0.0],
                            "imbue_emitter": [0.0, 12.0, 0.0]
                        }
                    }
                ]
            }
        ]
    }
    geo_path = os.path.join(MODELS_DIR, f"{asset_id}.geo.json")
    with open(geo_path, "w", encoding="utf-8") as f:
        json.dump(geo_data, f, indent=2)
    print(f"  [OK] Saved Bedrock Geo: {geo_path}")

    # 3. Wavefront OBJ & MTL
    mtl_path_w = os.path.join(MESHES_WEAPONS_DIR, f"{asset_id}.mtl")
    mtl_path_v = os.path.join(MESHES_VFX_DIR, f"{asset_id}.mtl")
    for mtl_p in [mtl_path_w, mtl_path_v]:
        with open(mtl_p, "w", encoding="utf-8") as f:
            f.write(f"# Avatar Elements Canonical Weapon Material: {asset_id}\n")
            f.write(f"newmtl {asset_id}_mat\n")
            f.write("Kd 1.0 1.0 1.0\n")
            f.write("Ks 0.25 0.25 0.25\n")
            f.write("Ns 30.0\n")
            f.write("d 1.0\n")
            f.write(f"map_Kd {tex_filename}\n")

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

    obj_primary_path = os.path.join(MESHES_WEAPONS_DIR, f"{asset_id}.obj")
    for obj_p in [obj_primary_path, os.path.join(MESHES_VFX_DIR, f"{asset_id}.obj")]:
        with open(obj_p, "w", encoding="utf-8") as f:
            f.write(f"# Avatar Elements Canonical 3D Weapon Mesh: {asset_id}\n")
            f.write(f"# Pivot: Hand Grip Point (0, 0, 0) | Units: Metric (1.0 = 1.0 meter)\n")
            f.write(f"mtllib {asset_id}.mtl\n")
            f.write(f"o {asset_id}\n")
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
    print(f"  [OK] Saved Wavefront OBJ: {obj_primary_path}")

    # 4. Java Display Model .json
    # Crucial rule: all coordinates must fit within [-16, 32].
    # Offset by +8.0 to place the grip pivot at [8, 8, 8].
    java_elements = []
    min_coord, max_coord = 999.0, -999.0

    for elem in elements:
        j_from = [elem["from"][0] + 8.0, elem["from"][1] + 8.0, elem["from"][2] + 8.0]
        j_to   = [elem["to"][0] + 8.0,   elem["to"][1] + 8.0,   elem["to"][2] + 8.0]

        for val in j_from + j_to:
            if val < min_coord: min_coord = val
            if val > max_coord: max_coord = val

        u0, v0, u1, v1 = elem.get("uv", [0, 0, 16, 16])
        # Map 64x64 UV to 0..16 Minecraft UV
        uv_mc = [u0 / 4.0, v0 / 4.0, u1 / 4.0, v1 / 4.0]
        faces = {}
        for f in ["north", "east", "south", "west", "up", "down"]:
            faces[f] = {"uv": uv_mc, "texture": "#texture"}

        j_elem = {"name": elem["name"], "from": j_from, "to": j_to, "faces": faces}

        if "rotation" in elem:
            rot = elem["rotation"]
            raw_angle = rot["angle"]
            # Minecraft vanilla Java models strictly allow angles: -45, -22.5, 0, 22.5, 45
            allowed_angles = [-45.0, -22.5, 0.0, 22.5, 45.0]
            snapped_angle = min(allowed_angles, key=lambda a: abs(a - raw_angle))
            if abs(snapped_angle) > 0.01:
                j_elem["rotation"] = {
                    "origin": [rot["origin"][0] + 8.0, rot["origin"][1] + 8.0, rot["origin"][2] + 8.0],
                    "axis": rot["axis"],
                    "angle": snapped_angle
                }
        java_elements.append(j_elem)

    # Standard weapon handheld display transforms
    default_display = {
        "thirdperson_righthand": {
            "rotation": [0, -90, 55],
            "translation": [0, 4.0, 0.5],
            "scale": [0.85, 0.85, 0.85]
        },
        "thirdperson_lefthand": {
            "rotation": [0, 90, -55],
            "translation": [0, 4.0, 0.5],
            "scale": [0.85, 0.85, 0.85]
        },
        "firstperson_righthand": {
            "rotation": [0, -90, 25],
            "translation": [1.13, 3.2, 1.13],
            "scale": [0.68, 0.68, 0.68]
        },
        "firstperson_lefthand": {
            "rotation": [0, 90, -25],
            "translation": [1.13, 3.2, 1.13],
            "scale": [0.68, 0.68, 0.68]
        },
        "ground": {
            "rotation": [0, 0, 0],
            "translation": [0, 2.0, 0],
            "scale": [0.55, 0.55, 0.55]
        },
        "gui": {
            "rotation": [0, 0, -45],
            "translation": [0, 0, 0],
            "scale": [0.65, 0.65, 0.65]
        },
        "fixed": {
            "rotation": [0, 180, 0],
            "translation": [0, 0, 0],
            "scale": [0.7, 0.7, 0.7]
        }
    }
    if display_override:
        default_display.update(display_override)

    java_data = {
        "credit": f"Avatar Elements Mod - Canonical Weapon: {asset_title} (Fabric 1.21.1)",
        "texture_size": [w, h],
        "textures": {
            "texture": f"avatar_elements:textures/weapons/{asset_id}",
            "particle": f"avatar_elements:textures/weapons/{asset_id}"
        },
        "elements": java_elements,
        "display": default_display
    }

    java_paths = [
        os.path.join(MODELS_DIR, f"{asset_id}.json"),
        os.path.join(ITEM_MODELS_DIR, f"{asset_id}.json"),
    ]
    for leg in legacy_ids:
        java_paths.append(os.path.join(ITEM_MODELS_DIR, f"{leg}.json"))

    for jp in java_paths:
        with open(jp, "w", encoding="utf-8") as f:
            json.dump(java_data, f, indent=2)

    print(f"  [OK] Saved Java Display Model (Bounds check: min={min_coord:.1f}, max={max_coord:.1f} in [-16, 32]): {java_paths[0]}")

    # 5. High-Resolution Multi-Angle 3D Previews (Still & Turntable GIF)
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

    def render_one(yaw, pitch, w_px=480, h_px=480, sc=180, cx=240, cy=250, col_base=custom_preview_tint):
        im = Image.new("RGBA", (w_px, h_px), (16, 18, 22, 255))
        d = ImageDraw.Draw(im)

        # Draw subtle grid at ground level
        grid_col = (30, 34, 42, 255)
        for gx in range(-5, 6, 2):
            p_a = project_v((gx * 0.1, 0, -0.5), yaw, pitch, sc, cx, cy)
            p_b = project_v((gx * 0.1, 0, 0.5), yaw, pitch, sc, cx, cy)
            d.line([(p_a[0], p_a[1]), (p_b[0], p_b[1])], fill=grid_col, width=1)
        for gz in range(-5, 6, 2):
            p_a = project_v((-0.5, 0, gz * 0.1), yaw, pitch, sc, cx, cy)
            p_b = project_v((0.5, 0, gz * 0.1), yaw, pitch, sc, cx, cy)
            d.line([(p_a[0], p_a[1]), (p_b[0], p_b[1])], fill=grid_col, width=1)

        quads = []
        l_dir = (-0.577, 0.707, 0.408)
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
            dot = max(0.15, nx * l_dir[0] + ny * l_dir[1] + nz * l_dir[2])
            inte = 0.35 + 0.65 * dot

            # Check if this face has distinctive accent color based on height/part
            mid_y = (p0[1] + p2[1]) / 2.0
            r_c = min(255, int(col_base[0] * inte))
            g_c = min(255, int(col_base[1] * inte))
            b_c = min(255, int(col_base[2] * inte))
            c_fill = (r_c, g_c, b_c, 255)
            c_edge = (max(0, int(r_c * 0.4)), max(0, int(g_c * 0.4)), max(0, int(b_c * 0.4)), 255)

            pr0 = project_v(p0, yaw, pitch, sc, cx, cy)
            pr1 = project_v(p1, yaw, pitch, sc, cx, cy)
            pr2 = project_v(p2, yaw, pitch, sc, cx, cy)
            pr3 = project_v(p3, yaw, pitch, sc, cx, cy)
            ad = (pr0[2] + pr1[2] + pr2[2] + pr3[2]) / 4.0
            quads.append((ad, [(pr0[0], pr0[1]), (pr1[0], pr1[1]), (pr2[0], pr2[1]), (pr3[0], pr3[1])], c_fill, c_edge))

        quads.sort(key=lambda q: q[0])
        for q in quads:
            d.polygon(q[1], fill=q[2], outline=q[3])

        # Header label
        d.text((15, 15), f"AVATAR ELEMENTS 3D WEAPON: {asset_title}", fill=(240, 240, 240, 255))
        d.text((15, 30), f"ID: {asset_id} | Pivot: Grip (0,0,0) | Metric (1.0 = 1m)", fill=(160, 170, 185, 255))
        return im

    # Isometric Still Preview
    iso_img = render_one(45, 25, 480, 480, 220, 240, 250)
    iso_path = os.path.join(preview_sub, f"{asset_id}_isometric.png")
    iso_img.save(iso_path)
    iso_img.save(os.path.join(PREVIEWS_DIR, f"{asset_id}_isometric.png"))

    # Front and Side orthogonal/isometric previews
    front_img = render_one(0, 5, 400, 400, 200, 200, 210)
    front_img.save(os.path.join(preview_sub, f"{asset_id}_front.png"))
    side_img = render_one(90, 5, 400, 400, 200, 200, 210)
    side_img.save(os.path.join(preview_sub, f"{asset_id}_side.png"))

    # 360-degree Turntable GIF (24 frames, 15-degree steps)
    gif_frames = []
    for deg in range(0, 360, 15):
        frame = render_one(deg, 20, 300, 300, 140, 150, 155)
        gif_frames.append(frame)
    gif_path = os.path.join(preview_sub, f"{asset_id}_turntable.gif")
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=65, loop=0)
    gif_frames[0].save(os.path.join(PREVIEWS_DIR, f"{asset_id}_turntable.gif"), save_all=True, append_images=gif_frames[1:], duration=65, loop=0)

    print(f"  [OK] Saved 3D Previews & Turntable GIF: {iso_path}")
    return bb_primary_path, geo_path, java_paths[0], obj_primary_path


# =============================================================================
# 1. SM_Dual_Swords (Zuko Dao Broadswords - Twin Dao + Twin Sheath)
# =============================================================================
print("\n>>> CRAFTING WEAPON 1: SM_Dual_Swords (ZUKO DAO BROADSWORDS)")

# 64x64 Cel-Shaded Texture Atlas
tex_dao = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pix_dao = tex_dao.load()

# Color Palettes:
C_STEEL_BRIGHT = (235, 242, 250, 255)  # Razor cutting edge
C_STEEL_MID    = (185, 195, 208, 255)  # Blade flat
C_STEEL_DARK   = (125, 138, 152, 255)  # Fuller groove
C_STEEL_SHADOW = (80, 90, 105, 255)    # Edge shadow

C_BRASS_HI     = (255, 225, 120, 255)  # Gold/brass highlight
C_BRASS_MID    = (218, 175, 55, 255)   # Guard face
C_BRASS_DARK   = (160, 118, 28, 255)   # Antique brass rim
C_BRASS_DEEP   = (105, 75, 18, 255)

C_CORD_CRIMSON = (165, 25, 30, 255)    # Zuko burgundy cord
C_CORD_DARK    = (108, 12, 18, 255)
C_CORD_LIGHT   = (215, 45, 50, 255)

C_WOOD_ROSE    = (68, 28, 24, 255)     # Lacquered rosewood scabbard
C_WOOD_DARK    = (42, 15, 14, 255)
C_WOOD_LIGHT   = (96, 42, 35, 255)

# Quadrant 0: [0..32, 0..32] -> Steel Blade Surfaces & Fullers
for y in range(0, 32):
    for x in range(0, 32):
        if x in (0, 1, 30, 31) or y in (0, 31):
            c = C_STEEL_SHADOW
        elif x in (2, 3):
            c = C_STEEL_BRIGHT  # Razor edge
        elif 8 <= x <= 12:
            c = C_STEEL_DARK    # Central fuller groove
        elif x > 20:
            c = C_STEEL_MID if (y % 4 != 0) else C_STEEL_BRIGHT  # Forged folded damascus wave
        else:
            c = C_STEEL_MID
        pix_dao[x, y] = c

# Quadrant 1: [32..64, 0..32] -> Brass Guards, Tunhou Collar, Pommel Rings
for y in range(0, 32):
    for x in range(32, 64):
        lx, ly = x - 32, y
        d = math.sqrt((lx - 16)**2 + (ly - 16)**2)
        if d > 14:
            c = C_BRASS_DEEP
        elif d > 11:
            c = C_BRASS_DARK
        elif d > 8:
            c = C_BRASS_MID
        elif d > 5:
            c = C_BRASS_HI
        else:
            c = C_BRASS_MID
        pix_dao[x, y] = c

# Quadrant 2: [0..32, 32..64] -> Hardwood Grip & Diamond Cord Wrap
for y in range(32, 64):
    for x in range(0, 32):
        ly = y - 32
        diag1 = (x + ly) % 6
        diag2 = (x - ly) % 6
        if diag1 == 0 or diag2 == 0:
            c = C_CORD_DARK
        elif diag1 == 1 or diag2 == 1:
            c = C_CORD_LIGHT
        else:
            c = C_CORD_CRIMSON
        pix_dao[x, y] = c

# Quadrant 3: [32..64, 32..64] -> Twin Scabbard Lacquer & Brass Fittings
for y in range(32, 64):
    for x in range(32, 64):
        lx, ly = x - 32, y - 32
        if ly < 8 or ly > 26:
            c = C_BRASS_MID if (lx % 4 != 0) else C_BRASS_HI  # Brass locket / chape
        else:
            c = C_WOOD_ROSE if ((lx + ly) % 8 != 0) else C_WOOD_LIGHT
        pix_dao[x, y] = c

# Elements for SM_Dual_Swords (Primary Dao, Off-hand Dao, Twin Scabbard)
elem_dao = []

# --- PRIMARY DAO SWORD (Grip Center at (0, 0, 0)) ---
# Pommel
elem_dao.append({"name": "primary_pommel_cap", "from": [-1.0, -4.2, -0.8], "to": [1.0, -3.2, 0.8], "uv": [34, 4, 46, 12]})
elem_dao.append({"name": "primary_pommel_ring", "from": [-0.6, -5.2, -0.3], "to": [0.6, -4.2, 0.3], "uv": [40, 2, 46, 8]})
elem_dao.append({"name": "primary_tassel_cord", "from": [-0.3, -7.0, -0.3], "to": [0.3, -5.2, 0.3], "uv": [8, 36, 12, 44]})
elem_dao.append({"name": "primary_tassel_skirt", "from": [-0.6, -9.2, -0.6], "to": [0.6, -7.0, 0.6], "uv": [4, 40, 16, 52]})

# Handle / Grip
elem_dao.append({"name": "primary_grip_core", "from": [-0.8, -3.2, -0.7], "to": [0.8, 1.2, 0.7], "uv": [2, 34, 18, 62]})
elem_dao.append({"name": "primary_grip_collar_low", "from": [-0.9, -3.2, -0.8], "to": [0.9, -2.4, 0.8], "uv": [36, 6, 44, 10]})
elem_dao.append({"name": "primary_grip_collar_high", "from": [-0.9, 0.4, -0.8], "to": [0.9, 1.2, 0.8], "uv": [36, 6, 44, 10]})

# Brass Disc Guard (Asymmetric half-guard fitting against twin blade)
elem_dao.append({"name": "primary_guard_disc", "from": [-2.2, 1.2, -2.0], "to": [0.5, 2.0, 2.0], "uv": [34, 2, 58, 26]})
elem_dao.append({"name": "primary_tunhou_collar", "from": [-0.9, 2.0, -1.0], "to": [0.3, 3.2, 1.0], "uv": [38, 12, 48, 20]})

# Curved Dao Blade Segments (Primary)
# Segment 1: Base forte
elem_dao.append({"name": "primary_blade_base", "from": [-0.4, 3.2, -1.2], "to": [0.2, 9.0, 1.0], "uv": [2, 2, 14, 28]})
# Segment 2: Mid-blade curving forward
elem_dao.append({"name": "primary_blade_mid", "from": [-0.35, 9.0, -1.6], "to": [0.2, 15.0, 0.7], "uv": [4, 2, 16, 28]})
# Segment 3: Flared Dao Belly (characteristic broad chopping section)
elem_dao.append({"name": "primary_blade_belly", "from": [-0.35, 15.0, -2.2], "to": [0.2, 20.0, 0.4], "uv": [6, 2, 20, 28]})
# Segment 4: Clipped Tip
elem_dao.append({"name": "primary_blade_clip", "from": [-0.3, 20.0, -1.8], "to": [0.15, 22.8, 0.0], "uv": [8, 4, 18, 24]})
# Segment 5: Sharp Piercing Point
elem_dao.append({"name": "primary_blade_tip", "from": [-0.25, 22.8, -1.0], "to": [0.1, 23.8, -0.2], "uv": [10, 6, 16, 18]})

# --- SECONDARY DAO SWORD (Paired at X offset +1.8) ---
elem_dao.append({"name": "secondary_pommel_cap", "from": [1.4, -4.2, -0.8], "to": [3.4, -3.2, 0.8], "uv": [34, 4, 46, 12]})
elem_dao.append({"name": "secondary_pommel_ring", "from": [2.0, -5.2, -0.3], "to": [3.2, -4.2, 0.3], "uv": [40, 2, 46, 8]})
elem_dao.append({"name": "secondary_tassel_cord", "from": [2.3, -7.0, -0.3], "to": [2.9, -5.2, 0.3], "uv": [8, 36, 12, 44]})
elem_dao.append({"name": "secondary_tassel_skirt", "from": [2.0, -9.2, -0.6], "to": [3.2, -7.0, 0.6], "uv": [4, 40, 16, 52]})

elem_dao.append({"name": "secondary_grip_core", "from": [1.6, -3.2, -0.7], "to": [3.2, 1.2, 0.7], "uv": [2, 34, 18, 62]})
elem_dao.append({"name": "secondary_guard_disc", "from": [1.9, 1.2, -2.0], "to": [4.6, 2.0, 2.0], "uv": [34, 2, 58, 26]})
elem_dao.append({"name": "secondary_tunhou_collar", "from": [2.1, 2.0, -1.0], "to": [3.3, 3.2, 1.0], "uv": [38, 12, 48, 20]})

elem_dao.append({"name": "secondary_blade_base", "from": [2.2, 3.2, -1.2], "to": [2.8, 9.0, 1.0], "uv": [2, 2, 14, 28]})
elem_dao.append({"name": "secondary_blade_mid", "from": [2.2, 9.0, -1.6], "to": [2.75, 15.0, 0.7], "uv": [4, 2, 16, 28]})
elem_dao.append({"name": "secondary_blade_belly", "from": [2.2, 15.0, -2.2], "to": [2.75, 20.0, 0.4], "uv": [6, 2, 20, 28]})
elem_dao.append({"name": "secondary_blade_clip", "from": [2.25, 20.0, -1.8], "to": [2.7, 22.8, 0.0], "uv": [8, 4, 18, 24]})
elem_dao.append({"name": "secondary_blade_tip", "from": [2.3, 22.8, -1.0], "to": [2.65, 23.8, -0.2], "uv": [10, 6, 16, 18]})

# --- TWIN SHEATH SCABBARD (Slung along back/hip at Z = +3.4) ---
# Holds both swords in a single elegant housing
elem_dao.append({"name": "scabbard_chape_tip", "from": [-1.8, -2.5, 3.2], "to": [4.2, 0.2, 5.6], "uv": [34, 54, 62, 62]})
elem_dao.append({"name": "scabbard_lower_body", "from": [-1.6, 0.2, 3.4], "to": [4.0, 10.0, 5.4], "uv": [36, 40, 60, 56]})
elem_dao.append({"name": "scabbard_mid_band", "from": [-1.8, 10.0, 3.2], "to": [4.2, 12.5, 5.6], "uv": [34, 32, 62, 40]})
elem_dao.append({"name": "scabbard_upper_body", "from": [-1.6, 12.5, 3.4], "to": [4.0, 19.5, 5.4], "uv": [36, 40, 60, 56]})
elem_dao.append({"name": "scabbard_locket_throat", "from": [-1.9, 19.5, 3.1], "to": [4.3, 22.0, 5.7], "uv": [34, 32, 62, 40]})
# Suspension cord loop / ring
elem_dao.append({"name": "scabbard_mount_loop_left", "from": [-2.5, 10.5, 4.0], "to": [-1.8, 12.0, 4.8], "uv": [40, 2, 46, 8]})
elem_dao.append({"name": "scabbard_mount_loop_right", "from": [4.2, 10.5, 4.0], "to": [4.9, 12.0, 4.8], "uv": [40, 2, 46, 8]})

locators_dao = {
    "trail_begin": [1.2, 3.2, -0.2],
    "trail_end": [1.2, 23.8, -0.6],
    "imbue_emitter": [1.2, 16.0, -0.8]
}

export_weapon(
    asset_id="SM_Dual_Swords",
    legacy_ids=["weapon_zuko_dual_dao"],
    asset_title="Zuko Dao Broadswords",
    elements=elem_dao,
    texture_img=tex_dao,
    locators=locators_dao,
    custom_preview_tint=(220, 190, 150)
)


# =============================================================================
# 2. SM_Earth_Hammer (Kyoshi Earthbender Warhammer - Gow / Kyoshi)
# =============================================================================
print("\n>>> CRAFTING WEAPON 2: SM_Earth_Hammer (KYOSHI WARHAMMER)")

# 64x64 Cel-Shaded Texture Atlas
tex_hammer = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pix_hammer = tex_hammer.load()

# Color Palettes:
C_STONE_CORE   = (84, 76, 68, 255)     # Dark basalt stone
C_STONE_CHISEL = (118, 108, 98, 255)   # Chiseled facets
C_STONE_DARK   = (52, 46, 40, 255)     # Deep cracks / loam
C_STONE_HI     = (154, 142, 130, 255)  # Sunlit edge

C_IRON_BAND    = (70, 76, 84, 255)     # Wrought iron
C_IRON_HI      = (128, 138, 152, 255)  # Polished iron edge
C_IRON_RIVET   = (175, 185, 200, 255)  # Silver rivet stud
C_IRON_DARK    = (40, 44, 50, 255)

C_LEATHER_WRAP = (120, 78, 48, 255)    # Tough harness leather
C_LEATHER_DARK = (78, 48, 28, 255)
C_LEATHER_LACE = (175, 125, 85, 255)

C_WOOD_HAFT    = (95, 80, 65, 255)     # Dense ash wood
C_JADE_VEIN    = (45, 175, 95, 255)    # Ba Sing Se green jade crystal
C_JADE_CORE    = (145, 245, 185, 255)

# Quadrant 0: [0..32, 0..32] -> Basalt & Loam Stone Head
for y in range(0, 32):
    for x in range(0, 32):
        grain = (x * 7 + y * 13) % 7
        if x in (0, 31) or y in (0, 31):
            c = C_STONE_DARK
        elif grain == 0:
            c = C_STONE_DARK
        elif grain in (1, 2):
            c = C_STONE_CHISEL
        elif grain == 3:
            c = C_STONE_HI
        else:
            c = C_STONE_CORE
        pix_hammer[x, y] = c

# Quadrant 1: [32..64, 0..32] -> Reinforced Wrought Iron Bands & Rivets
for y in range(0, 32):
    for x in range(32, 64):
        lx, ly = x - 32, y
        if lx in (0, 1, 30, 31) or ly in (0, 31):
            c = C_IRON_DARK
        elif (lx % 8 in (3, 4)) and (ly % 8 in (3, 4)):
            c = C_IRON_RIVET  # Rivet heads
        elif ly in (1, 2):
            c = C_IRON_HI
        else:
            c = C_IRON_BAND
        pix_hammer[x, y] = c

# Quadrant 2: [0..32, 32..64] -> Leather Wrap & Haft Cross-Lacing
for y in range(32, 64):
    for x in range(0, 32):
        ly = y - 32
        if (x + ly) % 6 == 0 or (x - ly) % 6 == 0:
            c = C_LEATHER_LACE
        elif ly % 8 == 0:
            c = C_LEATHER_DARK
        else:
            c = C_LEATHER_WRAP
        pix_hammer[x, y] = c

# Quadrant 3: [32..64, 32..64] -> Jade Crystal Vein & Wood Haft
for y in range(32, 64):
    for x in range(32, 64):
        lx, ly = x - 32, y - 32
        if lx < 14:
            # Jade crystal vein
            d = abs(lx - 7) + abs(ly - 16) % 8
            c = C_JADE_CORE if d < 3 else (C_JADE_VEIN if d < 6 else C_STONE_DARK)
        else:
            c = C_WOOD_HAFT if (ly % 3 != 0) else C_STONE_DARK
        pix_hammer[x, y] = c

elem_hammer = []

# Long Shaft (Ash Wood Haft)
elem_hammer.append({"name": "shaft_lower", "from": [-0.8, -10.5, -0.8], "to": [0.8, -3.5, 0.8], "uv": [46, 34, 62, 62]})
elem_hammer.append({"name": "shaft_grip_leather", "from": [-1.1, -3.5, -1.1], "to": [1.1, 4.0, 1.1], "uv": [2, 34, 30, 62]})
elem_hammer.append({"name": "shaft_upper", "from": [-0.8, 4.0, -0.8], "to": [0.8, 13.0, 0.8], "uv": [46, 34, 62, 62]})

# Butt Counterbalance & Earth-Spike
elem_hammer.append({"name": "butt_iron_collar", "from": [-1.3, -12.0, -1.3], "to": [1.3, -10.5, 1.3], "uv": [34, 4, 46, 12]})
elem_hammer.append({"name": "butt_spike_pyramid", "from": [-0.8, -13.5, -0.8], "to": [0.8, -12.0, 0.8], "uv": [34, 4, 46, 12]})
elem_hammer.append({"name": "butt_spike_point", "from": [-0.4, -14.2, -0.4], "to": [0.4, -13.5, 0.4], "uv": [38, 2, 42, 6]})

# Iron Socket & Langets (Side straps securing head)
elem_hammer.append({"name": "socket_iron_sleeve", "from": [-1.4, 11.5, -1.4], "to": [1.4, 14.0, 1.4], "uv": [34, 6, 50, 18]})
elem_hammer.append({"name": "langet_strap_left", "from": [-1.5, 7.5, -0.6], "to": [-0.8, 12.0, 0.6], "uv": [36, 10, 42, 26]})
elem_hammer.append({"name": "langet_strap_right", "from": [0.8, 7.5, -0.6], "to": [1.5, 12.0, 0.6], "uv": [36, 10, 42, 26]})

# Monolithic Stone Mallet Head (Loam & Basalt)
# Main block: centered at Y=17.5
elem_hammer.append({"name": "hammer_stone_core", "from": [-5.0, 14.0, -3.5], "to": [5.0, 21.0, 3.5], "uv": [2, 2, 30, 30]})
# Left Chiseled Strike Face (Flat anvil strike face)
elem_hammer.append({"name": "strike_face_left", "from": [-6.6, 14.8, -2.8], "to": [-5.0, 20.2, 2.8], "uv": [4, 4, 28, 28]})
# Right Beveled Rock Pick / Anvil (Kinetic puncture face)
elem_hammer.append({"name": "strike_face_right_base", "from": [5.0, 15.0, -2.6], "to": [6.8, 20.0, 2.6], "uv": [4, 4, 28, 28]})
elem_hammer.append({"name": "strike_face_right_pick", "from": [6.8, 16.0, -1.8], "to": [8.0, 19.0, 1.8], "uv": [8, 8, 24, 24]})

# Reinforced Wrought-Iron Bands
# Horizontal band encircling the stone
elem_hammer.append({"name": "iron_band_horizontal", "from": [-5.2, 16.5, -3.7], "to": [5.2, 18.5, 3.7], "uv": [34, 12, 62, 20]})
# Vertical cross-strap over crown
elem_hammer.append({"name": "iron_strap_crown", "from": [-1.8, 13.8, -3.7], "to": [1.8, 21.3, 3.7], "uv": [34, 4, 62, 16]})
# Crown iron spike wedge
elem_hammer.append({"name": "crown_iron_spike", "from": [-1.0, 21.3, -1.0], "to": [1.0, 23.2, 1.0], "uv": [36, 2, 44, 10]})

# Heavy Iron Rivets on band
elem_hammer.append({"name": "rivet_front_left", "from": [-2.8, 17.0, 3.7], "to": [-1.8, 18.0, 4.1], "uv": [34, 34, 38, 38]})
elem_hammer.append({"name": "rivet_front_right", "from": [1.8, 17.0, 3.7], "to": [2.8, 18.0, 4.1], "uv": [34, 34, 38, 38]})
elem_hammer.append({"name": "rivet_back_left", "from": [-2.8, 17.0, -4.1], "to": [-1.8, 18.0, -3.7], "uv": [34, 34, 38, 38]})
elem_hammer.append({"name": "rivet_back_right", "from": [1.8, 17.0, -4.1], "to": [2.8, 18.0, -3.7], "uv": [34, 34, 38, 38]})

# Ba Sing Se Jade Mineral Seam (Visible embedded gem vein)
elem_hammer.append({"name": "jade_crystal_vein_front", "from": [-0.6, 15.0, 3.52], "to": [0.6, 20.0, 3.72], "uv": [34, 40, 44, 58]})
elem_hammer.append({"name": "jade_crystal_vein_back", "from": [-0.6, 15.0, -3.72], "to": [0.6, 20.0, -3.52], "uv": [34, 40, 44, 58]})

locators_hammer = {
    "trail_begin": [0.0, 13.5, 0.0],
    "trail_end": [0.0, 23.2, 0.0],
    "imbue_emitter": [0.0, 17.5, 0.0]
}

export_weapon(
    asset_id="SM_Earth_Hammer",
    legacy_ids=["weapon_earth_war_hammer"],
    asset_title="Kyoshi Earthbender Warhammer",
    elements=elem_hammer,
    texture_img=tex_hammer,
    locators=locators_hammer,
    custom_preview_tint=(160, 140, 120)
)


# =============================================================================
# 3. SM_War_Fan (Kyoshi Warriors War Fan - Suki / Avatar Kyoshi)
# =============================================================================
print("\n>>> CRAFTING WEAPON 3: SM_War_Fan (KYOSHI WAR FAN)")

# 64x64 Cel-Shaded Texture Atlas
tex_fan = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pix_fan = tex_fan.load()

# Color Palettes:
C_FAN_JADE     = (24, 98, 54, 255)     # Kyoshi emerald silk
C_FAN_JADE_HI  = (48, 158, 88, 255)    # Pleat crest highlight
C_FAN_JADE_SH  = (14, 54, 30, 255)     # Pleat valley shadow

C_GOLD_LEAF    = (245, 205, 55, 255)   # Gold leaf trim
C_GOLD_HI      = (255, 238, 135, 255)  # Radiant gold rim
C_GOLD_SHADOW  = (175, 135, 25, 255)

C_FAN_STEEL    = (210, 222, 235, 255)  # Razor steel outer ribs
C_FAN_STEEL_SH = (130, 145, 165, 255)

C_KANAME_BRASS = (215, 165, 45, 255)   # Brass pivot rivet
C_TASSEL_RED   = (195, 30, 35, 255)    # Silk tassel

# Quadrant 0: [0..32, 0..32] -> Emerald Silk Pleated Fan Membrane
for y in range(0, 32):
    for x in range(0, 32):
        pleat = (x * 4) % 12
        if pleat in (0, 1, 2):
            c = C_FAN_JADE_HI
        elif pleat in (3, 4, 5, 6, 7):
            c = C_FAN_JADE
        else:
            c = C_FAN_JADE_SH
        pix_fan[x, y] = c

# Quadrant 1: [32..64, 0..32] -> Radiant Gold Leaf Trim & Crest
for y in range(0, 32):
    for x in range(32, 64):
        lx, ly = x - 32, y
        if ly < 6 or ly > 26:
            c = C_GOLD_HI
        elif lx in (15, 16) or ly in (15, 16):
            c = C_GOLD_HI  # Central chrysanthemum cross
        else:
            c = C_GOLD_LEAF if ((lx + ly) % 4 != 0) else C_GOLD_SHADOW
        pix_fan[x, y] = c

# Quadrant 2: [0..32, 32..64] -> Razor Outer Ribs & Steel Frame
for y in range(32, 64):
    for x in range(0, 32):
        ly = y - 32
        if x in (0, 1, 30, 31):
            c = C_FAN_STEEL
        elif 14 <= x <= 17:
            c = C_FAN_STEEL
        else:
            c = C_FAN_STEEL_SH
        pix_fan[x, y] = c

# Quadrant 3: [32..64, 32..64] -> Brass Kaname Pivot Pin & Tassel
for y in range(32, 64):
    for x in range(32, 64):
        lx, ly = x - 32, y - 32
        d = math.sqrt((lx - 16)**2 + (ly - 16)**2)
        if d < 7:
            c = C_KANAME_BRASS
        elif ly > 20:
            c = C_TASSEL_RED
        else:
            c = C_GOLD_SHADOW
        pix_fan[x, y] = c

elem_fan = []

# Base Pivot (Kaname) & Handle Guard
elem_fan.append({"name": "pivot_kaname_pin", "from": [-0.8, -0.6, -0.8], "to": [0.8, 0.8, 0.8], "uv": [40, 40, 56, 56]})
elem_fan.append({"name": "pivot_cord_loop", "from": [-0.5, -1.8, -0.4], "to": [0.5, -0.6, 0.4], "uv": [42, 36, 52, 44]})
elem_fan.append({"name": "jade_tassel_bead", "from": [-0.6, -2.6, -0.6], "to": [0.6, -1.8, 0.6], "uv": [4, 4, 12, 12]})
elem_fan.append({"name": "silk_tassel_skirt", "from": [-0.5, -4.5, -0.5], "to": [0.5, -2.6, 0.5], "uv": [44, 52, 54, 62]})

# Grip Handle Ribs (Base where fingers grasp)
elem_fan.append({"name": "handle_rib_bundle", "from": [-0.9, 0.6, -0.5], "to": [0.9, 3.5, 0.5], "uv": [4, 34, 18, 58]})

# Sharpened Outer Steel Ribs (Oya-bone)
# Far Left Razor Rib (-45 deg tilt)
elem_fan.append({
    "name": "outer_rib_left",
    "from": [-1.0, 3.2, -0.4],
    "to": [0.2, 16.5, 0.4],
    "uv": [2, 34, 8, 62],
    "rotation": {"origin": [0.0, 3.2, 0.0], "axis": "z", "angle": 45.0}
})
# Far Right Razor Rib (+45 deg tilt)
elem_fan.append({
    "name": "outer_rib_right",
    "from": [-0.2, 3.2, -0.4],
    "to": [1.0, 16.5, 0.4],
    "uv": [2, 34, 8, 62],
    "rotation": {"origin": [0.0, 3.2, 0.0], "axis": "z", "angle": -45.0}
})

# Inner Steel Ribs (Naka-bone)
# Mid-Left Rib (-22.5 deg)
elem_fan.append({
    "name": "inner_rib_mid_left",
    "from": [-0.6, 3.2, -0.3],
    "to": [0.4, 16.8, 0.3],
    "uv": [12, 34, 18, 62],
    "rotation": {"origin": [0.0, 3.2, 0.0], "axis": "z", "angle": 22.5}
})
# Center Rib (0 deg)
elem_fan.append({
    "name": "inner_rib_center",
    "from": [-0.5, 3.5, -0.3],
    "to": [0.5, 17.2, 0.3],
    "uv": [12, 34, 18, 62]
})
# Mid-Right Rib (+22.5 deg)
elem_fan.append({
    "name": "inner_rib_mid_right",
    "from": [-0.4, 3.2, -0.3],
    "to": [0.6, 16.8, 0.3],
    "uv": [12, 34, 18, 62],
    "rotation": {"origin": [0.0, 3.2, 0.0], "axis": "z", "angle": -22.5}
})

# Folded Silk Fan Leaf Panels (Pleated Kyoshi Green Silk)
# Panel 1: Far Left Pleat
elem_fan.append({
    "name": "silk_panel_far_left",
    "from": [-3.5, 6.0, -0.2],
    "to": [0.5, 15.2, 0.2],
    "uv": [2, 4, 16, 28],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": 33.75}
})
# Panel 2: Center Left Pleat
elem_fan.append({
    "name": "silk_panel_center_left",
    "from": [-2.2, 7.0, -0.15],
    "to": [0.8, 16.2, 0.15],
    "uv": [8, 4, 22, 28],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": 11.25}
})
# Panel 3: Center Right Pleat
elem_fan.append({
    "name": "silk_panel_center_right",
    "from": [-0.8, 7.0, -0.15],
    "to": [2.2, 16.2, 0.15],
    "uv": [8, 4, 22, 28],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": -11.25}
})
# Panel 4: Far Right Pleat
elem_fan.append({
    "name": "silk_panel_far_right",
    "from": [-0.5, 6.0, -0.2],
    "to": [3.5, 15.2, 0.2],
    "uv": [16, 4, 30, 28],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": -33.75}
})

# Gold Leaf Outer Arch Trims
elem_fan.append({
    "name": "gold_trim_left",
    "from": [-4.0, 14.5, -0.25],
    "to": [0.5, 16.2, 0.25],
    "uv": [34, 4, 52, 14],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": 33.75}
})
elem_fan.append({
    "name": "gold_trim_center",
    "from": [-2.5, 15.8, -0.22],
    "to": [2.5, 17.4, 0.22],
    "uv": [34, 4, 62, 14]
})
elem_fan.append({
    "name": "gold_trim_right",
    "from": [-0.5, 14.5, -0.25],
    "to": [4.0, 16.2, 0.25],
    "uv": [44, 4, 62, 14],
    "rotation": {"origin": [0.0, 3.5, 0.0], "axis": "z", "angle": -33.75}
})

locators_fan = {
    "trail_begin": [0.0, 3.5, 0.0],
    "trail_end": [0.0, 17.4, 0.0],
    "imbue_emitter": [0.0, 11.0, 0.0]
}

export_weapon(
    asset_id="SM_War_Fan",
    legacy_ids=["weapon_kyoshi_war_fans"],
    asset_title="Kyoshi Warriors War Fan",
    elements=elem_fan,
    texture_img=tex_fan,
    locators=locators_fan,
    custom_preview_tint=(190, 215, 160)
)


# =============================================================================
# 4. SM_Water_Spear (Water Tribe Harpoon Spear - Hakoda / Bato / Sokka)
# =============================================================================
print("\n>>> CRAFTING WEAPON 4: SM_Water_Spear (WATER TRIBE HARPOON SPEAR)")

# 64x64 Cel-Shaded Texture Atlas
tex_spear = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pix_spear = tex_spear.load()

# Color Palettes:
C_BONE_IVORY   = (242, 238, 224, 255)  # Carved polar bear-whale bone
C_BONE_MID     = (212, 204, 185, 255)
C_BONE_SHADOW  = (165, 155, 135, 255)

C_ICE_CYAN     = (185, 240, 255, 255)  # Glacial frost tip highlight
C_ICE_MID      = (125, 205, 235, 255)  # Translucent dense ice core
C_ICE_SHADOW   = (65, 145, 185, 255)

C_DRIFTWOOD    = (158, 148, 138, 255)  # Weathered arctic driftwood shaft
C_DRIFT_DARK   = (112, 102, 94, 255)
C_DRIFT_LIGHT  = (195, 185, 175, 255)

C_SINEW_BIND   = (96, 68, 48, 255)     # Rawhide sinew cord binding
C_SINEW_HI     = (148, 110, 78, 255)

C_LEATHER_NAVY = (28, 55, 92, 255)     # Water Tribe dyed indigo sealskin
C_LEATHER_HI   = (52, 92, 148, 255)
C_LEATHER_DEEP = (16, 32, 58, 255)

# Quadrant 0: [0..32, 0..32] -> Carved Polar Bone Spearhead
for y in range(0, 32):
    for x in range(0, 32):
        if x in (0, 31) or y in (0, 31):
            c = C_BONE_SHADOW
        elif 14 <= x <= 17:
            c = C_BONE_IVORY  # Central spinal ridge
        elif (x + y) % 5 == 0:
            c = C_BONE_MID
        else:
            c = C_BONE_IVORY
        pix_spear[x, y] = c

# Quadrant 1: [32..64, 0..32] -> Glacial Ice Spearpoint & Barbs
for y in range(0, 32):
    for x in range(32, 64):
        lx, ly = x - 32, y
        if lx in (0, 31) or ly in (0, 31):
            c = C_ICE_SHADOW
        elif ly < 8:
            c = C_ICE_CYAN  # Frosty glint tip
        elif (lx + ly) % 6 in (0, 1):
            c = C_ICE_CYAN
        else:
            c = C_ICE_MID
        pix_spear[x, y] = c

# Quadrant 2: [0..32, 32..64] -> Weathered Arctic Driftwood Shaft
for y in range(32, 64):
    for x in range(0, 32):
        ly = y - 32
        if x in (0, 31):
            c = C_DRIFT_DARK
        elif ly % 7 == 0:
            c = C_DRIFT_LIGHT
        else:
            c = C_DRIFTWOOD
        pix_spear[x, y] = c

# Quadrant 3: [32..64, 32..64] -> Rawhide Sinew Binding & Indigo Leather Grip
for y in range(32, 64):
    for x in range(32, 64):
        lx, ly = x - 32, y - 32
        if ly < 16:
            # Sinew cord cross-wrap
            c = C_SINEW_HI if ((lx + ly) % 5 == 0) else C_SINEW_BIND
        else:
            # Navy dyed sealskin grip
            c = C_LEATHER_HI if ((lx - ly) % 6 == 0) else (C_LEATHER_NAVY if lx % 4 != 0 else C_LEATHER_DEEP)
        pix_spear[x, y] = c

elem_spear = []

# Weathered Driftwood Shaft
elem_spear.append({"name": "shaft_lower", "from": [-0.75, -11.0, -0.75], "to": [0.75, -3.0, 0.75], "uv": [2, 34, 18, 62]})
# Indigo Sealskin Grip Wrap (Hand rest at Y=0)
elem_spear.append({"name": "grip_indigo_leather", "from": [-1.0, -3.0, -1.0], "to": [1.0, 3.5, 1.0], "uv": [34, 48, 62, 62]})
elem_spear.append({"name": "shaft_upper", "from": [-0.75, 3.5, -0.75], "to": [0.75, 14.0, 0.75], "uv": [2, 34, 18, 62]})

# Butt Counterbalance (Carved Polar Whale-bone Butt)
elem_spear.append({"name": "butt_bone_collar", "from": [-1.1, -12.5, -1.1], "to": [1.1, -11.0, 1.1], "uv": [4, 4, 20, 16]})
elem_spear.append({"name": "butt_fishtail_fluke", "from": [-1.8, -14.2, -0.5], "to": [1.8, -12.5, 0.5], "uv": [6, 6, 26, 24]})
elem_spear.append({"name": "butt_ground_spike", "from": [-0.4, -15.0, -0.4], "to": [0.4, -14.2, 0.4], "uv": [10, 10, 18, 18]})

# Rawhide Sinew Head Binding
elem_spear.append({"name": "sinew_binding_socket", "from": [-1.1, 13.5, -1.1], "to": [1.1, 16.5, 1.1], "uv": [34, 34, 62, 46]})
elem_spear.append({"name": "sinew_cord_crisscross", "from": [-1.25, 14.2, -1.25], "to": [1.25, 15.8, 1.25], "uv": [36, 36, 60, 44]})

# Carved Bone & Dense Glacial Ice Spearpoint
elem_spear.append({"name": "spearhead_bone_base", "from": [-0.6, 16.5, -0.6], "to": [0.6, 18.0, 0.6], "uv": [4, 4, 16, 16]})
# Main double-edged spear blade (Ivory & Ice)
elem_spear.append({"name": "spearhead_ice_blade", "from": [-1.2, 18.0, -0.45], "to": [1.2, 21.2, 0.45], "uv": [34, 2, 62, 26]})
# Tapering Piercing Tip
elem_spear.append({"name": "spearhead_ice_taper", "from": [-0.75, 21.2, -0.35], "to": [0.75, 22.8, 0.35], "uv": [38, 4, 58, 20]})
# Needle-sharp Glacier Needle Point
elem_spear.append({"name": "spearhead_ice_needle", "from": [-0.35, 22.8, -0.25], "to": [0.35, 23.6, 0.25], "uv": [42, 2, 54, 12]})

# Barbed Toggles (Harpoon Barbs / Flukes)
# Left Barbed Hook (Pointing downward-outward)
elem_spear.append({
    "name": "barb_hook_arm_left",
    "from": [-2.2, 17.2, -0.35],
    "to": [-1.0, 19.0, 0.35],
    "uv": [36, 6, 52, 20]
})
elem_spear.append({
    "name": "barb_hook_point_left",
    "from": [-2.5, 16.2, -0.25],
    "to": [-1.9, 17.5, 0.25],
    "uv": [40, 8, 48, 18]
})

# Right Barbed Hook (Pointing downward-outward)
elem_spear.append({
    "name": "barb_hook_arm_right",
    "from": [1.0, 17.2, -0.35],
    "to": [2.2, 19.0, 0.35],
    "uv": [36, 6, 52, 20]
})
elem_spear.append({
    "name": "barb_hook_point_right",
    "from": [1.9, 16.2, -0.25],
    "to": [2.5, 17.5, 0.25],
    "uv": [40, 8, 48, 18]
})

locators_spear = {
    "trail_begin": [0.0, 14.0, 0.0],
    "trail_end": [0.0, 23.6, 0.0],
    "imbue_emitter": [0.0, 19.5, 0.0]
}

export_weapon(
    asset_id="SM_Water_Spear",
    legacy_ids=["weapon_water_jaw_blade"],
    asset_title="Water Tribe Harpoon Spear",
    elements=elem_spear,
    texture_img=tex_spear,
    locators=locators_spear,
    custom_preview_tint=(160, 205, 235)
)

print("\n=======================================================")
print(" ALL 4 CANONICAL WEAPONS EXPORTED SUCCESSFULLY!")
print("=======================================================\n")
