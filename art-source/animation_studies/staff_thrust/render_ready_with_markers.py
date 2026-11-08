import urllib.request
import json
import base64
import os
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

# 1. Update the bbmodel file on disk with the corrected cube definitions
OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
READY_ARTISTIC_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready_artistic.bbmodel")
BRAIN_DIR = r"C:\Users\USER\.gemini\antigravity\brain\54a80670-a4c4-4299-bd5f-db191f100d71"

with open(READY_ARTISTIC_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find staff group origin
staff_group = None
for g in data["outliner"]:
    if g.get("name") == "staff_assembly":
        staff_group = g
        break

staff_origin = staff_group["origin"] # e.g. [11.0423, 7.6923, 11.8315] or similar

# Staff cube local definitions
staff_defs = {
    "staff_lower_cap":   ([-1.0, 0.0, -1.0], [1.0, 1.0, 1.0]),
    "staff_lower_shaft": ([-0.75, 1.0, -0.75], [0.75, 12.0, 0.75]),
    "staff_grip_wrap":   ([-1.0, 12.0, -1.0], [1.0, 18.0, 1.0]),
    "staff_upper_shaft": ([-0.75, 18.0, -0.75], [0.75, 29.0, 0.75]),
    "staff_upper_cap":   ([-1.0, 29.0, -1.0], [1.0, 30.0, 1.0]),
}

for elem in data["elements"]:
    if elem["name"] in staff_defs:
        l_min, l_max = staff_defs[elem["name"]]
        elem["origin"] = [staff_origin[0], staff_origin[1], staff_origin[2]]
        elem["from"] = [round(staff_origin[0] + l_min[0], 4), round(staff_origin[1] + l_min[1], 4), round(staff_origin[2] + l_min[2], 4)]
        elem["to"]   = [round(staff_origin[0] + l_max[0], 4), round(staff_origin[1] + l_max[1], 4), round(staff_origin[2] + l_max[2], 4)]

with open(READY_ARTISTIC_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Updated player_staff_thrust_ready_artistic.bbmodel with matching cube origins!")

# 2. Reload project in Blockbench
call_bb('load_project', {'path': READY_ARTISTIC_PATH})

# 3. Add visual markers directly in Blockbench Three.js scene
code_markers = '''
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

// Remove old markers if any
let old_marker_grp = scene.getObjectByName('diagnostic_markers');
if (old_marker_grp) scene.remove(old_marker_grp);

let marker_grp = new THREE.Group();
marker_grp.name = 'diagnostic_markers';

function createMarker(pos, colorHex, size) {
    let geom = new THREE.BoxGeometry(size, size, size);
    let mat = new THREE.MeshBasicMaterial({ color: colorHex, wireframe: false, depthTest: false });
    let m = new THREE.Mesh(geom, mat);
    m.position.copy(pos);
    m.renderOrder = 999;
    return m;
}

// 1. Right wrist (Rear Hand Attachment): Green (0x00FF00)
marker_grp.add(createMarker(rw, 0x00FF00, 1.2));
// 2. Rear staff grip (Staff Axis Point): Yellow (0xFFFF00)
marker_grp.add(createMarker(rg, 0xFFFF00, 0.9));
// 3. Left wrist (Lead Hand Attachment): Cyan (0x00FFFF)
marker_grp.add(createMarker(lw, 0x00FFFF, 1.2));
// 4. Lead staff grip (Staff Axis Point): Magenta (0xFF00FF)
marker_grp.add(createMarker(lg, 0xFF00FF, 0.9));

scene.add(marker_grp);

unselectAll();
Canvas.show_gizmos = false;
Canvas.show_element_markers = false;
Canvas.updateView();

return {
    rear_wrist: [rw.x, rw.y, rw.z],
    rear_staff_grip: [rg.x, rg.y, rg.z],
    lead_wrist: [lw.x, lw.y, lw.z],
    lead_staff_grip: [lg.x, lg.y, lg.z]
};
'''

telemetry = call_bb('execute_script', {'code': code_markers})['result']
print("Telemetry with markers:", telemetry)

# 4. Capture DIAGNOSTIC perspective screenshot WITH MARKERS
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

# 5. Remove markers and capture pristine clean screenshots: front, right, perspective
code_remove_markers = '''
let marker_grp = scene.getObjectByName('diagnostic_markers');
if (marker_grp) scene.remove(marker_grp);
Canvas.updateView();
'''
call_bb('execute_script', {'code': code_remove_markers})

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
