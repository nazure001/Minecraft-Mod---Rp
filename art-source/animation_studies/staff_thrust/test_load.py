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

model_path = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready_artistic.bbmodel'
res = call_bb('load_project', {'path': model_path})
print('load_project:', res)

check_code = '''
return {
    project_name: Project ? Project.name : null,
    groups: Group.all.map(g => g.name),
    cubes: Cube.all.map(c => ({ name: c.name, parent: c.parent ? c.parent.name : null }))
};
'''
print('after load:', call_bb('execute_script', {'code': check_code}))
