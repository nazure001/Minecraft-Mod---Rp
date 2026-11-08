import os
import json
import math
import numpy as np

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
BBMODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_rigged.bbmodel")

# -------------------------------------------------------------------------
# 1. RIGID KINEMATIC GEOMETRY
# -------------------------------------------------------------------------
# Shoulder pivots in Minecraft Blockbench (model facing -Z):
# Right shoulder: [+5, 22, 0] (+X is model's right)
# Left shoulder:  [-5, 22, 0] (-X is model's left)
S_R = np.array([5.0, 22.0, 0.0])
S_L = np.array([-5.0, 22.0, 0.0])

# Staff Placement:
# Butt cap: P_b = [6.5, 12.5, 6.0]
# Direction vector: v_dir = [-0.2503884, 0.40062145, -0.88136718]
# Staff length: exactly 30.0 units
P_b = np.array([6.5, 12.5, 6.0])
v_dir = np.array([-0.2503884, 0.40062145, -0.88136718])
v_dir = v_dir / np.linalg.norm(v_dir)

# Target attachment points along the staff:
# u_R = 4.0 (right hand grips lower shaft at 4 units from butt)
# u_L = 12.5 (left hand grips crimson wrap at 12.5 units from butt)
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

# Rotation matrices helper to convert segment vectors to Euler angles
def vec_to_euler(vec):
    # Default unrotated arm vector points down: [0, -1, 0]
    # In Blockbench:
    # +X rotation rotates -Y towards -Z (forward)
    # +Y rotation rotates around Y axis
    # +Z rotation tips top toward left
    v = vec / np.linalg.norm(vec)
    # v = [vx, vy, vz]
    # Pitch (X): angle in YZ plane from [0, -1, 0]
    pitch = math.degrees(math.atan2(-v[2], -v[1]))
    # Roll (Z): angle in XY plane
    roll = math.degrees(math.atan2(v[0], -v[1]))
    # Yaw (Y): angle in XZ plane
    yaw = math.degrees(math.atan2(-v[0], -v[2]))
    return pitch, yaw, roll

print("Rig calculations complete.")

# -------------------------------------------------------------------------
# 2. CONSTRUCT CUBES WITH EXACT WORLD COORDINATES
# -------------------------------------------------------------------------
# To ensure 100% faithful and deterministic visualization in Blockbench:
# We build the model elements so their default rest geometry IS THE READY POSE!
# That way, whether in 'Edit' mode or 'Animate' mode, the user sees the EXACT pose!

def make_oriented_box_cubes(p1, p2, thickness, name, color=0):
    # Oriented bounding representation or segment
    pass

# We construct the 5 Candidate 2 Staff Cubes directly transformed along (P_b + v_dir * u):
# Cubes:
# 1. lower_cap: u in [0, 1] (size 2.0x2.0, radius 1.0)
# 2. lower_shaft: u in [1, 12] (size 1.5x1.5, radius 0.75)
# 3. grip_wrap: u in [12, 18] (size 2.0x2.0, radius 1.0)
# 4. upper_shaft: u in [18, 29] (size 1.5x1.5, radius 0.75)
# 5. upper_cap: u in [29, 30] (size 2.0x2.0, radius 1.0)

# Arm cubes:
# Right upper arm: from S_R to E_R (box width 4, depth 4, length 6)
# Right forearm: from E_R to T_R (box width 4, depth 4, length 6)
# Left upper arm: from S_L to E_L (box width 4, depth 4, length 6)
# Left forearm: from E_L to T_L (box width 4, depth 4, length 6)

print("Building model structure...")
