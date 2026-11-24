import os

ref_base = r"d:\repo\Minecraft Mod & Rp\reference\avatar-legend-reforged-1.3.0"
print(f"Surveying: {ref_base}")

for root, dirs, files in os.walk(ref_base):
    for f in files:
        if f.endswith((".geo.json", ".animation.json", ".png")):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ref_base)
            print(f"{rel} ({os.path.getsize(p)} bytes)")
