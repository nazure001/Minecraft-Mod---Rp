"""
Procedural VFX Texture Generator for Air Element Prototypes
Outputs:
- air_arc.png (128x128 RGBA): Crescent slash arc for air sweeps / blade trails
- air_ring.png (128x128 RGBA): Shockwave pressure ring with transparent center
- preview_vfx_composite.png: Multi-background preview (dark, light, checkerboard)
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\vfx\air_prototype"

# Color Palette (Pale Air / Bluish White)
# Primary: #D8ECF8 -> (216, 236, 248)
# Core Highlight: #F4FAFF -> (244, 250, 255)
# Soft Falloff Fringe: #B5DCF4 -> (181, 220, 244)
COLOR_CORE = np.array([244.0, 250.0, 255.0])
COLOR_MID = np.array([216.0, 236.0, 248.0])
COLOR_EDGE = np.array([178.0, 218.0, 244.0])

def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0 + 1e-7), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def generate_air_arc(size=128, supersample=4):
    """
    Generates a crescent slash arc (air_arc.png).
    Uses high-resolution supersampling (512x512) downsampled to 128x128 for pristine anti-aliasing.
    Orientation: Curving upwards/forward, tapered at both ends, denser near the leading sweep.
    """
    res = size * supersample
    y, x = np.mgrid[0:res, 0:res]
    
    # Normalized coordinates [-1, 1]
    nx = (x - res * 0.5) / (res * 0.5)
    ny = (y - res * 0.52) / (res * 0.5)  # slightly shifted down to center the crescent arch

    # Arc geometry: Center of curvature slightly below center
    cx, cy = 0.0, 0.42
    dx = nx - cx
    dy = ny - cy
    dist = np.sqrt(dx * dx + dy * dy)
    angle = np.arctan2(dy, dx)  # Angle from circle center

    # The arc spans approximately from -145 deg (-2.53 rad) to -35 deg (-0.61 rad)
    # Peak center of arc is around -90 deg (-pi/2)
    arc_center_angle = -np.pi / 2.0
    arc_half_angle = np.deg2rad(62.0)  # total spread ~124 degrees
    
    angle_diff = np.abs(angle - arc_center_angle)
    # Normalized angular coordinate: 0 at crest (-90 deg), 1 at tips
    ang_t = angle_diff / arc_half_angle
    
    # Angular fade mask: smoothstep taper towards tips
    ang_mask = smoothstep(1.0, 0.65, ang_t) * (ang_t < 1.0)
    
    # Slight asymmetry for a dynamic slash feel (left tail slightly longer/softer, right head sharp)
    # Or keep clean aerodynamic crescent:
    r_center = 0.76  # nominal radius
    # Thickness tapers from center (0.13) to tips (0.01)
    thickness = 0.135 * (1.0 - (ang_t ** 1.8) * 0.92)
    
    # Radial distance from the arc centerline
    radial_dist = np.abs(dist - r_center)
    
    # Core intensity profile (Gaussian-like core with soft falloff)
    norm_radial = radial_dist / np.maximum(thickness, 1e-4)
    radial_mask = np.exp(-3.2 * (norm_radial ** 2)) * (norm_radial < 2.0)
    
    # Inner sharpness vs outer soft edge:
    # A true air blade has a slightly sharper outer compression edge and a softer inner wake
    sign_dist = (dist - r_center) / np.maximum(thickness, 1e-4)
    edge_shaping = np.where(sign_dist > 0, 
                            np.exp(-3.8 * (sign_dist ** 2)), 
                            np.exp(-2.6 * (sign_dist ** 2)))
    
    raw_alpha = edge_shaping * ang_mask
    raw_alpha = np.clip(raw_alpha, 0.0, 1.0)
    
    # Hard boundary clamp to ensure 0 alpha at outer frame margins
    margin_mask = smoothstep(0.96, 0.88, np.maximum(np.abs(nx), np.abs(ny)))
    raw_alpha *= margin_mask

    # Downsample with anti-aliasing
    img_alpha = Image.fromarray((raw_alpha * 255.0).astype(np.uint8), mode='L')
    img_alpha = img_alpha.resize((size, size), Image.Resampling.LANCZOS)
    alpha_arr = np.array(img_alpha, dtype=np.float32) / 255.0

    # Color grading based on intensity:
    # High alpha = Core Highlight (#F4FAFF), Mid = #D8ECF8, Low = #B5DCF4
    intensity = alpha_arr[:, :, np.newaxis]
    rgb = (
        intensity ** 2 * COLOR_CORE +
        intensity * (1.0 - intensity) * 1.5 * COLOR_MID +
        (1.0 - intensity) * COLOR_EDGE
    )
    rgb = np.clip(rgb, 0.0, 255.0).astype(np.uint8)
    
    # Construct RGBA
    rgba = np.dstack([rgb, (alpha_arr * 230.0).astype(np.uint8)]) # Max opacity ~90% (translucent air)
    return Image.fromarray(rgba, mode='RGBA')


def generate_air_ring(size=128, supersample=4):
    """
    Generates an expanding shockwave pressure ring (air_ring.png).
    Transparent center, soft inner and outer falloff, no bounding box artifacts.
    """
    res = size * supersample
    y, x = np.mgrid[0:res, 0:res]
    
    # Normalized coordinates centered at (0, 0)
    nx = (x - res * 0.5 + 0.5) / (res * 0.5)
    ny = (y - res * 0.5 + 0.5) / (res * 0.5)
    dist = np.sqrt(nx * nx + ny * ny)

    # Ring dimensions (normalized, max radius ~ 0.72 so fits comfortably within 1.0)
    # r=0.0 is center, r=0.55 is primary pressure peak
    r_peak = 0.56
    ring_width_outer = 0.18
    ring_width_inner = 0.20

    # Outer falloff: from r_peak to r_peak + ring_width_outer
    outer_falloff = smoothstep(r_peak + ring_width_outer, r_peak, dist)
    # Inner falloff: from r_peak - ring_width_inner to r_peak
    inner_falloff = smoothstep(r_peak - ring_width_inner, r_peak, dist)
    
    primary_ring = outer_falloff * inner_falloff

    # Subtle secondary inner compression fringe (acoustic wave reverberation)
    r_secondary = 0.38
    sec_falloff = np.exp(-((dist - r_secondary) / 0.05) ** 2) * 0.35
    
    raw_alpha = primary_ring + sec_falloff
    # Pure zero at center (r < 0.22)
    center_clear = smoothstep(0.18, 0.30, dist)
    raw_alpha *= center_clear
    
    # Ensure zero alpha at borders
    edge_guard = smoothstep(0.85, 0.74, dist)
    raw_alpha *= edge_guard
    raw_alpha = np.clip(raw_alpha, 0.0, 1.0)

    # Downsample
    img_alpha = Image.fromarray((raw_alpha * 255.0).astype(np.uint8), mode='L')
    img_alpha = img_alpha.resize((size, size), Image.Resampling.LANCZOS)
    alpha_arr = np.array(img_alpha, dtype=np.float32) / 255.0

    # Color mapping
    intensity = alpha_arr[:, :, np.newaxis]
    rgb = (
        (intensity ** 1.8) * COLOR_CORE +
        intensity * (1.0 - intensity) * 1.6 * COLOR_MID +
        (1.0 - intensity) * COLOR_EDGE
    )
    rgb = np.clip(rgb, 0.0, 255.0).astype(np.uint8)

    # Alpha: shockwaves are translucent air pressure (max alpha ~0.82)
    final_alpha = (alpha_arr * 210.0).astype(np.uint8)
    rgba = np.dstack([rgb, final_alpha])
    return Image.fromarray(rgba, mode='RGBA')


def create_checkerboard(width, height, tile_size=8, col1=(36, 40, 50), col2=(48, 52, 64)):
    """Creates a transparent preview checkerboard."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            c = col1 if ((x // tile_size) + (y // tile_size)) % 2 == 0 else col2
            draw.rectangle([x, y, x + tile_size, y + tile_size], fill=c)
    return img


def generate_composite_preview(arc_img, ring_img):
    """
    Creates a clear composite preview (preview_vfx_composite.png)
    Showing both assets under:
    1. Dark Background (#14171E - night sky / deep cave tone)
    2. Light Background (#98B5D5 - bright daylight sky / outdoor tone)
    3. Checkerboard background (transparency audit)
    4. Blend Mode Mockup (Alpha vs Additive simulation)
    """
    canvas_w = 640
    canvas_h = 420
    canvas = Image.new('RGB', (canvas_w, canvas_h), color=(22, 24, 29))
    draw = ImageDraw.Draw(canvas)

    # Header title
    draw.text((20, 15), "AIR VFX TEXTURE PROTOTYPES (128x128 RGBA)", fill=(240, 245, 252))
    draw.text((20, 32), "Pale Air Palette #D8ECF8 | Soft Falloff | Zero Bounding Box Artifacts", fill=(140, 165, 190))

    sections = [
        ("Dark Tone (#13161C)", (19, 22, 28)),
        ("Sky Tone (#92B1D3)", (146, 177, 211)),
        ("Alpha Checkerboard", None),
        ("Additive Glow Sim", (16, 20, 30))
    ]

    card_w = 135
    card_h = 320
    top_y = 65

    for i, (title, bg_col) in enumerate(sections):
        left_x = 20 + i * 152
        
        # Section title
        draw.text((left_x, top_y), title, fill=(200, 215, 230))
        
        # Upper box: air_arc (128x128)
        box1_y = top_y + 22
        if bg_col is not None:
            box1 = Image.new('RGBA', (128, 128), color=(*bg_col, 255))
        else:
            box1 = create_checkerboard(128, 128, tile_size=8).convert('RGBA')
            
        if title == "Additive Glow Sim":
            # Simulate additive blending over dark background
            base_np = np.array(box1, dtype=np.float32)
            arc_np = np.array(arc_img, dtype=np.float32)
            alpha = (arc_np[:, :, 3:] / 255.0)
            add_rgb = base_np[:, :, :3] + arc_np[:, :, :3] * alpha * 1.2
            add_rgb = np.clip(add_rgb, 0, 255).astype(np.uint8)
            box1 = Image.fromarray(add_rgb, mode='RGB').convert('RGBA')
        else:
            box1.alpha_composite(arc_img)
            
        canvas.paste(box1.convert('RGB'), (left_x, box1_y))
        draw.rectangle([left_x, box1_y, left_x + 128, box1_y + 128], outline=(55, 65, 80))
        draw.text((left_x + 4, box1_y + 110), "air_arc.png", fill=(255, 255, 255, 180))

        # Lower box: air_ring (128x128)
        box2_y = box1_y + 144
        if bg_col is not None:
            box2 = Image.new('RGBA', (128, 128), color=(*bg_col, 255))
        else:
            box2 = create_checkerboard(128, 128, tile_size=8).convert('RGBA')

        if title == "Additive Glow Sim":
            base_np = np.array(box2, dtype=np.float32)
            ring_np = np.array(ring_img, dtype=np.float32)
            alpha = (ring_np[:, :, 3:] / 255.0)
            add_rgb = base_np[:, :, :3] + ring_np[:, :, :3] * alpha * 1.2
            add_rgb = np.clip(add_rgb, 0, 255).astype(np.uint8)
            box2 = Image.fromarray(add_rgb, mode='RGB').convert('RGBA')
        else:
            box2.alpha_composite(ring_img)

        canvas.paste(box2.convert('RGB'), (left_x, box2_y))
        draw.rectangle([left_x, box2_y, left_x + 128, box2_y + 128], outline=(55, 65, 80))
        draw.text((left_x + 4, box2_y + 110), "air_ring.png", fill=(255, 255, 255, 180))

    return canvas


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating VFX textures...")

    arc_img = generate_air_arc(size=128)
    arc_path = os.path.join(OUTPUT_DIR, "air_arc.png")
    arc_img.save(arc_path, format="PNG")
    print(f"Saved: {arc_path}")

    ring_img = generate_air_ring(size=128)
    ring_path = os.path.join(OUTPUT_DIR, "air_ring.png")
    ring_img.save(ring_path, format="PNG")
    print(f"Saved: {ring_path}")

    composite_img = generate_composite_preview(arc_img, ring_img)
    preview_path = os.path.join(OUTPUT_DIR, "preview_vfx_composite.png")
    composite_img.save(preview_path, format="PNG")
    print(f"Saved: {preview_path}")

    # Inspect border alpha values to mathematically verify NO bounding box artifacts
    arc_arr = np.array(arc_img)
    ring_arr = np.array(ring_img)
    
    border_pixels_arc = np.concatenate([
        arc_arr[0, :, 3], arc_arr[-1, :, 3], arc_arr[:, 0, 3], arc_arr[:, -1, 3]
    ])
    border_pixels_ring = np.concatenate([
        ring_arr[0, :, 3], ring_arr[-1, :, 3], ring_arr[:, 0, 3], ring_arr[:, -1, 3]
    ])
    
    print(f"air_arc max border alpha: {border_pixels_arc.max()} (must be 0)")
    print(f"air_ring max border alpha: {border_pixels_ring.max()} (must be 0)")
    print(f"air_ring center pixel (64,64) alpha: {ring_arr[64, 64, 3]} (must be 0)")


if __name__ == "__main__":
    main()
