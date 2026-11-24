import os

for sub in ["Avatar-Addon-1.3.2-Beta", "avatarmod-0.3.0"]:
    p = os.path.join(r"d:\repo\Minecraft Mod & Rp\reference", sub)
    print(f"=== {sub} ===")
    if os.path.exists(p):
        for root, dirs, files in os.walk(p):
            for f in files:
                if f.endswith((".geo.json", ".animation.json", ".bbmodel", ".png")) and "entity" in root:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, p)
                    print(f"  {rel} ({os.path.getsize(full)} bytes)")
