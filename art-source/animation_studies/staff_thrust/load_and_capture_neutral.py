import urllib.request
import json
import base64
import os
import shutil

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

# 1. Load project
model_path = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_neutral.bbmodel'
load_res = call_bb('load_project', {'path': model_path})
print('Loaded project:', load_res)

# 2. Check geometry groups of all cubes in Blockbench
check_code = '''
return Cube.all.map(c => ({
    name: c.name,
    visible: c.visibility,
    mesh_visible: c.mesh ? c.mesh.visible : false,
    groups_count: c.mesh && c.mesh.geometry ? c.mesh.geometry.groups.length : 0,
    world_bounds: (() => {
        if (!c.mesh) return null;
        let b = new THREE.Box3().setFromObject(c.mesh);
        return { min: [b.min.x, b.min.y, b.min.z], max: [b.max.x, b.max.y, b.max.z] };
    })()
}));
'''
geom_check = call_bb('execute_script', {'code': check_code})
print('Geom check for cubes:')
for c in geom_check.get('result', []):
    print(f" - {c['name']:18s}: groups={c['groups_count']}, bounds={c['world_bounds']}")

# 3. Capture screenshots from front, right, and perspective
output_dir = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust'
brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

views = [
    ('front', 'neutral_rig_front.png'),
    ('right', 'neutral_rig_side.png'),
    ('front_right', 'neutral_rig_perspective.png')
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
        print(f"Captured {view_name} -> {dest_brain} (size: {len(data)} bytes)")
    else:
        print(f"Failed {view_name}: {shot}")
