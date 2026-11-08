import os
import sys
import json
import uuid
import math
import shutil
import base64
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Add staff_thrust to path for math utilities
STAFF_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
if STAFF_DIR not in sys.path:
    sys.path.append(STAFF_DIR)

from solve_ready_pose_ik import solve_2bone_ik, euler_from_matrix_zyx, rotation_matrix_zyx

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\fire_jab"
BBMODEL_PATH = os.path.join(OUTPUT_DIR, "player_fire_jab_study.bbmodel")
BRAIN_DIR = r"C:\Users\USER\.gemini\antigravity\brain\54a80670-a4c4-4299-bd5f-db191f100d71"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

def new_uuid():
    return str(uuid.uuid4())

def make_faces(dx, dy, dz):
    return {
        "north": {"uv": [0, 0, dx, dy], "texture": False},
        "east":  {"uv": [0, 0, dz, dy], "texture": False},
        "south": {"uv": [0, 0, dx, dy], "texture": False},
        "west":  {"uv": [0, 0, dz, dy], "texture": False},
        "up":    {"uv": [0, 0, dx, dz], "texture": False},
        "down":  {"uv": [0, 0, dx, dz], "texture": False}
    }

# ==============================================================================
# 1. BUILD EMPTY-HANDED BBMODEL (NO STAFF)
# ==============================================================================
c_torso = new_uuid()
c_head = new_uuid()
c_ru = new_uuid()
c_rf = new_uuid()
c_lu = new_uuid()
c_lf = new_uuid()
c_rleg = new_uuid()
c_lleg = new_uuid()

g_torso = new_uuid()
g_head = new_uuid()
g_ru = new_uuid()
g_rf = new_uuid()
g_lu = new_uuid()
g_lf = new_uuid()
g_rleg = new_uuid()
g_lleg = new_uuid()

elements = [
    {"name": "torso", "box_uv": False, "uuid": c_torso, "from": [-4, 12, -2], "to": [4, 24, 2], "origin": [0, 12, 0], "color": 0, "faces": make_faces(8, 12, 4)},
    {"name": "head", "box_uv": False, "uuid": c_head, "from": [-4, 24, -4], "to": [4, 32, 4], "origin": [0, 24, 0], "color": 1, "faces": make_faces(8, 8, 8)},
    {"name": "right_upper_arm", "box_uv": False, "uuid": c_ru, "from": [4, 16, -2], "to": [8, 22, 2], "origin": [5, 22, 0], "color": 3, "faces": make_faces(4, 6, 4)},
    {"name": "right_forearm", "box_uv": False, "uuid": c_rf, "from": [4, 10, -2], "to": [8, 16, 2], "origin": [5, 16, 0], "color": 4, "faces": make_faces(4, 6, 4)},
    {"name": "left_upper_arm", "box_uv": False, "uuid": c_lu, "from": [-8, 16, -2], "to": [-4, 22, 2], "origin": [-5, 22, 0], "color": 5, "faces": make_faces(4, 6, 4)},
    {"name": "left_forearm", "box_uv": False, "uuid": c_lf, "from": [-8, 10, -2], "to": [-4, 16, 2], "origin": [-5, 16, 0], "color": 6, "faces": make_faces(4, 6, 4)},
    {"name": "right_leg", "box_uv": False, "uuid": c_rleg, "from": [0, 0, -2], "to": [4, 12, 2], "origin": [2, 12, 0], "color": 7, "faces": make_faces(4, 12, 4)},
    {"name": "left_leg", "box_uv": False, "uuid": c_lleg, "from": [-4, 0, -2], "to": [0, 12, 2], "origin": [-2, 12, 0], "color": 8, "faces": make_faces(4, 12, 4)}
]

outliner = [
    {
        "name": "torso",
        "uuid": g_torso,
        "origin": [0, 12, 0],
        "rotation": [0, 0, 0],
        "children": [
            c_torso,
            {"name": "head", "uuid": g_head, "origin": [0, 24, 0], "rotation": [0, 0, 0], "children": [c_head]},
            {
                "name": "right_upper_arm",
                "uuid": g_ru,
                "origin": [5, 22, 0],
                "rotation": [0, 0, 0],
                "children": [
                    c_ru,
                    {"name": "right_forearm", "uuid": g_rf, "origin": [5, 16, 0], "rotation": [0, 0, 0], "children": [c_rf]}
                ]
            },
            {
                "name": "left_upper_arm",
                "uuid": g_lu,
                "origin": [-5, 22, 0],
                "rotation": [0, 0, 0],
                "children": [
                    c_lu,
                    {"name": "left_forearm", "uuid": g_lf, "origin": [-5, 16, 0], "rotation": [0, 0, 0], "children": [c_lf]}
                ]
            }
        ]
    },
    {"name": "right_leg", "uuid": g_rleg, "origin": [2, 12, 0], "rotation": [0, 0, 0], "children": [c_rleg]},
    {"name": "left_leg", "uuid": g_lleg, "origin": [-2, 12, 0], "rotation": [0, 0, 0], "children": [c_lleg]}
]

bb_model = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730985000,
        "model_format": "modded_entity",
        "box_uv": False
    },
    "name": "player_fire_jab_study",
    "geometry_name": "player_fire_jab",
    "visible_box": [2, 3, 2],
    "resolution": {"width": 64, "height": 64},
    "elements": elements,
    "outliner": outliner,
    "animations": []
}

with open(BBMODEL_PATH, "w", encoding="utf-8") as f:
    json.dump(bb_model, f, indent=2)

print(f"Generated clean empty-handed model: {BBMODEL_PATH}")

# ==============================================================================
# 2. KINEMATICS DEFINITION FOR 4 KEY PHASES OF FIRE JAB
# Timing contract from SkillTimeline & skill_definitions.json:
#   Phase 1: Ready / Stance (t = 0 ticks, 0.00s) - Stance tangan kosong
#   Phase 2: Anticipation / Windup (t = 2 ticks, 0.10s) - Coiling torso, tarikan tinju kanan
#   Phase 3: Active / Strike (t = 3 ticks, 0.15s) - Full extension, Flame & Hitbox event di tick 1 Active
#   Phase 4: Recovery (t = 4 ticks, 0.20s) - Recoil snap back ke stance siap
# Total duration: 9 ticks = 0.45s
# ==============================================================================

def solve_phase(torso_rot, head_rot, rw_target, lw_target, rleg_rot, lleg_rot):
    # Torso
    R_torso = rotation_matrix_zyx(torso_rot[0], torso_rot[1], torso_rot[2])
    torso_pivot = np.array([0.0, 12.0, 0.0])
    
    # Shoulders in world
    s_ru_world = torso_pivot + R_torso @ np.array([5.0, 10.0, 0.0])
    s_lu_world = torso_pivot + R_torso @ np.array([-5.0, 10.0, 0.0])
    
    # IK arms (right: striking, left: guard)
    ik_r = solve_2bone_ik(s_ru_world, np.array(rw_target), pole_hint=np.array([1.0, -0.2, 0.5]))
    ik_l = solve_2bone_ik(s_lu_world, np.array(lw_target), pole_hint=np.array([-1.0, -0.2, -0.5]))
    
    # Local upper arm rotation
    R_ru_local = R_torso.T @ ik_r['R_upper']
    R_lu_local = R_torso.T @ ik_l['R_upper']
    
    euler_ru = euler_from_matrix_zyx(R_ru_local)
    euler_rf = ik_r['euler_forearm']
    euler_lu = euler_from_matrix_zyx(R_lu_local)
    euler_lf = ik_l['euler_forearm']
    
    # Knuckles / Flame emit point: 2u past right wrist along forearm direction
    v_rf = (np.array(rw_target) - ik_r['elbow']) / 6.0
    flame_emit_point = np.array(rw_target) + v_rf * 2.0
    
    # Leg endpoints
    R_rleg = rotation_matrix_zyx(rleg_rot[0], rleg_rot[1], rleg_rot[2])
    R_lleg = rotation_matrix_zyx(lleg_rot[0], lleg_rot[1], lleg_rot[2])
    r_foot = np.array([2.0, 12.0, 0.0]) + R_rleg @ np.array([0.0, -12.0, 0.0])
    l_foot = np.array([-2.0, 12.0, 0.0]) + R_lleg @ np.array([0.0, -12.0, 0.0])
    
    return {
        "torso": torso_rot,
        "head": head_rot,
        "right_upper_arm": [round(float(x), 2) for x in euler_ru],
        "right_forearm": [round(float(x), 2) for x in euler_rf],
        "left_upper_arm": [round(float(x), 2) for x in euler_lu],
        "left_forearm": [round(float(x), 2) for x in euler_lf],
        "right_leg": rleg_rot,
        "left_leg": lleg_rot,
        "telemetry": {
            "right_shoulder": [round(float(x), 2) for x in s_ru_world],
            "right_elbow": [round(float(x), 2) for x in ik_r['elbow']],
            "right_wrist": [round(float(x), 2) for x in rw_target],
            "flame_emit": [round(float(x), 2) for x in flame_emit_point],
            "left_shoulder": [round(float(x), 2) for x in s_lu_world],
            "left_elbow": [round(float(x), 2) for x in ik_l['elbow']],
            "left_wrist": [round(float(x), 2) for x in lw_target],
            "right_foot": [round(float(x), 2) for x in r_foot],
            "left_foot": [round(float(x), 2) for x in l_foot]
        }
    }

phases = {
    "1_Ready": solve_phase(
        torso_rot=[0.0, -20.0, 0.0],
        head_rot=[0.0, 20.0, 0.0],
        rw_target=[4.5, 13.0, 1.0],      # Right fist chambered at hip/ribs
        lw_target=[-1.5, 17.5, -4.5],    # Left fist guard in front of chest/chin
        rleg_rot=[10.0, -10.0, 0.0],
        lleg_rot=[-12.0, -10.0, 0.0]
    ),
    "2_Anticipation": solve_phase(
        torso_rot=[4.0, -35.0, 0.0],     # Torso coiling deeper (-35 deg)
        head_rot=[-4.0, 35.0, 0.0],      # Head locked forward
        rw_target=[5.2, 13.5, 3.2],      # Right fist pulled back to coil
        lw_target=[-1.0, 18.0, -5.0],    # Left guard held high
        rleg_rot=[15.0, -15.0, 0.0],
        lleg_rot=[-15.0, -15.0, 0.0]
    ),
    "3_Strike": solve_phase(
        torso_rot=[2.0, 12.0, 0.0],      # Explosive hip & torso drive (+12 deg)
        head_rot=[-2.0, -12.0, 0.0],     # Focus forward
        rw_target=[0.5, 16.5, -10.2],    # Right fist extended straight forward!
        lw_target=[-4.5, 12.5, 1.5],     # Left fist recoils to left hip
        rleg_rot=[20.0, 10.0, 0.0],      # Rear leg drive
        lleg_rot=[-10.0, 5.0, 0.0]       # Lead leg planted
    ),
    "4_Recovery": solve_phase(
        torso_rot=[0.0, -15.0, 0.0],
        head_rot=[0.0, 15.0, 0.0],
        rw_target=[3.5, 14.0, -2.0],     # Right fist snapping back
        lw_target=[-2.5, 16.0, -2.5],    # Left guard returning
        rleg_rot=[8.0, -8.0, 0.0],
        lleg_rot=[-10.0, -8.0, 0.0]
    )
}

DATA_JSON_PATH = os.path.join(OUTPUT_DIR, "fire_jab_blocking_data.json")
with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(phases, f, indent=2)

print("Saved kinematic blocking data:", DATA_JSON_PATH)

# ==============================================================================
# 3. GENERATE 4-PANEL STORYBOARD IMAGES (FRONT & SIDE)
# ==============================================================================

def draw_stick_figure(draw, phase_data, ox, oy, scale, phase_key, view='front'):
    c_torso = (70, 130, 220)
    c_head = (235, 195, 140)
    c_r_arm = (240, 80, 40)       # Red-orange striking arm
    c_l_arm = (80, 180, 90)       # Green guard arm
    c_r_leg = (90, 100, 180)
    c_l_leg = (120, 130, 210)
    c_flame = (255, 120, 0)
    
    t = phase_data["telemetry"]
    
    def project(pt):
        # pt: [x, y, z], Minecraft coords: y is up, z is depth (into screen is -z)
        if view == 'front':
            px = ox + pt[0] * scale
            py = oy - (pt[1] - 12.0) * scale # centered around waist Y=12
        else: # side view: looking from right (+X towards -X), horizontal is -Z
            px = ox - pt[2] * scale
            py = oy - (pt[1] - 12.0) * scale
        return (int(round(px)), int(round(py)))
    
    # Head & Torso
    head_center = project([0, 28, 0])
    torso_top = project([0, 24, 0])
    torso_bot = project([0, 12, 0])
    
    # Draw Legs first
    r_hip = project([2, 12, 0])
    l_hip = project([-2, 12, 0])
    r_foot = project(t["right_foot"])
    l_foot = project(t["left_foot"])
    
    draw.line([r_hip, r_foot], fill=c_r_leg, width=int(5 * scale / 12))
    draw.line([l_hip, l_foot], fill=c_l_leg, width=int(5 * scale / 12))
    draw.ellipse([r_foot[0]-3, r_foot[1]-3, r_foot[0]+3, r_foot[1]+3], fill=(130, 140, 220))
    draw.ellipse([l_foot[0]-3, l_foot[1]-3, l_foot[0]+3, l_foot[1]+3], fill=(160, 170, 250))
    
    # Draw Torso
    draw.line([torso_top, torso_bot], fill=c_torso, width=int(10 * scale / 12))
    
    # Draw Head
    r_head = int(4 * scale)
    draw.ellipse([head_center[0] - r_head, head_center[1] - r_head, head_center[0] + r_head, head_center[1] + r_head], fill=c_head, outline=(120, 90, 60), width=2)
    
    # Left Arm (Guard Arm)
    ls = project(t["left_shoulder"])
    le = project(t["left_elbow"])
    lw = project(t["left_wrist"])
    draw.line([ls, le], fill=c_l_arm, width=int(5 * scale / 12))
    draw.line([le, lw], fill=c_l_arm, width=int(5 * scale / 12))
    draw.ellipse([lw[0]-3, lw[1]-3, lw[0]+3, lw[1]+3], fill=(120, 220, 120))
    
    # Right Arm (Striking Arm)
    rs = project(t["right_shoulder"])
    re = project(t["right_elbow"])
    rw = project(t["right_wrist"])
    fe = project(t["flame_emit"])
    draw.line([rs, re], fill=c_r_arm, width=int(7 * scale / 12))
    draw.line([re, rw], fill=c_r_arm, width=int(6 * scale / 12))
    draw.ellipse([rw[0]-4, rw[1]-4, rw[0]+4, rw[1]+4], fill=(255, 100, 40))
    
    # Flame burst on Strike
    if "Strike" in phase_key:
        draw.line([rw, fe], fill=(255, 230, 70), width=4)
        draw.ellipse([fe[0]-8, fe[1]-8, fe[0]+8, fe[1]+8], fill=(255, 230, 80))
        # Particle sparks
        if view == 'side':
            draw.line([fe, (fe[0]+int(20*scale/12), fe[1]-int(10*scale/12))], fill=c_flame, width=3)
            draw.line([fe, (fe[0]+int(20*scale/12), fe[1]+int(10*scale/12))], fill=c_flame, width=3)
            draw.line([fe, (fe[0]+int(28*scale/12), fe[1])], fill=(255, 200, 0), width=4)
        else:
            draw.line([fe, (fe[0]+int(12*scale/12), fe[1]-int(8*scale/12))], fill=c_flame, width=3)
            draw.line([fe, (fe[0]-int(12*scale/12), fe[1]+int(8*scale/12))], fill=c_flame, width=3)

W, H = 1200, 560
img_front = Image.new("RGBA", (W, H), (24, 26, 34, 255))
img_side  = Image.new("RGBA", (W, H), (24, 26, 34, 255))

draw_f = ImageDraw.Draw(img_front)
draw_s = ImageDraw.Draw(img_side)

panel_w = W // 4
phase_keys = ["1_Ready", "2_Anticipation", "3_Strike", "4_Recovery"]
phase_titles = [
    "Phase 1: Ready Stance\n(t = 0t / 0.00s)\nTangan Kosong",
    "Phase 2: Anticipation\n(t = 2t / 0.10s)\nCoiling & Windup",
    "Phase 3: Active Strike\n(t = 3t / 0.15s)\nFlame Burst & Hitbox",
    "Phase 4: Recovery\n(t = 4t / 0.20s)\nSnap Back Recoil"
]

scale = 13.0

for i, (pkey, title) in enumerate(zip(phase_keys, phase_titles)):
    pdata = phases[pkey]
    cx = i * panel_w + panel_w // 2
    cy = H // 2 + 25
    
    # Vertical divider
    draw_f.line([(i * panel_w, 0), (i * panel_w, H)], fill=(40, 44, 56), width=1)
    draw_s.line([(i * panel_w, 0), (i * panel_w, H)], fill=(40, 44, 56), width=1)
    
    # Title
    draw_f.text((i * panel_w + 12, 20), title, fill=(225, 230, 245))
    draw_s.text((i * panel_w + 12, 20), title, fill=(225, 230, 245))
    
    # Ground plane
    ground_y = cy - (0.0 - 12.0) * scale
    draw_f.line([(i * panel_w + 15, ground_y), ((i+1) * panel_w - 15, ground_y)], fill=(60, 65, 80), width=2)
    draw_s.line([(i * panel_w + 15, ground_y), ((i+1) * panel_w - 15, ground_y)], fill=(60, 65, 80), width=2)
    
    draw_stick_figure(draw_f, pdata, cx, cy, scale, pkey, view='front')
    draw_stick_figure(draw_s, pdata, cx, cy, scale, pkey, view='side')

front_path = os.path.join(OUTPUT_DIR, "fire_jab_storyboard_front.png")
side_path  = os.path.join(OUTPUT_DIR, "fire_jab_storyboard_side.png")
img_front.save(front_path)
img_side.save(side_path)

shutil.copyfile(front_path, os.path.join(BRAIN_DIR, "fire_jab_storyboard_front.png"))
shutil.copyfile(side_path,  os.path.join(BRAIN_DIR, "fire_jab_storyboard_side.png"))

print("Saved front storyboard:", front_path)
print("Saved side storyboard :", side_path)

# ==============================================================================
# 4. RENDER ACTUAL 3D SHOTS FROM BLOCKBENCH VIA HTTP BRIDGE (PORT 8787)
# ==============================================================================

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

try:
    print("Connecting to Blockbench on port 8787...")
    res = call_bb('load_project', {'path': BBMODEL_PATH})
    print("Loaded project into Blockbench:", res.get('ok'))
    
    # Helper to apply pose to Blockbench groups
    apply_pose_script = '''
    function applyPose(pose) {
        let torso = Group.all.find(g => g.name === 'torso');
        let head = Group.all.find(g => g.name === 'head');
        let ru = Group.all.find(g => g.name === 'right_upper_arm');
        let rf = Group.all.find(g => g.name === 'right_forearm');
        let lu = Group.all.find(g => g.name === 'left_upper_arm');
        let lf = Group.all.find(g => g.name === 'left_forearm');
        let rleg = Group.all.find(g => g.name === 'right_leg');
        let lleg = Group.all.find(g => g.name === 'left_leg');
        
        if (torso) torso.rotation = pose.torso;
        if (head) head.rotation = pose.head;
        if (ru) ru.rotation = pose.right_upper_arm;
        if (rf) rf.rotation = pose.right_forearm;
        if (lu) lu.rotation = pose.left_upper_arm;
        if (lf) lf.rotation = pose.left_forearm;
        if (rleg) rleg.rotation = pose.right_leg;
        if (lleg) lleg.rotation = pose.left_leg;
        
        Canvas.updateAllBones();
        unselectAll();
        Canvas.show_gizmos = false;
        Canvas.show_element_markers = false;
        Canvas.updateView();
    }
    '''
    
    # 4A. Render 3D views for Strike Phase (Peak action pose)
    strike_pose = phases["3_Strike"]
    apply_strike_code = apply_pose_script + f"\napplyPose({json.dumps(strike_pose)});\n"
    call_bb('execute_script', {'code': apply_strike_code})
    
    views = [
        ('front', 'fire_jab_strike_front.png'),
        ('right', 'fire_jab_strike_side.png'),
        ('front_right', 'fire_jab_strike_perspective.png')
    ]
    
    for view_name, file_name in views:
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
            print(f"Captured 3D Strike {view_name} -> {dest_brain}")
            
    # 4B. Render 3D views for Ready Phase (Empty-handed stance)
    ready_pose = phases["1_Ready"]
    apply_ready_code = apply_pose_script + f"\napplyPose({json.dumps(ready_pose)});\n"
    call_bb('execute_script', {'code': apply_ready_code})
    
    views_ready = [
        ('front', 'fire_jab_ready_front.png'),
        ('right', 'fire_jab_ready_side.png'),
        ('front_right', 'fire_jab_ready_perspective.png')
    ]
    for view_name, file_name in views_ready:
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
            print(f"Captured 3D Ready {view_name} -> {dest_brain}")

except Exception as e:
    print(f"Blockbench bridge warning: {e}")

print("Fire Jab blocking study generation complete!")
