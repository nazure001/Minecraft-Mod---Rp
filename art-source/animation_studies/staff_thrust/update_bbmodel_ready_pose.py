import os
import json
import math
import numpy as np

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
BBMODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_rigged.bbmodel")

# -------------------------------------------------------------------------
# 1. RIGID KINEMATIC GEOMETRY IN WORLD SPACE
# -------------------------------------------------------------------------
# Shoulder pivots in Minecraft Blockbench (model facing -Z):
# Right shoulder: S_R = [+5, 22, 0] (+X is model's right)
# Left shoulder:  S_L = [-5, 22, 0] (-X is model's left)
S_R = np.array([5.0, 22.0, 0.0])
S_L = np.array([-5.0, 22.0, 0.0])

# Staff Placement:
# Butt cap: P_b = [6.5, 12.5, 6.0]
# Direction vector: v_dir = [-0.2503884, 0.40062145, -0.88136718]
# Staff length: exactly 30.0 units
P_b = np.array([6.5, 12.5, 6.0])
v_dir = np.array([-0.2503884, 0.40062145, -0.88136718])
v_dir = v_dir / np.linalg.norm(v_dir)

# Target attachments along staff:
# u_R = 4.0 (right hand holds lower shaft at 4 units from butt)
# u_L = 12.5 (left hand holds crimson wrap at 12.5 units from butt)
u_R = 4.0
u_L = 12.5

T_R = P_b + v_dir * u_R
T_L = P_b + v_dir * u_L

# Elbow positions (analytical law of cosines with upper=6.0, lower=6.0):
def solve_elbow(S, T, L1=6.0, L2=6.0, hint=[0, -1, 0]):
    S = np.array(S, dtype=float)
    T = np.array(T, dtype=float)
    d_vec = T - S
    d = np.linalg.norm(d_vec)
    d_dir = d_vec / d
    cos_a = (L1**2 + d**2 - L2**2) / (2.0 * L1 * d)
    cos_a = max(-1.0, min(1.0, cos_a))
    angle_a = math.acos(cos_a)
    h = np.array(hint, dtype=float)
    h_proj = h - np.dot(h, d_dir) * d_dir
    h_perp = h_proj / np.linalg.norm(h_proj)
    elbow = S + d_dir * (L1 * math.cos(angle_a)) + h_perp * (L1 * math.sin(angle_a))
    return elbow

E_R = solve_elbow(S_R, T_R, hint=[1.0, -0.2, 0.5])
E_L = solve_elbow(S_L, T_L, hint=[-0.5, -1.0, -0.5])

# Calculate distances and errors
d_R = float(np.linalg.norm(T_R - S_R))
d_L = float(np.linalg.norm(T_L - S_L))
print(f"Right reach: {d_R:.3f}u / 12.0u (max)")
print(f"Left reach:  {d_L:.3f}u / 12.0u (max)")

# -------------------------------------------------------------------------
# 2. HELPER TO CREATE ORIENTED CUBOIDS ALONG A 3D SEGMENT
# -------------------------------------------------------------------------
def make_segment_cube(p1, p2, thickness_x, thickness_z, name, color, uv_offset=[0,0]):
    # p1 is start, p2 is end
    # We create a cube whose origin is at p1, pointing along (p2 - p1)
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    vec = p2 - p1
    length = float(np.linalg.norm(vec))
    v = vec / length
    
    # Rotation angles to orient [0, -length, 0] to vec (for arms) or [0, length, 0] to vec (for staff)
    # Pitch (around X), Yaw (around Y), Roll (around Z)
    # Using atan2:
    # Pitch: angle in YZ plane
    pitch = math.degrees(math.atan2(-v[2], v[1])) - 90.0
    yaw = math.degrees(math.atan2(v[0], -v[2]))
    
    # We will orient using Blockbench rotation on the cube itself:
    hx = thickness_x / 2.0
    hz = thickness_z / 2.0
    
    cube = {
        "name": name,
        "box_uv": False,
        "from": [round(p1[0] - hx, 2), round(p1[1], 2), round(p1[2] - hz, 2)],
        "to": [round(p1[0] + hx, 2), round(p1[1] + length, 2), round(p1[2] + hz, 2)],
        "origin": [round(p1[0], 2), round(p1[1], 2), round(p1[2], 2)],
        "rotation": [round(pitch, 1), round(yaw, 1), 0.0],
        "color": color,
        "faces": {
            "north": {"uv": [0, 0, 4, 8], "texture": None},
            "east": {"uv": [0, 0, 4, 8], "texture": None},
            "south": {"uv": [0, 0, 4, 8], "texture": None},
            "west": {"uv": [0, 0, 4, 8], "texture": None},
            "up": {"uv": [0, 0, 4, 4], "texture": None},
            "down": {"uv": [0, 0, 4, 4], "texture": None}
        }
    }
    return cube

# -------------------------------------------------------------------------
# 3. BUILD BLOCKBENCH MODEL FOR THE SINGLE READY POSE
# -------------------------------------------------------------------------
# Staff rotation angles:
# Staff vector is v_dir: [-0.2503884, 0.40062145, -0.88136718]
# Staff default local axis is Y: [0, 1, 0]
v_s = v_dir / np.linalg.norm(v_dir)
staff_pitch = math.degrees(math.atan2(-v_s[2], v_s[1])) - 90.0
staff_yaw = math.degrees(math.atan2(v_s[0], -v_s[2]))

print(f"Staff pitch: {staff_pitch:.2f}, yaw: {staff_yaw:.2f}")

# Staff cubes (local to staff origin at P_b):
# P_b is [6.5, 12.5, 6.0]
# Cubes relative to P_b along local Y:
# 1. lower_cap: Y from 0 to 1 (size 2.0x2.0)
# 2. lower_shaft: Y from 1 to 12 (size 1.5x1.5)
# 3. grip_wrap: Y from 12 to 18 (size 2.0x2.0)
# 4. upper_shaft: Y from 18 to 29 (size 1.5x1.5)
# 5. upper_cap: Y from 29 to 30 (size 2.0x2.0)

# Arms:
# Right upper arm: S_R to E_R
# S_R = [5, 22, 0], E_R = [9.23, 18.79, 2.79]
v_ru = (E_R - S_R) / 6.0
ru_pitch = math.degrees(math.atan2(-v_ru[2], -v_ru[1]))
ru_yaw = math.degrees(math.atan2(v_ru[0], math.sqrt(v_ru[1]**2 + v_ru[2]**2)))

# Right forearm: E_R to T_R
# E_R = [9.23, 18.79, 2.79], T_R = [5.50, 14.10, 2.47]
v_rf = (T_R - E_R) / 6.0
rf_pitch = math.degrees(math.atan2(-v_rf[2], -v_rf[1]))
rf_yaw = math.degrees(math.atan2(v_rf[0], math.sqrt(v_rf[1]**2 + v_rf[2]**2)))

# Left upper arm: S_L to E_L
# S_L = [-5, 22, 0], E_L = [-2.39, 17.76, -3.35]
v_lu = (E_L - S_L) / 6.0
lu_pitch = math.degrees(math.atan2(-v_lu[2], -v_lu[1]))
lu_yaw = math.degrees(math.atan2(v_lu[0], math.sqrt(v_lu[1]**2 + v_lu[2]**2)))

# Left forearm: E_L to T_L
# E_L = [-2.39, 17.76, -3.35], T_L = [3.37, 17.51, -5.02]
v_lf = (T_L - E_L) / 6.0
lf_pitch = math.degrees(math.atan2(-v_lf[2], -v_lf[1]))
lf_yaw = math.degrees(math.atan2(v_lf[0], math.sqrt(v_lf[1]**2 + v_lf[2]**2)))

# Build elements
elements = [
    # 0: Torso (centered [0, 12, 0])
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
    # 1: Head
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
    # 2: Right Upper Arm (Pivot S_R=[5, 22, 0])
    {
        "name": "right_upper_arm",
        "box_uv": False,
        "from": [3, 16, -2],
        "to": [7, 22, 2],
        "origin": [5, 22, 0],
        "rotation": [round(ru_pitch, 1), round(ru_yaw, 1), 0.0],
        "color": 2,
        "faces": {"north": {"uv": [0, 0, 4, 6], "texture": None}}
    },
    # 3: Right Forearm (Pivot E_R=[9.23, 18.79, 2.79])
    {
        "name": "right_forearm",
        "box_uv": False,
        "from": [round(E_R[0] - 2), round(E_R[1] - 6), round(E_R[2] - 2)],
        "to": [round(E_R[0] + 2), round(E_R[1]), round(E_R[2] + 2)],
        "origin": [round(E_R[0], 2), round(E_R[1], 2), round(E_R[2], 2)],
        "rotation": [round(rf_pitch, 1), round(rf_yaw, 1), 0.0],
        "color": 3,
        "faces": {"north": {"uv": [0, 0, 4, 6], "texture": None}}
    },
    # 4: Left Upper Arm (Pivot S_L=[-5, 22, 0])
    {
        "name": "left_upper_arm",
        "box_uv": False,
        "from": [-7, 16, -2],
        "to": [-3, 22, 2],
        "origin": [-5, 22, 0],
        "rotation": [round(lu_pitch, 1), round(lu_yaw, 1), 0.0],
        "color": 2,
        "faces": {"north": {"uv": [0, 0, 4, 6], "texture": None}}
    },
    # 5: Left Forearm (Pivot E_L=[-2.39, 17.76, -3.35])
    {
        "name": "left_forearm",
        "box_uv": False,
        "from": [round(E_L[0] - 2), round(E_L[1] - 6), round(E_L[2] - 2)],
        "to": [round(E_L[0] + 2), round(E_L[1]), round(E_L[2] + 2)],
        "origin": [round(E_L[0], 2), round(E_L[1], 2), round(E_L[2], 2)],
        "rotation": [round(lf_pitch, 1), round(lf_yaw, 1), 0.0],
        "color": 3,
        "faces": {"north": {"uv": [0, 0, 4, 6], "texture": None}}
    },
    # 6: Right Leg
    {
        "name": "right_leg",
        "box_uv": False,
        "from": [0, 0, -2],
        "to": [4, 12, 2],
        "origin": [2, 12, 0],
        "color": 7,
        "faces": {}
    },
    # 7: Left Leg
    {
        "name": "left_leg",
        "box_uv": False,
        "from": [-4, 0, -2],
        "to": [0, 12, 2],
        "origin": [-2, 12, 0],
        "color": 7,
        "faces": {}
    },
    # Staff Cubes (Parented to staff_assembly bone with pivot at P_b=[6.5, 12.5, 6.0])
    # 8: lower_cap (u: 0..1)
    {
        "name": "lower_cap",
        "box_uv": False,
        "from": [5.5, 12.5, 5.0],
        "to": [7.5, 13.5, 7.0],
        "origin": [6.5, 12.5, 6.0],
        "color": 4,
        "faces": {"north": {"uv": [0, 0, 2, 1], "texture": None}}
    },
    # 9: lower_shaft (u: 1..12)
    {
        "name": "lower_shaft",
        "box_uv": False,
        "from": [5.75, 13.5, 5.25],
        "to": [7.25, 24.5, 6.75],
        "origin": [6.5, 12.5, 6.0],
        "color": 5,
        "faces": {"north": {"uv": [0, 0, 2, 11], "texture": None}}
    },
    # 10: grip_wrap (u: 12..18)
    {
        "name": "grip_wrap",
        "box_uv": False,
        "from": [5.5, 24.5, 5.0],
        "to": [7.5, 30.5, 7.0],
        "origin": [6.5, 12.5, 6.0],
        "color": 6,
        "faces": {"north": {"uv": [0, 0, 2, 6], "texture": None}}
    },
    # 11: upper_shaft (u: 18..29)
    {
        "name": "upper_shaft",
        "box_uv": False,
        "from": [5.75, 30.5, 5.25],
        "to": [7.25, 41.5, 6.75],
        "origin": [6.5, 12.5, 6.0],
        "color": 5,
        "faces": {"north": {"uv": [0, 0, 2, 11], "texture": None}}
    },
    # 12: upper_cap (u: 29..30)
    {
        "name": "upper_cap",
        "box_uv": False,
        "from": [5.5, 41.5, 5.0],
        "to": [7.5, 42.5, 7.0],
        "origin": [6.5, 12.5, 6.0],
        "color": 4,
        "faces": {"north": {"uv": [0, 0, 2, 1], "texture": None}}
    }
]

# Outliner structure:
outliner = [
    {
        "name": "torso",
        "origin": [0, 12, 0],
        "children": [
            0,
            {"name": "head", "origin": [0, 24, 0], "children": [1]},
            {
                "name": "right_upper_arm",
                "origin": [5, 22, 0],
                "rotation": [round(ru_pitch, 1), round(ru_yaw, 1), 0.0],
                "children": [
                    2,
                    {
                        "name": "right_forearm",
                        "origin": [round(E_R[0], 2), round(E_R[1], 2), round(E_R[2], 2)],
                        "rotation": [round(rf_pitch, 1), round(rf_yaw, 1), 0.0],
                        "children": [3]
                    }
                ]
            },
            {
                "name": "left_upper_arm",
                "origin": [-5, 22, 0],
                "rotation": [round(lu_pitch, 1), round(lu_yaw, 1), 0.0],
                "children": [
                    4,
                    {
                        "name": "left_forearm",
                        "origin": [round(E_L[0], 2), round(E_L[1], 2), round(E_L[2], 2)],
                        "rotation": [round(lf_pitch, 1), round(lf_yaw, 1), 0.0],
                        "children": [5]
                    }
                ]
            }
        ]
    },
    {"name": "right_leg", "origin": [2, 12, 0], "children": [6]},
    {"name": "left_leg", "origin": [-2, 12, 0], "children": [7]},
    {
        "name": "staff_assembly",
        "origin": [6.5, 12.5, 6.0],
        "rotation": [round(staff_pitch, 1), round(staff_yaw, 1), 0.0],
        "children": [8, 9, 10, 11, 12]
    }
]

bb_model = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730976000,
        "model_format": "modded_entity",
        "box_uv": False
    },
    "name": "player_staff_thrust_rigged",
    "geometry_name": "player_staff_thrust",
    "visible_box": [2, 3, 2],
    "resolution": {"width": 64, "height": 64},
    "elements": elements,
    "outliner": outliner,
    "animations": []
}

with open(BBMODEL_PATH, "w", encoding="utf-8") as f:
    json.dump(bb_model, f, indent=2)

print("Saved player_staff_thrust_rigged.bbmodel with exact ready pose!")
