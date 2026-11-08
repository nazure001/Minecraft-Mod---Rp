import os
import sys
import io
import json
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

# ==============================================================================
# 1. KINEMATICS & KEYFRAME DEFINITION WITH ACCURATE FEET (-Z FORWARD)
# ==============================================================================
# In Minecraft / Blockbench:
# -Z is Forward (arah musuh)
# +Z is Backward (arah belakang)
# Leg rotation: pitch > 0 rotates foot towards -Z (Forward)
#              pitch < 0 rotates foot towards +Z (Backward)
# Lead Leg (Left) is in front: pitch > 0 -> Z_foot < 0 (-Z)
# Rear Leg (Right) is in back: pitch < 0 -> Z_foot > 0 (+Z)

def solve_phase(torso_rot, head_rot, rw_target, lw_target, rleg_rot, lleg_rot):
    R_torso = rotation_matrix_zyx(torso_rot[0], torso_rot[1], torso_rot[2])
    torso_pivot = np.array([0.0, 12.0, 0.0])
    
    # Shoulders in world
    s_ru_world = torso_pivot + R_torso @ np.array([5.0, 10.0, 0.0])
    s_lu_world = torso_pivot + R_torso @ np.array([-5.0, 10.0, 0.0])
    
    # IK arms
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
            "lead_foot_left": [round(float(x), 2) for x in l_foot],
            "rear_foot_right": [round(float(x), 2) for x in r_foot]
        }
    }

# Keyframe 0 (t = 0t, 0.00s): Ready Stance
kf0_ready = solve_phase(
    torso_rot=[0.0, -20.0, 0.0],
    head_rot=[0.0, 20.0, 0.0],
    rw_target=[4.5, 13.0, 1.0],      # Right fist chambered at ribs/hip
    lw_target=[-1.5, 17.5, -4.5],    # Left fist guard in front of chest/chin
    rleg_rot=[-12.0, -10.0, 0.0],    # Rear foot (Right): pitch -12 -> Z > 0 (+2.5u)
    lleg_rot=[12.0, -10.0, 0.0]      # Lead foot (Left): pitch +12 -> Z < 0 (-2.5u)
)

# Keyframe 1 (t = 2t, 0.10s): Anticipation Peak (Windup End)
kf1_anticipation = solve_phase(
    torso_rot=[4.0, -35.0, 0.0],     # Deep torso coil
    head_rot=[-4.0, 35.0, 0.0],      # Head locked forward
    rw_target=[5.2, 13.5, 3.2],      # Right fist pulled back to load momentum
    lw_target=[-1.0, 18.0, -5.0],    # High guard
    rleg_rot=[-15.0, -15.0, 0.0],    # Weight loaded onto rear leg (Right)
    lleg_rot=[15.0, -15.0, 0.0]      # Lead leg (Left) forward
)

# Keyframe 2 (t = 3t, 0.15s): Strike Impact & Flame Burst (Active Tick 1)
kf2_strike = solve_phase(
    torso_rot=[2.0, 12.0, 0.0],      # Explosive hip rotation (+12 deg)
    head_rot=[-2.0, -12.0, 0.0],     # Focus forward
    rw_target=[0.5, 16.5, -10.2],    # Right fist extended straight forward (-10.2u)
    lw_target=[-4.5, 12.5, 1.5],     # Left fist recoiled to left hip
    rleg_rot=[-8.0, 10.0, 0.0],      # Rear leg pushes off ground
    lleg_rot=[16.0, 5.0, 0.0]        # Lead leg firmly planted
)

# Keyframe 3 (t = 5t, 0.25s): Active End / Follow-through (Recovery Start)
kf3_active_end = solve_phase(
    torso_rot=[1.0, 5.0, 0.0],       # Momentum absorbed
    head_rot=[-1.0, -5.0, 0.0],
    rw_target=[2.0, 15.5, -6.5],     # Right fist beginning snap-back
    lw_target=[-3.5, 14.5, -0.5],    # Left guard returning
    rleg_rot=[-10.0, 0.0, 0.0],
    lleg_rot=[14.0, 0.0, 0.0]
)

# Keyframe 4 (t = 9t, 0.45s): Recovery End -> EXACTLY IDENTICAL TO KEYFRAME 0!
kf4_recovery_end = {
    "torso": list(kf0_ready["torso"]),
    "head": list(kf0_ready["head"]),
    "right_upper_arm": list(kf0_ready["right_upper_arm"]),
    "right_forearm": list(kf0_ready["right_forearm"]),
    "left_upper_arm": list(kf0_ready["left_upper_arm"]),
    "left_forearm": list(kf0_ready["left_forearm"]),
    "right_leg": list(kf0_ready["right_leg"]),
    "left_leg": list(kf0_ready["left_leg"]),
    "telemetry": json.loads(json.dumps(kf0_ready["telemetry"]))
}

keyframe_timeline = [
    {"tick": 0.0, "time_s": 0.00, "name": "Keyframe 0: Ready Stance", "pose": kf0_ready},
    {"tick": 2.0, "time_s": 0.10, "name": "Keyframe 1: Anticipation Peak", "pose": kf1_anticipation},
    {"tick": 3.0, "time_s": 0.15, "name": "Keyframe 2: Strike Impact & Flame Event", "pose": kf2_strike},
    {"tick": 5.0, "time_s": 0.25, "name": "Keyframe 3: Active End / Snap Start", "pose": kf3_active_end},
    {"tick": 9.0, "time_s": 0.45, "name": "Keyframe 4: Recovery End (Return to Ready)", "pose": kf4_recovery_end}
]

# Save keyframe dataset
KEYFRAME_JSON_PATH = os.path.join(OUTPUT_DIR, "fire_jab_keyframes.json")
with open(KEYFRAME_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump({
        "timing_specification": {
            "total_duration_ticks": 9,
            "total_duration_seconds": 0.45,
            "tps": 20,
            "phases": [
                {
                    "phase_id": "windup",
                    "name": "Windup / Anticipation",
                    "start_tick": 0,
                    "end_tick": 2,
                    "duration_ticks": 2,
                    "duration_seconds": 0.10,
                    "description": "Coiling torso and chambering right fist"
                },
                {
                    "phase_id": "active",
                    "name": "Active Strike",
                    "start_tick": 2,
                    "end_tick": 5,
                    "duration_ticks": 3,
                    "duration_seconds": 0.15,
                    "event": {
                        "phase_tick": 1,
                        "absolute_tick": 3,
                        "absolute_time_s": 0.15,
                        "type": "HITBOX_AND_FLAME_BURST",
                        "hitbox_range_blocks": 2.5,
                        "damage": 4.0,
                        "knockback": 0.3,
                        "particle": "minecraft:flame",
                        "sound": "minecraft:entity.blaze.shoot"
                    }
                },
                {
                    "phase_id": "recovery",
                    "name": "Recovery / Return",
                    "start_tick": 5,
                    "end_tick": 9,
                    "duration_ticks": 4,
                    "duration_seconds": 0.20,
                    "description": "Snap back to ready stance; 100% matches keyframe 0 at tick 9"
                }
            ]
        },
        "rotation_order": "ZYX",
        "rotation_units": "degrees",
        "coordinate_convention": {
            "forward": "-Z",
            "up": "+Y",
            "right": "+X (entity left is -X, entity right is +X)",
            "lead_foot": "Left foot (pitch > 0, Z < 0 / towards -Z)",
            "rear_foot": "Right foot (pitch < 0, Z > 0 / towards +Z)"
        },
        "keyframes": keyframe_timeline
    }, f, indent=2)

print("Saved clean keyframe dataset to:", KEYFRAME_JSON_PATH)

# ==============================================================================
# 2. INTERPOLATE 18 SAMPLE FRAMES ACROSS 9 TICKS (0.5 TICK PER FRAME)
# ==============================================================================

def lerp(a, b, t):
    return a + (b - a) * t

def s_curve(t):
    return t * t * (3.0 - 2.0 * t)

def interpolate_pose(tick_val):
    # Find surrounding keyframes
    k_prev = keyframe_timeline[0]
    k_next = keyframe_timeline[-1]
    for i in range(len(keyframe_timeline) - 1):
        if keyframe_timeline[i]["tick"] <= tick_val <= keyframe_timeline[i+1]["tick"]:
            k_prev = keyframe_timeline[i]
            k_next = keyframe_timeline[i+1]
            break
            
    t_span = k_next["tick"] - k_prev["tick"]
    alpha = 0.0 if t_span == 0 else (tick_val - k_prev["tick"]) / t_span
    smooth_alpha = s_curve(alpha)
    
    interp = {}
    for bone in ["torso", "head", "right_upper_arm", "right_forearm", "left_upper_arm", "left_forearm", "right_leg", "left_leg"]:
        p_val = k_prev["pose"][bone]
        n_val = k_next["pose"][bone]
        interp[bone] = [round(lerp(p_val[j], n_val[j], smooth_alpha), 2) for j in range(3)]
        
    return interp

# ==============================================================================
# 3. RENDER 3D ANIMATION FRAMES IN BLOCKBENCH VIA HTTP BRIDGE (PORT 8787)
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

# Load project
call_bb('load_project', {'path': BBMODEL_PATH})

num_frames = 18
ticks = np.linspace(0.0, 8.5, num_frames) # 0.0, 0.5, 1.0, ... 8.5 ticks
frames_raw = []

# Font for HUD overlay
font_path_bold = r"C:\Windows\Fonts\arialbd.ttf"
font_path_regular = r"C:\Windows\Fonts\arial.ttf"
try:
    font_bold = ImageFont.truetype(font_path_bold, 18)
    font_large = ImageFont.truetype(font_path_bold, 22)
    font_small = ImageFont.truetype(font_path_regular, 13)
except:
    font_bold = ImageFont.load_default()
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

print("Rendering 18 animation frames via Blockbench...")

for i, tk in enumerate(ticks):
    t_sec = tk / 20.0
    pose = interpolate_pose(tk)
    is_impact_frame = (2.5 <= tk <= 3.5)
    
    # Script to apply pose, compute exact flame anchor from right_forearm matrixWorld,
    # and add flame burst mesh in Blockbench 3D scene!
    script = f'''
    try {{
        let pose = {json.dumps(pose)};
        let is_impact = {str(is_impact_frame).lower()};
        
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
        rf.mesh.updateMatrixWorld(true);
        
        // Knuckles / Flame anchor point: 2u past wrist along forearm
        // In local forearm space, bone extends from Y=0 to Y=-6. Wrist is at [0, -6, 0].
        // 2u further down is [0, -8, 0]
        let flame_local = new THREE.Vector3(0, -8.0, 0);
        let flame_world = flame_local.applyMatrix4(rf.mesh.matrixWorld);
        
        // Remove previous markers
        let old_fx = scene.getObjectByName('flame_tracking_fx');
        if (old_fx) scene.remove(old_fx);
        
        let fx_group = new THREE.Group();
        fx_group.name = 'flame_tracking_fx';
        
        // 1. Glowing anchor cube at knuckles (tracking across all frames!)
        let anchor_geo = new THREE.BoxGeometry(1.6, 1.6, 1.6);
        let anchor_mat = new THREE.MeshBasicMaterial({{ color: 0xFFAA00, depthTest: false }});
        let anchor_mesh = new THREE.Mesh(anchor_geo, anchor_mat);
        anchor_mesh.position.copy(flame_world);
        anchor_mesh.renderOrder = 999;
        fx_group.add(anchor_mesh);
        
        // 2. If impact frame (t = 3t), add flame burst particles spreading forward
        if (is_impact) {{
            let colors = [0xFF2200, 0xFF6600, 0xFFDD00, 0xFFFFFF];
            let offsets = [
                [0, 0, -2.0], [0.8, 0.4, -3.2], [-0.8, -0.4, -3.5],
                [0.4, -0.8, -4.5], [-0.4, 0.8, -4.2], [0, 0, -5.5]
            ];
            for (let j = 0; j < offsets.length; j++) {{
                let off = offsets[j];
                let p_geo = new THREE.BoxGeometry(1.2, 1.2, 1.2);
                let p_mat = new THREE.MeshBasicMaterial({{ color: colors[j % colors.length], depthTest: false }});
                let p_mesh = new THREE.Mesh(p_geo, p_mat);
                p_mesh.position.set(flame_world.x + off[0], flame_world.y + off[1], flame_world.z + off[2]);
                p_mesh.renderOrder = 1000;
                fx_group.add(p_mesh);
            }}
        }}
        
        scene.add(fx_group);
        unselectAll();
        Canvas.show_gizmos = false;
        Canvas.show_element_markers = false;
        Canvas.updatePositions();
        
        return {{ ok: true, flame_world: [flame_world.x, flame_world.y, flame_world.z] }};
    }} catch(e) {{
        return {{ ok: false, err: e.message }};
    }}
    '''
    res = call_bb('execute_script', {'code': script})
    flame_pos = res.get('result', {}).get('flame_world', [0, 0, 0])
    
    # Capture perspective screenshot
    shot = call_bb('screenshot', {'view': 'front_right', 'width': 700, 'height': 700, 'annotate': False})
    if shot.get('ok'):
        b64 = shot['result']['base64']
        img_bytes = base64.b64decode(b64)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        frames_raw.append({
            "image": img,
            "tick": tk,
            "time_s": t_sec,
            "flame_pos": flame_pos,
            "is_impact": is_impact_frame
        })
        print(f"  Frame {i+1:02d}/18: tick={tk:4.1f}t (t={t_sec:4.2f}s) flame={flame_pos}")

print(f"Successfully captured {len(frames_raw)} frames!")

# ==============================================================================
# 4. COMPOSE AND ANNOTATE ANIMATED GIFS
# ==============================================================================

normal_frames = []
slow_frames = []

for item in frames_raw:
    img = item["image"]
    tk = item["tick"]
    t_sec = item["time_s"]
    fpos = item["flame_pos"]
    is_impact = item["is_impact"]
    
    # 4A. Normal speed frame (Clean with subtle watermark)
    img_normal = img.copy()
    draw_n = ImageDraw.Draw(img_normal)
    draw_n.text((20, 20), "FIRE JAB (REALTIME: 0.45s)", fill=(240, 240, 255), font=font_bold)
    draw_n.text((20, 45), f"Flame Anchor: [{fpos[0]:.1f}, {fpos[1]:.1f}, {fpos[2]:.1f}]", fill=(255, 180, 50), font=font_small)
    if is_impact:
        draw_n.rectangle([15, 68, 230, 95], fill=(220, 60, 20))
        draw_n.text((22, 72), "HITBOX & FLAME BURST", fill=(255, 255, 255), font=font_bold)
    normal_frames.append(img_normal)
    
    # 4B. Slow annotated frame (Full HUD Banner)
    # Canvas size: 700 x 780 (top banner + main view)
    annotated = Image.new("RGBA", (700, 780), (22, 24, 30, 255))
    annotated.paste(img, (0, 80))
    
    draw_a = ImageDraw.Draw(annotated)
    
    # Top banner background
    draw_a.rectangle([0, 0, 700, 80], fill=(28, 32, 42))
    draw_a.line([(0, 80), (700, 80)], fill=(60, 65, 80), width=2)
    
    # Phase classification
    if tk < 2.0:
        p_name = "PHASE 1: WINDUP / ANTICIPATION"
        p_color = (100, 180, 255)
    elif tk <= 5.0:
        p_name = "PHASE 2: ACTIVE STRIKE"
        p_color = (255, 90, 40)
    else:
        p_name = "PHASE 3: RECOVERY (SNAP BACK)"
        p_color = (120, 220, 120)
        
    draw_a.text((20, 12), p_name, fill=p_color, font=font_bold)
    
    # Timecode
    time_str = f"Tick: {tk:3.1f} / 9.0t   |   Time: {t_sec:4.2f}s / 0.45s (Slowed 0.25x)"
    draw_a.text((20, 38), time_str, fill=(210, 215, 230), font=font_bold)
    
    # Flame Tracking Telemetry
    telemetry_str = f"Flame Anchor: X={fpos[0]:+5.1f}  Y={fpos[1]:4.1f}  Z={fpos[2]:+5.1f} (-Z is forward)"
    draw_a.text((20, 58), telemetry_str, fill=(255, 200, 80), font=font_small)
    
    # Impact Alert Badge
    if is_impact:
        draw_a.rectangle([470, 15, 680, 65], fill=(210, 40, 20), outline=(255, 220, 50), width=2)
        draw_a.text((485, 22), "HITBOX ACTIVE", fill=(255, 255, 255), font=font_bold)
        draw_a.text((495, 42), "Tick 3 / 0.15s", fill=(255, 230, 100), font=font_small)
        
    # Foot labels at bottom
    draw_a.rectangle([0, 740, 700, 780], fill=(28, 32, 42))
    draw_a.line([(0, 740), (700, 740)], fill=(50, 55, 70), width=1)
    foot_str = "Lead Foot (Left): Z < 0 (Depan, Arah -Z)   |   Rear Foot (Right): Z > 0 (Belakang, Arah +Z)"
    draw_a.text((25, 750), foot_str, fill=(160, 175, 200), font=font_small)
    
    slow_frames.append(annotated)

# Save GIFs
NORMAL_GIF_PATH = os.path.join(OUTPUT_DIR, "fire_jab_motion_normal.gif")
SLOW_GIF_PATH   = os.path.join(OUTPUT_DIR, "fire_jab_motion_slow_annotated.gif")

BRAIN_NORMAL_GIF = os.path.join(BRAIN_DIR, "fire_jab_motion_normal.gif")
BRAIN_SLOW_GIF   = os.path.join(BRAIN_DIR, "fire_jab_motion_slow_annotated.gif")

# Normal: 25ms per frame = 450ms total (0.45s exact realtime)
normal_frames[0].save(
    NORMAL_GIF_PATH,
    save_all=True,
    append_images=normal_frames[1:],
    duration=25,
    loop=0
)
shutil.copyfile(NORMAL_GIF_PATH, BRAIN_NORMAL_GIF)
print("Saved Realtime GIF:", NORMAL_GIF_PATH)

# Slow: 100ms per frame = 1800ms total (1.80s, 0.25x slow motion with HUD)
slow_frames[0].save(
    SLOW_GIF_PATH,
    save_all=True,
    append_images=slow_frames[1:],
    duration=100,
    loop=0
)
shutil.copyfile(SLOW_GIF_PATH, BRAIN_SLOW_GIF)
print("Saved Slow Annotated GIF:", SLOW_GIF_PATH)

# Clean up Blockbench scene markers
call_bb('execute_script', {'code': '''
let old_fx = scene.getObjectByName('flame_tracking_fx');
if (old_fx) scene.remove(old_fx);
Canvas.updateView();
'''})

print("Motion preview generation complete!")
