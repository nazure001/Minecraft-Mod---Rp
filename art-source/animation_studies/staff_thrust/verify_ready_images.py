from PIL import Image
import os

brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

for fname in ['ready_pose_front.png', 'ready_pose_side.png', 'ready_pose_perspective.png']:
    p = os.path.join(brain_dir, fname)
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{fname:30s}: size={im.size}, non-transparent bbox={bbox}")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    print(f"  Width={w}, Height={h}, Margin L={bbox[0]}, R={800-bbox[2]}, T={bbox[1]}, B={800-bbox[3]}")
