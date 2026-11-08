import json
import numpy as np
import math
import os
import shutil

from solve_ready_pose_ik import solve_2bone_ik, euler_from_matrix_zyx, rotation_matrix_zyx

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
BBMODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready.bbmodel")

# 1. Staff calculation
P_rear_grip = np.array([4.5, 14.0, 1.0])
P_lead_grip = np.array([1.5, 15.5, -4.5])

v_staff_raw = P_lead_grip - P_rear_grip
dist_grips = np.linalg.norm(v_staff_raw)
v_staff = v_staff_raw / dist_grips

u_rear = 13.0
u_lead = u_rear + dist_grips
P_butt = P_rear_grip - u_rear * v_staff
P_tip = P_butt + 30.0 * v_staff

v0 = np.array([0.0, 1.0, 0.0])
axis = np.cross(v0, v_staff)
axis = axis / np.linalg.norm(axis)
angle = math.acos(np.dot(v0, v_staff))
K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
R_staff = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
euler_staff = euler_from_matrix_zyx(R_staff)

# Wrist attachments
n_right = np.array([0.8, -0.2, 0.5])
n_right = n_right - np.dot(n_right, v_staff) * v_staff
n_right = n_right / np.linalg.norm(n_right)
W_rear = P_rear_grip + n_right * 1.5

n_left = np.array([-0.8, -0.4, -0.2])
n_left = n_left - np.dot(n_left, v_staff) * v_staff
n_left = n_left / np.linalg.norm(n_left)
W_lead = P_lead_grip + n_left * 1.5

# Shoulders
s_right = np.array([5.0, 22.0, 0.0])
s_left  = np.array([-5.0, 22.0, 0.0])

ik_rear = solve_2bone_ik(s_right, W_rear, pole_hint=np.array([1.0, -0.2, 0.5]))
ik_lead = solve_2bone_ik(s_left, W_lead, pole_hint=np.array([-1.0, -0.5, -0.2]))

# Read neutral bbmodel
with open(os.path.join(OUTPUT_DIR, "player_staff_thrust_neutral.bbmodel"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Update staff elements to be centered around butt [0, 0, 0] in local unrotated space:
staff_cube_defs = {
    "staff_lower_cap":   ([-1.0, 0.0, -1.0], [1.0, 1.0, 1.0]),
    "staff_lower_shaft": ([-0.75, 1.0, -0.75], [0.75, 12.0, 0.75]),
    "staff_grip_wrap":   ([-1.0, 12.0, -1.0], [1.0, 18.0, 1.0]),
    "staff_upper_shaft": ([-0.75, 18.0, -0.75], [0.75, 29.0, 0.75]),
    "staff_upper_cap":   ([-1.0, 29.0, -1.0], [1.0, 30.0, 1.0]),
}

for elem in data["elements"]:
    if elem["name"] in staff_cube_defs:
        f_box, t_box = staff_cube_defs[elem["name"]]
        elem["from"] = f_box
        elem["to"] = t_box
        elem["origin"] = [0.0, 0.0, 0.0]

# Update outliner groups
def update_group(groups):
    for g in groups:
        if g.get("name") == "right_upper_arm":
            g["rotation"] = [round(x, 4) for x in ik_rear["euler_upper"].tolist()]
        elif g.get("name") == "right_forearm":
            g["rotation"] = [round(x, 4) for x in ik_rear["euler_forearm"].tolist()]
        elif g.get("name") == "left_upper_arm":
            g["rotation"] = [round(x, 4) for x in ik_lead["euler_upper"].tolist()]
        elif g.get("name") == "left_forearm":
            g["rotation"] = [round(x, 4) for x in ik_lead["euler_forearm"].tolist()]
        elif g.get("name") == "staff_assembly":
            g["origin"] = [round(x, 4) for x in P_butt.tolist()]
            g["rotation"] = [round(x, 4) for x in euler_staff.tolist()]
        
        # Recurse children
        if "children" in g:
            subgroups = [c for c in g["children"] if isinstance(c, dict)]
            update_group(subgroups)

update_group(data["outliner"])

# Update colors for clear leg & arm distinction:
for elem in data["elements"]:
    if elem["name"] == "right_leg":
        elem["color"] = 7 # blue
    elif elem["name"] == "left_leg":
        elem["color"] = 8 # purple / dark cyan
    elif elem["name"] == "right_upper_arm":
        elem["color"] = 3
    elif elem["name"] == "right_forearm":
        elem["color"] = 4
    elif elem["name"] == "left_upper_arm":
        elem["color"] = 5
    elif elem["name"] == "left_forearm":
        elem["color"] = 6

with open(BBMODEL_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated clean ready pose model: {BBMODEL_PATH}")
