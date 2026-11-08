import os
import json
import math
import numpy as np
import urllib.request

# -----------------------------------------------------------------------------
# 1. READ ACTUAL NODES FROM LIVE BLOCKBENCH
# -----------------------------------------------------------------------------
def call_bb(action, params={}):
    req = urllib.request.Request(
        "http://127.0.0.1:8787/command",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"id": "req-math", "action": action, "params": params}).encode("utf-8")
    )
    resp = urllib.request.urlopen(req, timeout=5)
    return json.loads(resp.read().decode())

out = call_bb("list_outliner")
elements = out.get("result", [])

nodes_by_name = {}
for el in elements:
    nodes_by_name[el.get("name")] = el

# Helper: compute rotation matrix from Euler degrees (Blockbench convention: ZXY or standard Euler)
def rot_x(deg):
    r = math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(r), -math.sin(r)], [0, math.sin(r), math.cos(r)]])
def rot_y(deg):
    r = math.radians(deg)
    return np.array([[math.cos(r), 0, math.sin(r)], [0, 1, 0], [-math.sin(r), 0, math.cos(r)]])
def rot_z(deg):
    r = math.radians(deg)
    return np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])

def euler_to_mat(euler):
    # Blockbench uses Euler angles in degrees
    # Rotates: Yaw (Y) then Pitch (X) then Roll (Z)
    return rot_y(euler[1]) @ rot_x(euler[0]) @ rot_z(euler[2])

print("--- 1. SOLVER TARGETS ---")
S_R_solver = np.array([5.0, 22.0, 0.0])
E_R_solver = np.array([9.23, 18.79, 2.79])
T_R_solver = np.array([5.50, 14.10, 2.47])

S_L_solver = np.array([-5.0, 22.0, 0.0])
E_L_solver = np.array([-2.39, 17.76, -3.35])
T_L_solver = np.array([3.37, 17.51, -5.02])

P_butt_solver = np.array([6.50, 12.50, 6.00])
P_tip_solver = np.array([-1.01, 24.52, -20.44])

print(f"Right Shoulder (Solver): {S_R_solver}")
print(f"Right Elbow    (Solver): {E_R_solver}")
print(f"Right Wrist    (Solver): {T_R_solver}")
print(f"Left Shoulder  (Solver): {S_L_solver}")
print(f"Left Elbow     (Solver): {E_L_solver}")
print(f"Left Wrist     (Solver): {T_L_solver}")
print(f"Staff Butt     (Solver): {P_butt_solver}")
print(f"Staff Tip      (Solver): {P_tip_solver}")

# -----------------------------------------------------------------------------
# 2. ACTUAL RIG NODES IN BLOCKBENCH
# -----------------------------------------------------------------------------
print("\n--- 2. ACTUAL BLOCKBENCH NODE TRANSFORMS ---")
for key in ["torso", "head", "right_upper_arm", "right_forearm", "left_upper_arm", "left_forearm", "staff_assembly"]:
    node = nodes_by_name.get(key)
    if node:
        print(f"Node [{key}]: type={node.get('type')}, origin={node.get('origin')}, rot={node.get('rotation')}, parent={node.get('parent')}")

# Calculate actual endpoints from Blockbench element origins & rotations
# Right upper arm:
ru_node = nodes_by_name["right_upper_arm"]
ru_origin = np.array(ru_node["origin"]) # [5, 22, 0]
ru_rot = ru_node["rotation"]           # [-41.0, 44.8, 0]
# Default bone is [0, -6, 0]
R_ru = euler_to_mat(ru_rot)
E_R_actual = ru_origin + R_ru @ np.array([0.0, -6.0, 0.0])

# Right forearm:
rf_node = nodes_by_name["right_forearm"]
rf_origin = np.array(rf_node["origin"]) # [9.23, 18.79, 2.79]
rf_rot = rf_node["rotation"]           # [3.9, -38.5, 0]
R_rf = euler_to_mat(rf_rot)
T_R_actual = rf_origin + R_rf @ np.array([0.0, -6.0, 0.0])

# Left upper arm:
lu_node = nodes_by_name["left_upper_arm"]
lu_origin = np.array(lu_node["origin"]) # [-5, 22, 0]
lu_rot = lu_node["rotation"]           # [38.4, 25.8, 0]
R_lu = euler_to_mat(lu_rot)
E_L_actual = lu_origin + R_lu @ np.array([0.0, -6.0, 0.0])

# Left forearm:
lf_node = nodes_by_name["left_forearm"]
lf_origin = np.array(lf_node["origin"]) # [-2.39, 17.76, -3.35]
lf_rot = lf_node["rotation"]           # [81.2, 73.7, 0]
R_lf = euler_to_mat(lf_rot)
T_L_actual = lf_origin + R_lf @ np.array([0.0, -6.0, 0.0])

# Staff assembly:
staff_node = nodes_by_name["staff_assembly"]
staff_origin = np.array(staff_node["origin"]) # [6.5, 12.5, 6.0]
staff_rot = staff_node["rotation"]           # [-24.4, -15.9, 0]
R_staff = euler_to_mat(staff_rot)
P_butt_actual = staff_origin
P_tip_actual = staff_origin + R_staff @ np.array([0.0, 30.0, 0.0])

print(f"\nRight Elbow (Actual in Rig): {np.round(E_R_actual, 3)}")
print(f"Right Wrist (Actual in Rig): {np.round(T_R_actual, 3)}")
print(f"Left Elbow  (Actual in Rig): {np.round(E_L_actual, 3)}")
print(f"Left Wrist  (Actual in Rig): {np.round(T_L_actual, 3)}")
print(f"Staff Tip   (Actual in Rig): {np.round(P_tip_actual, 3)}")

# -----------------------------------------------------------------------------
# 3. DISCREPANCIES (ACTUAL RIG vs SOLVER)
# -----------------------------------------------------------------------------
print("\n--- 3. COMPARISON & DISCREPANCIES ---")
diff_E_R = np.linalg.norm(E_R_actual - E_R_solver)
diff_T_R = np.linalg.norm(T_R_actual - T_R_solver)
diff_E_L = np.linalg.norm(E_L_actual - E_L_solver)
diff_T_L = np.linalg.norm(T_L_actual - T_L_solver)
diff_P_tip = np.linalg.norm(P_tip_actual - P_tip_solver)

print(f"Right Elbow Delta: {diff_E_R:.4f} units")
print(f"Right Wrist Delta: {diff_T_R:.4f} units")
print(f"Left Elbow Delta:  {diff_E_L:.4f} units")
print(f"Left Wrist Delta:  {diff_T_L:.4f} units")
print(f"Staff Tip Delta:   {diff_P_tip:.4f} units")

# -----------------------------------------------------------------------------
# 4. CONTACT & SURFACE ERRORS ON ACTUAL RIG
# -----------------------------------------------------------------------------
print("\n--- 4. DETAILED ERROR TAXONOMY ON ACTUAL RIG ---")
# Staff line segment in actual rig: from P_butt_actual to P_tip_actual
v_staff = (P_tip_actual - P_butt_actual) / 30.0

def dist_point_to_line(pt, line_p0, line_dir):
    w = pt - line_p0
    proj = np.dot(w, line_dir)
    closest = line_p0 + proj * line_dir
    dist = np.linalg.norm(pt - closest)
    return dist, proj, closest

# Right Hand (Attachment target: u = 4.0 on lower shaft, shaft radius = 0.75u)
err_axis_R, u_proj_R, pt_axis_R = dist_point_to_line(T_R_actual, P_butt_actual, v_staff)
err_surface_R = abs(err_axis_R - 0.75) # deviation from cylindrical outer radius 0.75u
err_attach_R = abs(u_proj_R - 4.0)

# Left Hand (Attachment target: u = 12.5 on crimson wrap, wrap radius = 1.0u)
err_axis_L, u_proj_L, pt_axis_L = dist_point_to_line(T_L_actual, P_butt_actual, v_staff)
err_surface_L = abs(err_axis_L - 1.00) # deviation from wrap outer radius 1.00u
err_attach_L = abs(u_proj_L - 12.5)

print(f"RIGHT HAND:")
print(f" - Wrist Position (Actual): {np.round(T_R_actual, 3)}")
print(f" - Projected position on staff (u): {u_proj_R:.3f}u (Target: 4.0u -> Delta: {err_attach_R:.3f}u)")
print(f" - Error to Staff Axis:    {err_axis_R:.4f} units")
print(f" - Error to Shaft Surface: {err_surface_R:.4f} units (shaft radius = 0.75u)")

print(f"\nLEFT HAND:")
print(f" - Wrist Position (Actual): {np.round(T_L_actual, 3)}")
print(f" - Projected position on staff (u): {u_proj_L:.3f}u (Target: 12.5u -> Delta: {err_attach_L:.3f}u)")
print(f" - Error to Staff Axis:    {err_axis_L:.4f} units")
print(f" - Error to Wrap Surface:  {err_surface_L:.4f} units (wrap radius = 1.00u)")
