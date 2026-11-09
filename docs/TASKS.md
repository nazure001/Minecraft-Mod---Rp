> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# TASKS.md — Daftar Tugas Aktif

Format status: `[ ]` Belum | `[~]` Sedang dikerjakan | `[x]` Selesai

---

## Tahap 0 — Audit ✅

- [x] **T0-1** Inventaris semua aset (datapack, resourcepack, script, referensi) — Claude Code — 2026-11-07
- [x] **T0-2** Identifikasi konflik dan masalah kritis — Claude Code — 2026-11-07
- [x] **T0-3** Perbaiki masalah kritis datapack (chi failsafe, dua sistem skill, Avatar State) — Claude Code — 2026-11-07
- [x] **T0-4** Siapkan workspace (struktur folder, AGENTS.md, docs, .gitignore, Git init) — Claude Code — 2026-11-07

---

## Tahap 1 — Fondasi Fabric Mod

- [x] **T1-1** Scaffold mod Fabric 1.21.1 (fabric.mod.json, entry point, gradle) — Claude Code — 2026-11-07 — BUILD SUCCESSFUL (plugin: fabric-loom, Gradle 9.8.2, JDK25→JDK21, Yarn 1.21.1+build.3)
- [x] **T1-2** Implementasi keybinding test + C2S/S2C networking + rate limiting — Claude Code — 2026-11-07 — TERVERIFIKASI singleplayer ✅ + dedicated server ✅ (Player925, R→ack pipeline confirmed) (2 pemain: BELUM DIUJI)
- [x] **T1-3** Implementasi networking (C2S_SkillInput, S2C_SkillResult, S2C_HudUpdate) — Claude Code — 2026-11-07 — BUILD SUCCESSFUL, key G→fire_jab pipeline terdaftar ✅; air_staff item terdaftar + tampil in-game ✅ (posisi pegang menyusul saat moveset)
- [x] **T1-4** Implementasi `PlayerBendingData` (chi, cooldown, mastery, skills) via AttachmentType — Claude Code — 2026-11-07 — BUILD SUCCESSFUL ✅ (chi regen 1/4t, cooldown per skill, integrasi ke SkillNetworking)
- [x] **T1-5** Implementasi `SkillTimeline` (windup → active → recovery) — Claude Code — 2026-11-07 — BUILD SUCCESSFUL ✅ (IDLE→WINDUP→ACTIVE→RECOVERY→IDLE, di-tick via PlayerBendingData)
- [x] **T1-6** Implementasi `SkillValidator` server-side — Claude Code — 2026-11-07 — BUILD SUCCESSFUL ✅ (mastery+cooldown+chi+timeline check; SkillRegistry+SkillDefinition; SkillNetworking bersih dari tabel temp)
- [x] **T1-7** Implementasi `ChiManager` (regen, cost, clamp) — Claude Code — 2026-11-07 — BUILD SUCCESSFUL ✅ (regen pulse, cost multiplier, modifier API untuk T2+ buff/debuff)
- [x] **T1-8** HUD dasar (chi bar, cooldown, skill aktif) — Claude Code — 2026-11-07 — TERVERIFIKASI in-game ✅ (chi bar biru di atas hotbar, cooldown teks kuning, smooth lerp; NPE fix getAttachedOrCreate cbdecd9)
- [x] **T1-9** Konfigurasi bersama (JSON loader untuk skill_definitions) — Claude Code — 2026-11-07 — BUILD SUCCESSFUL ✅ (SkillConfigLoader baca dari jar; override via config/avatar_elements/skill_definitions.json)
- [x] **T1-10** Verifikasi berjalan di dedicated server tanpa crash — Claude Code — 2026-11-07 — TERVERIFIKASI ✅ (6 skill loaded dari JSON, fire_jab OK + cooldown aktif, chi bar HUD, dedicated server Done 3.193s)

---

## Tahap 2 — Prototipe Vertikal

- [x] **T2-1** Fire Jab: SPHERE 2.5, dmg 4.0, knockback 0.3, FLAME VFX, BLAZE_SHOOT SFX — TERVERIFIKASI in-game ✅
- [x] **T2-2** Flame Sweep: ARC 180°, 3 hit/active, dmg 6.0, +30% combo bonus — TERVERIFIKASI damage ✅ (Z key; ARC particles belum dikonfirmasi)
- [x] **T2-3** Fire Jet: velocity dash 2.2f, flame trail VFX — TERVERIFIKASI dash berfungsi ✅ (desain: dash singkat; rocket flight → backlog B-5)
- [x] **T2-4** Fire Guard: blok entity damage saat ACTIVE, shield shimmer VFX — particles ✅ (damage blocking belum diuji langsung)
- [x] **T2-5** Kombo Jab→Sweep→Jab: +50% dmg step3, range x1.3, lava particles — BUILD ✅ (belum diuji terpisah)
- [x] **T2-6** Air Staff Attack: 3-hit kombo (H), CLOUD particles — TERVERIFIKASI in-game ✅
- [x] **T2-7** Air Vortex: pull r6, 40 tik, spiral particles (V) — TERVERIFIKASI damage ✅ (pull VFX belum dikonfirmasi visual)
- [ ] **T2-8** Test sinkronisasi: dua pemain, dedicated server (chi/cooldown independen, kombo tidak tertukar)

---

## Tahap 3 — Empat Elemen (Gelombang 1)

- [x] **T3-1** Water Whip: LINE hitbox r6, dmg 3.0, pull knockback, DRIPPING_WATER+SPLASH VFX — keybinding C — BUILD ✅ (belum diuji)
- [x] **T3-2** Earth Boulder: projectile traveling 0.8b/t, dmg 5.0, lifetime 20 tik, no block modify — keybinding B — BUILD ✅ (belum diuji)
- [ ] **T3-3** Verifikasi Air Palm/Air Blast: definisi JSON dan handler `SkillDispatcher` kini ada; uji implementasi, nilai, dan pemetaan slot masih pending
- [ ] **T3-4** Test sinkronisasi T2-8 sebelum lanjut gelombang 2

---

## Tahap 3 — Charge Orb & Hold-Release Skills

- [x] **T3-5** Charge Orb VFX system: S2CPhaseSync, ChargeOrbRenderer (3rd), FirstPersonOrbRenderer (1st) — Claude Code — 2026-11-08
  - Fix: `setShader` missing → orb invisible
  - Fix: `new MatrixStack()` → `ctx.matrixStack()` pada 1st person renderer
  - Fix: skip self hanya saat 1st person (3rd person self-render kini berfungsi)
  - Fix: `timeline.tick()` dipindah ke SkillDispatcher agar IDLE broadcast terkirim saat skill selesai
  - Fix: additive blending (`SRC_ALPHA, ONE`) + alpha 0.40 untuk glowing sphere visual
  - Status: BUILD SUCCESSFUL, orb terlihat in-game ✅ (IDLE clearance & visual masih perlu verifikasi ulang)

- [x] **T3-6** Fire Blast: skill hold→release, charge grows orb, release spawns projectile entity — Antigravity — 2026-11-08
  - `cast_type: HOLD_RELEASE` terintegrasi dengan `C2SHoldStart` + `C2SHoldRelease`
  - Server-side charge state per player di SkillTimeline (Phase.HOLD, max 40 ticks)
  - FireBall projectile terbang ke arah pandang (speed 1.8 blok/tick)
  - Damage (35%-100% dari 7.0) & radius (1.0 - 3.0 blok) scaling dengan charge ratio
  - Orb membesar menggunakan interpolatedTicks() di ChargeOrbClientState dan KnuckleVfxHelper

- [x] **T3-7** Hold-Release framework generik: `C2SHoldStart`/`C2SHoldRelease` packet, Phase.HOLD di SkillTimeline — Antigravity — 2026-11-08
  - Prerequisite terintegrasi tanpa sistem chi/cooldown/timeline paralel
  - Siap dipakai untuk fire_blast, boulder_launch, lightning_strike, combustion_beam, ice_prison

- [x] **T3-8** Menyusun lima slot skill Fire — Antigravity — 2026-11-08
  - Slot Z: fire_jab (instant, terverifikasi)
  - Slot X: fire_blast (hold→release, baru)
  - Slot C: flame_sweep (instant, terverifikasi)
  - Slot V: fire_guard; Slot B: fire_jet (sesuai `element_slots.json`)

> T3-9 digabung ke T3-3: handler Air Blast sudah ada di source saat audit; ini bukan klaim build atau uji runtime yang lulus.

## Follow-up audit schema

- [ ] **SC-1** Validasi schema skill dan slot saat load: field wajib/enum, duplikasi ID, referensi slot yang tidak dikenal, serta laporkan resource/override invalid secara eksplisit.
- [ ] **SC-2** Tetapkan assignment slot WATER/EARTH; saat ini lima slot per elemen mengulang satu skill.
- [ ] **SC-3** Putuskan implementasi atau penghapusan perilaku `CHANNEL`, `TOGGLE`, dan chi sustain `chiPerTick`; enum/field saat ini belum menggerakkan perilaku runtime.
- [ ] **SC-4** Rekonsiliasi dependency PAL di Gradle dan metadata Fabric; client mengimpor PAL tetapi `fabric.mod.json` belum mendeklarasikannya di `depends`.

- [ ] **T3-10** Water Jet: channel skill, tekan+tahan untuk semburan air berkelanjutan

- [ ] **T3-11** Earth Pillar: raise column dari bawah target, launch ke atas

- [ ] **T3-12** Boulder Launch: hold→release, batu makin besar sesuai charge

---

## Tahap 3–8 (Gelombang Berikutnya)

Lihat `docs/PROJECT_PLAN.md` untuk daftar lengkap per tahap.
Lihat `docs/CONTENT_SPEC.md` → "Skill List Lengkap" untuk katalog semua teknik.

---

## Backlog (dari audit)

- [ ] **B-1** CIT tier armor: tambah layer definition untuk tier `basic` s/d `veteran` di resourcepack
- [ ] **B-2** Ganti XP vanilla sebagai progression → mastery tracking kustom
- [ ] **B-3** Pack format `pack.mcmeta` — verifikasi format 48 untuk 1.21.1
- [ ] **B-4** `avatar_skill_timer` di armor-datapack sudah tidak dipakai — hapus setelah konfirmasi
- [ ] **B-5** Fire Jet rocket flight: tahan tombol, chi berkelanjutan, aturan pendaratan (lanjutan dari dash T2-3)

---

## Selesai (arsip)

| ID | Deskripsi | Tanggal | Hasil |
|---|---|---|---|
| T0-1 | Audit aset | 2026-11-07 | 4 paket ditemukan, 4 masalah kritis teridentifikasi |
| T0-2 | Identifikasi konflik | 2026-11-07 | Dua sistem skill paralel, chi failsafe, Avatar State tanpa validasi |
| T0-3 | Perbaiki datapack | 2026-11-07 | 5 fix diterapkan, belum diuji di Minecraft |
| T0-4 | Setup workspace | 2026-11-07 | Struktur folder, docs, Git init |

---

## Backlog W — Manipulasi dunia, utilitas dan profesi (2026-11-08)

Semua status berikut BELUM DIIMPLEMENTASIKAN. Tidak mengubah status task lama menjadi terverifikasi.
- [ ] W-01 Audit schema/runtime config vs CONTENT_SPEC; pertahankan angka aktif sampai rekonsiliasi.
- [ ] W-02 Kontrak activation, duration, sustain, interruption, sumber, efek entity/world, unlock.
- [ ] W-03 Keputusan mode terrain default dan material/drop/restore; dokumentasikan keputusan sebelum world mutation.
- [ ] W-04 Transaksi material server + persistence dan migrasi versi data.
- [ ] W-05 Uji konservasi, cancel, restart, chunk unload, dimensi dan dua pemain berebut sumber.
- [ ] W-06 Earth Wall raise/hold dari sumber nyata; source check dan destination collision.
- [ ] W-07 Launch seluruh wall, swept collision, hit gating, impact, reclaim.
- [ ] W-08 Utilitas dasar FIRE/WATER/EARTH/AIR beserta efek PvP eksplisit.
- [ ] W-09 Waduk/wadah air dan lava, tag material, unit volume dan aturan isi ulang.
- [ ] W-10 Profil tribe/elemen/mastery/teknik/profesi dan latihan anti-farming.
- [ ] W-11 Ore extraction: tool/tier, loot, enchantment dan XP; tanpa duplikasi/auto-smelt.
- [ ] W-12 Konstruksi preview/confirm dan terraforming batch dengan permission serta persistence.
- [ ] W-13 Weapon imbue dan matriks interaksi elemen, tanpa damage handler ganda.
- [ ] W-14 Air riding TOGGLE/UNTIL_INTERRUPTED; sustain/fall/knock rules sebelum implementasi.
- [ ] W-15 Uji load budget dan dedicated multiplayer sebelum perluasan volume.

Dependensi: A–D aktif → W-01/02/03 → W-04/05 → W-06/07 → W-08/09 → W-10/11 → W-12.
W-13/14 dijadwalkan setelah fondasi terkait terbukti, bukan diimplementasikan semua sekaligus.

---

## Backlog UI — gulungan bertema tribe (2026-11-08)

Status semua task: BELUM DIIMPLEMENTASIKAN; detail `UI_THEME_SPEC.md`.
- [ ] UI-01 Audit HUD, data dan konflik input aktual; tetapkan mode overlay/pengganti dengan jelas.
- [ ] UI-02 Wireframe menu gulungan, HUD minimal dan tema tribe; buat preview, bukan klaim runtime.
- [ ] UI-03 Komponen scalable/background modular, text, tab, slider, toggle, tooltip dan pencarian.
- [ ] UI-04 Config client berversi, AUTO/manual/minimal, layout preview dan apply/cancel/reset.
- [ ] UI-05 Tema Fire/Water/Earth/Air/Nonbender memakai token yang sama.
- [ ] UI-06 Ikon chi/stamina/health, cooldown dan charge dari snapshot server; tanpa data dummy live.
- [ ] UI-07 Profil mastery/profesi dan widget material sesudah data terkait tersedia.
- [ ] UI-08 Keyboard, kontras, reduced motion/flash, resolusi dan GUI scale.
- [ ] UI-09 Uji overlap HUD/mod lain, input bocor, close saat charge, SP/MP dan izin server.
- [ ] UI-10 Catat provenance aset dan hasil build/runtime; tidak memasang Essential/RPG-HUD sebagai syarat inti.
