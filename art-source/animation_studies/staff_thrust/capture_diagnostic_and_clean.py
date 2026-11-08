import urllib.request
import json
import base64
import os

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
BRAIN_DIR = r"C:\Users\USER\.gemini\antigravity\brain\54a80670-a4c4-4299-bd5f-db191f100d71"

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

# 1. Add markers
code_add_markers = '''
let rf = Group.all.find(g => g.name === 'right_forearm');
let lf = Group.all.find(g => g.name === 'left_forearm');
let staff = Group.all.find(g => g.name === 'staff_assembly');

rf.mesh.updateMatrixWorld(true);
lf.mesh.updateMatrixWorld(true);
staff.mesh.updateMatrixWorld(true);

let local_wrist = new THREE.Vector3(0, -6, 0);
let rw = local_wrist.clone().applyMatrix4(rf.mesh.matrixWorld);
let lw = local_wrist.clone().applyMatrix4(lf.mesh.matrixWorld);

let rg = new THREE.Vector3(0, 13.0, 0).applyMatrix4(staff.mesh.matrixWorld);
let lg = new THREE.Vector3(0, 21.5, 0).applyMatrix4(staff.mesh.matrixWorld);

let old_m = scene.getObjectByName('diagnostic_markers');
if (old_m) scene.remove(old_m);

let marker_grp = new THREE.Group();
marker_grp.name = 'diagnostic_markers';

function makeMarker(pos, colorHex, size) {
    let g = new THREE.BoxGeometry(size, size, size);
    let m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: colorHex, wireframe: false, depthTest: false }));
    m.position.copy(pos);
    m.renderOrder = 999;
    return m;
}

// 1. Right wrist (Green): Hand attachment
marker_grp.add(makeMarker(rw, 0x00FF00, 1.4));
// 2. Rear staff grip (Yellow): Staff point
marker_grp.add(makeMarker(rg, 0xFFFF00, 1.0));
// 3. Left wrist (Cyan): Hand attachment
marker_grp.add(makeMarker(lw, 0x00FFFF, 1.4));
// 4. Lead staff grip (Magenta): Staff point
marker_grp.add(makeMarker(lg, 0xFF00FF, 1.0));

scene.add(marker_grp);

unselectAll();
Canvas.show_gizmos = false;
Canvas.show_element_markers = false;

return {
    rw: [rw.x, rw.y, rw.z],
    rg: [rg.x, rg.y, rg.z],
    lw: [lw.x, lw.y, lw.z],
    lg: [lg.x, lg.y, lg.z]
};
'''

res = call_bb('execute_script', {'code': code_add_markers})
print("Added markers:", res)

# 2. Capture diagnostic perspective screenshot WITH MARKERS
shot_diag = call_bb('screenshot', {'view': 'front_right', 'width': 800, 'height': 800, 'annotate': False})
if shot_diag.get('ok'):
    b64 = shot_diag['result']['base64']
    dest_local = os.path.join(OUTPUT_DIR, 'ready_diagnostic_perspective.png')
    dest_brain = os.path.join(BRAIN_DIR, 'ready_diagnostic_perspective.png')
    data = base64.b64decode(b64)
    with open(dest_local, 'wb') as f:
        f.write(data)
    with open(dest_brain, 'wb') as f:
        f.write(data)
    print("Saved diagnostic screenshot with markers: ready_diagnostic_perspective.png")

# 3. Remove markers
code_remove = '''
let m = scene.getObjectByName('diagnostic_markers');
if (m) scene.remove(m);
'''
call_bb('execute_script', {'code': code_remove})

# 4. Capture clean views
clean_views = [
    ('front', 'ready_clean_front.png'),
    ('right', 'ready_clean_side.png'),
    ('front_right', 'ready_clean_perspective.png')
]

for view_name, file_name in clean_views:
    shot = call_bb('screenshot', {'view': view_name, 'width': 800, 'height': 800, 'annotate': False})
    if shot.get('ok'):
        b64 = shot['result']['base64']
        dest_local = os.path.join(OUTPUT_DIR, file_name)
        dest_brain = os.path.join(BRAIN_DIR, file_name)
        data = base64.b64decode(b64)
        with open(dest_local, 'wb') as f:
            f.write(data)
        with open(dest_brain, 'wb') as f:
            f.write(data)
        print(f"Saved clean {view_name} -> {dest_brain}")
