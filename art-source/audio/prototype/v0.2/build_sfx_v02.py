import os
import shutil
import json
import wave

src_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype"
dst_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype\v0.2"
os.makedirs(dst_dir, exist_ok=True)

# Copy available audio files with exact variant names
mapping = {
    "fire_jab.wav": "fire_jab_1.wav",
    "flame_sweep.wav": "flame_sweep_1.wav",
    "fire_jet.wav": "fire_jet_start_1.wav",
    "fire_impact.wav": "fire_impact_1.wav",
    "staff_thrust.wav": "staff_thrust_1.wav",
    "staff_spin.wav": "staff_spin_1.wav",
    "staff_sweep.wav": "staff_sweep_1.wav",
    "air_vortex.wav": "air_vortex_cast_1.wav",
    "staff_impact.wav": "staff_impact_medium.wav"
}

for src_name, dst_name in mapping.items():
    sp = os.path.join(src_dir, src_name)
    dp = os.path.join(dst_dir, dst_name)
    if os.path.exists(sp):
        shutil.copy2(sp, dp)
        print(f"Copied {src_name} -> v0.2/{dst_name}")

# Build 14 core events / 27 variants manifest
manifest_v02 = {
    "manifest_version": "0.2-revised",
    "project": "Avatar: Elements",
    "target_stage": "Stage 2 - Vertical Prototype",
    "audio_target_format": "Minecraft Native OGG Vorbis 44.1kHz (Format saat ini: WAV PCM 16-bit Mono mockup)",
    "total_core_events": 14,
    "total_variants": 27,
    "total_variants_available": 9,
    "total_variants_pending": 18,
    "origin_and_license_rationale": {
        "origin": "Proyek internal Avatar: Elements (Disintesis secara matematis melalui modulasi frekuensi DSP Python)",
        "license_basis": "Karya prosedural orisinal buatan sendiri, bebas dari sampel berhak cipta pihak ketiga, dilisensikan di bawah CC0 (Public Domain Dedication) untuk penggunaan internal dan rilis mod.",
        "technical_limitations": "Audio yang tersedia saat ini berstatus MOCKUP AUDIO SINTETIS PROSEDURAL untuk verifikasi timeline dan sinkronisasi kombo; BUKAN rekaman studio Foley aktor laga asli. Memerlukan konversi ke OGG Vorbis dan registrasi sounds.json resmi sebelum pengujian in-game."
    },
    "events": [
        {
            "event_id": "avatar_elements:fire_jab",
            "category": "Fire Unarmed - Serangan Kombo 1",
            "description": "Pukulan tinju api cepat (windup 2t, active 3t, recovery 4t)",
            "variants": [
                {"variant_name": "fire_jab_1.wav", "duration": 0.35, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/fire_jab_1.wav"},
                {"variant_name": "fire_jab_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "fire_jab_3.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:flame_sweep",
            "category": "Fire Unarmed - Serangan Kombo 2",
            "description": "Tebasan sabit api menyapu 180 derajat (windup 3t, active 8t, recovery 6t)",
            "variants": [
                {"variant_name": "flame_sweep_1.wav", "duration": 0.65, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/flame_sweep_1.wav"},
                {"variant_name": "flame_sweep_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:fire_finisher",
            "category": "Fire Unarmed - Serangan Kombo 3 Penutup",
            "description": "Hentakan pukulan api ledakan penutup kombo",
            "variants": [
                {"variant_name": "fire_finisher_1.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "fire_finisher_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:fire_jet_start",
            "category": "Fire Unarmed - Skill Mobilitas (Ignition)",
            "description": "Letupan semburan api awal saat meluncur maju",
            "variants": [
                {"variant_name": "fire_jet_start_1.wav", "duration": 0.80, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/fire_jet_start_1.wav"},
                {"variant_name": "fire_jet_start_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:fire_jet_loop",
            "category": "Fire Unarmed - Skill Mobilitas (Loop)",
            "description": "Suara desis dorongan api kontinu di kaki selama gliding",
            "variants": [
                {"variant_name": "fire_jet_loop.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:fire_guard_cast",
            "category": "Fire Unarmed - Skill Pertahanan",
            "description": "Kobaran perisai api melingkar menangkis proyektil",
            "variants": [
                {"variant_name": "fire_guard_cast_1.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "fire_guard_cast_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:fire_impact",
            "category": "Fire Unarmed - Dampak Benturan",
            "description": "Suara ledakan dan sambaran panas saat jurus api menghantam target",
            "variants": [
                {"variant_name": "fire_impact_1.wav", "duration": 0.50, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/fire_impact_1.wav"},
                {"variant_name": "fire_impact_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "fire_impact_3.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:staff_thrust",
            "category": "Air Staff - Serangan Kombo 1",
            "description": "Tusukan lurus tongkat kayu berdesing di udara",
            "variants": [
                {"variant_name": "staff_thrust_1.wav", "duration": 0.30, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/staff_thrust_1.wav"},
                {"variant_name": "staff_thrust_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:staff_spin",
            "category": "Air Staff - Serangan Kombo 2",
            "description": "Putaran baling-baling tongkat kayu menangkis dan memukul",
            "variants": [
                {"variant_name": "staff_spin_1.wav", "duration": 0.75, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/staff_spin_1.wav"},
                {"variant_name": "staff_spin_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:staff_sweep",
            "category": "Air Staff - Serangan Kombo 3",
            "description": "Sapuan mendatar tongkat menghempaskan angin kencang",
            "variants": [
                {"variant_name": "staff_sweep_1.wav", "duration": 0.45, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/staff_sweep_1.wav"},
                {"variant_name": "staff_sweep_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:air_vortex_cast",
            "category": "Air Staff - Skill Khas (Inisiasi)",
            "description": "Hentakan tongkat membangkitkan pusaran angin sentrifugal",
            "variants": [
                {"variant_name": "air_vortex_cast_1.wav", "duration": 1.20, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/air_vortex_cast_1.wav"},
                {"variant_name": "air_vortex_cast_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:air_vortex_loop",
            "category": "Air Staff - Skill Khas (Loop)",
            "description": "Deru pusaran angin tornado berputar kontinu menyedot entitas",
            "variants": [
                {"variant_name": "air_vortex_loop.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:staff_impact",
            "category": "Air Staff - Dampak Benturan",
            "description": "Hantaman tumpul kayu mengenai tubuh lawan",
            "variants": [
                {"variant_name": "staff_impact_soft.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "staff_impact_medium.wav", "duration": 0.25, "status": "FILE DIBUAT (Mockup Sintetis)", "path": "v0.2/staff_impact_medium.wav"},
                {"variant_name": "staff_impact_heavy.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        },
        {
            "event_id": "avatar_elements:staff_parry",
            "category": "Air Staff - Tangkisan Kayu",
            "description": "Benturan kayu tongkat menangkis senjata tajam atau panah",
            "variants": [
                {"variant_name": "staff_parry_1.wav", "duration": None, "status": "BELUM DIBUAT", "path": None},
                {"variant_name": "staff_parry_2.wav", "duration": None, "status": "BELUM DIBUAT", "path": None}
            ]
        }
    ]
}

out_manifest = os.path.join(dst_dir, "SFX_MANIFEST_v02.json")
with open(out_manifest, "w", encoding="utf-8") as f:
    json.dump(manifest_v02, f, indent=2)
print("Saved revised manifest v0.2 to:", out_manifest)
