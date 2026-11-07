import os

dp = r"C:\Users\USER\AppData\Roaming\PrismLauncher\instances\Remarkably Optimized 1.0.0\minecraft\saves\avatar\datapacks\avatar-armor-datapack"
errs = []
for root, dirs, files in os.walk(dp):
    for f in files:
        if f.endswith(".mcfunction"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                for idx, line in enumerate(fp, 1):
                    if "\\u" in line:
                        errs.append((f, idx, "unicode escape"))
                    if "particle minecraft:block" in line:
                        errs.append((f, idx, "block particle"))
                    if "particle minecraft:dust " in line:
                        errs.append((f, idx, "old dust particle"))
print(f"Datapack check: {len(errs)} errors found!")
if errs:
    for e in errs:
        print(e)
