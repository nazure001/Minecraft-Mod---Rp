import json
import urllib.request
import os

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
READY_ARTISTIC_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_ready_artistic.bbmodel")

with open(READY_ARTISTIC_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find staff group in data['groups']
staff_grp = None
for g in data.get("groups", []):
    if g["name"] == "staff_assembly":
        staff_grp = g
        break

if not staff_grp:
    # If not in groups, check outliner
    for g in data.get("outliner", []):
        if g.get("name") == "staff_assembly":
            staff_grp = g
            break

print("Found staff_grp:", staff_grp["name"], "origin:", staff_grp["origin"])
so = staff_grp["origin"]

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
        elem["origin"] = [so[0], so[1], so[2]]
        elem["from"] = [round(so[0] + l_min[0], 4), round(so[1] + l_min[1], 4), round(so[2] + l_min[2], 4)]
        elem["to"]   = [round(so[0] + l_max[0], 4), round(so[1] + l_max[1], 4), round(so[2] + l_max[2], 4)]

with open(READY_ARTISTIC_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved fixed player_staff_thrust_ready_artistic.bbmodel")

# Now load into Blockbench and inspect actual Three.js world bounding boxes
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

call_bb('load_project', {'path': READY_ARTISTIC_PATH})

check_code = '''
let staff = Group.all.find(g => g.name === 'staff_assembly');
staff.mesh.updateMatrixWorld(true);

let rf = Group.all.find(g => g.name === 'right_forearm');
let lf = Group.all.find(g => g.name === 'left_forearm');
rf.mesh.updateMatrixWorld(true);
lf.mesh.updateMatrixWorld(true);

let local_wrist = new THREE.Vector3(0, -6, 0);
let rw = local_wrist.clone().applyMatrix4(rf.mesh.matrixWorld);
let lw = local_wrist.clone().applyMatrix4(lf.mesh.matrixWorld);

let cubes_info = staff.children.filter(c => c instanceof Cube).map(c => {
    c.mesh.updateMatrixWorld(true);
    let box = new THREE.Box3().setFromObject(c.mesh);
    return {
        name: c.name,
        mesh_pos: [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z],
        world_box: {
            min: [box.min.x, box.min.y, box.min.z],
            max: [box.max.x, box.max.y, box.max.z]
        }
    };
});

return {
    staff_mesh_pos: [staff.mesh.position.x, staff.mesh.position.y, staff.mesh.position.z],
    right_wrist: [rw.x, rw.y, rw.z],
    left_wrist: [lw.x, lw.y, lw.z],
    cubes: cubes_info
};
'''

res = call_bb('execute_script', {'code': check_code})
print("Result in Blockbench Three.js:")
print(json.dumps(res['result'], indent=2))
