import urllib.request
import json
import base64
import os
import numpy as np

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

# 1. Load project in Blockbench
model_path = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready.bbmodel'
load_res = call_bb('load_project', {'path': model_path})
print('Loaded project:', load_res)

# 2. Extract live matrixWorld telemetry from Blockbench
code = '''
let ru = Group.all.find(g => g.name === 'right_upper_arm');
let rf = Group.all.find(g => g.name === 'right_forearm');
let lu = Group.all.find(g => g.name === 'left_upper_arm');
let lf = Group.all.find(g => g.name === 'left_forearm');
let staff = Group.all.find(g => g.name === 'staff_assembly');

ru.mesh.updateMatrixWorld(true);
rf.mesh.updateMatrixWorld(true);
lu.mesh.updateMatrixWorld(true);
lf.mesh.updateMatrixWorld(true);
staff.mesh.updateMatrixWorld(true);

// Wrist attachment point is at bottom of forearm: [0, -6, 0] in forearm local space
let local_wrist = new THREE.Vector3(0, -6, 0);
let right_wrist_world = local_wrist.clone().applyMatrix4(rf.mesh.matrixWorld);
let left_wrist_world = local_wrist.clone().applyMatrix4(lf.mesh.matrixWorld);

// Elbow positions (origin of forearms)
let right_elbow_world = new THREE.Vector3();
rf.mesh.getWorldPosition(right_elbow_world);
let left_elbow_world = new THREE.Vector3();
lf.mesh.getWorldPosition(left_elbow_world);

// Staff butt (u=0) and tip (u=30) in staff local space: [0, u, 0]
let staff_butt_world = new THREE.Vector3(0, 0, 0).applyMatrix4(staff.mesh.matrixWorld);
let staff_rear_grip_world = new THREE.Vector3(0, 13.0, 0).applyMatrix4(staff.mesh.matrixWorld);
let staff_lead_grip_world = new THREE.Vector3(0, 19.442, 0).applyMatrix4(staff.mesh.matrixWorld);
let staff_tip_world = new THREE.Vector3(0, 30.0, 0).applyMatrix4(staff.mesh.matrixWorld);

return {
    right_shoulder: [ru.origin[0], ru.origin[1], ru.origin[2]],
    right_elbow: [right_elbow_world.x, right_elbow_world.y, right_elbow_world.z],
    right_wrist: [right_wrist_world.x, right_wrist_world.y, right_wrist_world.z],
    left_shoulder: [lu.origin[0], lu.origin[1], lu.origin[2]],
    left_elbow: [left_elbow_world.x, left_elbow_world.y, left_elbow_world.z],
    left_wrist: [left_wrist_world.x, left_wrist_world.y, left_wrist_world.z],
    staff_butt: [staff_butt_world.x, staff_butt_world.y, staff_butt_world.z],
    staff_rear_grip: [staff_rear_grip_world.x, staff_rear_grip_world.y, staff_rear_grip_world.z],
    staff_lead_grip: [staff_lead_grip_world.x, staff_lead_grip_world.y, staff_lead_grip_world.z],
    staff_tip: [staff_tip_world.x, staff_tip_world.y, staff_tip_world.z]
};
'''

res = call_bb('execute_script', {'code': code})
t = res['result']

print("\n=== LIVE BLOCKBENCH RENDERER TELEMETRY ===")
rw = np.array(t['right_wrist'])
rg = np.array(t['staff_rear_grip'])
lw = np.array(t['left_wrist'])
lg = np.array(t['staff_lead_grip'])

d_rear_axis = np.linalg.norm(rw - rg)
d_lead_axis = np.linalg.norm(lw - lg)

# Surface radius: grip wrap has half-width = 1.0u, shaft has half-width = 0.75u
d_rear_surface = d_rear_axis - 1.0 # grip wrap radius is 1.0u
d_lead_surface = d_lead_axis - 0.75 # shaft radius is 0.75u

print(f"Rear Grip (Right Hand):")
print(f"  Wrist World Pos    : {rw.tolist()}")
print(f"  Staff Axis Point   : {rg.tolist()}")
print(f"  Delta Vector (W - G): {(rw - rg).tolist()}")
print(f"  Distance to Axis   : {d_rear_axis:.4f} u")
print(f"  Distance to Surface: {d_rear_surface:.4f} u (Staff radius = 1.0u)")

print(f"\nLead Grip (Left Hand):")
print(f"  Wrist World Pos    : {lw.tolist()}")
print(f"  Staff Axis Point   : {lg.tolist()}")
print(f"  Delta Vector (W - G): {(lw - lg).tolist()}")
print(f"  Distance to Axis   : {d_lead_axis:.4f} u")
print(f"  Distance to Surface: {d_lead_surface:.4f} u (Staff radius = 0.75u)")

print(f"\nArm Segment Length Verification:")
rs = np.array(t['right_shoulder'])
re = np.array(t['right_elbow'])
ls = np.array(t['left_shoulder'])
le = np.array(t['left_elbow'])
print(f"  Right Upper Arm : {np.linalg.norm(re - rs):.4f} u (Expected: 6.0u)")
print(f"  Right Forearm   : {np.linalg.norm(rw - re):.4f} u (Expected: 6.0u)")
print(f"  Left Upper Arm  : {np.linalg.norm(le - ls):.4f} u (Expected: 6.0u)")
print(f"  Left Forearm    : {np.linalg.norm(lw - le):.4f} u (Expected: 6.0u)")
print(f"  Staff Length    : {np.linalg.norm(np.array(t['staff_tip']) - np.array(t['staff_butt'])):.4f} u (Expected: 30.0u)")

# 3. Capture Screenshots
output_dir = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust'
brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

views = [
    ('front', 'ready_pose_front.png'),
    ('right', 'ready_pose_side.png'),
    ('front_right', 'ready_pose_perspective.png')
]

for view_name, file_name in views:
    shot = call_bb('screenshot', {'view': view_name, 'width': 800, 'height': 800, 'annotate': False})
    if shot.get('ok'):
        b64 = shot['result']['base64']
        dest_local = os.path.join(output_dir, file_name)
        dest_brain = os.path.join(brain_dir, file_name)
        data = base64.b64decode(b64)
        with open(dest_local, 'wb') as f:
            f.write(data)
        with open(dest_brain, 'wb') as f:
            f.write(data)
        print(f"Captured {view_name} -> {dest_brain} ({len(data)} bytes)")
