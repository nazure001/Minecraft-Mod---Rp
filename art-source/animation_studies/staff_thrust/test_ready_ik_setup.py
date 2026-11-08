import urllib.request
import json
import math
import numpy as np
import shutil
import os

from solve_ready_pose_ik import solve_2bone_ik, rotation_matrix_zyx, euler_from_matrix_zyx

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
NEUTRAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_neutral.bbmodel")
READY_MODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready.bbmodel")

# 1. Create a dedicated copy for ready pose
shutil.copyfile(NEUTRAL_MODEL_PATH, READY_MODEL_PATH)
print(f"Created ready pose checkpoint copy: {READY_MODEL_PATH}")

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

# First, load the ready model in Blockbench
call_bb('load_project', {'path': READY_MODEL_PATH})

# Let's define the Ready Pose parameters:
# Torso:
# Let torso be in neutral orientation: [0, 0, 0] or slight natural turn.
# Keeping torso at [0, 0, 0] simplifies tracking and isolates the arm & staff dynamics!

# Shoulder positions in world space (with torso at [0, 0, 0]):
# right shoulder: [5.0, 22.0, 0.0]
# left shoulder : [-5.0, 22.0, 0.0]
s_right = np.array([5.0, 22.0, 0.0])
s_left  = np.array([-5.0, 22.0, 0.0])

# Staff configuration:
# In Candidate 2, staff length = 30u.
# In local coordinates of staff_assembly:
# origin is [6.5, 0, 0].
# But let's position staff_assembly so that:
# Butt is near right hip/thigh, pointing forward-downward or forward-upward:
# Standard Ready Stance (Chudan):
# Staff angles forward into middle guard.
# Rear hand (right hand): holds staff near rear shaft / grip wrap at [4.5, 14.5, 1.0]
# Front hand (left hand, guiding): holds staff forward at [1.5, 16.5, -6.5]
# Let's check distance between shoulders and target wrists:
w_rear = np.array([4.2, 14.5, 1.0])
w_lead = np.array([1.0, 16.0, -6.5])

d_rear = np.linalg.norm(w_rear - s_right)
d_lead = np.linalg.norm(w_lead - s_left)
print(f"Rear arm reach required: {d_rear:.3f} u (Max: 12.0u)")
print(f"Lead arm reach required: {d_lead:.3f} u (Max: 12.0u)")

# Solve IK for Rear Arm (Right Arm):
# Pole hint for right arm: outward-backward [1.0, -0.5, 0.5]
ik_rear = solve_2bone_ik(s_right, w_rear, pole_hint=np.array([1.0, -0.2, 0.5]))
# Solve IK for Lead Arm (Left Arm):
# Pole hint for left arm: outward-downward [-1.0, -0.5, -0.2]
ik_lead = solve_2bone_ik(s_left, w_lead, pole_hint=np.array([-1.0, -0.5, -0.2]))

print("\nIK Rear Arm (Right):")
print(f"  Upper Arm Euler (ZYX): {ik_rear['euler_upper']}")
print(f"  Forearm Euler (ZYX)  : {ik_rear['euler_forearm']}")
print(f"  Calculated Elbow     : {ik_rear['elbow']}")

print("\nIK Lead Arm (Left):")
print(f"  Upper Arm Euler (ZYX): {ik_lead['euler_upper']}")
print(f"  Forearm Euler (ZYX)  : {ik_lead['euler_forearm']}")
print(f"  Calculated Elbow     : {ik_lead['elbow']}")

# Now let's calculate Staff transform:
# The staff must pass through w_rear and w_lead!
# Vector along staff axis:
v_staff = (w_lead - w_rear) / np.linalg.norm(w_lead - w_rear)
# In neutral, staff axis is [0, 1, 0] (pointing along +Y).
# We need rotation from [0, 1, 0] to v_staff:
v0_staff = np.array([0.0, 1.0, 0.0])
axis_s = np.cross(v0_staff, v_staff)
axis_s = axis_s / np.linalg.norm(axis_s)
angle_s = math.acos(np.dot(v0_staff, v_staff))
K_s = np.array([[0, -axis_s[2], axis_s[1]], [axis_s[2], 0, -axis_s[0]], [-axis_s[1], axis_s[0], 0]])
R_staff = np.eye(3) + math.sin(angle_s) * K_s + (1 - math.cos(angle_s)) * (K_s @ K_s)
euler_staff = euler_from_matrix_zyx(R_staff)
print(f"\nStaff Rotation Euler (ZYX): {euler_staff}")
