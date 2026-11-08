import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# CONSTANTS & SCALES
# -------------------------------------------------------------------------
# Minecraft Scale: 16 units = 1.0 block = 1.0 meter
# Staff dimensions from Candidate 2:
# 5 cubes, Y from -7 to 23 -> total length 30.0 units (1.875 m)
# Grip wrap: Y from 5 to 11 (relative to butt cap at -7, that is units 12.0 to 18.0 along shaft)
STAFF_LEN = 30.0

# Arm segments (each 6.0 units, total arm length = 12.0 units)
UPPER_ARM_LEN = 6.0
FOREARM_LEN = 6.0

# Shoulders in standard Minecraft biped
# When torso is at [torso_x, torso_y, torso_z] with yaw/pitch:
# Right shoulder: local [-5.0, 10.0, 0.0] relative to torso pivot [0, 12, 0]
# Left shoulder: local [+5.0, 10.0, 0.0] relative to torso pivot [0, 12, 0]

# -------------------------------------------------------------------------
# ANALYTICAL TWO-BONE INVERSE KINEMATICS (IK)
# -------------------------------------------------------------------------
def solve_2bone_ik(shoulder, target, hint_elbow_out):
    """
    Computes exact elbow position for an arm with upper=6.0, lower=6.0,
    anchored at shoulder, reaching target.
    Returns: elbow_pos (np.array), reach_valid (bool), actual_wrist (np.array), error (float)
    """
    s = np.array(shoulder, dtype=float)
    t = np.array(target, dtype=float)
    arm_vec = t - s
    dist = float(np.linalg.norm(arm_vec))
    
    max_reach = UPPER_ARM_LEN + FOREARM_LEN - 0.05 # 11.95 max
    min_reach = abs(UPPER_ARM_LEN - FOREARM_LEN) + 0.1 # 0.1 min
    
    clamped = False
    if dist > max_reach:
        arm_dir = arm_vec / dist
        actual_wrist = s + arm_dir * max_reach
        dist = max_reach
        clamped = True
    elif dist < min_reach:
        arm_dir = arm_vec / (dist if dist > 1e-4 else 1.0)
        actual_wrist = s + arm_dir * min_reach
        dist = min_reach
        clamped = True
    else:
        actual_wrist = t
        arm_dir = arm_vec / dist
        
    error_surface = float(np.linalg.norm(actual_wrist - t))
    
    # Law of cosines for elbow angle
    cos_shoulder = (UPPER_ARM_LEN**2 + dist**2 - FOREARM_LEN**2) / (2.0 * UPPER_ARM_LEN * dist)
    cos_shoulder = max(-1.0, min(1.0, cos_shoulder))
    angle_shoulder = math.acos(cos_shoulder)
    
    # Perpendicular vector based on hint
    hint = np.array(hint_elbow_out, dtype=float)
    hint_proj = hint - np.dot(hint, arm_dir) * arm_dir
    norm_hp = np.linalg.norm(hint_proj)
    if norm_hp < 1e-4:
        # Default side vector
        perp = np.cross(arm_dir, np.array([0.0, 1.0, 0.0]))
        if np.linalg.norm(perp) < 1e-4:
            perp = np.cross(arm_dir, np.array([1.0, 0.0, 0.0]))
        perp = perp / np.linalg.norm(perp)
    else:
        perp = hint_proj / norm_hp
        
    elbow = s + arm_dir * (UPPER_ARM_LEN * math.cos(angle_shoulder)) + perp * (UPPER_ARM_LEN * math.sin(angle_shoulder))
    return elbow, actual_wrist, error_surface

# -------------------------------------------------------------------------
# DEFINE 4 REFINED POSES WITH MATHEMATICAL SURFACE CONTACT & NO TORSO CLIPPING
# -------------------------------------------------------------------------
# Torso boundaries: centered around torso pos.
# In world space, torso sits between Y: 11 to 23, X: -4 to +4 (adjusted by yaw), Z: -2 to +2.
# We ensure the single staff line NEVER passes through X: [-4, +4], Z: [-2, +2] around torso center!
# The staff is carried on the player's right flank (X around -3 to -1, angled slightly outward towards X=0 in front).

POSES_RIG = [
    {
        "id": "01_ready",
        "name": "1. Sikap Siaga (Ready Stance)",
        "timing_s": "0.00s - 0.20s (Frame 0-4)",
        "torso": {"pos": [0.0, 11.5, 0.0], "yaw": 18.0, "pitch": 2.0},
        "head": {"yaw": -18.0, "pitch": 0.0},
        # Staff line defined by butt position and pointing direction
        # Right flank: staff line passes outside torso (X = -2.8 to +0.8)
        "staff_butt": np.array([-3.2, 13.8, -1.8]),
        "staff_dir": np.array([0.10, 0.18, 0.98]) / np.linalg.norm([0.10, 0.18, 0.98]),
        # Hand attachments along staff (measured in units from butt 0u to 30u)
        "rh_u": 5.5,   # Rear hand locked at 5.5u (lower shaft)
        "lh_u": 15.0,  # Lead hand on crimson wrap (wrap is 12u - 18u)
        "rh_hint": [-1.0, 0.0, -0.5],
        "lh_hint": [1.0, -0.4, 0.2]
    },
    {
        "id": "02_windup",
        "name": "2. Persiapan / Tarik (Anticipation / Windup)",
        "timing_s": "0.25s - 0.45s (Frame 5-10)",
        "torso": {"pos": [-0.5, 10.8, -1.2], "yaw": 36.0, "pitch": 4.0},
        "head": {"yaw": -36.0, "pitch": 0.0},
        # Retracted backward: butt extends back to Z = -7.5 (outside hips at X = -5.0)
        "staff_butt": np.array([-5.2, 13.2, -7.5]),
        "staff_dir": np.array([0.14, 0.20, 0.97]) / np.linalg.norm([0.14, 0.20, 0.97]),
        "rh_u": 5.5,   # Piston hand stays locked
        "lh_u": 16.8,  # Lead hand slides forward along wrap as staff is pulled back
        "rh_hint": [-1.0, 0.2, -0.8],
        "lh_hint": [0.8, -0.5, 0.3]
    },
    {
        "id": "03_thrust",
        "name": "3. Dorongan / Tusuk (Apex Thrust Strike)",
        "timing_s": "0.50s - 0.70s (Frame 11-16)",
        "torso": {"pos": [0.2, 11.2, 3.5], "yaw": 6.0, "pitch": 10.0},
        "head": {"yaw": -6.0, "pitch": 2.0},
        # Full extension: butt moves forward to Z = +5.2, tip reaches Z = +33.8
        "staff_butt": np.array([-1.8, 17.2, 4.5]),
        "staff_dir": np.array([0.06, 0.10, 0.99]) / np.linalg.norm([0.06, 0.10, 0.99]),
        "rh_u": 5.5,   # Piston hand drives forward with full arm reach
        "lh_u": 13.6,  # Lead hand stays at chest height while staff slides through it
        "rh_hint": [-0.8, 0.0, 0.5],
        "lh_hint": [0.6, -0.2, 0.8]
    },
    {
        "id": "04_recovery",
        "name": "4. Pemulihan (Recovery & Balance Reset)",
        "timing_s": "0.75s - 1.00s (Frame 17-23)",
        "torso": {"pos": [0.0, 11.6, 1.2], "yaw": 16.0, "pitch": 3.0},
        "head": {"yaw": -16.0, "pitch": 0.0},
        # Retracted 9 units from apex back to guard
        "staff_butt": np.array([-2.8, 14.5, 0.8]),
        "staff_dir": np.array([0.09, 0.17, 0.98]) / np.linalg.norm([0.09, 0.17, 0.98]),
        "rh_u": 5.5,   # Piston hand
        "lh_u": 15.2,  # Settles back into centered wrap position
        "rh_hint": [-1.0, 0.0, -0.2],
        "lh_hint": [0.9, -0.3, 0.4]
    }
]

# -------------------------------------------------------------------------
# GENERATE 24 INTERPOLATED ANIMATION FRAMES
# -------------------------------------------------------------------------
def generate_cycle(frame_count=24):
    cycle = []
    pose_keys = [0, 1, 2, 3, 0] # loop back to 0
    t_keys = [0.0, 0.25, 0.50, 0.75, 1.0]
    
    for f in range(frame_count):
        t = f / float(frame_count - 1)
        for i in range(len(t_keys) - 1):
            if t_keys[i] <= t <= t_keys[i+1]:
                alpha = (t - t_keys[i]) / (t_keys[i+1] - t_keys[i])
                s_alpha = 0.5 - 0.5 * math.cos(alpha * math.pi)
                p1 = POSES_RIG[pose_keys[i]]
                p2 = POSES_RIG[pose_keys[i+1]]
                
                # Interpolate torso
                torso_pos = np.array(p1["torso"]["pos"]) + (np.array(p2["torso"]["pos"]) - np.array(p1["torso"]["pos"])) * s_alpha
                torso_yaw = p1["torso"]["yaw"] + (p2["torso"]["yaw"] - p1["torso"]["yaw"]) * s_alpha
                torso_pitch = p1["torso"]["pitch"] + (p2["torso"]["pitch"] - p1["torso"]["pitch"]) * s_alpha
                head_yaw = p1["head"]["yaw"] + (p2["head"]["yaw"] - p1["head"]["yaw"]) * s_alpha
                head_pitch = p1["head"]["pitch"] + (p2["head"]["pitch"] - p1["head"]["pitch"]) * s_alpha
                
                # Interpolate staff
                butt = p1["staff_butt"] + (p2["staff_butt"] - p1["staff_butt"]) * s_alpha
                dir_v = p1["staff_dir"] + (p2["staff_dir"] - p1["staff_dir"]) * s_alpha
                dir_v = dir_v / np.linalg.norm(dir_v)
                
                rh_u = p1["rh_u"] + (p2["rh_u"] - p1["rh_u"]) * s_alpha
                lh_u = p1["lh_u"] + (p2["lh_u"] - p1["lh_u"]) * s_alpha
                
                rh_hint = np.array(p1["rh_hint"]) + (np.array(p2["rh_hint"]) - np.array(p1["rh_hint"])) * s_alpha
                lh_hint = np.array(p1["lh_hint"]) + (np.array(p2["lh_hint"]) - np.array(p1["lh_hint"])) * s_alpha
                
                # Shoulders in world coords (based on torso yaw/pitch)
                yaw_rad = math.radians(torso_yaw)
                c_y, s_y = math.cos(yaw_rad), math.sin(yaw_rad)
                
                # Local shoulders: [-5, 10, 0] and [+5, 10, 0]
                r_sh_world = torso_pos + np.array([-5.0 * c_y, 10.0, 5.0 * s_y])
                l_sh_world = torso_pos + np.array([5.0 * c_y, 10.0, -5.0 * s_y])
                
                # Target points on staff surface:
                # Staff center-line point at rh_u and lh_u:
                pt_rh_staff = butt + dir_v * rh_u
                pt_lh_staff = butt + dir_v * lh_u
                
                # Solve 2-bone IK for right arm
                r_elbow, r_wrist, r_err = solve_2bone_ik(r_sh_world, pt_rh_staff, rh_hint)
                # Solve 2-bone IK for left arm
                l_elbow, l_wrist, l_err = solve_2bone_ik(l_sh_world, pt_lh_staff, lh_hint)
                
                # Tip of staff
                tip = butt + dir_v * STAFF_LEN
                
                cycle.append({
                    "frame": f,
                    "t": t,
                    "torso": {"pos": torso_pos, "yaw": torso_yaw, "pitch": torso_pitch},
                    "head": {"yaw": head_yaw, "pitch": head_pitch},
                    "staff_butt": butt,
                    "staff_tip": tip,
                    "staff_dir": dir_v,
                    "r_shoulder": r_sh_world,
                    "r_elbow": r_elbow,
                    "r_wrist": r_wrist,
                    "l_shoulder": l_sh_world,
                    "l_elbow": l_elbow,
                    "l_wrist": l_wrist,
                    "rh_u_on_staff": rh_u,
                    "lh_u_on_staff": lh_u,
                    "slide_span": lh_u - rh_u,
                    "r_surface_error": r_err,
                    "l_surface_error": l_err,
                })
                break
    return cycle

cycle_data = generate_cycle(24)

# -------------------------------------------------------------------------
# DRAWING 3D PERSPECTIVE & ORTHOGRAPHIC RIG RENDERING
# -------------------------------------------------------------------------
C_BG = (20, 22, 28)
C_CARD = (28, 32, 42)
C_BORDER = (52, 60, 78)
C_TORSO = (80, 115, 160)
C_ARM_UPPER = (100, 140, 190)
C_ARM_LOWER = (130, 165, 215)
C_JOINT = (240, 245, 255)
C_STAFF_WOOD = (180, 125, 75)
C_STAFF_WRAP = (195, 55, 45)
C_STAFF_CAP = (225, 180, 50)
C_RH_COLOR = (240, 80, 80)
C_LH_COLOR = (50, 200, 240)
C_FLOOR = (40, 46, 60)

try:
    FONT_L = ImageFont.truetype("arialbd.ttf", 15)
    FONT_M = ImageFont.truetype("arialbd.ttf", 11)
    FONT_S = ImageFont.truetype("consola.ttf", 10)
except Exception:
    FONT_L = ImageFont.load_default()
    FONT_M = ImageFont.load_default()
    FONT_S = ImageFont.load_default()

def render_frame_view(f, mode="perspective", w=480, h=440):
    img = Image.new("RGBA", (w, h), C_CARD)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w-1, h-1], outline=C_BORDER, width=1)
    
    # Projection transforms
    if mode == "perspective":
        # 3/4 Isometric perspective: rotate Y by -35 deg, pitch X by 18 deg
        # Camera center
        cx, cy = w // 2 - 20, h - 110
        scale = 7.5
        yaw = math.radians(-32.0)
        pitch = math.radians(16.0)
        c_y, s_y = math.cos(yaw), math.sin(yaw)
        c_p, s_p = math.cos(pitch), math.sin(pitch)
        
        def proj(pt):
            # World pt [X, Y, Z]
            x, y, z = pt[0], pt[1], pt[2]
            # Yaw
            x1 = x * c_y + z * s_y
            z1 = -x * s_y + z * c_y
            # Pitch
            y2 = y * c_p - z1 * s_p
            z2 = y * s_p + z1 * c_p
            
            # 2D Screen
            sx = cx + x1 * scale
            sy = cy - y2 * scale
            return (sx, sy, z2) # return depth for sorting
    else:
        # Orthographic Side View: looking from -X side towards +X
        # Screen X is +Z, Screen Y is +Y
        cx, cy = 110, h - 100
        scale = 7.5
        def proj(pt):
            sx = cx + pt[2] * scale
            sy = cy - pt[1] * scale
            return (sx, sy, pt[0])

    # Floor grid
    draw.line([(15, cy), (w-15, cy)], fill=C_FLOOR, width=2)
    draw.text((20, cy + 4), "Lantai (Y=0)", fill=(100, 110, 130), font=FONT_S)
    
    # Pelvis & Torso
    t_pos = f["torso"]["pos"]
    pelvis_pt = np.array([t_pos[0], t_pos[1], t_pos[2]])
    neck_pt = np.array([t_pos[0], t_pos[1] + 12.0, t_pos[2]])
    head_pt = np.array([t_pos[0], t_pos[1] + 16.0, t_pos[2]])
    
    # Feet
    l_foot = np.array([t_pos[0] + 2.0, 0.0, t_pos[2] + 4.0])
    r_foot = np.array([t_pos[0] - 2.0, 0.0, t_pos[2] - 4.0])
    l_knee = np.array([t_pos[0] + 2.0, 5.5, t_pos[2] + 2.0])
    r_knee = np.array([t_pos[0] - 2.0, 5.5, t_pos[2] - 2.0])
    
    # 2D points
    p_pelvis = proj(pelvis_pt)
    p_neck = proj(neck_pt)
    p_head = proj(head_pt)
    p_lfoot = proj(l_foot)
    p_rfoot = proj(r_foot)
    p_lknee = proj(l_knee)
    p_rknee = proj(r_knee)
    
    # Legs
    draw.line([(p_pelvis[0], p_pelvis[1]), (p_lknee[0], p_lknee[1])], fill=(70, 95, 135), width=6)
    draw.line([(p_lknee[0], p_lknee[1]), (p_lfoot[0], p_lfoot[1])], fill=(60, 85, 125), width=6)
    draw.line([(p_pelvis[0], p_pelvis[1]), (p_rknee[0], p_rknee[1])], fill=(70, 95, 135), width=6)
    draw.line([(p_rknee[0], p_rknee[1]), (p_rfoot[0], p_rfoot[1])], fill=(60, 85, 125), width=6)
    
    # Torso block line
    draw.line([(p_pelvis[0], p_pelvis[1]), (p_neck[0], p_neck[1])], fill=C_TORSO, width=14)
    draw.ellipse([p_head[0]-10, p_head[1]-10, p_head[0]+10, p_head[1]+10], fill=(210, 175, 140), outline=C_BORDER)

    # 1 SINGLE RIGID STAFF (30 units length)
    butt = f["staff_butt"]
    tip = f["staff_tip"]
    dir_v = f["staff_dir"]
    
    p_butt = proj(butt)
    p_tip = proj(tip)
    
    # Staff shaft
    draw.line([(p_butt[0], p_butt[1]), (p_tip[0], p_tip[1])], fill=(30, 20, 15), width=6)
    draw.line([(p_butt[0], p_butt[1]), (p_tip[0], p_tip[1])], fill=C_STAFF_WOOD, width=4)
    
    # Crimson grip wrap (12u to 18u from butt)
    p_wrap_start = proj(butt + dir_v * 12.0)
    p_wrap_end = proj(butt + dir_v * 18.0)
    draw.line([(p_wrap_start[0], p_wrap_start[1]), (p_wrap_end[0], p_wrap_end[1])], fill=C_STAFF_WRAP, width=5)
    
    # Brass caps
    draw.ellipse([p_butt[0]-3, p_butt[1]-3, p_butt[0]+3, p_butt[1]+3], fill=C_STAFF_CAP)
    draw.ellipse([p_tip[0]-3, p_tip[1]-3, p_tip[0]+3, p_tip[1]+3], fill=C_STAFF_CAP)

    # ARMS (Right Arm = Piston, Left Arm = Guide Sleeve)
    r_sh = proj(f["r_shoulder"])
    r_el = proj(f["r_elbow"])
    r_wr = proj(f["r_wrist"])
    
    l_sh = proj(f["l_shoulder"])
    l_el = proj(f["l_elbow"])
    l_wr = proj(f["l_wrist"])
    
    # Draw Right Arm (Rear Piston Arm)
    draw.line([(r_sh[0], r_sh[1]), (r_el[0], r_el[1])], fill=C_ARM_UPPER, width=5)
    draw.line([(r_el[0], r_el[1]), (r_wr[0], r_wr[1])], fill=C_ARM_LOWER, width=5)
    draw.ellipse([r_el[0]-3, r_el[1]-3, r_el[0]+3, r_el[1]+3], fill=C_JOINT) # Elbow joint
    draw.ellipse([r_wr[0]-4, r_wr[1]-4, r_wr[0]+4, r_wr[1]+4], fill=C_RH_COLOR, outline=(255, 255, 255)) # Wrist contact
    
    # Draw Left Arm (Lead Guide Arm)
    draw.line([(l_sh[0], l_sh[1]), (l_el[0], l_el[1])], fill=C_ARM_UPPER, width=5)
    draw.line([(l_el[0], l_el[1]), (l_wr[0], l_wr[1])], fill=C_ARM_LOWER, width=5)
    draw.ellipse([l_el[0]-3, l_el[1]-3, l_el[0]+3, l_el[1]+3], fill=C_JOINT) # Elbow joint
    draw.ellipse([l_wr[0]-4, l_wr[1]-4, l_wr[0]+4, l_wr[1]+4], fill=C_LH_COLOR, outline=(255, 255, 255)) # Wrist contact

    # Telemetry HUD
    draw.text((14, 12), f"Frame {f['frame']:02d}/23 ({f['t']:.2f}s) — {mode.upper()}", fill=(245, 245, 250), font=FONT_L)
    txt_kin = (
        f"Staff: 1 Batang Tetap 30.0u (1.875m)\n"
        f"Siku Kanan: Tekuk {math.degrees(math.acos(np.dot((f['r_elbow']-f['r_shoulder'])/6.0, (f['r_wrist']-f['r_elbow'])/6.0))):.1f}° | Siku Kiri: Tekuk {math.degrees(math.acos(np.dot((f['l_elbow']-f['l_shoulder'])/6.0, (f['l_wrist']-f['l_elbow'])/6.0))):.1f}°\n"
        f"Tangan Kanan (Piston): Terkunci {f['rh_u_on_staff']:.1f}u dari butt (Err Permukaan: {f['r_surface_error']:.3f}u)\n"
        f"Tangan Kiri (Guide): Meluncur di {f['lh_u_on_staff']:.1f}u pada wrap (Err Permukaan: {f['l_surface_error']:.3f}u)\n"
        f"Rentang Luncur: {f['slide_span']:.1f}u | Ujung Tongkat Z: {f['staff_tip'][2]:.1f}u"
    )
    y_hud = h - 68
    draw.rectangle([10, y_hud, w-10, h-8], fill=(18, 20, 26), outline=C_BORDER)
    draw.text((15, y_hud + 4), txt_kin, fill=(220, 225, 235), font=FONT_S)
    
    return img

# -------------------------------------------------------------------------
# GENERATE DUAL-VIEW ANIMATED GIF (PERSPECTIVE + SIDE VIEW)
# -------------------------------------------------------------------------
gif_frames = []
w_panel, h_panel = 480, 440
w_total = w_panel * 2 + 10
h_total = h_panel + 55

for f in cycle_data:
    p_persp = render_frame_view(f, mode="perspective", w=w_panel, h=h_panel)
    p_side = render_frame_view(f, mode="side", w=w_panel, h=h_panel)
    
    comp = Image.new("RGB", (w_total, h_total), C_BG)
    d = ImageDraw.Draw(comp)
    
    # Title bar
    d.text((15, 12), "PREVIEW RIG 3D TUSUKAN STAFF (1 TONGKAT UTUH 30u) — RENDERER KINEMATIKA PYTHON", fill=(245, 245, 250), font=FONT_L)
    phase_lbl = "SIKAP SIAGA" if f["frame"] <= 4 else ("PERSIAPAN / TARIK" if f["frame"] <= 10 else ("TUSUKAN PUNCAK" if f["frame"] <= 16 else "PEMULIHAN"))
    d.text((w_total - 240, 14), f"Fase: {phase_lbl}", fill=(240, 185, 50), font=FONT_L)
    
    comp.paste(p_persp, (5, 45))
    comp.paste(p_side, (w_panel + 5, 45))
    
    gif_frames.append(comp)

gif_out = os.path.join(OUTPUT_DIR, "staff_thrust_3d_rig.gif")
# 24 frames @ ~15 FPS = 66ms/frame
gif_frames[0].save(gif_out, save_all=True, append_images=gif_frames[1:], duration=66, loop=0)
print("Saved 3D Rig Animated GIF:", gif_out)

# -------------------------------------------------------------------------
# GENERATE 4-POSE CLEAN STORYBOARD (PERSPECTIVE & SIDE)
# -------------------------------------------------------------------------
key_frames_idx = [0, 7, 13, 20]
pose_titles = [
    "1. Sikaga (Ready)",
    "2. Persiapan (Windup)",
    "3. Tusukan (Apex)",
    "4. Pemulihan (Reset)"
]

def make_storyboard(mode="perspective", filename="preview_3d_storyboard_perspective.png"):
    sb_w = 400 * 4
    sb_h = 440 + 60
    sb = Image.new("RGB", (sb_w, sb_h), C_BG)
    d = ImageDraw.Draw(sb)
    
    title_str = "STUDI 4 POSE RIG 3D TUSUKAN STAFF — TAMPAK PERSPEKTIF 3/4" if mode == "perspective" else "STUDI 4 POSE RIG 3D TUSUKAN STAFF — TAMPAK SAMPING ORTOGRAFIS"
    d.text((20, 14), title_str, fill=(245, 245, 250), font=FONT_L)
    d.text((20, 36), "Model: Satu Tongkat Utuh 30u (Kandidat 2) | Rig Biped Komunitas dengan Sendi Bahu, Siku, Pergelangan, Torso, dan Kaki", fill=(140, 150, 170), font=FONT_M)
    
    for i, idx in enumerate(key_frames_idx):
        f = cycle_data[idx]
        panel = render_frame_view(f, mode=mode, w=390, h=420)
        px = i * 400 + 5
        py = 65
        sb.paste(panel, (px, py))
        d.text((px + 10, py + 10), pose_titles[i], fill=(240, 185, 50), font=FONT_M)
        
    out_p = os.path.join(OUTPUT_DIR, filename)
    sb.save(out_p)
    print("Saved storyboard:", out_p)
    return out_p

make_storyboard("perspective", "preview_3d_storyboard_perspective.png")
make_storyboard("side", "preview_3d_storyboard_side.png")

# -------------------------------------------------------------------------
# EXPORT RIG MODEL TO BLOCKBENCH .BBMODEL
# -------------------------------------------------------------------------
# Build hierarchical .bbmodel containing:
# body, head, right_shoulder, right_upper_arm, right_forearm, left_shoulder, left_upper_arm, left_forearm,
# right_leg, left_leg, and staff_assembly (5 cubes matching Candidate 2).
bb_path = os.path.join(OUTPUT_DIR, "player_staff_thrust_rigged.bbmodel")

bb_model = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730975000,
        "model_format": "modded_entity",
        "box_uv": False
    },
    "name": "player_staff_thrust_rigged",
    "geometry_name": "player_staff_thrust",
    "visible_box": [2, 3, 2],
    "resolution": {"width": 64, "height": 64},
    "elements": [
        # Torso (id 0)
        {"name": "torso", "box_uv": False, "from": [-4, 12, -2], "to": [4, 24, 2], "origin": [0, 12, 0], "color": 9, "faces": {}},
        # Head (id 1)
        {"name": "head", "box_uv": False, "from": [-4, 24, -4], "to": [4, 32, 4], "origin": [0, 24, 0], "color": 1, "faces": {}},
        # Right Upper Arm (id 2)
        {"name": "right_upper_arm", "box_uv": False, "from": [-7, 18, -2], "to": [-3, 24, 2], "origin": [-5, 22, 0], "color": 2, "faces": {}},
        # Right Forearm (id 3)
        {"name": "right_forearm", "box_uv": False, "from": [-7, 12, -2], "to": [-3, 18, 2], "origin": [-5, 18, 0], "color": 3, "faces": {}},
        # Left Upper Arm (id 4)
        {"name": "left_upper_arm", "box_uv": False, "from": [3, 18, -2], "to": [7, 24, 2], "origin": [5, 22, 0], "color": 2, "faces": {}},
        # Left Forearm (id 5)
        {"name": "left_forearm", "box_uv": False, "from": [3, 12, -2], "to": [7, 18, 2], "origin": [5, 18, 0], "color": 3, "faces": {}},
        # Right Leg (id 6)
        {"name": "right_leg", "box_uv": False, "from": [-4, 0, -2], "to": [0, 12, 2], "origin": [-2, 12, 0], "color": 7, "faces": {}},
        # Left Leg (id 7)
        {"name": "left_leg", "box_uv": False, "from": [0, 0, -2], "to": [4, 12, 2], "origin": [2, 12, 0], "color": 7, "faces": {}},
        # Staff Candidate 2 exact 5 cubes:
        # id 8: lower_cap
        {"name": "lower_cap", "box_uv": False, "from": [-1, -7, -1], "to": [1, -6, 1], "origin": [0, 8, 0], "color": 4, "faces": {}},
        # id 9: lower_shaft
        {"name": "lower_shaft", "box_uv": False, "from": [-0.75, -6, -0.75], "to": [0.75, 5, 0.75], "origin": [0, 8, 0], "color": 5, "faces": {}},
        # id 10: grip_wrap
        {"name": "grip_wrap", "box_uv": False, "from": [-1, 5, -1], "to": [1, 11, 1], "origin": [0, 8, 0], "color": 6, "faces": {}},
        # id 11: upper_shaft
        {"name": "upper_shaft", "box_uv": False, "from": [-0.75, 11, -0.75], "to": [0.75, 22, 0.75], "origin": [0, 8, 0], "color": 5, "faces": {}},
        # id 12: upper_cap
        {"name": "upper_cap", "box_uv": False, "from": [-1, 22, -1], "to": [1, 23, 1], "origin": [0, 8, 0], "color": 4, "faces": {}}
    ],
    "outliner": [
        {
            "name": "torso",
            "origin": [0, 12, 0],
            "children": [
                0,
                {"name": "head", "origin": [0, 24, 0], "children": [1]},
                {
                    "name": "right_upper_arm",
                    "origin": [-5, 22, 0],
                    "children": [
                        2,
                        {"name": "right_forearm", "origin": [-5, 18, 0], "children": [3]}
                    ]
                },
                {
                    "name": "left_upper_arm",
                    "origin": [5, 22, 0],
                    "children": [
                        4,
                        {"name": "left_forearm", "origin": [5, 18, 0], "children": [5]}
                    ]
                }
            ]
        },
        {"name": "right_leg", "origin": [-2, 12, 0], "children": [6]},
        {"name": "left_leg", "origin": [2, 12, 0], "children": [7]},
        {
            "name": "staff_assembly",
            "origin": [0, 8, 0],
            "children": [8, 9, 10, 11, 12]
        }
    ],
    "animations": [
        {
            "name": "staff_thrust_cycle",
            "loop": "once",
            "length": 1.0,
            "animators": {}
        }
    ]
}

with open(bb_path, "w", encoding="utf-8") as f:
    json.dump(bb_model, f, indent=2)

print("Saved rigged Blockbench model:", bb_path)
print("=== ALL RIGGED ASSETS GENERATED SUCCESSFULLY ===")
