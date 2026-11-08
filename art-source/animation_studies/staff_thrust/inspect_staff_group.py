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
return {
    staff_origin: [staff.origin[0], staff.origin[1], staff.origin[2]],
    staff_rotation: staff.rotation,
    mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    cubes: staff.children.filter(c => c instanceof Cube).map(c => ({
        name: c.name,
        from: c.from,
        to: c.to,
        mesh_pos: [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z]
    }))
};
'''

res = call_bb('execute_script', {'code': code})
print('Staff group structure in Blockbench:')
print(json.dumps(res, indent=2))
