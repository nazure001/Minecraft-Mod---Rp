import os
import math
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# CONSTANTS & PALETTE
# -------------------------------------------------------------------------
C_BG = (18, 20, 26)
C_PANEL = (28, 32, 42)
C_BORDER = (50, 58, 76)
C_TEXT = (240, 244, 250)
C_TEXT_MUTED = (140, 150, 170)
C_STAFF_WOOD = (176, 122, 74)
C_STAFF_CAP = (220, 175, 55)
C_STAFF_WRAP = (185, 50, 45)
C_RIGHT_HAND = (235, 80, 80)     # Rear Hand (Piston)
C_LEFT_HAND = (60, 190, 240)     # Lead Hand (Guide Sleeve)
C_BODY = (110, 140, 180)
C_LIMB = (85, 115, 155)
C_SKIN = (215, 175, 140)

# Minecraft scale: 16 units = 1.0 Block = 1.0 Meter
# Staff is strictly 30.0 units (1.875 meters)
STAFF_TOTAL_LEN = 30.0

# -------------------------------------------------------------------------
# 24-FRAME KINEMATICS CYCLE (WITH 1 RIGID 30-UNIT STAFF)
# -------------------------------------------------------------------------
# Keyframe poses at t = 0.0 (Ready), t = 0.25 (Windup), t = 0.50 (Thrust), t = 0.75 (Recovery), t = 1.0 (Ready)
keyframes = [
    {
        "t": 0.0,
        "torso_y": 11.5, "torso_z": 0.0, "torso_yaw": 22.0, "torso_pitch": 4.0,
        "head_yaw": -22.0, "head_pitch": -2.0,
        "rh_pos": np.array([-3.2, 14.0, 1.2]),    # Rear hand (piston)
        "lh_pos": np.array([1.8, 16.5, 7.8]),     # Lead hand (guide)
        "thrust_aim": np.array([0.0, 19.5, 20.0]) # Target vector aim
    },
    {
        "t": 0.25,
        "torso_y": 10.8, "torso_z": -1.0, "torso_yaw": 42.0, "torso_pitch": 6.0,
        "head_yaw": -42.0, "head_pitch": 0.0,
        "rh_pos": np.array([-5.6, 13.2, -3.4]),
        "lh_pos": np.array([-0.4, 16.2, 3.8]),
        "thrust_aim": np.array([0.0, 19.8, 20.0])
    },
    {
        "t": 0.50,
        "torso_y": 11.2, "torso_z": 3.8, "torso_yaw": 8.0, "torso_pitch": 12.0,
        "head_yaw": -8.0, "head_pitch": 4.0,
        "rh_pos": np.array([-1.4, 17.5, 9.2]),
        "lh_pos": np.array([1.2, 19.0, 16.8]),
        "thrust_aim": np.array([0.0, 20.3, 30.0])
    },
    {
        "t": 0.75,
        "torso_y": 11.6, "torso_z": 1.5, "torso_yaw": 18.0, "torso_pitch": 4.0,
        "head_yaw": -18.0, "head_pitch": -1.0,
        "rh_pos": np.array([-2.6, 14.8, 3.8]),
        "lh_pos": np.array([1.4, 17.2, 10.2]),
        "thrust_aim": np.array([0.0, 19.8, 22.0])
    },
    {
        "t": 1.0,
        "torso_y": 11.5, "torso_z": 0.0, "torso_yaw": 22.0, "torso_pitch": 4.0,
        "head_yaw": -22.0, "head_pitch": -2.0,
        "rh_pos": np.array([-3.2, 14.0, 1.2]),
        "lh_pos": np.array([1.8, 16.5, 7.8]),
        "thrust_aim": np.array([0.0, 19.5, 20.0])
    }
]

def interpolate_cycle(frames_count=24):
    frames = []
    for f_idx in range(frames_count):
        t = f_idx / float(frames_count - 1)
        # Find segment
        for i in range(len(keyframes) - 1):
            if keyframes[i]["t"] <= t <= keyframes[i+1]["t"]:
                seg_len = keyframes[i+1]["t"] - keyframes[i]["t"]
                alpha = (t - keyframes[i]["t"]) / seg_len
                # Smooth cosine blend
                s_alpha = 0.5 - 0.5 * math.cos(alpha * math.pi)
                k1, k2 = keyframes[i], keyframes[i+1]
                
                torso_y = k1["torso_y"] + (k2["torso_y"] - k1["torso_y"]) * s_alpha
                torso_z = k1["torso_z"] + (k2["torso_z"] - k1["torso_z"]) * s_alpha
                torso_yaw = k1["torso_yaw"] + (k2["torso_yaw"] - k1["torso_yaw"]) * s_alpha
                torso_pitch = k1["torso_pitch"] + (k2["torso_pitch"] - k1["torso_pitch"]) * s_alpha
                head_yaw = k1["head_yaw"] + (k2["head_yaw"] - k1["head_yaw"]) * s_alpha
                head_pitch = k1["head_pitch"] + (k2["head_pitch"] - k1["head_pitch"]) * s_alpha
                rh_pos = k1["rh_pos"] + (k2["rh_pos"] - k1["rh_pos"]) * s_alpha
                lh_pos = k1["lh_pos"] + (k2["lh_pos"] - k1["lh_pos"]) * s_alpha
                
                # --- RIGID STAFF CONSTRAINT (30.0 units EXACT) ---
                # The staff is clamped firmly in the rear hand (rh_pos) at offset 5.5 units from butt.
                # The staff axis points directly through the lead hand (lh_pos).
                aim_vec = lh_pos - rh_pos
                dist_between_hands = float(np.linalg.norm(aim_vec))
                if dist_between_hands < 1e-4:
                    staff_dir = np.array([0.0, 0.0, 1.0])
                else:
                    staff_dir = aim_vec / dist_between_hands
                
                butt_pos = rh_pos - staff_dir * 5.5
                tip_pos = butt_pos + staff_dir * STAFF_TOTAL_LEN
                
                # Hand positions on staff parameterization (0 to 30 units):
                rh_dist_from_butt = 5.5
                lh_dist_from_butt = dist_between_hands + 5.5
                
                frames.append({
                    "frame": f_idx,
                    "t": t,
                    "torso": {"y": torso_y, "z": torso_z, "yaw": torso_yaw, "pitch": torso_pitch},
                    "head": {"yaw": head_yaw, "pitch": head_pitch},
                    "rh_pos": rh_pos,
                    "lh_pos": lh_pos,
                    "staff_butt": butt_pos,
                    "staff_tip": tip_pos,
                    "staff_dir": staff_dir,
                    "dist_hands": dist_between_hands,
                    "lh_on_staff": lh_dist_from_butt,
                    "rh_on_staff": rh_dist_from_butt,
                    "staff_len": STAFF_TOTAL_LEN
                })
                break
    return frames

# Generate frames
cycle_frames = interpolate_cycle(24)

# -------------------------------------------------------------------------
# DRAWING HELPERS
# -------------------------------------------------------------------------
try:
    FONT_L = ImageFont.truetype("arialbd.ttf", 16)
    FONT_M = ImageFont.truetype("arialbd.ttf", 12)
    FONT_S = ImageFont.truetype("arial.ttf", 10)
    FONT_CODE = ImageFont.truetype("consola.ttf", 10)
except Exception:
    FONT_L = ImageFont.load_default()
    FONT_M = ImageFont.load_default()
    FONT_S = ImageFont.load_default()
    FONT_CODE = ImageFont.load_default()

def draw_pose_panel(frame_data, view="side", width=380, height=360):
    img = Image.new("RGBA", (width, height), C_PANEL)
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([0, 0, width-1, height-1], outline=C_BORDER, width=1)
    
    # Coords transform
    scale = 6.8
    if view == "side":
        # Side view: Z is right (+Z), Y is up (+Y)
        # origin center
        ox = 110
        oy = height - 70
        def p2d(pt3d):
            # pt3d = [X, Y, Z]
            x = ox + pt3d[2] * scale
            y = oy - pt3d[1] * scale
            return (x, y)
    else:
        # Front view: X is right (+X), Y is up (+Y)
        ox = width // 2
        oy = height - 70
        def p2d(pt3d):
            x = ox + pt3d[0] * scale
            y = oy - pt3d[1] * scale
            return (x, y)

    # Floor grid line (Y=0)
    y_floor = oy
    draw.line([(10, y_floor), (width-10, y_floor)], fill=(45, 52, 68), width=2)
    draw.text((15, y_floor - 12), "Y=0 (Lantai)", fill=C_TEXT_MUTED, font=FONT_S)
    
    # Chest elevation guide line (Y=20)
    y_chest = oy - 20.0 * scale
    draw.line([(10, y_chest), (width-10, y_chest)], fill=(40, 70, 90), width=1)
    draw.text((15, y_chest - 12), "Y=20 (Ulu Hati)", fill=(70, 140, 180), font=FONT_S)
    
    # 1. Draw Player Body Silhouettes
    torso_y = frame_data["torso"]["y"]
    torso_z = frame_data["torso"]["z"]
    
    # Torso (h=12, w=8, d=4)
    p_pelvis = p2d([0, torso_y, torso_z])
    p_neck = p2d([0, torso_y + 12.0, torso_z])
    draw.line([p_pelvis, p_neck], fill=C_BODY, width=14)
    
    # Head (h=8)
    p_head_center = p2d([0, torso_y + 16.0, torso_z])
    draw.ellipse([p_head_center[0]-10, p_head_center[1]-10, p_head_center[0]+10, p_head_center[1]+10], fill=C_SKIN, outline=C_BORDER)
    
    # Legs to ground
    p_lfoot = p2d([2.0, 0.0, torso_z + 3.0])
    p_rfoot = p2d([-2.0, 0.0, torso_z - 3.0])
    draw.line([p_pelvis, p_lfoot], fill=C_LIMB, width=6)
    draw.line([p_pelvis, p_rfoot], fill=C_LIMB, width=6)
    
    # 2. Draw SINGLE 30-UNIT STAFF
    p_butt = p2d(frame_data["staff_butt"])
    p_tip = p2d(frame_data["staff_tip"])
    
    # Staff shadow line
    draw.line([p_butt, p_tip], fill=(20, 15, 10), width=6)
    # Staff main shaft (Wood)
    draw.line([p_butt, p_tip], fill=C_STAFF_WOOD, width=4)
    
    # Draw grip wrap segment on staff (units 12 to 18 along 30-unit length)
    butt_pt = frame_data["staff_butt"]
    s_dir = frame_data["staff_dir"]
    wrap_start = butt_pt + s_dir * 12.0
    wrap_end = butt_pt + s_dir * 18.0
    draw.line([p2d(wrap_start), p2d(wrap_end)], fill=C_STAFF_WRAP, width=5)
    
    # Brass Caps
    draw.ellipse([p_butt[0]-3, p_butt[1]-3, p_butt[0]+3, p_butt[1]+3], fill=C_STAFF_CAP)
    draw.ellipse([p_tip[0]-3, p_tip[1]-3, p_tip[0]+3, p_tip[1]+3], fill=C_STAFF_CAP)
    
    # 3. Draw Arms connecting to the Staff
    p_rh = p2d(frame_data["rh_pos"])
    p_lh = p2d(frame_data["lh_pos"])
    
    # Right arm (rear hand)
    p_r_shoulder = p2d([-4.0, torso_y + 10.0, torso_z])
    draw.line([p_r_shoulder, p_rh], fill=C_RIGHT_HAND, width=4)
    draw.ellipse([p_rh[0]-4, p_rh[1]-4, p_rh[0]+4, p_rh[1]+4], fill=C_RIGHT_HAND, outline=(255, 255, 255))
    
    # Left arm (lead hand)
    p_l_shoulder = p2d([4.0, torso_y + 10.0, torso_z])
    draw.line([p_l_shoulder, p_lh], fill=C_LEFT_HAND, width=4)
    draw.ellipse([p_lh[0]-4, p_lh[1]-4, p_lh[0]+4, p_lh[1]+4], fill=C_LEFT_HAND, outline=(255, 255, 255))
    
    # 4. Data Annotations
    draw.text((12, 10), f"Frame {frame_data['frame']:02d} / 24  ({frame_data['t']:.2f}s)", fill=C_TEXT, font=FONT_L)
    view_title = "TAMPAK SAMPING (+Z KANAN)" if view == "side" else "TAMPAK DEPAN (+X KANAN)"
    draw.text((12, 30), view_title, fill=C_TEXT_MUTED, font=FONT_M)
    
    # Grip telemetry
    y_info = height - 52
    draw.rectangle([8, y_info, width-8, height-8], fill=(22, 26, 34), outline=C_BORDER)
    info_txt = (
        f"Staff: 1 Batang Tetap (30.0u / 1.875m)\n"
        f"Genggam Belakang: {frame_data['rh_on_staff']:.1f}u | Depan: {frame_data['lh_on_staff']:.1f}u | Rentang: {frame_data['dist_hands']:.1f}u"
    )
    draw.text((14, y_info + 4), info_txt, fill=C_TEXT, font=FONT_CODE)
    
    return img

# -------------------------------------------------------------------------
# GENERATE STORYBOARD 4 POSES (FRONT & SIDE)
# -------------------------------------------------------------------------
# Sample 4 key frames: 0 (Ready), 6 (Windup), 12 (Thrust Strike), 18 (Recovery)
key_indices = [0, 6, 12, 18]
pose_labels = ["1. Sikap Awal (Ready)", "2. Persiapan (Windup)", "3. Tusukan (Apex)", "4. Pemulihan (Reset)"]

def create_storyboard_image(view="side", filename="preview_storyboard_side.png"):
    col_w, col_h = 360, 380
    total_w = col_w * 4
    total_h = col_h + 70
    
    sb = Image.new("RGBA", (total_w, total_h), C_BG)
    draw = ImageDraw.Draw(sb)
    
    # Header
    view_name = "TAMPAK SAMPING (SIDE ELEVATION - Z AXIS)" if view == "side" else "TAMPAK DEPAN (FRONT VIEW - X AXIS)"
    draw.text((20, 14), f"STUDI POSE TUSUKAN STAFF — {view_name}", fill=C_TEXT, font=FONT_L)
    draw.text((20, 38), "Verifikasi posisi kedua tangan terhadap SATU TONGKAT UTUH (Panjang konstan 30.0 unit / 1.875 meter Minecraft)", fill=C_TEXT_MUTED, font=FONT_M)
    
    for i, idx in enumerate(key_indices):
        frame_data = cycle_frames[idx]
        panel = draw_pose_panel(frame_data, view=view, width=col_w - 10, height=col_h - 10)
        
        px = i * col_w + 5
        py = 70
        sb.paste(panel, (px, py))
        
        # Subtitle
        draw.text((px + 10, py + 12), pose_labels[i], fill=(235, 180, 50), font=FONT_M)

    out_p = os.path.join(OUTPUT_DIR, filename)
    sb.save(out_p)
    print("Saved storyboard:", out_p)
    return out_p

create_storyboard_image("side", "preview_storyboard_side.png")
create_storyboard_image("front", "preview_storyboard_front.png")

# -------------------------------------------------------------------------
# GENERATE SHORT MOTION GIF (24-FRAME CYCLE DUAL VIEW)
# -------------------------------------------------------------------------
gif_frames = []
frame_w = 340
frame_h = 360
dual_w = frame_w * 2 + 10
dual_h = frame_h + 50

for f in cycle_frames:
    side_panel = draw_pose_panel(f, view="side", width=frame_w, height=frame_h)
    front_panel = draw_pose_panel(f, view="front", width=frame_w, height=frame_h)
    
    comp = Image.new("RGB", (dual_w, dual_h), C_BG)
    d = ImageDraw.Draw(comp)
    
    # Title bar
    d.text((14, 12), f"SIKLUS GERAKAN TUSUKAN STAFF (24 FRAMES) — SATU TONGKAT UTUH", fill=C_TEXT, font=FONT_L)
    phase_str = "SIKAP AWAL" if f["frame"] < 6 else ("PERSIAPAN (TARIK)" if f["frame"] < 12 else ("TUSUKAN PUNCAK" if f["frame"] < 18 else "PEMULIHAN"))
    d.text((dual_w - 200, 14), f"Fase: {phase_str}", fill=(240, 180, 50), font=FONT_M)
    
    comp.paste(front_panel, (5, 45))
    comp.paste(side_panel, (frame_w + 5, 45))
    
    gif_frames.append(comp)

gif_path = os.path.join(OUTPUT_DIR, "staff_thrust_motion.gif")
gif_frames[0].save(
    gif_path,
    save_all=True,
    append_images=gif_frames[1:],
    duration=65,  # ~15 FPS
    loop=0
)
print("Saved animated motion GIF:", gif_path)

# -------------------------------------------------------------------------
# GENERATE DEDICATED GRIP SLIP / DRIFT DIAGNOSTIC
# -------------------------------------------------------------------------
diag_w, diag_h = 750, 420
diag = Image.new("RGBA", (diag_w, diag_h), C_BG)
d_draw = ImageDraw.Draw(diag)

d_draw.rectangle([0, 0, diag_w-1, diag_h-1], outline=C_BORDER)
d_draw.text((20, 15), "DIAGNOSTIK TITIK KONTAK KEDUA TANGAN PADA SATU TONGKAT UTUH (30u)", fill=C_TEXT, font=FONT_L)
d_draw.text((20, 38), "Analisis Mekanika Pergeseran Genggaman (Slide Sleeve) vs Pegangan Kunci Piston (Piston Lock)", fill=C_TEXT_MUTED, font=FONT_S)

# Graph area
gx, gy, gw, gh = 60, 80, 630, 260
d_draw.rectangle([gx, gy, gx+gw, gy+gh], fill=(24, 28, 38), outline=C_BORDER)

# Grid lines for distance along staff (0 to 30 units)
for u in range(0, 35, 5):
    y_pos = gy + gh - int((u / 30.0) * gh)
    d_draw.line([(gx, y_pos), (gx+gw, y_pos)], fill=(40, 46, 60), width=1)
    d_draw.text((gx - 35, y_pos - 6), f"{u}u", fill=C_TEXT_MUTED, font=FONT_CODE)

# Wrap zone highlight on staff (units 12 to 18)
y_wrap_top = gy + gh - int((18.0 / 30.0) * gh)
y_wrap_bot = gy + gh - int((12.0 / 30.0) * gh)
d_draw.rectangle([gx, y_wrap_top, gx+gw, y_wrap_bot], fill=(60, 25, 25, 120))
d_draw.text((gx + 10, y_wrap_top + 4), "ZONA LILITAN GRIP STAFF (12u - 18u)", fill=(240, 100, 100), font=FONT_S)

# Plot curves
rh_points = []
lh_points = []
span_points = []

for f in cycle_frames:
    fx = gx + int((f["frame"] / 23.0) * gw)
    # RH on staff
    rh_y = gy + gh - int((f["rh_on_staff"] / 30.0) * gh)
    rh_points.append((fx, rh_y))
    # LH on staff
    lh_y = gy + gh - int((f["lh_on_staff"] / 30.0) * gh)
    lh_points.append((fx, lh_y))

# Draw lines
d_draw.line(rh_points, fill=C_RIGHT_HAND, width=3)
d_draw.line(lh_points, fill=C_LEFT_HAND, width=3)

# Key labels
d_draw.text((gx + 20, gy + gh + 12), "Frame 0 (Awal)", fill=C_TEXT_MUTED, font=FONT_CODE)
d_draw.text((gx + gw//4, gy + gh + 12), "Frame 6 (Tarik)", fill=C_TEXT_MUTED, font=FONT_CODE)
d_draw.text((gx + gw//2, gy + gh + 12), "Frame 12 (Tusuk)", fill=C_TEXT_MUTED, font=FONT_CODE)
d_draw.text((gx + 3*gw//4, gy + gh + 12), "Frame 18 (Pulih)", fill=C_TEXT_MUTED, font=FONT_CODE)
d_draw.text((gx + gw - 60, gy + gh + 12), "Frame 24 (Reset)", fill=C_TEXT_MUTED, font=FONT_CODE)

# Legend
leg_y = gy + 15
d_draw.rectangle([gx + gw - 280, leg_y, gx + gw - 15, leg_y + 60], fill=(18, 20, 26), outline=C_BORDER)
d_draw.line([(gx + gw - 270, leg_y + 18), (gx + gw - 240, leg_y + 18)], fill=C_RIGHT_HAND, width=3)
d_draw.text((gx + gw - 230, leg_y + 12), "Tangan Kanan (Kunci Butt: 5.5u)", fill=C_TEXT, font=FONT_S)
d_draw.line([(gx + gw - 270, leg_y + 42), (gx + gw - 240, leg_y + 42)], fill=C_LEFT_HAND, width=3)
d_draw.text((gx + gw - 230, leg_y + 36), "Tangan Kiri (Meluncur: 13.4u - 15.5u)", fill=C_TEXT, font=FONT_S)

diag_path = os.path.join(OUTPUT_DIR, "staff_grip_contact_analysis.png")
diag.save(diag_path)
print("Saved grip diagnostic:", diag_path)

print("=== GENERATION OF CORRECTED MOTION & STORYBOARD COMPLETE ===")
