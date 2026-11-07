import os
import re

dp_dirs = [
    r"d:\repo\avatar-armor-datapack",
    r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft\saves\avatar\datapacks\avatar-armor-datapack"
]

for d in dp_dirs:
    for root, dirs, files in os.walk(d):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                t = fp.read()
            orig = t
            t = t.replace("Dolphin's", "Dolphins")
            t = t.replace("Ocean's", "Oceans")
            t = re.sub(r"particle\s+minecraft:dust(?:\s+[\d\.]+)+\s+", "particle minecraft:spore_blossom_air ", t)
            if t != orig:
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write(t)
                print(f"Updated {f} in {d}")
