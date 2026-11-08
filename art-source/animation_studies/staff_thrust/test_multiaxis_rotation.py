import urllib.request
import json
import math
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

# In Blockbench:
# Test multi-axis rotation on right_upper_arm:
# Let rx = 30 degrees, ry = 45 degrees, rz = 0 (or rx=30, ry=20, rz=-15)
rx_deg = 30.0
ry_deg = 45.0
rz_deg = 0.0

code = f'''
let ru = Group.all.find(g => g.name === 'right_upper_arm');
let rf = Group.all.find(g => g.name === 'right_forearm');
let torso = Group.all.find(g => g.name === 'torso');

// Reset first
ru.rotation = [0, 0, 0];
rf.rotation = [0, 0, 0];
torso.rotation = [0, 0, 0];
Canvas.updateAllBones();

// Apply 2-axis rotation to right_upper_arm:
ru.rotation = [{rx_deg}, {ry_deg}, {rz_deg}];
Canvas.updateAllBones();

ru.mesh.updateMatrixWorld(true);
rf.mesh.updateMatrixWorld(true);

let ru_world_pos = new THREE.Vector3();
let ru_world_quat = new THREE.Quaternion();
ru.mesh.getWorldPosition(ru_world_pos);
ru.mesh.getWorldQuaternion(ru_world_quat);

let rf_world_pos = new THREE.Vector3();
let rf_world_quat = new THREE.Quaternion();
rf.mesh.getWorldPosition(rf_world_pos);
rf.mesh.getWorldQuaternion(rf_world_quat);

// Also measure wrist end point (bottom of forearm cube in local space: [0, -6, 0] from rf pivot)
let wrist_local = new THREE.Vector3(0, -6, 0);
let wrist_world = wrist_local.clone().applyMatrix4(rf.mesh.matrixWorld);

return {{
    order: ru.mesh.rotation.order,
    ru_origin: [ru.origin[0], ru.origin[1], ru.origin[2]],
    rf_origin: [rf.origin[0], rf.origin[1], rf.origin[2]],
    ru_matrixWorld: Array.from(ru.mesh.matrixWorld.elements),
    rf_matrixWorld: Array.from(rf.mesh.matrixWorld.elements),
    ru_world_pos: [ru_world_pos.x, ru_world_pos.y, ru_world_pos.z],
    ru_world_quat: [ru_world_quat.x, ru_world_quat.y, ru_world_quat.z, ru_world_quat.w],
    rf_world_pos: [rf_world_pos.x, rf_world_pos.y, rf_world_pos.z],
    rf_world_quat: [rf_world_quat.x, rf_world_quat.y, rf_world_quat.z, rf_world_quat.w],
    wrist_world: [wrist_world.x, wrist_world.y, wrist_world.z]
}};
'''

res = call_bb('execute_script', {'code': code})
ed = res['result']

# Now let's calculate analytically in Python using Three.js "ZYX" Euler convention:
# In Three.js with order "ZYX", rotation matrix is: R = Rz * Ry * Rx
# Note: In Blockbench, Euler angles in .rotation are in degrees.
rx = math.radians(rx_deg)
ry = math.radians(ry_deg)
rz = math.radians(rz_deg)

# Rotation matrices:
Rx = np.array([
    [1, 0, 0],
    [0, math.cos(rx), -math.sin(rx)],
    [0, math.sin(rx), math.cos(rx)]
])

Ry = np.array([
    [math.cos(ry), 0, math.sin(ry)],
    [0, 1, 0],
    [-math.sin(ry), 0, math.cos(ry)]
])

Rz = np.array([
    [math.cos(rz), -math.sin(rz), 0],
    [math.sin(rz), math.cos(rz), 0],
    [0, 0, 1]
])

# Order "ZYX": R = Rz @ Ry @ Rx
R = Rz @ Ry @ Rx

# Pivot of ru is [5, 22, 0]
ru_pivot = np.array([5.0, 22.0, 0.0])
# Pivot of rf in neutral is [5, 16, 0]. Relative vector from ru to rf is [0, -6, 0]
v_elbow_local = np.array([0.0, -6.0, 0.0])
# Forearm vector from rf to wrist in neutral is [0, -6, 0]
v_wrist_local = np.array([0.0, -12.0, 0.0])

calculated_elbow_pos = ru_pivot + R @ v_elbow_local
calculated_wrist_pos = ru_pivot + R @ v_wrist_local

print("=== MULTI-AXIS ROTATION TEST RESULTS ===")
print(f"Inputs: rx={rx_deg} deg, ry={ry_deg} deg, rz={rz_deg} deg (Order: {ed['order']})")
print("\n1. Elbow Position (rf origin):")
print(f"  Calculated (Python ZYX) : {calculated_elbow_pos.tolist()}")
print(f"  Editor (Blockbench mesh): {ed['rf_world_pos']}")
diff_elbow = np.linalg.norm(calculated_elbow_pos - np.array(ed['rf_world_pos']))
print(f"  Difference: {diff_elbow:.6e} units")

print("\n2. Wrist Position (forearm end):")
print(f"  Calculated (Python ZYX) : {calculated_wrist_pos.tolist()}")
print(f"  Editor (Blockbench mesh): {ed['wrist_world']}")
diff_wrist = np.linalg.norm(calculated_wrist_pos - np.array(ed['wrist_world']))
print(f"  Difference: {diff_wrist:.6e} units")

# Reset bones back to neutral in editor
call_bb('execute_script', {'code': '''
let ru = Group.all.find(g => g.name === "right_upper_arm");
let rf = Group.all.find(g => g.name === "right_forearm");
ru.rotation = [0, 0, 0];
rf.rotation = [0, 0, 0];
Canvas.updateAllBones();
'''})
print("\nReset bones back to neutral: DONE")
