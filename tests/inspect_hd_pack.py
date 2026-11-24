import zipfile

zip_path = r"d:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft\resourcepacks\HDResourcePack.zip"

with zipfile.ZipFile(zip_path, "r") as z:
    all_files = z.namelist()

vfx_textures = [f for f in all_files if "vfx" in f.lower() and f.endswith(".png")]
vfx_models = [f for f in all_files if ("vfx" in f.lower() or "slash" in f.lower() or "impact" in f.lower() or "skill" in f.lower()) and f.endswith(".json")]

me_items = set()
for f in all_files:
    if "modelengine/items/" in f.lower():
        parts = f.split("/")
        for i, p in enumerate(parts):
            if p.lower() == "items" and i + 1 < len(parts):
                me_items.add(parts[i+1])

print(f"Total files: {len(all_files)}")
print(f"VFX Textures count: {len(vfx_textures)}")
print(f"VFX Models count: {len(vfx_models)}")
print(f"ModelEngine Unique Models: {len(me_items)}")

print("\n=== SAMPLE VFX TEXTURES ===")
for t in vfx_textures[:25]:
    print(" -", t)

print("\n=== SAMPLE MODELENGINE VFX MODELS ===")
vfx_me = [m for m in sorted(list(me_items)) if "vfx" in m.lower() or "slash" in m.lower() or "impact" in m.lower() or "strike" in m.lower() or "fire" in m.lower() or "water" in m.lower() or "earth" in m.lower()]
for m in vfx_me[:35]:
    print(" -", m)

print("\n=== ELEMENTAL VISUAL BREAKDOWN ===")
for elem in ["earth", "water", "fire", "wind", "air", "thunder", "slash", "impact"]:
    matches = [f for f in all_files if elem in f.lower() and (f.endswith(".png") or f.endswith(".json"))]
    print(f"Keyword '{elem}': {len(matches)} files")
