import os
import json
import wave

manifest_dir = r"D:\repo\Minecraft Mod & Rp\art-source\audio\prototype\v0.2"

# 14 Core Events and their variants definition
# Strictly aligned with the 14 core events and 27 variants specification
# Every legacy mapping is justified by sound character rationale; no artificial renaming.
events_spec = [
    {
        "event": "avatar_elements:fire.swing",
        "description": "Suara ayunan serangan api",
        "variants": [
            {
                "name": "fire_swing_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "flame_sweep.wav",
                "sound_character_rationale": "Sapuan frekuensi desiran api 200-800Hz (durasi 0.65s), cocok merepresentasikan ayunan serangan api sebelum mengenai sasaran."
            },
            {
                "name": "fire_swing_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi foley ayunan api sekunder (belum tersedia di draft lama)."
            },
            {
                "name": "fire_swing_3.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi foley ayunan api tersier (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:fire.release",
        "description": "Pelepasan letupan api instan dari tinju/tendangan",
        "variants": [
            {
                "name": "fire_release_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "fire_jab.wav",
                "sound_character_rationale": "Letupan pendek pop kompresi udara panas (durasi 0.35s), cocok merepresentasikan pelepasan api instan dari tinju/tendangan."
            },
            {
                "name": "fire_release_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi letupan pelepasan api sekunder (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:fire.impact",
        "description": "Benturan dan sambaran api mengenai sasaran",
        "variants": [
            {
                "name": "fire_impact_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "fire_impact.wav",
                "sound_character_rationale": "Ledakan benturan bass ~60Hz berpadu suara sambaran api membakar target (durasi 0.50s)."
            },
            {
                "name": "fire_impact_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi ledakan benturan sekunder (belum tersedia di draft lama)."
            },
            {
                "name": "fire_impact_3.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi ledakan benturan tersier (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:fire.charge_start",
        "description": "Inisiasi pengisian energi api atau ignition semburan lunge",
        "variants": [
            {
                "name": "fire_charge_start_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "fire_jet.wav",
                "sound_character_rationale": "Deru pengapian awal (ignition swell) yang naik secara eksponensial (durasi 0.80s), cocok untuk inisiasi luncuran semburan api."
            }
        ]
    },
    {
        "event": "avatar_elements:fire.charge_loop",
        "description": "Deru kobaran api kontinu selama pengisian atau luncuran",
        "variants": [
            {
                "name": "fire_charge_loop_1.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan looping audio deru kobaran api mulus tanpa sambungan klik (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:fire.charge_release",
        "description": "Pelepasan energi api terisi secara eksplosif",
        "variants": [
            {
                "name": "fire_charge_release_1.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan letupan pelepasan energi api bermassa besar (belum tersedia di draft lama)."
            },
            {
                "name": "fire_charge_release_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi pelepasan energi api sekunder (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:staff.swing",
        "description": "Desiran ayunan bilah tongkat kayu di udara",
        "variants": [
            {
                "name": "staff_swing_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "staff_sweep.wav",
                "sound_character_rationale": "Desiran kayu padat membelah massa udara (durasi 0.45s), merepresentasikan ayunan tongkat di udara."
            },
            {
                "name": "staff_swing_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi desiran ayunan tongkat kayu sekunder (belum tersedia di draft lama)."
            },
            {
                "name": "staff_swing_3.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi desiran ayunan tongkat kayu tersier (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:staff.spin",
        "description": "Putaran tongkat kayu berulang secara kontinu",
        "variants": [
            {
                "name": "staff_spin_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "staff_spin.wav",
                "sound_character_rationale": "Putaran tongkat kayu berulang secara siklik (~5Hz osilasi, durasi 0.75s), cocok merepresentasikan teknik baling-baling tongkat."
            },
            {
                "name": "staff_spin_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi putaran tongkat kayu berkecepatan berbeda (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:staff.impact",
        "description": "Benturan tumpul tongkat kayu mengenai target",
        "variants": [
            {
                "name": "staff_impact_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "staff_impact.wav",
                "sound_character_rationale": "Benturan tumpul kayu keras membentur benda padat (resonansi transient ~190Hz, durasi 0.25s)."
            },
            {
                "name": "staff_impact_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi benturan tumpul kayu sekunder (belum tersedia di draft lama)."
            },
            {
                "name": "staff_impact_3.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi benturan tumpul kayu tersier (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:air.release",
        "description": "Hembusan pelepasan tekanan udara",
        "variants": [
            {
                "name": "air_release_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "staff_thrust.wav",
                "sound_character_rationale": "Hembusan dorongan udara tajam dan terfokus (durasi 0.30s), merepresentasikan pelepasan tekanan udara."
            },
            {
                "name": "air_release_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi dorongan pelepasan udara sekunder (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:air.impact",
        "description": "Dentuman benturan tekanan udara mengenai sasaran",
        "variants": [
            {
                "name": "air_impact_1.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan dentuman benturan gelombang tekanan angin ke tubuh/dinding (belum tersedia di draft lama)."
            },
            {
                "name": "air_impact_2.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan variasi dentuman benturan udara sekunder (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:air.vortex_start",
        "description": "Inisiasi pembentukan pusaran angin",
        "variants": [
            {
                "name": "air_vortex_start_1.wav",
                "status": "FILE DIBUAT (Draft Mockup Sintetis)",
                "source_draft": "air_vortex.wav",
                "sound_character_rationale": "Pusaran angin sentrifugal resonan berdurasi 1.20s yang mengawali pembentukan pusaran udara."
            }
        ]
    },
    {
        "event": "avatar_elements:air.vortex_loop",
        "description": "Deru pusaran angin berputar kontinu",
        "variants": [
            {
                "name": "air_vortex_loop_1.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan loop angin tornado kontinu tanpa jeda klik (belum tersedia di draft lama)."
            }
        ]
    },
    {
        "event": "avatar_elements:air.vortex_end",
        "description": "Peredaan atau pelepasan akhir pusaran angin",
        "variants": [
            {
                "name": "air_vortex_end_1.wav",
                "status": "BELUM DIBUAT",
                "source_draft": None,
                "sound_character_rationale": "Memerlukan suara pelepasan atau peredaan pusaran angin (belum tersedia di draft lama)."
            }
        ]
    }
]

# Process variants and extract metadata strictly from files
processed_events = []
total_variants_count = 0
available_variants_count = 0
pending_variants_count = 0

for ev in events_spec:
    ev_variants = []
    for var in ev["variants"]:
        total_variants_count += 1
        var_name = var["name"]
        status = var["status"]
        source_draft = var["source_draft"]
        sound_rationale = var["sound_character_rationale"]
        
        if status.startswith("FILE DIBUAT"):
            rel_path = var_name # Relatif terhadap lokasi manifest
            abs_path = os.path.join(manifest_dir, rel_path)
            
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"File varian yang dinyatakan tersedia tidak ditemukan: {abs_path}")
            
            with wave.open(abs_path, "rb") as wf:
                nchannels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                nframes = wf.getnframes()
                duration = round(nframes / float(framerate), 4)
                bit_depth = sampwidth * 8
            
            available_variants_count += 1
            ev_variants.append({
                "name": var_name,
                "relative_path": rel_path,
                "status": status,
                "source_draft": source_draft,
                "sound_character_rationale": sound_rationale,
                "audio_properties": {
                    "duration_seconds": duration,
                    "sample_rate_hz": framerate,
                    "channels": nchannels,
                    "bit_depth": bit_depth
                }
            })
        else:
            pending_variants_count += 1
            ev_variants.append({
                "name": var_name,
                "relative_path": None,
                "status": status,
                "source_draft": None,
                "sound_character_rationale": sound_rationale,
                "audio_properties": None
            })
    
    processed_events.append({
        "event": ev["event"],
        "description": ev["description"],
        "total_variants": len(ev_variants),
        "variants": ev_variants
    })

# Validasi penghitungan dari array
calculated_total_events = len(processed_events)
calculated_total_variants = sum(len(e["variants"]) for e in processed_events)
assert calculated_total_events == 14, f"Total event harus 14, didapat {calculated_total_events}"
assert calculated_total_variants == 27, f"Total varian harus 27, didapat {calculated_total_variants}"
assert available_variants_count == 9, f"Varian tersedia harus 9, didapat {available_variants_count}"
assert pending_variants_count == 18, f"Varian pending harus 18, didapat {pending_variants_count}"

manifest_data = {
    "manifest_version": "0.2-revised",
    "project": "Avatar: Elements",
    "mod_id": "avatar_elements",
    "status": "DRAFT PARSIAL, MENUNGGU REVIEW ASET",
    "audio_format_current": "WAV PCM 16-bit 44.1kHz Mono (Draft Mockup Sintetis)",
    "audio_format_target": "OGG Vorbis 44.1kHz (Minecraft Native Runtime)",
    "counters_calculated_from_array": {
        "total_core_events": calculated_total_events,
        "total_variants": calculated_total_variants,
        "variants_draft_available": available_variants_count,
        "variants_pending": pending_variants_count
    },
    "documentation": {
        "origin": "Proyek internal Avatar: Elements (Disintesis secara matematis menggunakan modulasi frekuensi DSP Python)",
        "license_basis": "Karya prosedural orisinal tanpa sampel pihak ketiga berhak cipta. Dilisensikan di bawah CC0 (Public Domain Dedication) untuk kebutuhan internal proyek mod.",
        "mapping_policy": "Pemetaan draf audio lama ke event baru didasarkan murni pada kesesuaian karakter akustik (sapuan frekuensi, resonansi kayu, durasi letupan, atau pusaran), bukan sekadar mengganti nama file agar jumlah terpenuhi. Sebanyak 18 varian lainnya yang belum memiliki karakter audio yang cocok dicatat jujur berstatus BELUM DIBUAT.",
        "technical_limitation": "Audio saat ini berstatus DRAFT MOCKUP SINTETIS PROSEDURAL untuk verifikasi keberadaan event dan alur trigger; BUKAN rekaman studio foley aktor laga asli. Tidak mengandung estimasi timing gameplay tanpa spesifikasi resmi. Belum dikonversi ke OGG Vorbis dan belum diuji in-game."
    },
    "core_events": processed_events
}

manifest_path = os.path.join(manifest_dir, "SFX_MANIFEST_v02.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2)

print(f"SFX Manifest v0.2 generated successfully at: {manifest_path}")
print(f" - Events: {calculated_total_events}")
print(f" - Variants total: {calculated_total_variants}")
print(f" - Available: {available_variants_count}")
print(f" - Pending: {pending_variants_count}")
