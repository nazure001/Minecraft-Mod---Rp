from PIL import Image
import os

brain_dir = r'C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71'

for fname in ['ready_pose_clean_front.png', 'ready_pose_clean_side.png', 'ready_pose_clean_perspective.png']:
    p = os.path.join(brain_dir, fname)
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{fname:35s}: size={im.size}, non-transparent bbox={bbox}")
