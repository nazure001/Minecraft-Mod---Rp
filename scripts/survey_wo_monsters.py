import os

ref_wo = r"d:\repo\Minecraft Mod & Rp\reference\WOLegendaryMonsters-1.1.0-forge-1.20.1"
print(f"Surveying: {ref_wo}")

for root, dirs, files in os.walk(ref_wo):
    for f in files:
        if f.endswith((".geo.json", ".animation.json", ".png")):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ref_wo)
            print(f"{rel} ({os.path.getsize(p)} bytes)")
