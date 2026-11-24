import os
from PIL import Image

base = r"d:\repo\Minecraft Mod & Rp\mod\src\main\resources\assets\avatar_elements\textures\entity"
print("Scanning:", base)

for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".png"):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base)
            try:
                with Image.open(p) as img:
                    # sample unique colors or check if it's flat
                    colors = len(set(img.getdata()))
                    print(f"{rel}: size={img.size}, mode={img.mode}, unique_colors={colors}, file_size={os.path.getsize(p)} bytes")
            except Exception as e:
                print(f"{rel}: ERROR {e}")
