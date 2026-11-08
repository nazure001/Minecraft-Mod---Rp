import urllib.request
import json
import base64
import os

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

# Make sure project is player_staff_thrust_ready.bbmodel
model_path = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready.bbmodel'
call_bb('load_project', {'path': model_path})

# Clear selection and ensure no gizmos are shown
call_bb('execute_script', {'code': '''
unselectAll();
Canvas.show_gizmos = false;
Canvas.show_element_markers = false;
Canvas.updateView();
'''})

output_dir = r'D:/repo/Minecraft Mod & Rp/art-source/animation_studies/staff_thrust'
brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

views = [
    ('front', 'ready_pose_clean_front.png'),
    ('right', 'ready_pose_clean_side.png'),
    ('front_right', 'ready_pose_clean_perspective.png')
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
        print(f"Captured clean {view_name} -> {dest_brain} ({len(data)} bytes)")
    else:
        print(f"Failed {view_name}: {shot}")
