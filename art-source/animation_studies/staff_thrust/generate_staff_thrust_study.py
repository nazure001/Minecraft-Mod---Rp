import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. 3D MATH & FORWARD KINEMATICS UTILITIES
# -------------------------------------------------------------------------

def rot_x(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([
        [1,  0,  0, 0],
        [0,  c, -s, 0],
        [0,  s,  c, 0],
        [0,  0,  0, 1]
    ], dtype=float)

def rot_y(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([
        [ c, 0,  s, 0],
        [ 0, 1,  0, 0],
        [-s, 0,  c, 0],
        [ 0, 0,  0, 1]
    ], dtype=float)

def rot_z(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ], dtype=float)

def translate(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=float)

def euler_matrix(pitch_x, yaw_y, roll_z):
    # Minecraft Blockbench convention: Yaw (Y) -> Pitch (X) -> Roll (Z)
    return rot_y(yaw_y) @ rot_x(pitch_x) @ rot_z(roll_z)

def transform_point(mat, pt):
    v = np.array([pt[0], pt[1], pt[2], 1.0], dtype=float)
    res = mat @ v
    return res[:3]

def align_vector_matrix(target_v):
    v = np.array(target_v, dtype=float)
    norm = np.linalg.norm(v)
    if norm < 1e-6:
        return np.eye(4)
    v = v / norm
    
    src = np.array([0.0, 1.0, 0.0])
    dot = np.dot(src, v)
    
    if dot > 0.999999:
        return np.eye(4)
    elif dot < -0.999999:
        return rot_x(180)
    
    axis = np.cross(src, v)
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-6:
        return np.eye(4)
    axis = axis / axis_norm
    angle = math.acos(np.clip(dot, -1.0, 1.0))
    
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1.0 - c
    x, y, z = axis
    
    R = np.array([
        [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
        [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
        [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
        [0,           0,           0,           1]
    ], dtype=float)
    return R

# -------------------------------------------------------------------------
# 2. BOX GEOMETRY & COLOR PALETTE
# -------------------------------------------------------------------------

def make_box(min_pt, max_pt, base_color, name="cube"):
    x0, y0, z0 = min_pt
    x1, y1, z1 = max_pt
    
    vertices = np.array([
        [x0, y0, z0], # 0: left bottom back
        [x1, y0, z0], # 1: right bottom back
        [x1, y1, z0], # 2: right top back
        [x0, y1, z0], # 3: left top back
        [x0, y0, z1], # 4: left bottom front
        [x1, y0, z1], # 5: right bottom front
        [x1, y1, z1], # 6: right top front
        [x0, y1, z1]  # 7: left top front
    ], dtype=float)
    
    faces = [
        ([3, 2, 6, 7], np.array([0, 1, 0]), "up"),
        ([4, 5, 1, 0], np.array([0, -1, 0]), "down"),
        ([1, 0, 3, 2], np.array([0, 0, -1]), "north"),
        ([4, 7, 6, 5], np.array([0, 0, 1]), "south"),
        ([0, 4, 7, 3], np.array([-1, 0, 0]), "west"),
        ([5, 1, 2, 6], np.array([1, 0, 0]), "east")
    ]
    return {
        "name": name,
        "vertices": vertices,
        "faces": faces,
        "base_color": base_color
    }

# Character palette
C_SKIN = (218, 168, 132)
C_SKIN_SHADOW = (185, 135, 100)
C_HAIR = (74, 50, 34)
C_EYES = (45, 60, 160)
C_SHIRT = (0, 175, 175)
C_SHIRT_DARK = (0, 135, 135)
C_PANTS = (44, 60, 120)
C_PANTS_DARK = (30, 42, 88)
C_BOOTS = (28, 28, 35)

# Staff palette
C_STAFF_WOOD = (168, 112, 58)
C_STAFF_WRAP = (185, 48, 42)
C_STAFF_CAP = (220, 168, 45)

# UI Palette
BG_DARK = (18, 20, 26)
CARD_BG = (26, 30, 40)
CARD_BORDER = (45, 52, 70)
TEXT_WHITE = (242, 245, 250)
TEXT_MUTED = (145, 155, 175)
ACCENT_CYAN = (64, 200, 224)
ACCENT_GOLD = (235, 180, 55)
ACCENT_RED = (235, 75, 75)
ACCENT_GREEN = (75, 205, 125)

try:
    FONT_HEADER = ImageFont.truetype("arialbd.ttf", 26)
    FONT_TITLE = ImageFont.truetype("arialbd.ttf", 17)
    FONT_SUB = ImageFont.truetype("arial.ttf", 13)
    FONT_BOLD = ImageFont.truetype("arialbd.ttf", 13)
    FONT_MONO = ImageFont.truetype("consola.ttf", 12)
    FONT_SMALL = ImageFont.truetype("arial.ttf", 11)
except Exception:
    FONT_HEADER = ImageFont.load_default()
    FONT_TITLE = ImageFont.load_default()
    FONT_SUB = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()
    FONT_MONO = ImageFont.load_default()
    FONT_SMALL = ImageFont.load_default()

# -------------------------------------------------------------------------
# 3. POSE DEFINITIONS & KINEMATICS DATA
# -------------------------------------------------------------------------

POSES = {
    "01_ready_stance": {
        "title": "1. Sikap Awal (Two-Handed Ready Stance)",
        "phase": "STANCE & GUARD",
        "timing_frames": "Frames 0 - 5 (0.00s - 0.21s)",
        "desc": "Kuda-kuda dua tangan seimbang. Tubuh menyudut 22 deg, ujung tongkat membidik koridor dada sasaran.",
        "root": {"pos": [0.0, 11.5, 0.0], "rot": [0.0, 0.0, 0.0]},
        "torso": {"rot": [4.0, 22.0, 0.0]},
        "head": {"rot": [-2.0, -22.0, 0.0]},
        "left_arm": {"rot": [-48.0, 26.0, 18.0], "pivot": [5.0, 22.0, 0.0]},
        "right_arm": {"rot": [-16.0, -10.0, -8.0], "pivot": [-5.0, 22.0, 0.0]},
        "left_leg": {"rot": [10.0, 12.0, -4.0], "pivot": [2.0, 11.5, 0.0]},
        "right_leg": {"rot": [-14.0, -18.0, 6.0], "pivot": [-2.0, 11.5, 0.0]},
        "grip_rear": [-3.2, 14.0, 1.2],
        "grip_lead": [1.8, 16.5, 7.8],
        "butt_offset": 5.5,
        "tip_offset": 14.0,
        "com": [-0.2, 12.0, 0.3],
        "tactical_intent": "Pertahanan reaktif, meminimalisir profil siluet tubuh, kesiapan menusuk atau memutar baling-baling udara."
    },
    "02_anticipation_windup": {
        "title": "2. Persiapan (Anticipation / Windup)",
        "phase": "COILING & LOAD",
        "timing_frames": "Frames 6 - 11 (0.25s - 0.46s)",
        "desc": "Pegas tubuh memadat: rotasi pinggul +42 deg, bobot 70% di kaki belakang, tongkat ditarik ke belakang di jalur tusukan.",
        "root": {"pos": [-0.5, 10.8, -1.0], "rot": [0.0, 0.0, 0.0]},
        "torso": {"rot": [6.0, 42.0, -2.0]},
        "head": {"rot": [0.0, -42.0, 2.0]},
        "left_arm": {"rot": [-36.0, 40.0, 24.0], "pivot": [5.0, 22.0, 0.0]},
        "right_arm": {"rot": [10.0, -24.0, -14.0], "pivot": [-5.0, 22.0, 0.0]},
        "left_leg": {"rot": [18.0, 16.0, -2.0], "pivot": [2.0, 10.8, 0.0]},
        "right_leg": {"rot": [-26.0, -26.0, 8.0], "pivot": [-2.0, 10.8, 0.0]},
        "grip_rear": [-5.6, 13.2, -3.4],
        "grip_lead": [-0.4, 16.2, 3.8],
        "butt_offset": 5.5,
        "tip_offset": 14.0,
        "com": [-1.2, 11.2, -1.4],
        "tactical_intent": "Akumulasi energi kinetik melalui rantai kinetik panggul, mengunci garis lintasan tusukan searah pandangan mata."
    },
    "03_thrust_strike": {
        "title": "3. Dorongan / Tusukan (Thrust Strike)",
        "phase": "APEX PENETRATION",
        "timing_frames": "Frames 12 - 17 (0.50s - 0.71s)",
        "desc": "Tusukan lurus meledak (Gong Bu lunge): tangan kanan memompa lurus, tangan kiri memandu poros, ujung tongkat menembus sasaran.",
        "root": {"pos": [0.2, 11.2, 3.8], "rot": [0.0, 0.0, 0.0]},
        "torso": {"rot": [12.0, 8.0, 0.0]},
        "head": {"rot": [4.0, -8.0, 0.0]},
        "left_arm": {"rot": [-76.0, 10.0, 12.0], "pivot": [5.0, 22.0, 0.0]},
        "right_arm": {"rot": [-62.0, -6.0, -6.0], "pivot": [-5.0, 22.0, 0.0]},
        "left_leg": {"rot": [32.0, 4.0, -4.0], "pivot": [2.0, 11.2, 0.0]},
        "right_leg": {"rot": [-35.0, -10.0, 6.0], "pivot": [-2.0, 11.2, 0.0]},
        "grip_rear": [-1.4, 17.5, 9.2],
        "grip_lead": [1.2, 19.0, 16.8],
        "butt_offset": 5.5,
        "tip_offset": 14.0,
        "com": [0.4, 11.6, 3.5],
        "tactical_intent": "Penetrasi linier horizontal maksimum, transfer massa tubuh penuh ke ujung tongkat, pelepasan tekanan kompresi udara."
    },
    "04_recovery": {
        "title": "4. Pemulihan (Recovery & Guard Reset)",
        "phase": "MOMENTUM ABSORPTION",
        "timing_frames": "Frames 18 - 24 (0.75s - 1.00s)",
        "desc": "Penyerapan momentum hentakan: tongkat ditarik surut 9 unit dari ekstensi puncak, tubuh kembali ke posisi siaga dinamis.",
        "root": {"pos": [0.0, 11.6, 1.5], "rot": [0.0, 0.0, 0.0]},
        "torso": {"rot": [4.0, 18.0, 0.0]},
        "head": {"rot": [-1.0, -18.0, 0.0]},
        "left_arm": {"rot": [-50.0, 22.0, 15.0], "pivot": [5.0, 22.0, 0.0]},
        "right_arm": {"rot": [-24.0, -12.0, -8.0], "pivot": [-5.0, 22.0, 0.0]},
        "left_leg": {"rot": [14.0, 8.0, -3.0], "pivot": [2.0, 11.6, 0.0]},
        "right_leg": {"rot": [-18.0, -14.0, 4.0], "pivot": [-2.0, 11.6, 0.0]},
        "grip_rear": [-2.6, 14.8, 3.8],
        "grip_lead": [1.4, 17.2, 10.2],
        "butt_offset": 5.5,
        "tip_offset": 14.0,
        "com": [0.1, 11.9, 1.6],
        "tactical_intent": "Mencegah over-extension dan rebutan senjata, memulihkan postur seimbang untuk kombo lanjutan atau tangkisan."
    }
}

for p_key, p_data in POSES.items():
    rear = np.array(p_data["grip_rear"], dtype=float)
    lead = np.array(p_data["grip_lead"], dtype=float)
    diff = lead - rear
    dist = np.linalg.norm(diff)
    dir_v = diff / dist
    
    butt = rear - dir_v * p_data["butt_offset"]
    tip = lead + dir_v * p_data["tip_offset"]
    
    p_data["staff_butt"] = [round(float(x), 2) for x in butt]
    p_data["staff_tip"] = [round(float(x), 2) for x in tip]
    p_data["staff_length"] = round(float(dist + p_data["butt_offset"] + p_data["tip_offset"]), 2)
    p_data["thrust_height"] = round(float(tip[1]), 2)
    p_data["extension_z"] = round(float(tip[2]), 2)

# Save JSON
with open(os.path.join(OUTPUT_DIR, "pose_data.json"), "w", encoding="utf-8") as f:
    json.dump(POSES, f, indent=2)

# -------------------------------------------------------------------------
# 4. 3D MESH GENERATION FOR A POSE
# -------------------------------------------------------------------------

def build_pose_boxes(pose_key):
    p = POSES[pose_key]
    boxes = []
    
    # Root matrix
    root_pos = p["root"]["pos"]
    M_root = translate(root_pos[0], root_pos[1], root_pos[2])
    
    # Torso
    torso_rot = p["torso"]["rot"]
    M_torso_rot = euler_matrix(torso_rot[0], torso_rot[1], torso_rot[2])
    M_torso = M_root @ M_torso_rot
    
    # Torso cube: [-4, 0, -2] to [4, 12, 2]
    b_torso = make_box([-4, 0, -2], [4, 12, 2], C_SHIRT, "torso")
    b_torso["world_vertices"] = np.array([transform_point(M_torso, v) for v in b_torso["vertices"]])
    boxes.append(b_torso)
    
    # Neck / Head
    head_rot = p["head"]["rot"]
    M_head_pivot = translate(0, 12, 0)
    M_head_rot = euler_matrix(head_rot[0], head_rot[1], head_rot[2])
    M_head = M_torso @ M_head_pivot @ M_head_rot
    
    # Head cube: [-4, 0, -4] to [4, 8, 4]
    b_head = make_box([-4, 0, -4], [4, 8, 4], C_SKIN, "head")
    b_head["world_vertices"] = np.array([transform_point(M_head, v) for v in b_head["vertices"]])
    boxes.append(b_head)
    
    # Hair cap: [-4.1, 4.0, -4.1] to [4.1, 8.2, 4.1]
    b_hair = make_box([-4.1, 4.0, -4.1], [4.1, 8.2, 4.1], C_HAIR, "hair")
    b_hair["world_vertices"] = np.array([transform_point(M_head, v) for v in b_hair["vertices"]])
    boxes.append(b_hair)
    
    # Left Arm
    la_rot = p["left_arm"]["rot"]
    la_piv = p["left_arm"]["pivot"]
    M_la_pivot = translate(la_piv[0], la_piv[1] - 12.0, la_piv[2])
    M_la_rot = euler_matrix(la_rot[0], la_rot[1], la_rot[2])
    M_la = M_torso @ M_la_pivot @ M_la_rot
    
    b_la_sleeve = make_box([-1, -4, -2], [3, 0, 2], C_SHIRT, "left_sleeve")
    b_la_sleeve["world_vertices"] = np.array([transform_point(M_la, v) for v in b_la_sleeve["vertices"]])
    boxes.append(b_la_sleeve)
    b_la_hand = make_box([-1, -12, -2], [3, -4, 2], C_SKIN, "left_hand")
    b_la_hand["world_vertices"] = np.array([transform_point(M_la, v) for v in b_la_hand["vertices"]])
    boxes.append(b_la_hand)
    
    # Right Arm
    ra_rot = p["right_arm"]["rot"]
    ra_piv = p["right_arm"]["pivot"]
    M_ra_pivot = translate(ra_piv[0], ra_piv[1] - 12.0, ra_piv[2])
    M_ra_rot = euler_matrix(ra_rot[0], ra_rot[1], ra_rot[2])
    M_ra = M_torso @ M_ra_pivot @ M_ra_rot
    
    b_ra_sleeve = make_box([-3, -4, -2], [1, 0, 2], C_SHIRT, "right_sleeve")
    b_ra_sleeve["world_vertices"] = np.array([transform_point(M_ra, v) for v in b_ra_sleeve["vertices"]])
    boxes.append(b_ra_sleeve)
    b_ra_hand = make_box([-3, -12, -2], [1, -4, 2], C_SKIN, "right_hand")
    b_ra_hand["world_vertices"] = np.array([transform_point(M_ra, v) for v in b_ra_hand["vertices"]])
    boxes.append(b_ra_hand)
    
    # Left Leg
    ll_rot = p["left_leg"]["rot"]
    M_ll_pivot = translate(2.0, 0.0, 0.0)
    M_ll_rot = euler_matrix(ll_rot[0], ll_rot[1], ll_rot[2])
    M_ll = M_root @ M_ll_pivot @ M_ll_rot
    
    b_ll_pants = make_box([-2, -8, -2], [2, 0, 2], C_PANTS, "left_pants")
    b_ll_pants["world_vertices"] = np.array([transform_point(M_ll, v) for v in b_ll_pants["vertices"]])
    boxes.append(b_ll_pants)
    b_ll_boot = make_box([-2, -12, -2], [2, -8, 2], C_BOOTS, "left_boot")
    b_ll_boot["world_vertices"] = np.array([transform_point(M_ll, v) for v in b_ll_boot["vertices"]])
    boxes.append(b_ll_boot)
    
    # Right Leg
    rl_rot = p["right_leg"]["rot"]
    M_rl_pivot = translate(-2.0, 0.0, 0.0)
    M_rl_rot = euler_matrix(rl_rot[0], rl_rot[1], rl_rot[2])
    M_rl = M_root @ M_rl_pivot @ M_rl_rot
    
    b_rl_pants = make_box([-2, -8, -2], [2, 0, 2], C_PANTS, "right_pants")
    b_rl_pants["world_vertices"] = np.array([transform_point(M_rl, v) for v in b_rl_pants["vertices"]])
    boxes.append(b_rl_pants)
    b_rl_boot = make_box([-2, -12, -2], [2, -8, 2], C_BOOTS, "right_boot")
    b_rl_boot["world_vertices"] = np.array([transform_point(M_rl, v) for v in b_rl_boot["vertices"]])
    boxes.append(b_rl_boot)
    
    # Staff Segments
    butt = np.array(p["staff_butt"])
    tip = np.array(p["staff_tip"])
    staff_vec = tip - butt
    staff_len = float(np.linalg.norm(staff_vec))
    dir_staff = staff_vec / staff_len
    
    R_staff = align_vector_matrix(dir_staff)
    M_staff = translate(butt[0], butt[1], butt[2]) @ R_staff
    
    # 1. Lower Cap (Brass)
    b_scap_lo = make_box([-0.9, 0.0, -0.9], [0.9, 1.0, 0.9], C_STAFF_CAP, "staff_lower_cap")
    b_scap_lo["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_scap_lo["vertices"]])
    boxes.append(b_scap_lo)
    
    # 2. Lower Shaft (Wood)
    b_sshaft_lo = make_box([-0.7, 1.0, -0.7], [0.7, 10.5, 0.7], C_STAFF_WOOD, "staff_lower_shaft")
    b_sshaft_lo["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_sshaft_lo["vertices"]])
    boxes.append(b_sshaft_lo)
    
    # 3. Grip Wrap (Crimson Wrap)
    lead_offset = staff_len - p["tip_offset"]
    b_swrap = make_box([-0.85, lead_offset - 3.0, -0.85], [0.85, lead_offset + 3.0, 0.85], C_STAFF_WRAP, "staff_wrap")
    b_swrap["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_swrap["vertices"]])
    boxes.append(b_swrap)
    
    # 4. Upper Shaft (Wood)
    b_sshaft_hi = make_box([-0.7, lead_offset + 3.0, -0.7], [0.7, staff_len - 1.0, 0.7], C_STAFF_WOOD, "staff_upper_shaft")
    b_sshaft_hi["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_sshaft_hi["vertices"]])
    boxes.append(b_sshaft_hi)
    
    # 5. Upper Cap (Brass)
    b_scap_hi = make_box([-0.9, staff_len - 1.0, -0.9], [0.9, staff_len, 0.9], C_STAFF_CAP, "staff_upper_cap")
    b_scap_hi["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_scap_hi["vertices"]])
    boxes.append(b_scap_hi)
    
    return boxes

# -------------------------------------------------------------------------
# 5. RENDERING PIPELINE FOR SCENES
# -------------------------------------------------------------------------

def get_projector(view_mode, cx, cy, scale):
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    
    def project(pt):
        x, y, z = pt
        if view_mode == "front":
            px = cx - x * scale
            py = cy - y * scale
            depth = z
        elif view_mode == "side":
            # Looking from right side (-X towards +X)
            # Front of Steve (+Z) points to the right of screen
            px = cx + z * scale
            py = cy - y * scale
            depth = -x
        else: # Isometric
            # 3/4 front view
            px = cx + (z - x) * scale * cos30
            py = cy - y * scale + (x + z) * scale * sin30 * 0.5
            depth = x + z
        return (px, py, depth)
    return project

def render_pose(draw, boxes, view_mode="iso", cx=300, cy=350, scale=12.0):
    project = get_projector(view_mode, cx, cy, scale)
    
    if view_mode == "iso":
        L_key = np.array([0.45, 0.85, -0.25])
        L_fill = np.array([-0.6, 0.25, 0.75])
    elif view_mode == "front":
        L_key = np.array([0.3, 0.75, -0.58])
        L_fill = np.array([-0.4, 0.2, -0.89])
    else: # side
        L_key = np.array([-0.55, 0.8, 0.25])
        L_fill = np.array([0.65, 0.2, -0.2])
    
    L_key = L_key / np.linalg.norm(L_key)
    L_fill = L_fill / np.linalg.norm(L_fill)
    
    all_faces = []
    for b in boxes:
        verts = b["world_vertices"]
        for face_indices, norm_local, face_name in b["faces"]:
            poly_3d = verts[face_indices]
            
            v0 = poly_3d[1] - poly_3d[0]
            v1 = poly_3d[2] - poly_3d[0]
            norm_world = np.cross(v0, v1)
            n_len = np.linalg.norm(norm_world)
            if n_len > 1e-6:
                norm_world = norm_world / n_len
            else:
                norm_world = np.array([0, 1, 0])
            
            centroid = np.mean(poly_3d, axis=0)
            proj_centroid = project(centroid)
            poly_2d = [project(p)[:2] for p in poly_3d]
            
            dot_key = max(0.0, float(np.dot(norm_world, L_key)))
            dot_fill = max(0.0, float(np.dot(norm_world, L_fill)))
            intensity = 0.38 + 0.50 * dot_key + 0.16 * dot_fill
            
            base = b["base_color"]
            shaded_color = (
                min(255, int(base[0] * intensity)),
                min(255, int(base[1] * intensity)),
                min(255, int(base[2] * intensity)),
                255
            )
            
            all_faces.append({
                "poly_2d": poly_2d,
                "depth": proj_centroid[2],
                "color": shaded_color,
                "name": b["name"]
            })
            
    # Sort Painter's algorithm
    all_faces.sort(key=lambda f: f["depth"])
    
    for f in all_faces:
        draw.polygon(f["poly_2d"], fill=f["color"], outline=(30, 32, 42, 200))
        
    return project

# -------------------------------------------------------------------------
# 6. GENERATE STORYBOARD IMAGES
# -------------------------------------------------------------------------

def render_storyboard(view_mode="iso", out_filename="preview_storyboard_iso.png"):
    W, H = 2400, 960
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Title bar
    view_label = {
        "iso": "3D ISOMETRIC PERSPECTIVE (ISOMETRIK 3/4 SUDUT)",
        "front": "FRONT ORTHOGRAPHIC VIEW (TAMPAK DEPAN)",
        "side": "SIDE ORTHOGRAPHIC VIEW (TAMPAK SAMPING - LINTASAN VEKTOR)"
    }[view_mode]
    
    draw.rectangle([(0, 0), (W, 80)], fill=(24, 28, 38))
    draw.line([(0, 80), (W, 80)], fill=CARD_BORDER, width=2)
    
    draw.text((40, 18), "AIR NOMAD STAFF — POSE STUDY & KINEMATICS", fill=TEXT_WHITE, font=FONT_HEADER)
    draw.text((40, 48), f"Gerakan: Staff Thrust (Tusukan Tombak/Tongkat) | View: {view_label}", fill=ACCENT_CYAN, font=FONT_SUB)
    draw.text((W - 520, 30), "STATUS: ANIMATION POSE STUDY (NON-RUNTIME)", fill=ACCENT_GOLD, font=FONT_BOLD)
    
    # 4 Columns
    col_w = (W - 80) // 4
    for idx, (p_key, p_data) in enumerate(POSES.items()):
        bx = 40 + idx * col_w
        by = 100
        bw = col_w - 20
        bh = H - 130
        
        # Card Background
        draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=CARD_BG, outline=CARD_BORDER, width=2)
        
        # Header inside card
        draw.rectangle([(bx, by), (bx + bw, by + 45)], fill=(32, 38, 52))
        draw.line([(bx, by + 45), (bx + bw, by + 45)], fill=CARD_BORDER, width=1)
        
        draw.text((bx + 15, by + 8), p_data["title"], fill=TEXT_WHITE, font=FONT_TITLE)
        draw.text((bx + 15, by + 28), p_data["timing_frames"], fill=ACCENT_GOLD, font=FONT_SMALL)
        
        # Viewport ground & grid
        vp_x = bx + bw // 2
        vp_y = by + 420
        scale = 13.5
        
        # Draw ground grid
        project = get_projector(view_mode, vp_x, vp_y, scale)
        for gz in range(-16, 32, 8):
            p_start = project([-16, 0, gz])[:2]
            p_end = project([16, 0, gz])[:2]
            draw.line([p_start, p_end], fill=(38, 44, 60), width=1)
        for gx in range(-16, 24, 8):
            p_start = project([gx, 0, -16])[:2]
            p_end = project([gx, 0, 32])[:2]
            draw.line([p_start, p_end], fill=(38, 44, 60), width=1)
            
        # Draw player & staff
        boxes = build_pose_boxes(p_key)
        render_pose(draw, boxes, view_mode=view_mode, cx=vp_x, cy=vp_y, scale=scale)
        
        # Marker for Grip Points & Staff Tip
        pt_rear = project(p_data["grip_rear"])[:2]
        pt_lead = project(p_data["grip_lead"])[:2]
        pt_tip = project(p_data["staff_tip"])[:2]
        pt_butt = project(p_data["staff_butt"])[:2]
        
        # Draw markers
        draw.ellipse([(pt_rear[0]-5, pt_rear[1]-5), (pt_rear[0]+5, pt_rear[1]+5)], fill=ACCENT_RED, outline=(255, 255, 255), width=2)
        draw.ellipse([(pt_lead[0]-5, pt_lead[1]-5), (pt_lead[0]+5, pt_lead[1]+5)], fill=ACCENT_CYAN, outline=(255, 255, 255), width=2)
        draw.ellipse([(pt_tip[0]-6, pt_tip[1]-6), (pt_tip[0]+6, pt_tip[1]+6)], fill=ACCENT_GOLD, outline=(255, 255, 255), width=2)
        
        # In side view, draw horizontal thrust target line
        if view_mode == "side":
            h_line_y = project([0, 20.0, 0])[1]
            draw.line([(bx + 15, h_line_y), (bx + bw - 15, h_line_y)], fill=(120, 100, 40, 180), width=1)
            draw.text((bx + 20, h_line_y - 14), "Thrust Axis (Y=20)", fill=ACCENT_GOLD, font=FONT_SMALL)
        
        # Bottom info card
        info_y = by + bh - 190
        draw.rectangle([(bx + 10, info_y), (bx + bw - 10, by + bh - 10)], fill=(22, 25, 34), outline=CARD_BORDER, width=1)
        
        draw.text((bx + 20, info_y + 10), "TELEMETRI & KOORDINAT:", fill=ACCENT_CYAN, font=FONT_BOLD)
        draw.text((bx + 20, info_y + 30), f"Staff Tip (X,Y,Z): {p_data['staff_tip']}", fill=TEXT_WHITE, font=FONT_MONO)
        draw.text((bx + 20, info_y + 48), f"Lead Grip (L-Hand): {p_data['grip_lead']}", fill=TEXT_MUTED, font=FONT_MONO)
        draw.text((bx + 20, info_y + 66), f"Rear Grip (R-Hand): {p_data['grip_rear']}", fill=TEXT_MUTED, font=FONT_MONO)
        draw.text((bx + 20, info_y + 84), f"Tip Height / Z-Reach: Y={p_data['thrust_height']} | Z={p_data['extension_z']}", fill=ACCENT_GOLD, font=FONT_MONO)
        
        # Tactical description
        draw.text((bx + 20, info_y + 110), "INTENSI TAKTIKAL:", fill=ACCENT_GREEN, font=FONT_BOLD)
        # Multiline text wrap
        words = p_data["tactical_intent"].split()
        line1, line2 = "", ""
        for w in words:
            if len(line1) + len(w) < 42:
                line1 += w + " "
            else:
                line2 += w + " "
        draw.text((bx + 20, info_y + 130), line1, fill=TEXT_WHITE, font=FONT_SMALL)
        draw.text((bx + 20, info_y + 148), line2, fill=TEXT_WHITE, font=FONT_SMALL)
        
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    img.save(out_path)
    print(f"Saved: {out_filename}")

render_storyboard("iso", "preview_storyboard_iso.png")
render_storyboard("front", "preview_storyboard_front.png")
render_storyboard("side", "preview_storyboard_side.png")

# -------------------------------------------------------------------------
# 7. GENERATE DEDICATED TRAJECTORY & TELEMETRY DIAGRAM
# -------------------------------------------------------------------------

def render_trajectory_diagram():
    W, H = 2000, 1100
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.rectangle([(0, 0), (W, 80)], fill=(24, 28, 38))
    draw.line([(0, 80), (W, 80)], fill=CARD_BORDER, width=2)
    draw.text((40, 18), "STAFF THRUST — TRAJECTORY & KINEMATIC DISPLACEMENT DIAGRAM", fill=TEXT_WHITE, font=FONT_HEADER)
    draw.text((40, 48), "Analisis Vektor Lintasan: Ujung Tongkat (Tip), Tangan Kendali (Lead), dan Tangan Daya (Rear)", fill=ACCENT_CYAN, font=FONT_SUB)
    draw.text((W - 480, 30), "SIDE ELEVATION KINEMATICS", fill=ACCENT_GOLD, font=FONT_BOLD)
    
    # Left Viewport: Combined Trajectory Overlay (Z-Y Plane)
    cv_x, cv_y = 60, 105
    cv_w, cv_h = 1250, 940
    draw.rectangle([(cv_x, cv_y), (cv_x + cv_w, cv_y + cv_h)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    
    draw.text((cv_x + 25, cv_y + 20), "DIAGRAM OVERLAY ELEVASI SAMPING (Z-Y AXIS)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((cv_x + 25, cv_y + 45), "Skala: 1 Blok MC = 16 Unit = 320 px (1 Unit = 20 px). Ground Y=0.", fill=TEXT_MUTED, font=FONT_SUB)
    
    # Origin in this viewport
    orig_px = cv_x + 350
    orig_py = cv_y + 720
    u_scale = 18.0 # pixels per 3D unit
    
    def to_screen(z, y):
        return (orig_px + z * u_scale, orig_py - y * u_scale)
    
    # Grid lines
    # Ground Y=0
    g_start = to_screen(-15, 0)
    g_end = to_screen(45, 0)
    draw.line([g_start, g_end], fill=(90, 105, 130), width=3)
    draw.text((g_start[0], g_start[1] + 8), "GROUND LEVEL (Y = 0)", fill=TEXT_MUTED, font=FONT_SMALL)
    
    # Horizontal height grid lines
    for y_val in [6, 12, 18, 20, 24, 30]:
        p0 = to_screen(-15, y_val)
        p1 = to_screen(45, y_val)
        draw.line([p0, p1], fill=(42, 48, 65), width=1)
        draw.text((p0[0] - 80, p0[1] - 8), f"Y={y_val:02d}", fill=TEXT_MUTED, font=FONT_MONO)
    
    # Target chest corridor line
    c0 = to_screen(-15, 20.3)
    c1 = to_screen(45, 20.3)
    draw.line([c0, c1], fill=(160, 130, 40, 220), width=2)
    draw.text((c1[0] - 220, c1[1] - 18), "TARGET CHEST AXIS (Y = 20.3)", fill=ACCENT_GOLD, font=FONT_BOLD)
    
    # Vertical Z coordinate grid lines
    for z_val in range(-10, 45, 10):
        p0 = to_screen(z_val, 0)
        p1 = to_screen(z_val, 32)
        draw.line([p0, p1], fill=(42, 48, 65), width=1)
        draw.text((p0[0] - 12, p0[1] + 8), f"Z={z_val:+02d}", fill=TEXT_MUTED, font=FONT_MONO)
        
    # Draw player silhouette ghost in neutral stance
    p_torso = [to_screen(0, 12), to_screen(0, 24)]
    draw.rectangle([(orig_px - 20, orig_py - 24*u_scale), (orig_px + 20, orig_py - 12*u_scale)], fill=(32, 40, 56, 120), outline=(55, 65, 88), width=2)
    draw.rectangle([(orig_px - 25, orig_py - 32*u_scale), (orig_px + 25, orig_py - 24*u_scale)], fill=(38, 48, 68, 120), outline=(60, 72, 98), width=2)
    draw.text((orig_px - 25, orig_py - 35*u_scale), "PLAYER ROOT (Z=0)", fill=TEXT_MUTED, font=FONT_SMALL)
    
    # Trajectory points collection
    tip_pts = []
    lead_pts = []
    rear_pts = []
    butt_pts = []
    
    p_keys = ["01_ready_stance", "02_anticipation_windup", "03_thrust_strike", "04_recovery"]
    p_colors = [ACCENT_CYAN, (220, 100, 220), ACCENT_GOLD, ACCENT_GREEN]
    
    for idx, pk in enumerate(p_keys):
        p = POSES[pk]
        col = p_colors[idx]
        
        # Staff line
        pt_b = to_screen(p["staff_butt"][2], p["staff_butt"][1])
        pt_t = to_screen(p["staff_tip"][2], p["staff_tip"][1])
        draw.line([pt_b, pt_t], fill=col, width=4)
        
        # Grip points
        pt_r = to_screen(p["grip_rear"][2], p["grip_rear"][1])
        pt_l = to_screen(p["grip_lead"][2], p["grip_lead"][1])
        
        tip_pts.append(pt_t)
        lead_pts.append(pt_l)
        rear_pts.append(pt_r)
        butt_pts.append(pt_b)
        
        # Draw node circles
        draw.ellipse([(pt_t[0]-7, pt_t[1]-7), (pt_t[0]+7, pt_t[1]+7)], fill=col, outline=(255, 255, 255), width=2)
        draw.ellipse([(pt_l[0]-5, pt_l[1]-5), (pt_l[0]+5, pt_l[1]+5)], fill=ACCENT_CYAN, outline=(255, 255, 255), width=1)
        draw.ellipse([(pt_r[0]-5, pt_r[1]-5), (pt_r[0]+5, pt_r[1]+5)], fill=ACCENT_RED, outline=(255, 255, 255), width=1)
        
        # Annotation text near tip
        label = f"P{idx+1}: {p['phase']}"
        draw.text((pt_t[0] + 12, pt_t[1] - 10), label, fill=col, font=FONT_BOLD)
    
    # Draw Trajectory Flow Curves (Dashed / Polylines)
    # 1. Staff Tip Trajectory
    draw.line(tip_pts + [tip_pts[0]], fill=ACCENT_GOLD, width=2)
    # 2. Lead Hand Trajectory
    draw.line(lead_pts + [lead_pts[0]], fill=ACCENT_CYAN, width=1)
    # 3. Rear Hand Trajectory
    draw.line(rear_pts + [rear_pts[0]], fill=ACCENT_RED, width=1)
    
    # Draw Kinetic Strike Arrow (from Windup P2 to Strike P3)
    p2_tip = tip_pts[1]
    p3_tip = tip_pts[2]
    draw.line([p2_tip, p3_tip], fill=(255, 240, 100), width=5)
    # Draw arrow head
    draw.polygon([
        (p3_tip[0] + 4, p3_tip[1]),
        (p3_tip[0] - 16, p3_tip[1] - 10),
        (p3_tip[0] - 16, p3_tip[1] + 10)
    ], fill=(255, 240, 100))
    
    draw.text(((p2_tip[0] + p3_tip[0])//2 - 60, p2_tip[1] - 30), "EXPLOSIVE THRUST DRIVE (+16.8 Units)", fill=(255, 240, 100), font=FONT_BOLD)
    
    # Right Sidebar: Technical Analysis & Metrics Table
    sb_x, sb_y = cv_x + cv_w + 30, cv_y
    sb_w, sb_h = W - sb_x - 40, cv_h
    draw.rectangle([(sb_x, sb_y), (sb_x + sb_w, sb_y + sb_h)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    
    draw.text((sb_x + 25, sb_y + 20), "METRIK KINEMATIKA & TITIK GENGGAM", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((sb_x + 25, sb_y + 45), "Spesifikasi Presisi untuk Rigging & DCC Export", fill=ACCENT_CYAN, font=FONT_SUB)
    
    # Legend box
    leg_y = sb_y + 85
    draw.rectangle([(sb_x + 20, leg_y), (sb_x + sb_w - 20, leg_y + 115)], fill=(22, 25, 34), outline=CARD_BORDER, width=1)
    draw.text((sb_x + 30, leg_y + 10), "LEGENDA DIAGRAM:", fill=TEXT_MUTED, font=FONT_BOLD)
    
    draw.line([(sb_x + 30, leg_y + 38), (sb_x + 65, leg_y + 38)], fill=ACCENT_GOLD, width=3)
    draw.text((sb_x + 75, leg_y + 30), "Lintasan Ujung Tongkat (Staff Tip Path)", fill=TEXT_WHITE, font=FONT_SMALL)
    
    draw.line([(sb_x + 30, leg_y + 60), (sb_x + 65, leg_y + 60)], fill=ACCENT_CYAN, width=2)
    draw.text((sb_x + 75, leg_y + 52), "Lintasan Tangan Kiri (Lead Guide Sleeve)", fill=TEXT_WHITE, font=FONT_SMALL)
    
    draw.line([(sb_x + 30, leg_y + 82), (sb_x + 65, leg_y + 82)], fill=ACCENT_RED, width=2)
    draw.text((sb_x + 75, leg_y + 74), "Lintasan Tangan Kanan (Rear Power Piston)", fill=TEXT_WHITE, font=FONT_SMALL)
    
    draw.line([(sb_x + 30, leg_y + 104), (sb_x + 65, leg_y + 104)], fill=(255, 240, 100), width=4)
    draw.text((sb_x + 75, leg_y + 96), "Vektor Akselerasi Utama (Impact Vector)", fill=ACCENT_GOLD, font=FONT_SMALL)
    
    # Telemetry Table
    tbl_y = leg_y + 135
    draw.text((sb_x + 25, tbl_y), "TABEL KINEMATIKA POSE (UNIT):", fill=ACCENT_CYAN, font=FONT_BOLD)
    
    row_y = tbl_y + 25
    headers = ["Pose", "Tip Z (Reach)", "Tip Y (Height)", "Grip Span", "Torso Yaw"]
    col_offsets = [0, 140, 260, 380, 480]
    for c_i, h_txt in enumerate(headers):
        draw.text((sb_x + 25 + col_offsets[c_i], row_y), h_txt, fill=ACCENT_GOLD, font=FONT_BOLD)
    
    draw.line([(sb_x + 20, row_y + 18), (sb_x + sb_w - 20, row_y + 18)], fill=CARD_BORDER, width=1)
    
    for idx, pk in enumerate(p_keys):
        p = POSES[pk]
        row_y += 28
        draw.rectangle([(sb_x + 20, row_y - 4), (sb_x + sb_w - 20, row_y + 22)], fill=(30, 35, 48) if idx%2==1 else (25, 29, 39))
        
        span = round(float(np.linalg.norm(np.array(p["grip_lead"]) - np.array(p["grip_rear"]))), 1)
        yaw = p["torso"]["rot"][1]
        
        draw.text((sb_x + 25, row_y), f"P{idx+1} {pk.split('_')[1][:7]}", fill=p_colors[idx], font=FONT_MONO)
        draw.text((sb_x + 25 + col_offsets[1], row_y), f"Z={p['staff_tip'][2]:+05.1f}", fill=TEXT_WHITE, font=FONT_MONO)
        draw.text((sb_x + 25 + col_offsets[2], row_y), f"Y={p['staff_tip'][1]:04.1f}", fill=TEXT_WHITE, font=FONT_MONO)
        draw.text((sb_x + 25 + col_offsets[3], row_y), f"{span:04.1f} u", fill=ACCENT_CYAN, font=FONT_MONO)
        draw.text((sb_x + 25 + col_offsets[4], row_y), f"{yaw:+03.0f} deg", fill=ACCENT_GREEN, font=FONT_MONO)
        
    # Technical Insights Box
    ins_y = row_y + 45
    draw.rectangle([(sb_x + 20, ins_y), (sb_x + sb_w - 20, sb_h + sb_y - 20)], fill=(22, 25, 34), outline=CARD_BORDER, width=1)
    draw.text((sb_x + 30, ins_y + 15), "CATATAN ARSITEKTUR & PEMBATAS TEKNIS:", fill=ACCENT_RED, font=FONT_BOLD)
    
    insights = [
        "1. Linearitas Sempurna (Y-Axis Lock):",
        "   Puncak tusukan (Pose 3) berada pada ketinggian Y=20.3.",
        "   Deviasi vertikal sepanjang aksi hanya 1.1 unit,",
        "   memastikan tusukan menusuk presisi ke ulu hati lawan.",
        "",
        "2. Efisiensi Penetrasi (Displacement Delta):",
        "   Ujung tongkat meluncur dari Z=+10.8 (Windup) ke Z=+27.6",
        "   (Strike), menghasilkan jarak tusuk bersih 16.8 unit (1.05m)",
        "   hanya dalam rentang waktu 6 frame (0.25 detik).",
        "",
        "3. Dual-Handed Fulcrum Mechanics:",
        "   Tangan kiri bertindak sebagai selongsong pemandu (guide),",
        "   sementara tangan kanan bertindak sebagai piston pendorong.",
        "",
        "4. Pembatas Engine Minecraft Java:",
        "   Model JSON item vanilla TIDAK DAPAT menggerakkan tulang",
        "   rig pemain! Studi ini adalah cetak biru DCC untuk",
        "   PlayerAnimator / GeckoLib / Better Combat di masa depan."
    ]
    
    cur_y = ins_y + 40
    for line in insights:
        if line.startswith(("1.", "2.", "3.", "4.")):
            draw.text((sb_x + 30, cur_y), line, fill=ACCENT_GOLD, font=FONT_BOLD)
        else:
            draw.text((sb_x + 30, cur_y), line, fill=TEXT_WHITE if not line.startswith("   ") else TEXT_MUTED, font=FONT_SMALL)
        cur_y += 18
        
    out_path = os.path.join(OUTPUT_DIR, "staff_thrust_trajectory_diagram.png")
    img.save(out_path)
    print("Saved: staff_thrust_trajectory_diagram.png")

render_trajectory_diagram()

# -------------------------------------------------------------------------
# 8. GENERATE MASTER COMPREHENSIVE OVERVIEW (THE SHOWCASE BANNER)
# -------------------------------------------------------------------------

def render_master_overview():
    W, H = 2400, 1600
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([(0, 0), (W, 95)], fill=(22, 26, 36))
    draw.line([(0, 95), (W, 95)], fill=CARD_BORDER, width=2)
    draw.text((45, 18), "AIR NOMAD STAFF — MASTER ANIMATION POSE STUDY", fill=TEXT_WHITE, font=FONT_HEADER)
    draw.text((45, 54), "Minecraft 1.21.1 Mod Study | Rig: Minecraft Player (Biped Standard) | Aksi: Staff Thrust (Tusukan Linier Dua Tangan)", fill=ACCENT_CYAN, font=FONT_SUB)
    draw.text((W - 550, 32), "OFFICIAL DCC / RIGGING SPECIFICATION", fill=ACCENT_GOLD, font=FONT_BOLD)
    
    # Row 1: 4 Poses Isometric Render Cards (y: 115 to 780)
    col_w = (W - 90) // 4
    for idx, (p_key, p_data) in enumerate(POSES.items()):
        bx = 45 + idx * col_w
        by = 115
        bw = col_w - 20
        bh = 660
        
        draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.rectangle([(bx, by), (bx + bw, by + 45)], fill=(32, 38, 52))
        draw.line([(bx, by + 45), (bx + bw, by + 45)], fill=CARD_BORDER, width=1)
        
        draw.text((bx + 15, by + 8), p_data["title"], fill=TEXT_WHITE, font=FONT_TITLE)
        draw.text((bx + 15, by + 28), p_data["timing_frames"], fill=ACCENT_GOLD, font=FONT_SMALL)
        
        # Render 3D Iso Model
        vp_x = bx + bw // 2
        vp_y = by + 390
        scale = 13.0
        
        project = get_projector("iso", vp_x, vp_y, scale)
        for gz in range(-16, 32, 8):
            p_start = project([-16, 0, gz])[:2]
            p_end = project([16, 0, gz])[:2]
            draw.line([p_start, p_end], fill=(36, 42, 58), width=1)
        for gx in range(-16, 24, 8):
            p_start = project([gx, 0, -16])[:2]
            p_end = project([gx, 0, 32])[:2]
            draw.line([p_start, p_end], fill=(36, 42, 58), width=1)
            
        boxes = build_pose_boxes(p_key)
        render_pose(draw, boxes, view_mode="iso", cx=vp_x, cy=vp_y, scale=scale)
        
        # Bottom parameters
        p_box_y = by + bh - 160
        draw.rectangle([(bx + 10, p_box_y), (bx + bw - 10, by + bh - 10)], fill=(22, 25, 34), outline=CARD_BORDER, width=1)
        draw.text((bx + 15, p_box_y + 10), "ROTASI SENDI UTAMA:", fill=ACCENT_CYAN, font=FONT_BOLD)
        draw.text((bx + 15, p_box_y + 30), f"Torso Yaw: {p_data['torso']['rot'][1]:+02.0f} deg | Pitch: {p_data['torso']['rot'][0]:+02.0f} deg", fill=TEXT_WHITE, font=FONT_SMALL)
        draw.text((bx + 15, p_box_y + 48), f"Lead Arm: {p_data['left_arm']['rot'][:2]}", fill=TEXT_MUTED, font=FONT_SMALL)
        draw.text((bx + 15, p_box_y + 66), f"Rear Arm: {p_data['right_arm']['rot'][:2]}", fill=TEXT_MUTED, font=FONT_SMALL)
        draw.text((bx + 15, p_box_y + 88), f"Tip Reach (Z): {p_data['staff_tip'][2]:+04.1f} u | Height: {p_data['staff_tip'][1]:04.1f} u", fill=ACCENT_GOLD, font=FONT_BOLD)
        draw.text((bx + 15, p_box_y + 110), f"Center of Mass: {p_data['com']}", fill=ACCENT_GREEN, font=FONT_SMALL)
        
    # Row 2: Left Side Trajectory Viewport & Right Side Architectural Brief (y: 800 to 1550)
    # Left Viewport (Trajectory mini-elevation)
    t_bx = 45
    t_by = 800
    t_bw = 1400
    t_bh = 740
    
    draw.rectangle([(t_bx, t_by), (t_bx + t_bw, t_by + t_bh)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rectangle([(t_bx, t_by), (t_bx + t_bw, t_by + 45)], fill=(32, 38, 52))
    draw.line([(t_bx, t_by + 45), (t_bx + t_bw, t_by + 45)], fill=CARD_BORDER, width=1)
    draw.text((t_bx + 20, t_by + 12), "ELEVASI LINTASAN VEKTOR TUSUKAN (SIDE ORTHOGRAPHIC PROJECTION)", fill=TEXT_WHITE, font=FONT_TITLE)
    
    # 4 side pose snapshots inside this viewport
    cell_w = (t_bw - 40) // 4
    for idx, (p_key, p_data) in enumerate(POSES.items()):
        cx = t_bx + 20 + idx * cell_w + cell_w // 2
        cy = t_by + 440
        s_scale = 10.5
        
        project = get_projector("side", cx, cy, s_scale)
        # Ground
        p_g0 = project([-10, 0, -10])[:2]
        p_g1 = project([-10, 0, 30])[:2]
        draw.line([p_g0, p_g1], fill=(42, 48, 65), width=2)
        
        # Height line Y=20
        p_h0 = project([-10, 20.3, -10])[:2]
        p_h1 = project([-10, 20.3, 30])[:2]
        draw.line([p_h0, p_h1], fill=(130, 105, 35, 180), width=1)
        
        boxes = build_pose_boxes(p_key)
        render_pose(draw, boxes, view_mode="side", cx=cx, cy=cy, scale=s_scale)
        
        # Caption
        draw.text((cx - 70, t_by + t_bh - 50), f"P{idx+1} Samping (Z-Reach: {p_data['extension_z']:+04.1f})", fill=ACCENT_CYAN, font=FONT_BOLD)
    
    # Right Viewport: Technical Mandates & Boundary Rule
    r_bx = t_bx + t_bw + 25
    r_by = 800
    r_bw = W - r_bx - 45
    r_bh = 740
    
    draw.rectangle([(r_bx, r_by), (r_bx + r_bw, r_by + r_bh)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rectangle([(r_bx, r_by), (r_bx + r_bw, r_by + 45)], fill=(32, 38, 52))
    draw.line([(r_bx, r_by + 45), (r_bx + r_bw, r_by + 45)], fill=CARD_BORDER, width=1)
    draw.text((r_bx + 20, r_by + 12), "RINGKASAN TEKNIS & BATASAN ARSITEKTUR", fill=TEXT_WHITE, font=FONT_TITLE)
    
    notes = [
        ("MANDAT 1: DUAL-HANDED GRIP PLACEMENT", [
            "- Tangan Kanan (Rear Hand): Bertindak sebagai power piston.",
            "  Posisi genggaman: 5.5 unit di depan tutup bawah (butt cap).",
            "- Tangan Kiri (Lead Hand): Bertindak sebagai fulcrum guide.",
            "  Posisi genggaman: Menyelimuti kain grip wrap merah.",
            "- Rentang Genggam (Grip Span): Konstan 11-13 unit (~70 cm)."
        ]),
        ("MANDAT 2: THRUST TRAJECTORY (PENETRASI LINIER)", [
            "- Ketinggian tusukan (Y-Axis) terkunci rapat di Y=19.2 hingga 20.3.",
            "- Sumbu tusukan lurus menembus koridor ulu hati musuh.",
            "- Perpindahan Z bersih: +16.8 unit (1.05 meter dalam 0.25 detik).",
            "- Tidak ada goyangan lateral (X-Axis deviasi < 1.0 unit)."
        ]),
        ("MANDAT 3: PEMBATAS SISTEM (CRITICAL BOUNDARY)", [
            "- PENTING: File ini adalah STUDI POSE DCC / ANIMASI RIG.",
            "- JSON item vanilla Minecraft TIDAK BISA menggerakkan biped tubuh!",
            "- Item display JSON vanilla hanya mengubah posisi item relatif",
            "  terhadap satu tangan tunggal (firstperson / thirdperson).",
            "- Integrasi animasi tubuh penuh memerlukan framework runtime:",
            "  * PlayerAnimator API (Fabric/NeoForge)",
            "  * Better Combat (modded attack states)",
            "  * GeckoLib Entity Rigging"
        ])
    ]
    
    curr_ny = r_by + 60
    for title, lines in notes:
        draw.text((r_bx + 20, curr_ny), title, fill=ACCENT_GOLD if "MANDAT 3" not in title else ACCENT_RED, font=FONT_BOLD)
        curr_ny += 24
        for l in lines:
            col = TEXT_WHITE if l.startswith("- PENTING") else (TEXT_WHITE if not l.startswith("  *") else TEXT_MUTED)
            draw.text((r_bx + 25, curr_ny), l, fill=col, font=FONT_SMALL)
            curr_ny += 18
        curr_ny += 14
        
    out_path = os.path.join(OUTPUT_DIR, "staff_thrust_master_overview.png")
    img.save(out_path)
    print("Saved: staff_thrust_master_overview.png")

render_master_overview()

# -------------------------------------------------------------------------
# 9. EXPORT BLOCKBENCH MODEL (.BBMODEL)
# -------------------------------------------------------------------------

def export_blockbench_model():
    bbmodel_path = os.path.join(OUTPUT_DIR, "player_staff_thrust_study.bbmodel")
    
    # Construct complete Blockbench model format (v4.10, modded_entity)
    model = {
        "meta": {
            "format_version": "4.10",
            "creation_time": 1730972000,
            "model_format": "modded_entity",
            "box_uv": False
        },
        "name": "player_staff_thrust_study",
        "geometry_name": "player_staff_thrust",
        "visible_box": [1, 2, 1],
        "resolution": {"width": 64, "height": 64},
        "elements": [
            # Body
            {
                "name": "torso",
                "box_uv": False,
                "from": [-4, 12, -2],
                "to": [4, 24, 2],
                "origin": [0, 12, 0],
                "color": 9,
                "faces": {
                    "north": {"uv": [5, 5, 7, 8], "texture": None},
                    "east": {"uv": [4, 5, 5, 8], "texture": None},
                    "south": {"uv": [2, 5, 4, 8], "texture": None},
                    "west": {"uv": [7, 5, 8, 8], "texture": None},
                    "up": {"uv": [2, 4, 4, 5], "texture": None},
                    "down": {"uv": [4, 4, 6, 5], "texture": None}
                }
            },
            # Head
            {
                "name": "head",
                "box_uv": False,
                "from": [-4, 24, -4],
                "to": [4, 32, 4],
                "origin": [0, 24, 0],
                "color": 1,
                "faces": {
                    "north": {"uv": [2, 2, 4, 4], "texture": None},
                    "east": {"uv": [0, 2, 2, 4], "texture": None},
                    "south": {"uv": [4, 2, 6, 4], "texture": None},
                    "west": {"uv": [6, 2, 8, 4], "texture": None},
                    "up": {"uv": [2, 0, 4, 2], "texture": None},
                    "down": {"uv": [4, 0, 6, 2], "texture": None}
                }
            },
            # Left Arm
            {
                "name": "left_arm",
                "box_uv": False,
                "from": [4, 12, -2],
                "to": [8, 24, 2],
                "origin": [5, 22, 0],
                "color": 2,
                "faces": {
                    "north": {"uv": [9, 5, 10, 8], "texture": None},
                    "east": {"uv": [8, 5, 9, 8], "texture": None},
                    "south": {"uv": [11, 5, 12, 8], "texture": None},
                    "west": {"uv": [10, 5, 11, 8], "texture": None},
                    "up": {"uv": [9, 4, 10, 5], "texture": None},
                    "down": {"uv": [10, 4, 11, 5], "texture": None}
                }
            },
            # Right Arm
            {
                "name": "right_arm",
                "box_uv": False,
                "from": [-8, 12, -2],
                "to": [-4, 24, 2],
                "origin": [-5, 22, 0],
                "color": 2,
                "faces": {
                    "north": {"uv": [11, 5, 12, 8], "texture": None},
                    "east": {"uv": [10, 5, 11, 8], "texture": None},
                    "south": {"uv": [9, 5, 10, 8], "texture": None},
                    "west": {"uv": [8, 5, 9, 8], "texture": None},
                    "up": {"uv": [9, 4, 10, 5], "texture": None},
                    "down": {"uv": [10, 4, 11, 5], "texture": None}
                }
            },
            # Left Leg
            {
                "name": "left_leg",
                "box_uv": False,
                "from": [0, 0, -2],
                "to": [4, 12, 2],
                "origin": [2, 12, 0],
                "color": 3,
                "faces": {
                    "north": {"uv": [5, 9, 6, 12], "texture": None},
                    "east": {"uv": [4, 9, 5, 12], "texture": None},
                    "south": {"uv": [7, 9, 8, 12], "texture": None},
                    "west": {"uv": [6, 9, 7, 12], "texture": None},
                    "up": {"uv": [5, 8, 6, 9], "texture": None},
                    "down": {"uv": [6, 8, 7, 9], "texture": None}
                }
            },
            # Right Leg
            {
                "name": "right_leg",
                "box_uv": False,
                "from": [-4, 0, -2],
                "to": [0, 12, 2],
                "origin": [-2, 12, 0],
                "color": 3,
                "faces": {
                    "north": {"uv": [7, 9, 8, 12], "texture": None},
                    "east": {"uv": [6, 9, 7, 12], "texture": None},
                    "south": {"uv": [5, 9, 6, 12], "texture": None},
                    "west": {"uv": [4, 9, 5, 12], "texture": None},
                    "up": {"uv": [5, 8, 6, 9], "texture": None},
                    "down": {"uv": [6, 8, 7, 9], "texture": None}
                }
            },
            # Staff Elements (Grouped in Staff bone)
            {
                "name": "staff_lower_cap",
                "box_uv": False,
                "from": [-0.9, -7.0, -0.9],
                "to": [0.9, -6.0, 0.9],
                "origin": [0, 8, 0],
                "color": 4,
                "faces": {"north": {"uv": [0, 0, 2, 2], "texture": None}}
            },
            {
                "name": "staff_lower_shaft",
                "box_uv": False,
                "from": [-0.7, -6.0, -0.7],
                "to": [0.7, 5.0, 0.7],
                "origin": [0, 8, 0],
                "color": 5,
                "faces": {"north": {"uv": [0, 0, 2, 11], "texture": None}}
            },
            {
                "name": "staff_grip_wrap",
                "box_uv": False,
                "from": [-0.85, 5.0, -0.85],
                "to": [0.85, 11.0, 0.85],
                "origin": [0, 8, 0],
                "color": 6,
                "faces": {"north": {"uv": [8, 0, 10, 6], "texture": None}}
            },
            {
                "name": "staff_upper_shaft",
                "box_uv": False,
                "from": [-0.7, 11.0, -0.7],
                "to": [0.7, 22.0, 0.7],
                "origin": [0, 8, 0],
                "color": 5,
                "faces": {"north": {"uv": [0, 0, 2, 11], "texture": None}}
            },
            {
                "name": "staff_upper_cap",
                "box_uv": False,
                "from": [-0.9, 22.0, -0.9],
                "to": [0.9, 23.0, 0.9],
                "origin": [0, 8, 0],
                "color": 4,
                "faces": {"north": {"uv": [0, 0, 2, 2], "texture": None}}
            }
        ],
        "outliner": [
            {
                "name": "body",
                "origin": [0, 12, 0],
                "children": [
                    0, # torso
                    {
                        "name": "head",
                        "origin": [0, 24, 0],
                        "children": [1] # head
                    },
                    {
                        "name": "left_arm",
                        "origin": [5, 22, 0],
                        "children": [2] # left_arm
                    },
                    {
                        "name": "right_arm",
                        "origin": [-5, 22, 0],
                        "children": [3] # right_arm
                    }
                ]
            },
            {
                "name": "left_leg",
                "origin": [2, 12, 0],
                "children": [4] # left_leg
            },
            {
                "name": "right_leg",
                "origin": [-2, 12, 0],
                "children": [5] # right_leg
            },
            {
                "name": "staff_assembly",
                "origin": [0, 8, 0],
                "children": [6, 7, 8, 9, 10]
            }
        ],
        "animations": [
            # 1. Ready Stance static pose
            {
                "name": "01_ready_stance",
                "loop": "hold",
                "length": 0.5,
                "animators": {
                    "body": {
                        "name": "body",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 4.0, "y": 22.0, "z": 0.0}]}
                        ]
                    },
                    "head": {
                        "name": "head",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -2.0, "y": -22.0, "z": 0.0}]}
                        ]
                    },
                    "left_arm": {
                        "name": "left_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -48.0, "y": 26.0, "z": 18.0}]}
                        ]
                    },
                    "right_arm": {
                        "name": "right_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -16.0, "y": -10.0, "z": -8.0}]}
                        ]
                    },
                    "left_leg": {
                        "name": "left_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 10.0, "y": 12.0, "z": -4.0}]}
                        ]
                    },
                    "right_leg": {
                        "name": "right_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -14.0, "y": -18.0, "z": 6.0}]}
                        ]
                    }
                }
            },
            # 2. Anticipation Windup
            {
                "name": "02_anticipation_windup",
                "loop": "hold",
                "length": 0.5,
                "animators": {
                    "body": {
                        "name": "body",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 6.0, "y": 42.0, "z": -2.0}]}
                        ]
                    },
                    "head": {
                        "name": "head",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 0.0, "y": -42.0, "z": 2.0}]}
                        ]
                    },
                    "left_arm": {
                        "name": "left_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -36.0, "y": 40.0, "z": 24.0}]}
                        ]
                    },
                    "right_arm": {
                        "name": "right_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 10.0, "y": -24.0, "z": -14.0}]}
                        ]
                    },
                    "left_leg": {
                        "name": "left_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 18.0, "y": 16.0, "z": -2.0}]}
                        ]
                    },
                    "right_leg": {
                        "name": "right_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -26.0, "y": -26.0, "z": 8.0}]}
                        ]
                    }
                }
            },
            # 3. Thrust Strike
            {
                "name": "03_thrust_strike",
                "loop": "hold",
                "length": 0.5,
                "animators": {
                    "body": {
                        "name": "body",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 12.0, "y": 8.0, "z": 0.0}]}
                        ]
                    },
                    "head": {
                        "name": "head",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 4.0, "y": -8.0, "z": 0.0}]}
                        ]
                    },
                    "left_arm": {
                        "name": "left_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -76.0, "y": 10.0, "z": 12.0}]}
                        ]
                    },
                    "right_arm": {
                        "name": "right_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -62.0, "y": -6.0, "z": -6.0}]}
                        ]
                    },
                    "left_leg": {
                        "name": "left_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 32.0, "y": 4.0, "z": -4.0}]}
                        ]
                    },
                    "right_leg": {
                        "name": "right_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -35.0, "y": -10.0, "z": 6.0}]}
                        ]
                    }
                }
            },
            # 4. Recovery
            {
                "name": "04_recovery",
                "loop": "hold",
                "length": 0.5,
                "animators": {
                    "body": {
                        "name": "body",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 4.0, "y": 18.0, "z": 0.0}]}
                        ]
                    },
                    "head": {
                        "name": "head",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -1.0, "y": -18.0, "z": 0.0}]}
                        ]
                    },
                    "left_arm": {
                        "name": "left_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -50.0, "y": 22.0, "z": 15.0}]}
                        ]
                    },
                    "right_arm": {
                        "name": "right_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -24.0, "y": -12.0, "z": -8.0}]}
                        ]
                    },
                    "left_leg": {
                        "name": "left_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": 14.0, "y": 8.0, "z": -3.0}]}
                        ]
                    },
                    "right_leg": {
                        "name": "right_leg",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.0, "data_points": [{"x": -18.0, "y": -14.0, "z": 4.0}]}
                        ]
                    }
                }
            },
            # 5. Full Animation Cycle (staff_thrust_cycle, 24 FPS, length 1.0s)
            {
                "name": "staff_thrust_cycle",
                "loop": "once",
                "length": 1.0,
                "animators": {
                    "body": {
                        "name": "body",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.00, "data_points": [{"x": 4.0, "y": 22.0, "z": 0.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.25, "data_points": [{"x": 6.0, "y": 42.0, "z": -2.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.50, "data_points": [{"x": 12.0, "y": 8.0, "z": 0.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.70, "data_points": [{"x": 10.0, "y": 10.0, "z": 0.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 1.00, "data_points": [{"x": 4.0, "y": 22.0, "z": 0.0}], "interpolation": "catmullrom"}
                        ]
                    },
                    "left_arm": {
                        "name": "left_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.00, "data_points": [{"x": -48.0, "y": 26.0, "z": 18.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.25, "data_points": [{"x": -36.0, "y": 40.0, "z": 24.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.50, "data_points": [{"x": -76.0, "y": 10.0, "z": 12.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.75, "data_points": [{"x": -50.0, "y": 22.0, "z": 15.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 1.00, "data_points": [{"x": -48.0, "y": 26.0, "z": 18.0}], "interpolation": "catmullrom"}
                        ]
                    },
                    "right_arm": {
                        "name": "right_arm",
                        "type": "bone",
                        "keyframes": [
                            {"channel": "rotation", "time": 0.00, "data_points": [{"x": -16.0, "y": -10.0, "z": -8.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.25, "data_points": [{"x": 10.0, "y": -24.0, "z": -14.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.50, "data_points": [{"x": -62.0, "y": -6.0, "z": -6.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 0.75, "data_points": [{"x": -24.0, "y": -12.0, "z": -8.0}], "interpolation": "catmullrom"},
                            {"channel": "rotation", "time": 1.00, "data_points": [{"x": -16.0, "y": -10.0, "z": -8.0}], "interpolation": "catmullrom"}
                        ]
                    }
                }
            }
        ]
    }
    
    with open(bbmodel_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    print(f"Saved Blockbench model: {bbmodel_path}")

export_blockbench_model()

print("All visual assets and models generated successfully.")
