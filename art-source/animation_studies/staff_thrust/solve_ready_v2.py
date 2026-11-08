import numpy as np
import math
import json
import os
import shutil

from solve_ready_pose_ik import solve_2bone_ik, euler_from_matrix_zyx, rotation_matrix_zyx

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
NEUTRAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_neutral.bbmodel")
READY_V2_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready_v2.bbmodel")

# 1. Torso stance
# Torso origin is [0, 12, 0].
# Turned slightly sideways: Yaw Y = 15 deg.
torso_yaw_deg = 15.0
torso_pitch_deg = 0.0
torso_roll_deg = 0.0

R_torso = rotation_matrix_zyx(torso_pitch_deg, torso_yaw_deg, torso_roll_deg)
torso_pivot = np.array([0.0, 12.0, 0.0])

# Shoulders in torso local space:
# Right shoulder: [5, 10, 0] relative to torso origin [0, 12, 0] -> world [5, 22, 0] in neutral
s_ru_local = np.array([5.0, 10.0, 0.0])
s_lu_local = np.array([-5.0, 10.0, 0.0])

s_right_world = torso_pivot + R_torso @ s_ru_local
s_left_world  = torso_pivot + R_torso @ s_lu_local

print(f"Torso Yaw: {torso_yaw_deg} deg")
print(f"Right Shoulder World: {s_right_world.tolist()}")
print(f"Left Shoulder World : {s_left_world.tolist()}")

# 2. Staff Stance (Diagonal across waist / lower chest):
# Rear hand near right hip / waist:
P_rear_grip = np.array([4.8, 12.5, 0.5])
# Front hand guiding at lower chest / abdomen:
P_lead_grip = np.array([1.2, 14.5, -4.8])

v_staff_raw = P_lead_grip - P_rear_grip
dist_grips = np.linalg.norm(v_staff_raw)
v_staff = v_staff_raw / dist_grips

u_rear = 13.0 # On grip wrap
u_lead = u_rear + dist_grips # ~19.67, on lower shaft
P_butt = P_rear_grip - u_rear * v_staff
P_tip = P_butt + 30.0 * v_staff

v0 = np.array([0.0, 1.0, 0.0])
axis = np.cross(v0, v_staff)
axis = axis / np.linalg.norm(axis)
angle = math.acos(np.dot(v0, v_staff))
K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
R_staff = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
euler_staff = euler_from_matrix_zyx(R_staff)

print(f"\nStaff:")
print(f"  Butt: {P_butt.tolist()}")
print(f"  Rear Grip: {P_rear_grip.tolist()} (u={u_rear})")
print(f"  Lead Grip: {P_lead_grip.tolist()} (u={u_lead:.3f})")
print(f"  Tip : {P_tip.tolist()}")
print(f"  Euler (ZYX): {euler_staff.tolist()}")

# 3. Hand Attachment Targets:
# Right hand wraps around staff from outside (+X, +Z):
n_right = np.array([0.9, -0.1, 0.4])
n_right = n_right - np.dot(n_right, v_staff) * v_staff
n_right = n_right / np.linalg.norm(n_right)
W_rear = P_rear_grip + n_right * 1.5

# Left hand wraps around staff from underneath / left (-X, -Y):
n_left = np.array([-0.7, -0.6, -0.3])
n_left = n_left - np.dot(n_left, v_staff) * v_staff
n_left = n_left / np.linalg.norm(n_left)
W_lead = P_lead_grip + n_left * 1.5

# Check reaches from shoulders to wrists:
d_rear = np.linalg.norm(W_rear - s_right_world)
d_lead = np.linalg.norm(W_lead - s_left_world)
print(f"\nArm reach required:")
print(f"  Right Arm: {d_rear:.3f} u (Max: 12.0u, elbow bent comfortably)")
print(f"  Left Arm : {d_lead:.3f} u (Max: 12.0u, elbow bent comfortably)")

# Solve IK for arms (in world space, then convert upper arm to torso local space):
ik_rear = solve_2bone_ik(s_right_world, W_rear, pole_hint=np.array([1.0, -0.3, 0.3]))
ik_lead = solve_2bone_ik(s_left_world, W_lead, pole_hint=np.array([-1.0, -0.5, -0.3]))

# In Blockbench hierarchy:
# torso -> right_upper_arm -> right_forearm
# R_upper_world = R_torso @ R_upper_local => R_upper_local = R_torso.T @ R_upper_world
R_ru_local = R_torso.T @ ik_rear['R_upper']
euler_ru = euler_from_matrix_zyx(R_ru_local)
euler_rf = ik_rear['euler_forearm'] # forearm is already local to upper arm

R_lu_local = R_torso.T @ ik_lead['R_upper']
euler_lu = euler_from_matrix_zyx(R_lu_local)
euler_lf = ik_lead['euler_forearm']

print(f"\nRight Arm Euler Local:")
print(f"  Upper Arm: {euler_ru.tolist()}")
print(f"  Forearm  : {euler_rf.tolist()}")

print(f"\nLeft Arm Euler Local:")
print(f"  Upper Arm: {euler_lu.tolist()}")
print(f"  Forearm  : {euler_lf.tolist()}")

# 4. Legs Stance:
# Left leg stepped forward slightly (lead leg):
# right_leg: origin [2, 12, 0], slight back angle: pitch X = +12 deg
# left_leg : origin [-2, 12, 0], slight forward angle: pitch X = -12 deg, yaw = 10 deg
euler_rleg = [12.0, 0.0, 0.0]
euler_lleg = [-12.0, 10.0, 0.0]

# 5. Build bbmodel
with open(NEUTRAL_MODEL_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Update staff elements in local unrotated space:
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
    elif elem["name"] == "right_leg":
        elem["color"] = 7
    elif elem["name"] == "left_leg":
        elem["color"] = 8
    elif elem["name"] == "right_upper_arm":
        elem["color"] = 3
    elif elem["name"] == "right_forearm":
        elem["color"] = 4
    elif elem["name"] == "left_upper_arm":
        elem["color"] = 5
    elif elem["name"] == "left_forearm":
        elem["color"] = 6

def update_group(groups):
    for g in groups:
        if g.get("name") == "torso":
            g["rotation"] = [round(torso_pitch_deg, 4), round(torso_yaw_deg, 4), round(torso_roll_deg, 4)]
        elif g.get("name") == "right_upper_arm":
            g["rotation"] = [round(x, 4) for x in euler_ru.tolist()]
        elif g.get("name") == "right_forearm":
            g["rotation"] = [round(x, 4) for x in euler_rf.tolist()]
        elif g.get("name") == "left_upper_arm":
            g["rotation"] = [round(x, 4) for x in euler_lu.tolist()]
        elif g.get("name") == "left_forearm":
            g["rotation"] = [round(x, 4) for x in euler_lf.tolist()]
        elif g.get("name") == "right_leg":
            g["rotation"] = euler_rleg
        elif g.get("name") == "left_leg":
            g["rotation"] = euler_lleg
        elif g.get("name") == "staff_assembly":
            g["origin"] = [round(x, 4) for x in P_butt.tolist()]
            g["rotation"] = [round(x, 4) for x in euler_staff.tolist()]
        
        if "children" in g:
            subgroups = [c for c in g["children"] if isinstance(c, dict)]
            update_group(subgroups)

update_group(data["outliner"])

data["name"] = "player_staff_thrust_ready_v2"

with open(READY_V2_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"\nGenerated Ready Pose v2 model: {READY_V2_PATH}")
