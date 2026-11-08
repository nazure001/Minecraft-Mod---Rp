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
let staff = Group.all.find(g => g.name === 'staff_assembly');
let o = staff.origin;

// Local box definitions along Y from 0 to 30:
let defs = {
    "staff_lower_cap":   { min: [-1.0, 0.0, -1.0], max: [1.0, 1.0, 1.0] },
    "staff_lower_shaft": { min: [-0.75, 1.0, -0.75], max: [0.75, 12.0, 0.75] },
    "staff_grip_wrap":   { min: [-1.0, 12.0, -1.0], max: [1.0, 18.0, 1.0] },
    "staff_upper_shaft": { min: [-0.75, 18.0, -0.75], max: [0.75, 29.0, 0.75] },
    "staff_upper_cap":   { min: [-1.0, 29.0, -1.0], max: [1.0, 30.0, 1.0] }
};

staff.children.filter(c => c instanceof Cube).forEach(c => {
    let d = defs[c.name];
    if (d) {
        c.origin = [o[0], o[1], o[2]];
        c.from = [o[0] + d.min[0], o[1] + d.min[1], o[2] + d.min[2]];
        c.to   = [o[0] + d.max[0], o[1] + d.max[1], o[2] + d.max[2]];
    }
});

Canvas.updateAll();
Canvas.updateAllBones();
staff.mesh.updateMatrixWorld(true);

let results = [];
staff.children.filter(c => c instanceof Cube).forEach(c => {
    c.mesh.updateMatrixWorld(true);
    let box = new THREE.Box3().setFromObject(c.mesh);
    results.push({
        name: c.name,
        mesh_pos: [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z],
        world_box: {
            min: [box.min.x, box.min.y, box.min.z],
            max: [box.max.x, box.max.y, box.max.z]
        }
    });
});

return {
    staff_mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    cubes: results
};
'''

res = call_bb('execute_script', {'code': code})
print(json.dumps(res['result'], indent=2))
