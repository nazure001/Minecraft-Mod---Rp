import numpy as np
import math
import json
import urllib.request
import os
import shutil

from solve_ready_pose_ik import solve_2bone_ik, euler_from_matrix_zyx, rotation_matrix_zyx

def call_bb(action, params=None):
    if params is None:
        params = {}
    req = urllib.request.Request(
        'http://127.0.0.1:8787/',
        data=json.dumps({'action': action, 'params': params}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Staff geometry:
P_rear_grip = np.array([4.5, 14.0, 1.0])
P_lead_grip = np.array([1.5, 15.5, -4.5])

v_staff_raw = P_lead_grip - P_rear_grip
dist_grips = np.linalg.norm(v_staff_raw)
v_staff = v_staff_raw / dist_grips

# Staff butt and tip:
u_rear = 13.0 # On grip wrap
u_lead = u_rear + dist_grips # ~19.442, on lower upper shaft
P_butt = P_rear_grip - u_rear * v_staff
P_tip = P_butt + 30.0 * v_staff

# Rotation matrix for staff from [0, 1, 0] to v_staff:
v0 = np.array([0.0, 1.0, 0.0])
axis = np.cross(v0, v_staff)
axis = axis / np.linalg.norm(axis)
angle = math.acos(np.dot(v0, v_staff))
K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
R_staff = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
euler_staff = euler_from_matrix_zyx(R_staff)

# Hand wrist targets:
# Hand wraps around staff.
# Right hand (rear): wraps from outside (+X) toward staff:
# Offset wrist center by ~1.5u along normal to staff:
# Normal perpendicular to staff and roughly along +X:
n_right = np.array([0.8, -0.2, 0.5])
n_right = n_right - np.dot(n_right, v_staff) * v_staff
n_right = n_right / np.linalg.norm(n_right)
W_rear = P_rear_grip + n_right * 1.5

# Left hand (lead): wraps from underneath/left (-X, -Y) toward staff:
n_left = np.array([-0.8, -0.4, -0.2])
n_left = n_left - np.dot(n_left, v_staff) * v_staff
n_left = n_left / np.linalg.norm(n_left)
W_lead = P_lead_grip + n_left * 1.5

# Shoulders:
s_right = np.array([5.0, 22.0, 0.0])
s_left  = np.array([-5.0, 22.0, 0.0])

# Solve IK:
ik_rear = solve_2bone_ik(s_right, W_rear, pole_hint=np.array([1.0, -0.2, 0.5]))
ik_lead = solve_2bone_ik(s_left, W_lead, pole_hint=np.array([-1.0, -0.5, -0.2]))

print("=== READY POSE SOLVER RESULTS ===")
print("Staff:")
print(f"  Butt: {P_butt.tolist()}")
print(f"  Tip : {P_tip.tolist()}")
print(f"  Euler (ZYX): {euler_staff.tolist()}")
print(f"  Staff Group Position: {P_butt.tolist()}")

print("\nRear Hand (Right):")
print(f"  Grip point on staff axis: {P_rear_grip.tolist()} (u={u_rear})")
print(f"  Wrist attachment target : {W_rear.tolist()}")
print(f"  Wrist to axis distance  : {np.linalg.norm(W_rear - P_rear_grip):.4f} u")
print(f"  Upper Arm Euler (ZYX)   : {ik_rear['euler_upper'].tolist()}")
print(f"  Forearm Euler (ZYX)     : {ik_rear['euler_forearm'].tolist()}")

print("\nLead Hand (Left):")
print(f"  Grip point on staff axis: {P_lead_grip.tolist()} (u={u_lead:.3f})")
print(f"  Wrist attachment target : {W_lead.tolist()}")
print(f"  Wrist to axis distance  : {np.linalg.norm(W_lead - P_lead_grip):.4f} u")
print(f"  Upper Arm Euler (ZYX)   : {ik_lead['euler_upper'].tolist()}")
print(f"  Forearm Euler (ZYX)     : {ik_lead['euler_forearm'].tolist()}")
