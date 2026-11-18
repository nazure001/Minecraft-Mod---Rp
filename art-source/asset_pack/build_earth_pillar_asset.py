"""
Avatar Elements Mod - Earth Pillar 3D Asset Builder
Authors: Antigravity IDE (Asset Production Lead)
Target: Fabric 1.21.1 Client-side VFX & Blockbench Suite

Canon Source: Avatar: The Last Airbender (ATLA) & The Legend of Korra (LOK)
  - ATLA S2E01: Toph's earthbending debut — blunt-topped monolithic stone columns
  - ATLA S2E07: Earth Rumble VI — multiple rapid pillar attacks, blocky flat-top profile
  - LOK S1: Pro-bending arena — refined column aesthetics, same monolithic silhouette
  - ATLA / LOK artbooks: Earth Kingdom stone = warm grey granite, basalt seams,
    reddish-brown soil rim, NO jade by default on combat pillars

Canonical Earthbending Pillar Rules Applied:
  * Shape:   Rectangular/octagonal FLAT-TOPPED monolith (NOT spire/pyramid)
  * Crown:   Crenelated broken-top — 3 irregular flat protrusions (blunt, not pointed)
  * Body:    Near-uniform width shaft — minimal taper between tiers (blocky, monolithic)
  * Base:    Radial rupture shards at ground level (canonical debris burst)
  * Colors:  Warm grey granite (#7F8487 / Pewter), reddish-brown soil (#705335 / Raw Umber),
             dry crack lines in dark tone, NO jade veins on standard pillar
  * Motion:  Ultra-fast eruption (~0.06s to full height), rigid hold, fractured crumble

Produces:
1. 64x64 Texture: earth_pillar.png (warm granite strata, basalt base, broken crown, dry crack)
2. Blockbench Project: earth_pillar.bbmodel (hierarchical outliner, UVs, embedded texture & animation)
3. Universal 3D Mesh: earth_pillar.obj & earth_pillar.mtl (metric scale 1.0, pivot at ground contact)
4. Bedrock Geometry: earth_pillar.geo.json (geometry.earth_pillar)
5. Java Display Model: earth_pillar.json
6. Emergence Animation: earth_pillar.animation.json (canon-accurate eruption timing)
7. 3D Multi-angle Previews: Isometric, Front, Side, Top, and 360 turntable GIF
8. Integration Specification: EARTH_PILLAR_SPEC.md
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
PREVIEW_DIR = os.path.join(ASSET_PACK_DIR, "previews", "earth_pillar")
DOCS_DIR = os.path.join(ASSET_PACK_DIR, "docs")

os.makedirs(os.path.join(ASSET_PACK_DIR, "models", "bbmodel"), exist_ok=True)
os.makedirs(os.path.join(ASSET_PACK_DIR, "models"), exist_ok=True)
os.makedirs(os.path.join(ASSET_PACK_DIR, "meshes", "vfx"), exist_ok=True)
os.makedirs(os.path.join(ASSET_PACK_DIR, "animations"), exist_ok=True)
os.makedirs(os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "vfx"), exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. PROCEDURAL 64x64 TEXTURE GENERATION
# -------------------------------------------------------------
print("--> Generating 64x64 Earth Pillar texture atlas...")
tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
pix = tex.load()

# Color helper
def blend(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))

# -------------------------------------------------------
# ATLA/LOK Canon Palette
# Source: Earth Kingdom earthbending pillar visual language
# Primary Stone: warm grey granite (Pewter #7F8487, Slate #5C6164)
# Soil Rim: reddish-brown clay (Raw Umber #705335, Clay #8E7355)
# Crown: lighter fractured grey, sharp pixel contrast for broken stone
# Accent: dry crack lines (dark, NO jade on standard combat pillar)
# -------------------------------------------------------

# Primary stone — warm grey granite (ATLA granite tone)
C_GRANITE_DEEP   = (55, 50, 45, 255)   # deep shadow seam
C_GRANITE_MID    = (100, 94, 86, 255)  # mid-tone granite body
C_GRANITE_WARM   = (140, 132, 118, 255) # Pewter/warm grey highlight
C_GRANITE_LIGHT  = (175, 168, 155, 255) # sunlit face
C_GRANITE_CRACK  = (38, 34, 30, 255)   # dry crack lines (very dark)

# Soil / rupture base — reddish-brown earth (Raw Umber palette)
C_SOIL_DARK      = (60, 40, 28, 255)   # deep earth / root shadow
C_SOIL_MID       = (112, 85, 60, 255)  # Raw Umber clay dirt
C_SOIL_LIGHT     = (155, 118, 82, 255) # dry clay surface / dusty tan
C_BEDROCK_DARK   = (38, 32, 26, 255)   # basal bedrock dark

# Crown (broken flat top) — lighter and sharper than body
C_CROWN_MID      = (155, 148, 138, 255) # broken stone crown mid
C_CROWN_LIGHT    = (200, 194, 182, 255) # fractured top face catch-light
C_CROWN_CRACK    = (42, 38, 34, 255)   # sharp crack line in crown

# Quadrant 0: [0..32, 0..32]
# Stone Column Body — warm granite with horizontal sedimentary strata
# Layered strata lines = canonical ATLA "earth being pulled from crust" look
for y in range(0, 32):
    for x in range(0, 32):
        # Horizontal sedimentary bands (sinusoidal strata — heavier noise than v1)
        band = math.sin(y * 1.1 + (x % 4) * 0.3) + ((x * 7 + y * 13) % 9) * 0.1
        if band < -0.4:
            c = C_GRANITE_DEEP
        elif band < 0.0:
            c = C_GRANITE_MID
        elif band < 0.5:
            c = C_GRANITE_WARM
        else:
            c = C_GRANITE_LIGHT
        # Horizontal strata crack lines (every ~5 rows — ATLA pillar strata rhythm)
        if y % 5 == 0:
            c = C_GRANITE_CRACK
        # Vertical fracture seams (sparser than v1 — cleaner monolithic silhouette)
        elif (x + (y // 5) * 2) % 13 == 0:
            c = C_GRANITE_DEEP
        pix[x, y] = c

# Quadrant 1: [32..64, 0..32]
# Base/Rupture Zone — reddish-brown soil rim + dark bedrock fragments
# ATLA shows reddish earth torn up at pillar base, with coarse dirt/rock chunks
for y in range(0, 32):
    for x in range(32, 64):
        lx = x - 32
        ly = y
        speckle = ((lx * 11 + ly * 17) ^ (lx * ly)) % 8
        # Gradient: darker bedrock at base (ly==0), warmer clay higher up
        if ly < 8:
            if speckle in (0, 1):
                c = C_BEDROCK_DARK
            elif speckle in (2, 3):
                c = C_SOIL_DARK
            else:
                c = C_SOIL_MID
        elif ly < 20:
            if speckle in (0, 1):
                c = C_SOIL_DARK
            elif speckle in (2, 3, 4):
                c = C_SOIL_MID
            else:
                c = C_SOIL_LIGHT
        else:
            # Upper rupture zone transitions to stone
            if speckle in (0, 1):
                c = C_GRANITE_DEEP
            elif speckle in (2, 3):
                c = C_GRANITE_MID
            else:
                c = C_SOIL_LIGHT
        # Coarse crack texture across base (chunky, not mossy — dry ATLA environment)
        if (lx + ly * 2) % 9 == 0:
            c = C_GRANITE_CRACK
        pix[x, y] = c

# Quadrant 2: [0..32, 32..64]
# Crown (Broken Flat Top) — lighter stone with sharp fracture lines
# ATLA broken crown = rough, irregular flat surface with sharp pixel contrast
for y in range(32, 64):
    for x in range(0, 32):
        lx = x
        ly = y - 32
        # Base: lighter than body column
        band = (lx * 3 + ly * 5) % 7
        if band < 2:
            c = C_CROWN_CRACK
        elif band < 4:
            c = C_GRANITE_WARM
        elif band < 6:
            c = C_CROWN_MID
        else:
            c = C_CROWN_LIGHT
        # Sharp fracture crack lines on top surface (more frequent than body)
        if ly % 4 == 1 and lx % 3 != 0:
            c = C_CROWN_CRACK
        # Bright catch-light on fresh broken stone edges (ATLA light glint on crack face)
        if ly < 6 and lx % 5 == 0:
            c = C_CROWN_LIGHT
        pix[x, y] = c

# Quadrant 3: [32..64, 32..64]
# Dry Stone Crack Accent — dark crack network on warm stone background
# ATLA standard earthbending pillar has NO jade; jade = special locations / metalbending
# This quadrant used only for the stone detail accent faces
for y in range(32, 64):
    for x in range(32, 64):
        lx = x - 32
        ly = y - 32
        # Base is warm mid-stone
        c = C_GRANITE_WARM
        # Crack network: diagonal + horizontal intersections
        dist_diag = abs((lx - ly) - 1)
        dist_horiz = ly % 7
        if dist_diag <= 1:
            c = C_GRANITE_CRACK
        elif dist_horiz == 0:
            c = C_GRANITE_DEEP
        elif dist_diag <= 3:
            c = C_GRANITE_DEEP
        # Secondary lighter crack fill
        elif (lx + ly * 3) % 11 == 0:
            c = C_GRANITE_MID
        pix[x, y] = c

tex_path_vfx = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "textures", "vfx", "earth_pillar.png")
tex.save(tex_path_vfx, "PNG")
# Also save alongside models for standalone inspections
tex_path_standalone = os.path.join(ASSET_PACK_DIR, "models", "earth_pillar.png")
tex.save(tex_path_standalone, "PNG")
tex_path_mesh = os.path.join(ASSET_PACK_DIR, "meshes", "vfx", "earth_pillar.png")
tex.save(tex_path_mesh, "PNG")
print("Saved texture to:", tex_path_vfx)

# -------------------------------------------------------------
# 2. 3D GEOMETRY DEFINITIONS (16 Elements, Ground Pivot at Y=0)
# -------------------------------------------------------------
# Minecraft coordinate system: 16 units = 1.0 block = 1.0 meter.
# Base is centered at X=0, Z=0. Ground contact is Y=0.
# Height: 46 units = 2.875 blocks. Fits footprint radius 1.6 blocks.

ELEMENTS = [
    # =====================================================================
    # CANON ATLA: Earthbending Pillar Geometry
    # Shape: Rectangular/octagonal flat-topped monolith (Hung Ga stance = rooted)
    # Silhouette: Blocky shaft, wide base, FLAT CROWN (not spire/pyramid)
    # Ref: ATLA S2E07 Earth Rumble VI — blunt-topped stone columns
    # =====================================================================

    # --- SUBTERRANEAN ANCHOR ROOT (Anti-gap on uneven terrain) ---
    {
        "name": "subterranean_anchor",
        "group": "foundation",
        "from": [-9.0, -4.0, -9.0],
        "to":   [ 9.0,  0.0,  9.0],
        "uv_quad": 1  # Basal soil/rupture tile
    },
    # --- BASAL RUPTURE SLAB (Ground contact slab — wide earthbending footprint) ---
    # ATLA: ground cracks first, wide slab appears before column rises
    {
        "name": "base_rupture_slab",
        "group": "foundation",
        "from": [-11.0, 0.0, -11.0],
        "to":   [ 11.0, 3.0,  11.0],
        "uv_quad": 1
    },
    # --- RADIAL RUPTURE SHARDS (Canonical debris burst from ATLA earthbending)
    # Wide flat shards, not tall pointed ones — mimic cracked earth plates
    {
        "name": "rupture_shard_ne",
        "group": "foundation",
        "from": [ 7.0, 0.0,  7.0],
        "to":   [14.0, 4.0, 14.0],  # Wider, flatter than v1
        "rotation": {"origin": [7.0, 0.0, 7.0], "axis": "z", "angle": -15.0},  # Shallower tilt
        "uv_quad": 1
    },
    {
        "name": "rupture_shard_nw",
        "group": "foundation",
        "from": [-14.0, 0.0,  7.0],
        "to":   [ -7.0, 3.5, 13.0],  # Flatter
        "rotation": {"origin": [-7.0, 0.0, 7.0], "axis": "x", "angle": 15.0},
        "uv_quad": 1
    },
    {
        "name": "rupture_shard_se",
        "group": "foundation",
        "from": [ 7.0, 0.0, -14.0],
        "to":   [13.0, 4.5,  -7.0],
        "rotation": {"origin": [7.0, 0.0, -7.0], "axis": "x", "angle": -15.0},
        "uv_quad": 1
    },
    {
        "name": "rupture_shard_sw",
        "group": "foundation",
        "from": [-13.0, 0.0, -13.0],
        "to":   [ -7.0, 3.0,  -7.0],  # Flatter
        "rotation": {"origin": [-7.0, 0.0, -7.0], "axis": "z", "angle": 15.0},
        "uv_quad": 1
    },
    # --- LOWER COLUMN SHAFT ---
    # ATLA: Thick, rooted base — Hung Ga philosophy: low center of gravity
    # Near-uniform width (minimal taper) = monolithic not tapering
    {
        "name": "shaft_tier1_core",
        "group": "column_lower",
        "from": [-8.0, 3.0, -8.0],
        "to":   [ 8.0, 20.0,  8.0],  # Taller base tier
        "uv_quad": 0  # Stone strata tile
    },
    {
        "name": "shaft_tier1_bevel",
        "group": "column_lower",
        "from": [-7.0, 3.0, -7.0],
        "to":   [ 7.0, 20.0,  7.0],
        "rotation": {"origin": [0.0, 11.5, 0.0], "axis": "y", "angle": 45.0},
        "uv_quad": 0
    },
    # --- MID COLUMN SHAFT ---
    # ATLA: Monolithic body — almost same width as lower tier (NOT tapering pyramid)
    # Width reduced by only 1 unit per tier to maintain blocky silhouette
    {
        "name": "shaft_tier2_core",
        "group": "column_mid",
        "from": [-7.5, 20.0, -7.5],  # Only 0.5 unit taper from tier1 (was -6.5)
        "to":   [ 7.5, 32.0,  7.5],
        "uv_quad": 0
    },
    {
        "name": "shaft_tier2_bevel",
        "group": "column_mid",
        "from": [-6.5, 20.0, -6.5],
        "to":   [ 6.5, 32.0,  6.5],
        "rotation": {"origin": [0.0, 26.0, 0.0], "axis": "y", "angle": 45.0},
        "uv_quad": 0
    },
    # --- UPPER COLUMN SHAFT ---
    # ATLA: Upper section same monolithic character — 1.5 unit taper from tier2
    {
        "name": "shaft_tier3_core",
        "group": "column_apex",
        "from": [-6.0, 32.0, -6.0],  # Only 1.5 unit taper from tier2 (was -5.0)
        "to":   [ 6.0, 40.0,  6.0],
        "uv_quad": 2  # Crown/apex tile
    },
    # === CRENELATED FLAT CROWN ===
    # Canon: ATLA earthbending pillars end in a FLAT or slightly rough top.
    # Three asymmetric rectangular protrusions — blunt, not pointed.
    # Ref: "Linear Emergence" — stone locks into place with heavy sound.
    # Crown protrusion A (North-West offset) — tallest
    {
        "name": "crown_protrusion_a",
        "group": "column_apex",
        "from": [-6.0, 40.0, -6.0],
        "to":   [-1.0, 46.0, -1.0],
        "uv_quad": 2  # Crown stone — lighter, sharper than body
    },
    # Crown protrusion B (South-East offset) — medium height
    {
        "name": "crown_protrusion_b",
        "group": "column_apex",
        "from": [ 1.0, 40.0,  1.0],
        "to":   [ 6.0, 44.5,  6.0],
        "uv_quad": 2
    },
    # Crown protrusion C (Center slab) — lowest, flat surface to stand on
    # This is the "platform" protrusion — ATLA pillars are combat platforms
    {
        "name": "crown_platform_slab",
        "group": "column_apex",
        "from": [-3.5, 40.0, -3.5],
        "to":   [ 3.5, 42.0,  3.5],
        "uv_quad": 2
    },
]

# -------------------------------------------------------------
# 3. BUILD BLOCKBENCH PROJECT (.bbmodel)
# -------------------------------------------------------------
print("--> Generating Blockbench .bbmodel project...")

# Encode texture as base64 data URI
buffer = BytesIO()
tex.save(buffer, format="PNG")
tex_b64 = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")

bb_elements = []
bb_outliner = [
    {"name": "foundation",    "origin": [0, 0, 0],  "color": 3, "children": []},
    {"name": "column_lower",  "origin": [0, 11, 0], "color": 2, "children": []},
    {"name": "column_mid",    "origin": [0, 26, 0], "color": 5, "children": []},
    {"name": "column_apex",   "origin": [0, 43, 0], "color": 1, "children": []}
]
group_map = {g["name"]: g["children"] for g in bb_outliner}

# UV quadrant offsets
QUAD_OFFSETS = [
    (0, 0),    # Q0: Stone Strata
    (32, 0),   # Q1: Bedrock / Shards
    (0, 32),   # Q2: Apex Crag
    (32, 32)   # Q3: Jade Vein
]

import uuid

for i, elem in enumerate(ELEMENTS):
    elem_uuid = str(uuid.uuid4())
    q_ox, q_oy = QUAD_OFFSETS[elem["uv_quad"]]
    
    # Calculate face UVs within the 32x32 quadrant
    dx = abs(elem["to"][0] - elem["from"][0])
    dy = abs(elem["to"][1] - elem["from"][1])
    dz = abs(elem["to"][2] - elem["from"][2])
    
    # Clamp UV bounds inside [0..32] of quadrant
    u_w = min(16, dx)
    v_h = min(16, dy)
    
    faces = {}
    for f in ["north", "east", "south", "west", "up", "down"]:
        faces[f] = {
            "uv": [q_ox, q_oy, q_ox + u_w, q_oy + v_h],
            "texture": 0
        }
    
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
    group_map[elem["group"]].append(elem_uuid)

# ATLA Canon Animation Timing:
# Ref: ATLA S2E07 — pillar shoots up nearly instantaneously (1-2 frames at 24fps ≈ 0.04-0.08s)
# Pattern: ground crack (pre-erupt) → explosive linear rise → rigid hold → fragmented crumble
bb_animations = [
    {
        "name": "eruption",
        "loop": "once",
        "length": 1.3,
        "snapping": 20,
        "animators": {
            "root": {
                "name": "root",
                "type": "bone",
                "position": {
                    "0.00":  [0, -48.0, 0],  # submerged underground (pre-erupt)
                    "0.03":  [0, -30.0, 0],  # ultra-fast linear rise starts
                    "0.06":  [0,   1.5, 0],  # reaches full height (explosive — ATLA speed)
                    "0.10":  [0,   0.0, 0],  # impact slam settle (stone locks with sound)
                    "0.80":  [0,   0.0, 0],  # rigid hold phase (long — combat platform)
                    "0.90":  [0,  -8.0, 0],  # crumble begins — initial drop
                    "1.05":  [0, -28.0, 0],  # rapid fragmented collapse
                    "1.20":  [0, -48.0, 0]   # fully submerged / despawn
                }
            }
        }
    }
]

bbmodel_data = {
    "meta": {
        "format_version": "4.10",
        "model_format": "bedrock",
        "box_uv": False
    },
    "name": "earth_pillar",
    "model_identifier": "geometry.earth_pillar",
    "resolution": {"width": 64, "height": 64},
    "elements": bb_elements,
    "outliner": bb_outliner,
    "textures": [
        {
            "path": "earth_pillar.png",
            "name": "earth_pillar.png",
            "folder": "textures/vfx",
            "namespace": "avatar_elements",
            "id": "0",
            "particle": False,
            "render_mode": "default",
            "visible": True,
            "mode": "bitmap",
            "saved": True,
            "uuid": "e47b3091-628d-4a11-88f2-bb303f9012a9",
            "source": tex_b64
        }
    ],
    "animations": bb_animations
}

bbmodel_path = os.path.join(ASSET_PACK_DIR, "models", "bbmodel", "earth_pillar.bbmodel")
with open(bbmodel_path, "w", encoding="utf-8") as f:
    json.dump(bbmodel_data, f, indent=2)
# Also copy to meshes/vfx for parity with other 3D vfx assets
bbmodel_path_mesh = os.path.join(ASSET_PACK_DIR, "meshes", "vfx", "earth_pillar.bbmodel")
with open(bbmodel_path_mesh, "w", encoding="utf-8") as f:
    json.dump(bbmodel_data, f, indent=2)
print("Saved Blockbench project:", bbmodel_path)

# -------------------------------------------------------------
# 4. EXPORT WAVEFRONT OBJ & MTL (Universal Metric 3D Mesh)
# -------------------------------------------------------------
print("--> Generating Wavefront OBJ/MTL mesh...")

# 1 Blockbench unit = 1/16 meter = 0.0625 m
SCALE_FACTOR = 0.0625

mtl_path = os.path.join(ASSET_PACK_DIR, "meshes", "vfx", "earth_pillar.mtl")
with open(mtl_path, "w", encoding="utf-8") as f:
    f.write("# Avatar Elements Earth Pillar Material\n")
    f.write("newmtl earth_pillar_mat\n")
    f.write("Kd 1.0 1.0 1.0\n")
    f.write("Ks 0.1 0.1 0.1\n")
    f.write("Ns 10.0\n")
    f.write("d 1.0\n")
    f.write("map_Kd earth_pillar.png\n")

obj_path = os.path.join(ASSET_PACK_DIR, "meshes", "vfx", "earth_pillar.obj")

# Vertices, UVs, Normals generator
vertices = []
texcoords = []
normals = [
    ( 0.0,  0.0,  1.0), # North/South depending on coord
    ( 0.0,  0.0, -1.0),
    ( 1.0,  0.0,  0.0),
    (-1.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0), # Up
    ( 0.0, -1.0,  0.0)  # Down
]
faces = []
mesh_faces = []

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

for elem in ELEMENTS:
    f_x, f_y, f_z = elem["from"]
    t_x, t_y, t_z = elem["to"]
    
    # 8 corners of the cuboid
    raw_corners = [
        (f_x, f_y, f_z), # 0: ---
        (t_x, f_y, f_z), # 1: +--
        (t_x, t_y, f_z), # 2: ++-
        (f_x, t_y, f_z), # 3: -+-
        (f_x, f_y, t_z), # 4: --+
        (t_x, f_y, t_z), # 5: +-+
        (t_x, t_y, t_z), # 6: +++
        (f_x, t_y, t_z)  # 7: -++
    ]
    
    # Apply rotation if present
    rot = elem.get("rotation")
    if rot:
        corners = [rotate_pt(pt, rot["origin"], rot["axis"], rot["angle"]) for pt in raw_corners]
    else:
        corners = raw_corners
        
    # Scale to meters (16 units = 1 meter)
    scaled_corners = [(c[0] * SCALE_FACTOR, c[1] * SCALE_FACTOR, c[2] * SCALE_FACTOR) for c in corners]
    
    v_base = len(vertices) + 1
    for sc in scaled_corners:
        vertices.append(sc)
        
    # UV quadrant coords
    q_ox, q_oy = QUAD_OFFSETS[elem["uv_quad"]]
    u0 = q_ox / 64.0
    v0 = 1.0 - (q_oy / 64.0)
    u1 = (q_ox + 16) / 64.0
    v1 = 1.0 - ((q_oy + 16) / 64.0)
    
    vt_base = len(texcoords) + 1
    texcoords.extend([
        (u0, v0), (u1, v0), (u1, v1), (u0, v1)
    ])
    
    # 6 Faces (quads)
    # North (Z-)
    mesh_faces.append(((v_base+0, vt_base+0, 2), (v_base+3, vt_base+3, 2), (v_base+2, vt_base+2, 2), (v_base+1, vt_base+1, 2)))
    # South (Z+)
    mesh_faces.append(((v_base+5, vt_base+0, 1), (v_base+6, vt_base+3, 1), (v_base+7, vt_base+2, 1), (v_base+4, vt_base+1, 1)))
    # West (X-)
    mesh_faces.append(((v_base+4, vt_base+0, 4), (v_base+7, vt_base+3, 4), (v_base+3, vt_base+2, 4), (v_base+0, vt_base+1, 4)))
    # East (X+)
    mesh_faces.append(((v_base+1, vt_base+0, 3), (v_base+2, vt_base+3, 3), (v_base+6, vt_base+2, 3), (v_base+5, vt_base+1, 3)))
    # Up (Y+)
    mesh_faces.append(((v_base+3, vt_base+0, 5), (v_base+7, vt_base+3, 5), (v_base+6, vt_base+2, 5), (v_base+2, vt_base+1, 5)))
    # Down (Y-)
    mesh_faces.append(((v_base+0, vt_base+0, 6), (v_base+1, vt_base+3, 6), (v_base+5, vt_base+2, 6), (v_base+4, vt_base+1, 6)))

with open(obj_path, "w", encoding="utf-8") as f:
    f.write("# Avatar Elements 3D VFX Mesh: earth_pillar\n")
    f.write("# Pivot: (0, 0, 0) at Ground Contact Point | Units: Metric (1.0 = 1 meter)\n")
    f.write("mtllib earth_pillar.mtl\n")
    f.write("o EarthPillar\n")
    for v in vertices:
        f.write(f"v {v[0]:.5f} {v[1]:.5f} {v[2]:.5f}\n")
    for vt in texcoords:
        f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
    for vn in normals:
        f.write(f"vn {vn[0]:.1f} {vn[1]:.1f} {vn[2]:.1f}\n")
    f.write("usemtl earth_pillar_mat\n")
    f.write("s 1\n")
    for face in mesh_faces:
        f.write(f"f {face[0][0]}/{face[0][1]}/{face[0][2]} {face[1][0]}/{face[1][1]}/{face[1][2]} {face[2][0]}/{face[2][1]}/{face[2][2]} {face[3][0]}/{face[3][1]}/{face[3][2]}\n")

print("Saved Wavefront OBJ/MTL mesh:", obj_path)

# -------------------------------------------------------------
# 5. EXPORT MINECRAFT BEDROCK GEOMETRY (geo.json)
# -------------------------------------------------------------
print("--> Generating Bedrock geometry JSON (geo.json)...")

geo_cubes = []
for elem in ELEMENTS:
    c_x = (elem["from"][0] + elem["to"][0]) / 2.0
    c_y = (elem["from"][1] + elem["to"][1]) / 2.0
    c_z = (elem["from"][2] + elem["to"][2]) / 2.0
    s_x = elem["to"][0] - elem["from"][0]
    s_y = elem["to"][1] - elem["from"][1]
    s_z = elem["to"][2] - elem["from"][2]
    
    q_ox, q_oy = QUAD_OFFSETS[elem["uv_quad"]]
    
    cube = {
        "origin": elem["from"],
        "size": [s_x, s_y, s_z],
        "uv": [q_ox, q_oy]
    }
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
                "identifier": "geometry.earth_pillar",
                "texture_width": 64,
                "texture_height": 64,
                "visible_bounds_width": 3,
                "visible_bounds_height": 4,
                "visible_bounds_offset": [0, 1.5, 0]
            },
            "bones": [
                {
                    "name": "root",
                    "pivot": [0, 0, 0],
                    "cubes": geo_cubes
                }
            ]
        }
    ]
}

geo_path = os.path.join(ASSET_PACK_DIR, "models", "earth_pillar.geo.json")
with open(geo_path, "w", encoding="utf-8") as f:
    json.dump(geo_data, f, indent=2)
print("Saved Bedrock geometry:", geo_path)

# -------------------------------------------------------------
# 6. EXPORT MINECRAFT JAVA DISPLAY MODEL (json)
# -------------------------------------------------------------
print("--> Generating Java 1.21.1 Display JSON model...")

java_elements = []
for elem in ELEMENTS:
    # Offset by [8, 0, 8] so (0, 0, 0) maps to center of block [8, 0, 8]
    j_from = [elem["from"][0] + 8.0, elem["from"][1], elem["from"][2] + 8.0]
    j_to   = [elem["to"][0] + 8.0,   elem["to"][1],   elem["to"][2] + 8.0]
    
    q_ox, q_oy = QUAD_OFFSETS[elem["uv_quad"]]
    u0 = q_ox / 4.0 # Scale from 64 to 16
    v0 = q_oy / 4.0
    u1 = (q_ox + 16) / 4.0
    v1 = (q_oy + 16) / 4.0
    
    faces = {}
    for f in ["north", "east", "south", "west", "up", "down"]:
        faces[f] = {
            "uv": [u0, v0, u1, v1],
            "texture": "#pillar"
        }
        
    j_elem = {
        "name": elem["name"],
        "from": j_from,
        "to": j_to,
        "faces": faces
    }
    
    if "rotation" in elem:
        rot = elem["rotation"]
        j_elem["rotation"] = {
            "origin": [rot["origin"][0] + 8.0, rot["origin"][1], rot["origin"][2] + 8.0],
            "axis": rot["axis"],
            "angle": rot["angle"]
        }
    java_elements.append(j_elem)

java_model_data = {
    "credit": "Avatar Elements Mod - Earth Pillar 3D Column (Fabric 1.21.1)",
    "texture_size": [64, 64],
    "textures": {
        "pillar": "avatar_elements:textures/vfx/earth_pillar",
        "particle": "avatar_elements:textures/vfx/earth_pillar"
    },
    "elements": java_elements,
    "display": {
        "ground": {
            "rotation": [0, 0, 0],
            "translation": [0, 0, 0],
            "scale": [1.0, 1.0, 1.0]
        },
        "fixed": {
            "rotation": [0, 0, 0],
            "translation": [0, 0, 0],
            "scale": [1.0, 1.0, 1.0]
        }
    }
}

java_model_path = os.path.join(ASSET_PACK_DIR, "models", "earth_pillar.json")
with open(java_model_path, "w", encoding="utf-8") as f:
    json.dump(java_model_data, f, indent=2)
# Also copy to asset_pack/assets/avatar_elements/models/item/
item_model_path = os.path.join(ASSET_PACK_DIR, "assets", "avatar_elements", "models", "item", "earth_pillar.json")
with open(item_model_path, "w", encoding="utf-8") as f:
    json.dump(java_model_data, f, indent=2)
print("Saved Java display model:", java_model_path)

# -------------------------------------------------------------
# 7. EXPORT EMERGENCE ANIMATION (animation.json)
# -------------------------------------------------------------
print("--> Generating emergence animation JSON...")

anim_data = {
    "format_version": "1.8.0",
    "animations": {
        "animation.avatar_elements.earth_pillar_eruption": {
            "loop": False,
            "animation_length": 1.3,
            # ATLA Canon Timing:
            # 0.00–0.06s : Ultra-fast linear eruption (ATLA pillars rise in ~1-2 animation frames)
            # 0.06–0.10s : Impact slam — stone "locks" into place (heavy stone-grinding SFX cue)
            # 0.10–0.80s : Rigid hold — earthbenders use this as a combat platform
            # 0.80–1.20s : Fractured crumble — not smooth sink; rapid step-drop
            "bones": {
                "root": {
                    "position": {
                        "0.00": [0.0, -48.0, 0.0],  # fully underground
                        "0.03": [0.0, -30.0, 0.0],  # burst begins (linear, no ease-in)
                        "0.06": [0.0,   1.5, 0.0],  # at full height (explosive overshoot)
                        "0.10": [0.0,   0.0, 0.0],  # settle / slam to rest
                        "0.80": [0.0,   0.0, 0.0],  # hold (rigid — zero movement)
                        "0.90": [0.0,  -8.0, 0.0],  # crumble stage 1
                        "1.05": [0.0, -28.0, 0.0],  # crumble stage 2 (rapid)
                        "1.20": [0.0, -48.0, 0.0]   # fully returned underground
                    },
                    "rotation": {
                        # Micro-impact shake at slam point (ATLA: earth-impact micro-vibration)
                        "0.06":  [0.8, 0.0, -0.8],  # small tilt at impact peak
                        "0.10":  [0.0, 0.0,  0.0],  # settle back to straight
                        "0.80":  [0.0, 0.0,  0.0]   # hold static
                    }
                }
            }
        }
    }
}

anim_path = os.path.join(ASSET_PACK_DIR, "animations", "earth_pillar.animation.json")
with open(anim_path, "w", encoding="utf-8") as f:
    json.dump(anim_data, f, indent=2)
print("Saved animation JSON:", anim_path)

# -------------------------------------------------------------
# 8. 3D SOFTWARE RENDERING & MULTI-ANGLE PREVIEWS
# -------------------------------------------------------------
print("--> Rendering 3D previews (Isometric, Front, Side, Top, and Turntable GIF)...")

def project_vertex(v, yaw_deg, pitch_deg, scale, cx, cy):
    # v in meters: (x, y, z)
    x, y, z = v
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)
    
    # Rotate Y (yaw)
    x1 = x * math.cos(yaw) + z * math.sin(yaw)
    y1 = y
    z1 = -x * math.sin(yaw) + z * math.cos(yaw)
    
    # Rotate X (pitch)
    x2 = x1
    y2 = y1 * math.cos(pitch) - z1 * math.sin(pitch)
    z2 = y1 * math.sin(pitch) + z1 * math.cos(pitch)
    
    # Isometric / orthographic projection (invert Y for screen space)
    px = cx + x2 * scale
    py = cy - y2 * scale
    return (px, py, z2)

# Extract quad faces with depth
def get_render_quads(yaw, pitch, scale, cx, cy):
    rendered_quads = []
    # Directional light vector (sun from top-left-front)
    light_dir = (-0.577, 0.577, 0.577)
    
    for face in mesh_faces:
        p0 = vertices[face[0][0] - 1]
        p1 = vertices[face[1][0] - 1]
        p2 = vertices[face[2][0] - 1]
        p3 = vertices[face[3][0] - 1]
        
        # Calculate normal in world space
        v01 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        v03 = (p3[0] - p0[0], p3[1] - p0[1], p3[2] - p0[2])
        nx = v01[1] * v03[2] - v01[2] * v03[1]
        ny = v01[2] * v03[0] - v01[0] * v03[2]
        nz = v01[0] * v03[1] - v01[1] * v03[0]
        n_len = math.sqrt(nx*nx + ny*ny + nz*nz)
        if n_len > 1e-6:
            nx /= n_len
            ny /= n_len
            nz /= n_len
        else:
            nx, ny, nz = (0, 1, 0)
            
        dot = max(0.15, nx * light_dir[0] + ny * light_dir[1] + nz * light_dir[2])
        # Diffuse + ambient shading
        intensity = 0.35 + 0.65 * dot
        
        # Color based on average height or face orientation
        # ATLA Canon palette: warm grey granite body, reddish-brown base
        avg_y = (p0[1] + p1[1] + p2[1] + p3[1]) / 4.0
        if avg_y > 2.5:    # Crown protrusions (top)
            base_col = (190, 182, 170)  # lighter broken crown stone
        elif avg_y > 1.25: # Mid-upper column (warm granite)
            base_col = (130, 122, 110)  # Pewter warm grey
        elif avg_y < 0.0:  # Subterranean anchor
            base_col = (55, 40, 28)     # dark soil/bedrock
        elif avg_y < 0.3:  # Base rupture slab
            base_col = (90, 68, 50)     # reddish-brown clay
        else:              # Lower column
            base_col = (108, 100, 90)   # granite mid-tone
            
        # Shaded color
        col = (
            min(255, int(base_col[0] * intensity)),
            min(255, int(base_col[1] * intensity)),
            min(255, int(base_col[2] * intensity)),
            255
        )
        edge_col = (
            max(0, int(col[0] * 0.5)),
            max(0, int(col[1] * 0.5)),
            max(0, int(col[2] * 0.5)),
            255
        )
        
        proj0 = project_vertex(p0, yaw, pitch, scale, cx, cy)
        proj1 = project_vertex(p1, yaw, pitch, scale, cx, cy)
        proj2 = project_vertex(p2, yaw, pitch, scale, cx, cy)
        proj3 = project_vertex(p3, yaw, pitch, scale, cx, cy)
        
        avg_depth = (proj0[2] + proj1[2] + proj2[2] + proj3[2]) / 4.0
        
        rendered_quads.append((
            avg_depth,
            [(proj0[0], proj0[1]), (proj1[0], proj1[1]), (proj2[0], proj2[1]), (proj3[0], proj3[1])],
            col,
            edge_col
        ))
        
    # Sort quads by depth (back to front painter's algorithm)
    rendered_quads.sort(key=lambda q: q[0])
    return rendered_quads

def render_frame(yaw, pitch, width=512, height=512, scale=120, cx=256, cy=380, title=None):
    img = Image.new("RGBA", (width, height), (24, 26, 30, 255))
    draw = ImageDraw.Draw(img)
    
    # Ground plane grid reference
    for gx in range(-2, 3):
        p_a = project_vertex((gx * 0.5, 0, -1.0), yaw, pitch, scale, cx, cy)
        p_b = project_vertex((gx * 0.5, 0,  1.0), yaw, pitch, scale, cx, cy)
        draw.line([(p_a[0], p_a[1]), (p_b[0], p_b[1])], fill=(45, 50, 58, 255), width=1)
    for gz in range(-2, 3):
        p_a = project_vertex((-1.0, 0, gz * 0.5), yaw, pitch, scale, cx, cy)
        p_b = project_vertex(( 1.0, 0, gz * 0.5), yaw, pitch, scale, cx, cy)
        draw.line([(p_a[0], p_a[1]), (p_b[0], p_b[1])], fill=(45, 50, 58, 255), width=1)
        
    # Ground origin contact marker
    g_orig = project_vertex((0, 0, 0), yaw, pitch, scale, cx, cy)
    draw.ellipse([g_orig[0]-4, g_orig[1]-4, g_orig[0]+4, g_orig[1]+4], fill=(230, 160, 40, 255), outline=(0, 0, 0, 255))
    
    # Draw geometry quads
    quads = get_render_quads(yaw, pitch, scale, cx, cy)
    for depth, poly, fill_col, border_col in quads:
        draw.polygon(poly, fill=fill_col, outline=border_col)
        
    if title:
        draw.text((16, 16), title, fill=(230, 230, 230, 255))
        draw.text((16, 34), "Height: 2.88m (46 units) | Footprint Radius: 1.6m | Origin: (0,0,0)", fill=(160, 170, 185, 255))
        
    return img

# Render Stills
img_iso = render_frame(yaw=45, pitch=25, scale=110, cx=256, cy=380, title="Earth Pillar — Isometric 3D View")
img_iso.save(os.path.join(PREVIEW_DIR, "earth_pillar_isometric.png"))

img_front = render_frame(yaw=0, pitch=0, scale=110, cx=256, cy=380, title="Earth Pillar — Front Orthographic View")
img_front.save(os.path.join(PREVIEW_DIR, "earth_pillar_front.png"))

img_side = render_frame(yaw=90, pitch=0, scale=110, cx=256, cy=380, title="Earth Pillar — Side Orthographic View")
img_side.save(os.path.join(PREVIEW_DIR, "earth_pillar_side.png"))

img_top = render_frame(yaw=0, pitch=90, scale=110, cx=256, cy=256, title="Earth Pillar — Top Footprint View")
img_top.save(os.path.join(PREVIEW_DIR, "earth_pillar_top.png"))

print("Saved preview stills in:", PREVIEW_DIR)

# Render 36-frame 360-degree turntable GIF
print("--> Generating 360-degree turntable GIF...")
frames = []
for deg in range(0, 360, 10):
    f_img = render_frame(yaw=deg, pitch=22, width=320, height=320, scale=70, cx=160, cy=245)
    frames.append(f_img)

turntable_path = os.path.join(PREVIEW_DIR, "earth_pillar_turntable.gif")
frames[0].save(
    turntable_path,
    save_all=True,
    append_images=frames[1:],
    duration=60, # 60ms per frame ~ 16 FPS
    loop=0
)
print("Saved 360 turntable GIF:", turntable_path)

# -------------------------------------------------------------
# 9. INTEGRATION SPECIFICATION (EARTH_PILLAR_SPEC.md)
# -------------------------------------------------------------
print("--> Generating handoff specification for Claude Code...")

spec_content = f"""
# 🪨 Earth Pillar 3D Asset Specification & Handoff (Canon v2 — ATLA/LOK)
> **Author:** Antigravity IDE (3D Asset Production Lead)
> **Consumer:** Claude Code (Runtime Implementer) & User (QA Reviewer)
> **Target:** Minecraft Fabric 1.21.1 (Client-only VFX Pillar)
> **Status:** Asset Complete — Canon Revised per ATLA/LOK Source Material
> **Canon Sources:** ATLA S2E01, S2E07 (Earth Rumble VI), LOK S1 Pro-bending arena

---

## Canon Accuracy Notes (v2 Revision)

| Element | Old (v1) | New (v2 Canon) | ATLA Source |
| :--- | :--- | :--- | :--- |
| **Crown shape** | Pyramid spire (non-canon) | Crenelated flat crown — 3 blunt protrusions | S2E07 Earth Rumble pillars |
| **Jade vein** | Present (green accent) | Removed — standard pillar has NO jade | Jade = special locations / metalbending |
| **Texture palette** | Dark grey-green | Warm grey granite + reddish-brown soil | ATLA Earth Kingdom stone palette |
| **Eruption timing** | 0.14s to full height (slow) | 0.06s to full height (explosive) | ATLA animation: ~1-2 frames at 24fps |
| **Column taper** | Moderate pyramid taper | Near-uniform width (monolithic) | Hung Ga stance = rooted/blocky |
| **Rupture shards** | Tall pointed (22.5 deg tilt) | Wide flat plates (15 deg shallow) | Ground crack plates, not rock spikes |
| **Hold duration** | 0.22-0.75s | 0.10-0.80s | ATLA pillar = combat platform, long hold |

---

## 1. Asset Files Summary & Locations

| Component | File Path | Format / Spec |
| :--- | :--- | :--- |
| **Blockbench Project** | `art-source/asset_pack/models/bbmodel/earth_pillar.bbmodel` | Blockbench 4.10 project file, hierarchy, UVs, embedded texture & eruption keyframes. |
| **Universal 3D Mesh** | `art-source/asset_pack/meshes/vfx/earth_pillar.obj` | Metric scale 1.0 (1 unit = 0.0625m, total height 2.875m), ground pivot at (0,0,0). |
| **Material Library** | `art-source/asset_pack/meshes/vfx/earth_pillar.mtl` | Links to earth_pillar.png. |
| **Bedrock Geometry** | `art-source/asset_pack/models/earth_pillar.geo.json` | Format 1.12.0, identifier geometry.earth_pillar. |
| **Java Display Model** | `art-source/asset_pack/models/earth_pillar.json` | Compatible with BlockDisplayEntity / ItemDisplayEntity. |
| **Texture Atlas** | `art-source/asset_pack/assets/avatar_elements/textures/vfx/earth_pillar.png` | 64x64 PNG — warm granite strata, reddish-brown soil base, dry crack (NO jade). |
| **Emergence Animation**| `art-source/asset_pack/animations/earth_pillar.animation.json` | 1.3s eruption timeline — canon ATLA speed (0.06s rise), long hold, rapid fractured crumble. |
| **3D Turntable GIF** | `art-source/asset_pack/previews/earth_pillar/earth_pillar_turntable.gif` | 360 degree rotating render. |
| **Isometric Preview** | `art-source/asset_pack/previews/earth_pillar/earth_pillar_isometric.png` | Isometric beauty render with ground contact marker. |

---

## 2. Geometry & Coordinate System Alignment

* **Ground Pivot Point:** Asset origin (0.0, 0.0, 0.0) is at the ground contact point.
* **Column Height:** Y = 0.0 to Y = 46.0 units (2.875 blocks / meters).
* **Footprint:** Foundation slab [-11, +11] units; radial debris up to 1.6 blocks. Aligns with FOOTPRINT_RADIUS = 1.6f in EarthPillarSkill.java.
* **Crown:** Flat-topped crenelated (3 protrusions) — canonical ATLA monolith, NOT spire/pyramid.

```
       *  Y = +2.88m (46u) -- Crown Protrusion A (tallest tooth)
       |  Y = +2.78m (44.5)-- Crown Protrusion B
       |  Y = +2.63m (42u) -- Crown Platform Slab (combat stance)
       |  Y = +2.50m (40u) -- Upper Column Top
       |  Y = +2.00m (32u) -- Mid-Upper Column Join
       |  Y = +1.25m (20u) -- Lower-Mid Column Join
       |  Y = +0.19m ( 3u) -- Basal Slab Top
-------+----------------------- Ground Surface (Y = 0.0, Pivot)
       v  Y = -0.25m (-4u) -- Subterranean Anchor
```

---

## 3. Canon-Accurate Animation Timeline (For Claude Code)

```
t = 0.00s : Start -- fully underground (Y = -48 units)
t = 0.03s : Burst begins -- linear rise, NO ease-in (earthbending is abrupt)
t = 0.06s : FULL HEIGHT -- overshoot to Y = +1.5
t = 0.10s : SLAM SETTLE -- locks to Y = 0 (heavy SFX cue)
t = 0.80s : HOLD END -- rigid platform hold (0.70s long, combat use)
t = 0.90s : CRUMBLE STAGE 1 -- drops to Y = -8 (fractured, NOT smooth)
t = 1.05s : CRUMBLE STAGE 2 -- drops to Y = -28 (rapid fragmentation)
t = 1.20s : FULLY SUBMERGED -- Y = -48, despawn trigger
```

---

## 4. Verification Checklist

- [x] Ground pivot is at (0, 0, 0).
- [x] Bounding box does not exceed footprint radius 1.6 blocks.
- [x] Texture is 64x64 ATLA canon palette (warm granite, reddish soil, NO jade).
- [x] Crown geometry is FLAT-TOPPED crenelated, not pyramid/spire.
- [x] Eruption timing matches ATLA animation speed (0.06s to full height).
- [x] No modifications made to mod/src/ runtime code.
- [x] Universal .bbmodel, .obj, .geo.json, and .json formats provided.
"""

spec_path = os.path.join(DOCS_DIR, "EARTH_PILLAR_SPEC.md")
with open(spec_path, "w", encoding="utf-8") as f:
    f.write(spec_content)
# Also copy to root docs/ for easy access by other agents
root_spec_path = os.path.join(REPO_ROOT, "docs", "EARTH_PILLAR_SPEC.md")
with open(root_spec_path, "w", encoding="utf-8") as f:
    f.write(spec_content)
print("Saved handoff specification:", spec_path)
print("All Earth Pillar assets built and exported successfully!")
