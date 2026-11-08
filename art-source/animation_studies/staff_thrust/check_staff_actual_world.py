import urllib.request
import json
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

code = '''
Canvas.updateAll();
Canvas.updateAllBones();
let staff = Group.all.find(g => g.name === 'staff_assembly');
staff.mesh.updateMatrixWorld(true);

let staff_cubes = staff.children.filter(c => c instanceof Cube);
let cube_data = staff_cubes.map(c => {
    c.mesh.updateMatrixWorld(true);
    let box = new THREE.Box3().setFromObject(c.mesh);
    return {
        name: c.name,
        from: c.from,
        to: c.to,
        origin: c.origin,
        mesh_pos: [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z],
        mesh_matrixWorld: Array.from(c.mesh.matrixWorld.elements),
        world_box: {
            min: [box.min.x, box.min.y, box.min.z],
            max: [box.max.x, box.max.y, box.max.z]
        }
    };
});

// Hands / wrists
let ru = Group.all.find(g => g.name === 'right_upper_arm');
let rf = Group.all.find(g => g.name === 'right_forearm');
let lu = Group.all.find(g => g.name === 'left_upper_arm');
let lf = Group.all.find(g => g.name === 'left_forearm');

rf.mesh.updateMatrixWorld(true);
lf.mesh.updateMatrixWorld(true);

let local_wrist = new THREE.Vector3(0, -6, 0);
let rw = local_wrist.clone().applyMatrix4(rf.mesh.matrixWorld);
let lw = local_wrist.clone().applyMatrix4(lf.mesh.matrixWorld);

return {
    staff_group_origin: staff.origin,
    staff_group_rotation: staff.rotation,
    staff_mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    staff_matrixWorld: Array.from(staff.mesh.matrixWorld.elements),
    cubes: cube_data,
    right_wrist_world: [rw.x, rw.y, rw.z],
    left_wrist_world: [lw.x, lw.y, lw.z]
};
'''

res = call_bb('execute_script', {'code': code})
print(json.dumps(res['result'], indent=2))
