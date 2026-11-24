import os
import zipfile
import shutil

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
ZIP_OUTPUT = os.path.join(REPO_ROOT, "Avatar_Elements_Master_Agent_Bundle.zip")
PROMPT_OUTPUT = os.path.join(REPO_ROOT, "docs", "COPY_PASTE_AGENT_PROMPT.txt")

def make_bundle():
    print("="*70)
    print("CREATING PORTABLE STANDALONE AGENT BUNDLE (ZIP)")
    print("="*70)

    # Folders and files to include in zip
    includes = [
        ("docs/MASTER_AGENT_HANDOFF_PACKAGE.md", "MASTER_AGENT_HANDOFF_PACKAGE.md"),
        ("docs/vfx_texture_and_asset_master_spec.md", "vfx_texture_and_asset_master_spec.md"),
        ("docs/mob_visual_mockup_showcase.md", "mob_visual_mockup_showcase.md"),
        ("docs/skills/minecraft-vfx-particle-authoring/SKILL.md", "SKILL_minecraft-vfx-particle-authoring.md"),
        ("scripts/audit_report.json", "audit_report.json"),
        ("scripts/total_asset_audit.py", "total_asset_audit.py")
    ]

    dir_includes = [
        ("mod/src", "mod/src"),
        ("avatar-skill-datapack", "avatar-skill-datapack"),
        ("avatar-skill-resourcepack", "avatar-skill-resourcepack"),
        ("avatar-armor-datapack", "avatar-armor-datapack"),
        ("avatar-armor-resourcepack", "avatar-armor-resourcepack"),
        ("art-source/showcase", "showcase_mockups")
    ]

    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add single files
        for rel_src, arc_dest in includes:
            full_src = os.path.join(REPO_ROOT, rel_src)
            if os.path.exists(full_src):
                zf.write(full_src, arc_dest)
                print(f"  Added file: {arc_dest}")

        # Add directories
        for rel_dir, arc_prefix in dir_includes:
            full_dir = os.path.join(REPO_ROOT, rel_dir)
            if os.path.exists(full_dir):
                for root, dirs, files in os.walk(full_dir):
                    # Skip any cache
                    dirs[:] = [d for d in dirs if d not in [".gradle", "build", "bin", "__pycache__", ".git"]]
                    for f in files:
                        p = os.path.join(root, f)
                        rel_in_dir = os.path.relpath(p, full_dir)
                        arc_path = os.path.join(arc_prefix, rel_in_dir).replace("\\", "/")
                        zf.write(p, arc_path)
                print(f"  Added directory tree: {arc_prefix}/")

    print(f"\nBundle created: {ZIP_OUTPUT} ({os.path.getsize(ZIP_OUTPUT)} bytes)")

if __name__ == "__main__":
    make_bundle()
