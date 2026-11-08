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
if (!staff) return { error: "No staff_assembly found" };
staff.mesh.updateMatrixWorld(true);

let results = [];
staff.children.filter(c => c instanceof Cube).forEach(c => {
    c.mesh.updateMatrixWorld(true);
    let box = new THREE.Box3().setFromObject(c.mesh);
    results.push({
        name: c.name,
        from: c.from,
        to: c.to,
        origin: c.origin,
        mesh_pos: [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z],
        world_box: {
            min: [box.min.x, box.min.y, box.min.z],
            max: [box.max.x, box.max.y, box.max.z]
        }
    });
});

return {
    project_name: Project ? Project.name : null,
    staff_group_origin: staff.origin,
    staff_group_rotation: staff.rotation,
    staff_mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    cubes: results
};
'''

res = call_bb('execute_script', {'code': code})
print('res:', res)
