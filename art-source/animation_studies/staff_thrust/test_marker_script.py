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

code_test = '''
try {
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

    marker_grp.add(makeMarker(rw, 0x00FF00, 1.4));
    marker_grp.add(makeMarker(rg, 0xFFFF00, 1.0));
    marker_grp.add(makeMarker(lw, 0x00FFFF, 1.4));
    marker_grp.add(makeMarker(lg, 0xFF00FF, 1.0));

    scene.add(marker_grp);

    unselectAll();
    Canvas.show_gizmos = false;
    Canvas.show_element_markers = false;
    Canvas.updateView();

    return { ok: true, rw: [rw.x, rw.y, rw.z] };
} catch(e) {
    return { ok: false, err: e.message, stack: e.stack };
}
'''
print(call_bb('execute_script', {'code': code_test}))
