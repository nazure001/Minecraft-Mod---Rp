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
return {
    project_name: Project ? Project.name : null,
    groups: Group.all.map(g => g.name),
    cubes: Cube.all.map(c => c.name)
};
'''
res = call_bb('execute_script', {'code': code})
print(json.dumps(res['result'], indent=2))
