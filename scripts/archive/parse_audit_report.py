import json
import os

with open(r"d:\repo\Minecraft Mod & Rp\scripts\audit_report.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("="*60)
print("AUDIT FINDINGS BREAKDOWN")
print("="*60)
for k, v in data.items():
    if isinstance(v, list):
        print(f"{k}: {len(v)}")
    else:
        print(f"{k}: {v}")

print("\n--- DETAIL OF CRITICAL ISSUES ---")
print(f"1. PNG Errors ({len(data['png_errors'])}):")
for item in data["png_errors"]:
    print("  ", item)

print(f"\n2. Zero-Byte Files ({len(data['zero_byte_files'])}):")
for item in data["zero_byte_files"]:
    print("  ", item)

print(f"\n3. Illegal Rotations ({len(data['illegal_rotations'])}):")
for item in data["illegal_rotations"][:10]:
    print("  ", item)

print(f"\n4. Out of Bounds Elements ({len(data['out_of_bounds_elements'])}):")
for item in data["out_of_bounds_elements"][:10]:
    print("  ", item)

print(f"\n5. CMD Conflicts ({len(data['cmd_conflicts'])}):")
for item in data["cmd_conflicts"]:
    print("  ", item)

print(f"\n6. Missing Model References ({len(data['missing_model_references'])}):")
for item in data["missing_model_references"]:
    print("  ", item)

print(f"\n7. Missing Textures ({len(data['missing_textures'])}):")
for item in data["missing_textures"]:
    print("  ", item)

print(f"\n8. Sounds Issues ({len(data['sounds_issues'])}):")
for item in data["sounds_issues"]:
    print("  ", item)
