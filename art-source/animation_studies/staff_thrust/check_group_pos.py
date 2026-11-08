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
    origin: staff.origin,
    has_pos: !!staff.position,
    mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    keys: Object.keys(staff)
};
'''

res = call_bb('execute_script', {'code': code})
print('Staff group keys & pos:', res)
