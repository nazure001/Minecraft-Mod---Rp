from PIL import Image
import os

brain_dir = r'C:\Users\USER\.gemini\antigravity\brain\54a80670-a4c4-4299-bd5f-db191f100d71'

for fname in ['ready_v2_clean_front.png', 'ready_v2_clean_side.png', 'ready_v2_clean_perspective.png']:
    p = os.path.join(brain_dir, fname)
    im = Image.open(p)
    bbox = im.getbbox()
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    print(f"{fname:35s}: bbox={bbox}, w={w}, h={h}")
    print(f"  Margin Left={bbox[0]}, Right={800-bbox[2]}, Top={bbox[1]}, Bottom={800-bbox[3]}")
