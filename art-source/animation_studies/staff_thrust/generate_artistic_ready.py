import urllib.request
import json
import base64
import os
import math
import numpy as np

from solve_ready_pose_ik import solve_2bone_ik, euler_from_matrix_zyx, rotation_matrix_zyx

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
NEUTRAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_neutral.bbmodel")
READY_ARTISTIC_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready_artistic.bbmodel")
BRAIN_DIR = r"C:\Users\USER\.gemini\antigravity\brain\54a80670-a4c4-4299-bd5f-db191f100d71"

# 1. Torso Stance: -25 deg yaw (stronger side angle), +5 deg athletic pitch
torso_yaw_deg = -25.0
torso_pitch_deg = 5.0
torso_roll_deg = 0.0

R_torso = rotation_matrix_zyx(torso_pitch_deg, torso_yaw_deg, torso_roll_deg)
torso_pivot = np.array([0.0, 12.0, 0.0])

# Shoulders in torso local space: [5, 10, 0] and [-5, 10, 0]
s_ru_local = np.array([5.0, 10.0, 0.0])
s_lu_local = np.array([-5.0, 10.0, 0.0])

s_right_world = torso_pivot + R_torso @ s_ru_local
s_left_world  = torso_pivot + R_torso @ s_lu_local

# Head looks forward at opponent: cancels torso yaw and pitch
head_yaw_deg = -torso_yaw_deg # +25 deg
head_pitch_deg = -torso_pitch_deg # -5 deg
head_roll_deg = 0.0

# 2. Staff Stance (Distinctly diagonal across pinggang - dada bawah):
# Rear hand: anchored near right hip
P_rear_grip = np.array([4.2, 11.5, 2.0])
# Lead hand: in front of lower chest / solar plexus
P_lead_grip = np.array([0.0, 14.0, -5.0])

v_staff_raw = P_lead_grip - P_rear_grip
dist_grips = np.linalg.norm(v_staff_raw)
v_staff = v_staff_raw / dist_grips

u_rear = 13.0 # On grip wrap
u_lead = u_rear + dist_grips # ~21.5
P_butt = P_rear_grip - u_rear * v_staff
P_tip = P_butt + 30.0 * v_staff

v0 = np.array([0.0, 1.0, 0.0])
axis = np.cross(v0, v_staff)
axis = axis / np.linalg.norm(axis)
angle = math.acos(np.dot(v0, v_staff))
K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
R_staff = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
euler_staff = euler_from_matrix_zyx(R_staff)

# 3. Hand Attachment Targets:
# Rear hand (right): wraps around staff from outside (+X)
n_right = np.array([0.9, -0.1, 0.4])
n_right = n_right - np.dot(n_right, v_staff) * v_staff
n_right = n_right / np.linalg.norm(n_right)
W_rear = P_rear_grip + n_right * 1.5

# Lead hand (left): wraps around staff from underneath / left (-X, -Y)
n_left = np.array([-0.8, -0.6, -0.2])
n_left = n_left - np.dot(n_left, v_staff) * v_staff
n_left = n_left / np.linalg.norm(n_left)
W_lead = P_lead_grip + n_left * 1.5

# Check reaches
d_rear = np.linalg.norm(W_rear - s_right_world)
d_lead = np.linalg.norm(W_lead - s_left_world)
print(f"Right arm reach: {d_rear:.3f} u (Max: 12.0u)")
print(f"Left arm reach : {d_lead:.3f} u (Max: 12.0u)")

# 4. Solve IK for Arms:
ik_rear = solve_2bone_ik(s_right_world, W_rear, pole_hint=np.array([1.0, -0.2, 0.4]))
ik_lead = solve_2bone_ik(s_left_world, W_lead, pole_hint=np.array([-1.0, -0.5, -0.3]))

R_ru_local = R_torso.T @ ik_rear['R_upper']
euler_ru = euler_from_matrix_zyx(R_ru_local)
euler_rf = ik_rear['euler_forearm']

R_lu_local = R_torso.T @ ik_lead['R_upper']
euler_lu = euler_from_matrix_zyx(R_lu_local)
euler_lf = ik_lead['euler_forearm']

# Legs stance: Left leg forward (-18 deg pitch, -15 deg yaw), right leg back (+14 deg pitch, -15 deg yaw)
euler_rleg = [14.0, -15.0, 0.0]
euler_lleg = [-18.0, -15.0, 0.0]

# 5. Build bbmodel JSON
with open(NEUTRAL_MODEL_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

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
        elif g.get("name") == "head":
            g["rotation"] = [round(head_pitch_deg, 4), round(head_yaw_deg, 4), round(head_roll_deg, 4)]
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
data["name"] = "player_staff_thrust_ready_artistic"

with open(READY_ARTISTIC_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated Ready Artistic Model: {READY_ARTISTIC_PATH}")

# 6. Load into Blockbench & Verify Telemetry
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

load_res = call_bb('load_project', {'path': READY_ARTISTIC_PATH})
print('Loaded project in Blockbench:', load_res)

# Unselect all and hide gizmos for pristine screenshots
call_bb('execute_script', {'code': '''
unselectAll();
Canvas.show_gizmos = false;
Canvas.show_element_markers = false;
Canvas.updateView();
'''})

# Read live matrixWorld telemetry
code = '''
let ru = Group.all.find(g => g.name === 'right_upper_arm');
let rf = Group.all.find(g => g.name === 'right_forearm');
let lu = Group.all.find(g => g.name === 'left_upper_arm');
let lf = Group.all.find(g => g.name === 'left_forearm');
let staff = Group.all.find(g => g.name === 'staff_assembly');
let head = Group.all.find(g => g.name === 'head');
let torso = Group.all.find(g => g.name === 'torso');

ru.mesh.updateMatrixWorld(true);
rf.mesh.updateMatrixWorld(true);
lu.mesh.updateMatrixWorld(true);
lf.mesh.updateMatrixWorld(true);
staff.mesh.updateMatrixWorld(true);
head.mesh.updateMatrixWorld(true);
torso.mesh.updateMatrixWorld(true);

let local_wrist = new THREE.Vector3(0, -6, 0);
let rw_world = local_wrist.clone().applyMatrix4(rf.mesh.matrixWorld);
let lw_world = local_wrist.clone().applyMatrix4(lf.mesh.matrixWorld);

let re_world = new THREE.Vector3(); rf.mesh.getWorldPosition(re_world);
let le_world = new THREE.Vector3(); lf.mesh.getWorldPosition(le_world);

let rs_world = new THREE.Vector3(); ru.mesh.getWorldPosition(rs_world);
let ls_world = new THREE.Vector3(); lu.mesh.getWorldPosition(ls_world);

let s_butt = new THREE.Vector3(0, 0, 0).applyMatrix4(staff.mesh.matrixWorld);
let s_rear_grip = new THREE.Vector3(0, 13.0, 0).applyMatrix4(staff.mesh.matrixWorld);
let s_lead_grip = new THREE.Vector3(0, ''' + str(round(u_lead, 4)) + ''', 0).applyMatrix4(staff.mesh.matrixWorld);
let s_tip = new THREE.Vector3(0, 30.0, 0).applyMatrix4(staff.mesh.matrixWorld);

let head_world = new THREE.Vector3(); head.mesh.getWorldPosition(head_world);

return {
    right_shoulder: [rs_world.x, rs_world.y, rs_world.z],
    right_elbow: [re_world.x, re_world.y, re_world.z],
    right_wrist: [rw_world.x, rw_world.y, rw_world.z],
    left_shoulder: [ls_world.x, ls_world.y, ls_world.z],
    left_elbow: [le_world.x, le_world.y, le_world.z],
    left_wrist: [lw_world.x, lw_world.y, lw_world.z],
    staff_butt: [s_butt.x, s_butt.y, s_butt.z],
    staff_rear_grip: [s_rear_grip.x, s_rear_grip.y, s_rear_grip.z],
    staff_lead_grip: [s_lead_grip.x, s_lead_grip.y, s_lead_grip.z],
    staff_tip: [s_tip.x, s_tip.y, s_tip.z],
    head_pos: [head_world.x, head_world.y, head_world.z]
};
'''

t = call_bb('execute_script', {'code': code})['result']

print("\n=== LIVE BLOCKBENCH TELEMETRY READY ARTISTIC ===")
rw = np.array(t['right_wrist'])
rg = np.array(t['staff_rear_grip'])
lw = np.array(t['left_wrist'])
lg = np.array(t['staff_lead_grip'])

d_rear_axis = np.linalg.norm(rw - rg)
d_lead_axis = np.linalg.norm(lw - lg)

print(f"Rear Grip (Right Hand):")
print(f"  Wrist World Pos    : {rw.tolist()}")
print(f"  Staff Axis Point   : {rg.tolist()}")
print(f"  Delta Vector (W - G): {(rw - rg).tolist()}")
print(f"  Distance to Axis   : {d_rear_axis:.4f} u")
print(f"  Radius Approx Wrap : {d_rear_axis - 1.0:.4f} u (R_wrap = 1.0u)")

print(f"\nLead Grip (Left Hand):")
print(f"  Wrist World Pos    : {lw.tolist()}")
print(f"  Staff Axis Point   : {lg.tolist()}")
print(f"  Delta Vector (W - G): {(lw - lg).tolist()}")
print(f"  Distance to Axis   : {d_lead_axis:.4f} u")
print(f"  Radius Approx Shaft: {d_lead_axis - 0.75:.4f} u (R_shaft = 0.75u)")

print(f"\nArm Integrity:")
print(f"  Right Arm Segments : {np.linalg.norm(np.array(t['right_elbow']) - np.array(t['right_shoulder'])):.4f} u + {np.linalg.norm(rw - np.array(t['right_elbow'])):.4f} u")
print(f"  Left Arm Segments  : {np.linalg.norm(np.array(t['left_elbow']) - np.array(t['left_shoulder'])):.4f} u + {np.linalg.norm(lw - np.array(t['left_elbow'])):.4f} u")
print(f"  Staff Length       : {np.linalg.norm(np.array(t['staff_tip']) - np.array(t['staff_butt'])):.4f} u")

print(f"\nVertical Heights:")
print(f"  Head Origin Y : {t['head_pos'][1]:.2f} u (Head spans Y: 24 to 32)")
print(f"  Staff Tip Y   : {t['staff_tip'][1]:.2f} u (Front tip diagonal at chest/rib height)")
print(f"  Staff Butt Y  : {t['staff_butt'][1]:.2f} u (Rear butt behind hip)")

# 7. Capture Clean Screenshots
views = [
    ('front', 'ready_artistic_clean_front.png'),
    ('right', 'ready_artistic_clean_side.png'),
    ('front_right', 'ready_artistic_clean_perspective.png')
]

for view_name, file_name in views:
    shot = call_bb('screenshot', {'view': view_name, 'width': 800, 'height': 800, 'annotate': False})
    if shot.get('ok'):
        b64 = shot['result']['base64']
        dest_local = os.path.join(OUTPUT_DIR, file_name)
        dest_brain = os.path.join(BRAIN_DIR, file_name)
        data = base64.b64decode(b64)
        with open(dest_local, 'wb') as f:
            f.write(data)
        with open(dest_brain, 'wb') as f:
            f.write(data)
        print(f"Captured clean {view_name} -> {dest_brain} ({len(data)} bytes)")
