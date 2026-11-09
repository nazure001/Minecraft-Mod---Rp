> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# ARCHITECTURE.md — Arsitektur Teknis

## Runtime saat ini (diaudit dari source dan resource)

Mod menggunakan Fabric 1.21.1 dengan source set `main` dan `client`. Client menangani keybind, HUD, renderer, dan state VFX lokal; server menangani validasi cast, chi/cooldown, timeline, hitbox/efek skill dan sinkronisasi phase. Server menjadi authority untuk hasil gameplay; dokumen rancangan W di bawah belum berarti manipulasi dunia/profesi sudah diimplementasikan.

### Networking

Payload aktual didefinisikan di `SkillPackets`:

| Arah | Payload |
|---|---|
| Client → Server | `C2SSkillInput`, `C2SSlotCast`, `C2SHoldStart`, `C2SHoldRelease`, `C2SSetElement` |
| Server → Client | `S2CSkillResult`, `S2CHudUpdate`, `S2CPhaseSync` |

`S2CPhaseSync` menyertakan UUID caster, skill ID, nama phase, tick phase, dan cast serial. Ini bukan packet `S2C_AnimationTrigger` seperti deskripsi scaffold lama.

### State dan konfigurasi

| Data | Lokasi/format aktual | Batasan yang diketahui |
|---|---|---|
| Chi, cooldown, mastery, elemen aktif, timeline/kombo | `PlayerBendingData` via Fabric `AttachmentType` | State saat ini tidak dipersistenkan lintas sesi |
| Definisi skill | Bundled `data/avatar_elements/skill_definitions.json` | Loader mendahulukan override `config/avatar_elements/skill_definitions.json`; parser manual hanya membaca field yang didukung |
| Pemetaan slot | Bundled `data/avatar_elements/element_slots.json` | Lima slot per elemen; belum ada override config |
| Preferensi client/server JSON | Belum ada sistem file config umum | Jangan menganggap path `config/avatar/...` pada rancangan lama sudah tersedia |

Runtime package root adalah `com.avatarmod.elements`; implementasi utama berada di `data/`, `network/`, `skill/`, `entity/`, `particle/`, dan client `client/`. Mod ID/asset namespace adalah `avatar_elements`; skill ID berbentuk string saat ini memakai prefix `avatar:`.

### Dependency dan build

`mod/build.gradle` mendeklarasikan Fabric Loom, Minecraft 1.21.1, Fabric Loader/API, dan Player Animation Library. Client source mengimpor PAL; namun `fabric.mod.json` belum mencantumkannya di `depends`, sehingga metadata dependency perlu direkonsiliasi sebelum paket distribusi. Epic Fight yang ada di `reference/` adalah referensi NeoForge, bukan dependency runtime mod Fabric; WTHIT/JADE juga bukan dependency yang dideklarasikan.

### Charge orb (as-built)

`OrbVisualConfig` mengaktifkan orb untuk `fire_jab` (WINDUP/ACTIVE), `fire_blast` (WINDUP/HOLD), `fire_jet` (WINDUP/ACTIVE), dan `air_blast` (WINDUP/ACTIVE). Renderer third-person memakai `KnuckleVfxHelper` untuk client player dan fallback offset berbasis yaw untuk player lain. Renderer first-person memakai offset camera-relative berbasis yaw/pitch; itu bukan query PAL bone/viewmodel hand transform. Nilai optik dan phase ini berasal dari source dan belum semuanya dinyatakan lolos uji visual.

---

## Arsitektur target: manipulasi dunia dan profesi (rancangan 2026-11-08)

Pekerjaan A–D tidak diperluas saat berjalan. Komponen berikut adalah kontrak desain, bukan kelas yang sudah ada.
- AbilityDefinition: aktivasi, durasi, sustain, efek entity/world, sumber, progression, dan event presentasi.
- AbilitySession: state server per cast, serial, waktu server, interrupt; memakai validator/resource/timeline yang ada.
- ConstructState: identitas dan pemilik konstruksi; dapat hidup lebih lama dari cast; referensi transaksi material.
- MaterialTransaction/Ledger: reserve → remove → in-control → place/drop/reclaim; commit/abort idempoten dan tersimpan.
- WorldPermissionAdapter: validasi sumber, tujuan, claim, PvP dan entity; jika integrasi claim tak tersedia, jangan mengklaim kompatibel.
- ProgressionProfile: tribe, elemen, mastery, teknik, profesi dan latihan; seluruh unlock diverifikasi server.
- Presentation: snapshot server menggerakkan animasi, attachment, VFX/SFX, preview; client tidak menentukan collision/damage.

Satu sumber konfigurasi runtime yang diparsing dipakai validasi dan hasil sinkronisasi HUD; dokumen menjadi referensi desain.
Path/schema loader aktual harus diaudit sebelum migrasi; jangan menambah registry atau chi/timeline kedua.
Ability bertipe utility memakai damage resolver yang sama dengan combat bila efek ofensif didefinisikan.

Persistence harus menyimpan pemilik/serial/material/konstruksi dan hasil transaksi; tangani save/restart/chunk unload,
disconnect, pindah dimensi, transaksi sebagian, serta resource contention dua pemain.
Temporary restore memerlukan deteksi konflik dan rekonsiliasi material, bukan sekadar setBlock snapshot lama.
Budget server: batasi volume, collision, entity debris, batch world edit, tracking dan jarak render.
Partikel/debris visual tidak menambah item atau menentukan kerusakan.

---

## UI gulungan modular (2026-11-08)

Acuan: `UI_THEME_SPEC.md`. Satu renderer/layout widget memakai theme tokens untuk lima identitas, bukan lima logika screen.
Screen/settings memakai perkamen modular; teks dan komponen terpisah dari background. HUD memakai bingkai kecil.
Preference client (tema/skala/posisi/efek/audio) terpisah dari authoritative player/server state.
Data HUD, profil, tooltip dan skill tree memakai definisi/snapshot yang sama; dilarang hardcode tabel gameplay kedua.
Input screen dikonsumsi sebelum combat; close/focus loss ditangani agar hold tidak macet.
Tidak ada dependency wajib Essential/RPG-HUD. Tidak menyalin GUI, font atau aset reference otomatis.
