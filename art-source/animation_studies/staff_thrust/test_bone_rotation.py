import urllib.request
import json

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

code = '''
// Inspect rotation order, node types, and parent-child matrix composition
let ru = Group.all.find(g => g.name === 'right_upper_arm');
let rf = Group.all.find(g => g.name === 'right_forearm');
let torso = Group.all.find(g => g.name === 'torso');

// Reset rotations first
ru.rotation = [0, 0, 0];
rf.rotation = [0, 0, 0];
torso.rotation = [0, 0, 0];
Canvas.updateAllBones();

// Initial positions
let ru_obj = ru.mesh;
let rf_obj = rf.mesh;

ru_obj.updateMatrixWorld(true);
rf_obj.updateMatrixWorld(true);

let initial_ru_world = new THREE.Vector3();
let initial_rf_world = new THREE.Vector3();
ru_obj.getWorldPosition(initial_ru_world);
rf_obj.getWorldPosition(initial_rf_world);

// Test step 1: Rotate right_upper_arm by X: 30 deg
ru.rotation = [30, 0, 0];
Canvas.updateAllBones();
ru_obj.updateMatrixWorld(true);
rf_obj.updateMatrixWorld(true);

let step1_ru_pos = new THREE.Vector3();
let step1_ru_quat = new THREE.Quaternion();
let step1_rf_pos = new THREE.Vector3();
let step1_rf_quat = new THREE.Quaternion();
ru_obj.getWorldPosition(step1_ru_pos);
ru_obj.getWorldQuaternion(step1_ru_quat);
rf_obj.getWorldPosition(step1_rf_pos);
rf_obj.getWorldQuaternion(step1_rf_quat);

// Test step 2: Rotate right_forearm by X: 45 deg
rf.rotation = [45, 0, 0];
Canvas.updateAllBones();
ru_obj.updateMatrixWorld(true);
rf_obj.updateMatrixWorld(true);

let step2_rf_pos = new THREE.Vector3();
let step2_rf_quat = new THREE.Quaternion();
rf_obj.getWorldPosition(step2_rf_pos);
rf_obj.getWorldQuaternion(step2_rf_quat);

// Reset back to neutral
ru.rotation = [0, 0, 0];
rf.rotation = [0, 0, 0];
Canvas.updateAllBones();

return {
    rotation_order: ru_obj.rotation.order,
    initial: {
        ru_pivot: [ru.origin[0], ru.origin[1], ru.origin[2]],
        ru_world_pos: [initial_ru_world.x, initial_ru_world.y, initial_ru_world.z],
        rf_pivot: [rf.origin[0], rf.origin[1], rf.origin[2]],
        rf_world_pos: [initial_rf_world.x, initial_rf_world.y, initial_rf_world.z]
    },
    step1_rotate_upper_arm_30x: {
        ru_world_pos: [step1_ru_pos.x, step1_ru_pos.y, step1_ru_pos.z],
        ru_world_quat: [step1_ru_quat.x, step1_ru_quat.y, step1_ru_quat.z, step1_ru_quat.w],
        rf_world_pos: [step1_rf_pos.x, step1_rf_pos.y, step1_rf_pos.z],
        rf_world_quat: [step1_rf_quat.x, step1_rf_quat.y, step1_rf_quat.z, step1_rf_quat.w]
    },
    step2_rotate_forearm_45x: {
        rf_world_pos: [step2_rf_pos.x, step2_rf_pos.y, step2_rf_pos.z],
        rf_world_quat: [step2_rf_quat.x, step2_rf_quat.y, step2_rf_quat.z, step2_rf_quat.w]
    }
};
'''

res = call_bb('execute_script', {'code': code})
print('Rotation and World Transform Test:')
print(json.dumps(res, indent=2))
