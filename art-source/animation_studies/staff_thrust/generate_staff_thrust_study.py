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
    # Minecraft convention: Yaw (Y) -> Pitch (X) -> Roll (Z)
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
BG_DARK = (20, 22, 28)
CARD_BG = (28, 32, 42)
CARD_BORDER = (46, 54, 72)
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
        "desc": "Kuda-kuda serang seimbang (Zhan Zhuang/Bo Stance). Tubuh menyudut 22 deg, ujung tongkat membidik dada lawan.",
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

# Compute staff tips and butt coordinates dynamically
for p_key, p_data in POSES.items():
    rear = np.array(p_data["grip_rear"], dtype=float)
    lead = np.array(p_data["grip_lead"], dtype=float)
    diff = lead - rear
    dist = np.linalg.norm(diff)
    dir_v = diff / dist
    
    butt = rear - dir_v * p_data["butt_offset"]
    tip = lead + dir_v * p_data["tip_offset"]
    
    p_data["staff_butt"] = [round(x, 2) for x in butt]
    p_data["staff_tip"] = [round(x, 2) for x in tip]
    p_data["staff_length"] = round(dist + p_data["butt_offset"] + p_data["tip_offset"], 2)
    p_data["thrust_height"] = round(tip[1], 2)
    p_data["extension_z"] = round(tip[2], 2)

print("Pose kinematics computed successfully.")

# Save pose data JSON
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
    # Torso pivot is at waist (0, 0, 0) relative to root
    M_torso = M_root @ M_torso_rot
    
    # Torso cube: [-4, 0, -2] to [4, 12, 2]
    # Shirt chest / abdomen
    b_torso = make_box([-4, 0, -2], [4, 12, 2], C_SHIRT, "torso")
    # Apply M_torso
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
    
    # Hair cap: [-4.2, 3.8, -4.2] to [4.2, 8.2, 4.2]
    b_hair = make_box([-4.1, 4.0, -4.1], [4.1, 8.2, 4.1], C_HAIR, "hair")
    b_hair["world_vertices"] = np.array([transform_point(M_head, v) for v in b_hair["vertices"]])
    boxes.append(b_hair)
    
    # Left Arm
    la_rot = p["left_arm"]["rot"]
    la_piv = p["left_arm"]["pivot"]
    M_la_pivot = translate(la_piv[0], la_piv[1] - 12.0, la_piv[2])
    M_la_rot = euler_matrix(la_rot[0], la_rot[1], la_rot[2])
    M_la = M_torso @ M_la_pivot @ M_la_rot
    
    # Upper sleeve: [-1, -4, -2] to [3, 0, 2]
    b_la_sleeve = make_box([-1, -4, -2], [3, 0, 2], C_SHIRT, "left_sleeve")
    b_la_sleeve["world_vertices"] = np.array([transform_point(M_la, v) for v in b_la_sleeve["vertices"]])
    boxes.append(b_la_sleeve)
    # Forearm & hand: [-1, -12, -2] to [3, -4, 2]
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
    
    # ---------------------------------------------------------------------
    # STAFF GEOMETRY (Air Nomad Staff)
    # ---------------------------------------------------------------------
    butt = np.array(p["staff_butt"])
    tip = np.array(p["staff_tip"])
    staff_vec = tip - butt
    staff_len = np.linalg.norm(staff_vec)
    dir_staff = staff_vec / staff_len
    
    # Build transformation matrix that maps [0, 0, 0] to butt, aligned with dir_staff
    R_staff = align_vector_matrix(dir_staff)
    M_staff = translate(butt[0], butt[1], butt[2]) @ R_staff
    
    # Staff segments along local Y (0 to staff_len):
    # 1. Lower Cap (Brass): length 1.0, width 1.8 x 1.8
    b_scap_lo = make_box([-0.9, 0.0, -0.9], [0.9, 1.0, 0.9], C_STAFF_CAP, "staff_lower_cap")
    b_scap_lo["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_scap_lo["vertices"]])
    boxes.append(b_scap_lo)
    
    # 2. Lower Shaft (Wood): length 9.5, width 1.4 x 1.4
    b_sshaft_lo = make_box([-0.7, 1.0, -0.7], [0.7, 10.5, 0.7], C_STAFF_WOOD, "staff_lower_shaft")
    b_sshaft_lo["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_sshaft_lo["vertices"]])
    boxes.append(b_sshaft_lo)
    
    # 3. Grip Wrap (Crimson Wrap): length 6.0, width 1.7 x 1.7 (Around lead grip area)
    # The lead hand is at offset `p["butt_offset"] + dist` = staff_len - p["tip_offset"]
    lead_offset = staff_len - p["tip_offset"]
    b_swrap = make_box([-0.85, lead_offset - 3.0, -0.85], [0.85, lead_offset + 3.0, 0.85], C_STAFF_WRAP, "staff_wrap")
    b_swrap["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_swrap["vertices"]])
    boxes.append(b_swrap)
    
    # 4. Upper Shaft (Wood): from wrap to near tip
    b_sshaft_hi = make_box([-0.7, lead_offset + 3.0, -0.7], [0.7, staff_len - 1.0, 0.7], C_STAFF_WOOD, "staff_upper_shaft")
    b_sshaft_hi["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_sshaft_hi["vertices"]])
    boxes.append(b_sshaft_hi)
    
    # 5. Upper Cap (Brass): length 1.0, width 1.8 x 1.8
    b_scap_hi = make_box([-0.9, staff_len - 1.0, -0.9], [0.9, staff_len, 0.9], C_STAFF_CAP, "staff_upper_cap")
    b_scap_hi["world_vertices"] = np.array([transform_point(M_staff, v) for v in b_scap_hi["vertices"]])
    boxes.append(b_scap_hi)
    
    return boxes

# -------------------------------------------------------------------------
# 5. 3D RENDERING PIPELINE (ORTHOGRAPHIC & ISOMETRIC)
# -------------------------------------------------------------------------

def render_scene(draw, boxes, view_mode="iso", cx=300, cy=350, scale=12.0, ground_y=0.0):
    # Lighting setup
    if view_mode == "iso":
        L_key = np.array([0.5, 0.8, -0.3])
        L_fill = np.array([-0.6, 0.3, 0.6])
    elif view_mode == "front":
        L_key = np.array([0.3, 0.7, -0.6])
        L_fill = np.array([-0.4, 0.2, -0.8])
    else: # side
        L_key = np.array([-0.6, 0.7, 0.3])
        L_fill = np.array([0.5, 0.2, -0.4])
    
    L_key = L_key / np.linalg.norm(L_key)
    L_fill = L_fill / np.linalg.norm(L_fill)
    
    # Projection functions
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    
    def project(pt):
        x, y, z = pt
        if view_mode == "front":
            # Looking towards +Z (Steve facing viewer)
            # Front of Steve is facing +Z, so +Z faces camera!
            px = cx - x * scale
            py = cy - y * scale
            depth = z
        elif view_mode == "side":
            # Looking from right side (-X looking towards +X)
            # Z is horizontal (right on screen), Y is vertical
            px = cx + z * scale
            py = cy - y * scale
            depth = -x
        else: # Isometric
            # Iso view: 3/4 front-right perspective
            # Camera angled 30 degrees down, 45 degrees yaw
            iso_x = cx + (z - x) * scale * cos30
            iso_y = cy - y * scale + (x + z) * scale * sin30 * 0.5
            depth = x + z
            px, py = iso_x, iso_y
        return (px, py, depth)
    
    # Collect all faces across all boxes
    all_faces = []
    for b in boxes:
        verts = b["world_vertices"]
        for face_indices, norm_local, face_name in b["faces"]:
            poly_3d = verts[face_indices]
            
            # Compute world normal
            v0 = poly_3d[1] - poly_3d[0]
            v1 = poly_3d[2] - poly_3d[0]
            norm_world = np.cross(v0, v1)
            n_len = np.linalg.norm(norm_world)
            if n_len > 1e-6:
                norm_world = norm_world / n_len
            else:
                norm_world = np.array([0, 1, 0])
            
            # Centroid
            centroid = np.mean(poly_3d, axis=0)
            proj_centroid = project(centroid)
            
            # Projected 2D polygon
            poly_2d = [project(p)[:2] for p in poly_3d]
            
            # Backface culling check
            # For 2D screen polygon winding: signed area
            area = 0.0
            for i in range(len(poly_2d)):
                p1 = poly_2d[i]
                p2 = poly_2d[(i + 1) % len(poly_2d)]
                area += (p2[0] - p1[0]) * (p2[1] + p1[1])
            
            # If area is positive or negative depending on view, or just depth sort
            # Shading calculation
            dot_key = max(0.0, float(np.dot(norm_world, L_key)))
            dot_fill = max(0.0, float(np.dot(norm_world, L_fill)))
            intensity = 0.38 + 0.52 * dot_key + 0.18 * dot_fill
            
            # Base color
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
    
    # Sort faces from back to front (Painter's algorithm)
    # Higher depth means further away or closer depending on view mode
    if view_mode == "front":
        all_faces.sort(key=lambda f: f["depth"]) # Lower Z is back (-Z), higher Z is front (+Z)
    elif view_mode == "side":
        all_faces.sort(key=lambda f: f["depth"]) # -x is closer
    else:
        all_faces.sort(key=lambda f: f["depth"])
        
    for f in all_faces:
        draw.polygon(f["poly_2d"], fill=f["color"], outline=(30, 32, 40, 180))
        
    return project

print("Rendering engine compiled.")
