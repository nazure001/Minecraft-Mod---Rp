import os
import shutil
import wave

src_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype"
dst_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype\v0.2"
os.makedirs(dst_dir, exist_ok=True)

# Copy 9 available audio files from prototype draft to v0.2 matching exact variant naming
mapping = {
    "flame_sweep.wav": "fire_swing_1.wav",
    "fire_jab.wav": "fire_release_1.wav",
    "fire_impact.wav": "fire_impact_1.wav",
    "fire_jet.wav": "fire_charge_start_1.wav",
    "staff_sweep.wav": "staff_swing_1.wav",
    "staff_spin.wav": "staff_spin_1.wav",
    "staff_impact.wav": "staff_impact_1.wav",
    "staff_thrust.wav": "air_release_1.wav",
    "air_vortex.wav": "air_vortex_start_1.wav"
}

print("Synchronizing 9 available WAV files:")
for src_name, dst_name in mapping.items():
    sp = os.path.join(src_dir, src_name)
    dp = os.path.join(dst_dir, dst_name)
    if os.path.exists(sp):
        shutil.copy2(sp, dp)
        print(f" - {src_name} -> {dst_name}")
    else:
        print(f" [!] Source not found: {sp}")
