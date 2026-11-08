from PIL import Image
import os

brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

for fname in ['neutral_rig_front.png', 'neutral_rig_side.png', 'neutral_rig_perspective.png']:
    p = os.path.join(brain_dir, fname)
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{fname:30s}: size={im.size}, non-transparent bbox={bbox}")
    if bbox:
        # Check pixel samples across Y
        mid_x = (bbox[0] + bbox[2]) // 2
        print(f"  Width={bbox[2]-bbox[0]}, Height={bbox[3]-bbox[1]}")
        # Sample head (Y around top of bbox + 10%)
        y_head = bbox[1] + int((bbox[3]-bbox[1]) * 0.1)
        y_torso = bbox[1] + int((bbox[3]-bbox[1]) * 0.4)
        y_legs = bbox[1] + int((bbox[3]-bbox[1]) * 0.8)
        print(f"  Head pixel at ({mid_x}, {y_head}): {im.getpixel((mid_x, y_head))}")
        print(f"  Torso pixel at ({mid_x}, {y_torso}): {im.getpixel((mid_x, y_torso))}")
        print(f"  Legs pixel at ({mid_x}, {y_legs}): {im.getpixel((mid_x, y_legs))}")
