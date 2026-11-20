> **STATUS 2026-11-16: Code-ready, Testing-Blocked**
> Phase 0-2 complete [x]. Phase 3 implementation done [~] but blocked on in-game verification.
> Blockers: Element bug retest required, Fire Jab animation not confirmed, Air Blast targeting not verified, T3-4 & T3-10 not started.
> See: docs/BLOCKERS_2026-11-16.md for dependency chain and unblock procedures.
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
- [~] **T2-8** Test sinkronisasi: dua pemain, dedicated server (chi/cooldown independen, kombo tidak tertukar) — User — 2026-11-12
  - Test completed; **BLOCKED** by element switching bug (critical) — RETEST REQUIRED after Fix #1
  - Chi/cooldown mechanics appear OK, multiplayer issues same as singleplayer
  - Retest after server-authoritative element-cycle change before treating multiplayer results as reliable
  - **Status 2026-11-16:** Element debounce deployed, awaiting in-game verification before T2-8 retest

---

## Tahap 3 — Verifikasi In-Game Wave 2 Blocker (2026-11-12)

- [~] **VA-02** Uji Fire Jab di client: stance/guard, transfer berat, frame impact, recovery — User — 2026-11-12
  - ⚠️ **PARTIAL FAIL**: Animasi ada tapi martial arts minimal (mostly vanilla cast)
  - Charge orb visible (5 ticks), glow OK, tapi orb shape piringan 2D bukan sphere 3D
  - 1st person: tangan/item tidak bergerak saat cast
  - 3rd person: player body visible tapi martial arts gerakan belum ada
  - 2026-11-13: Hilangkan pemicu animasi ganda dari hasil cast dan sinkronisasi fase; fase server kini menjadi satu-satunya jalur pemicu, dengan deduplikasi `castSerial`.
  - 2026-11-17: Animasi runtime `fire_jab.animation.json` dan keyframe impacts diperbarui; uji kontrak Gradle kini memvalidasi aset runtime tersebut, bukan hanya clip PoC lama.
  - **Status 2026-11-18:** Build/test otomatis lulus setelah kontrak aset diperbarui; playback, pose normal/slim, armor, first/third person, dan observer tetap **AWAITING IN-GAME TEST**.
  - Action: Uji in-game tampak orang pertama/ketiga dan observer; pastikan impact dan recovery terbaca sebelum mengubah choreography lebih lanjut. See docs/BLOCKERS_2026-11-16.md for test procedure.

- [~] **T3-3** Verifikasi Air Blast: JSON/handler dan hitbox garis pandang terarah ada; verifikasi in-game masih pending — User — 2026-11-12
  - ✅ **PASS mechanics**: chi 12 cost, cooldown 10, damage 3.0, knockback 2.5 working
  - ⚠️ **Targeting issue**: Z-skill (Air Blast) sering miss meskipun target ada
  - **Status 2026-11-16:** Hitbox logic reviewed, padding calculation improved. Build successful. **AWAITING IN-GAME TEST**.
  - Action: Uji in-game dengan 5 mobs di distance 2/4/6/8/12 blocks. See docs/BLOCKERS_2026-11-16.md for test procedure.

## Tahap 3 — Critical Issues Found (2026-11-12)

- [~] **BLOCKER — retest required** Element Switching Bug: Setelah cast skill 2–3x, active element berubah random
  - Element bar di HUD berubah warna tanpa user input
  - Skill yang di-cast jadi elemen lain
  - 2026-11-13: element cycle request kini hanya mengirim intent; server memajukan state per pemain dan mengirim hasilnya kembali. Automated cycle tests (2), seluruh Gradle tests (17), `test build`, dan adversarial network suite (32) lulus; belum membuktikan laporan gameplay teratasi.
  - 2026-11-14 FIX #1: Server-side debounce di SkillNetworking (elementCycleCooldown map, 6-tick throttle sama seperti client). Build ✅. Root cause analysis di DEBUG_ELEMENT_BUG_2026-11-14.md (3 suspect causes tersisa: concurrent PlayerBendingData creation, client/server sync desync).
  - **Status 2026-11-16:** Fix #1 deployed, debug logging added (AvatarAnimations.java). Build successful. **AWAITING IN-GAME TEST**.
  - Action: Uji in-game dengan cast Fire Jab 5+ kali, confirm elemen tetap FIRE. Jika bug masih ada, debug dengan logging untuk identify Cause 2 atau 3. See docs/BLOCKERS_2026-11-16.md for unblock procedure.

- [🟠] **HIGH** Z-Skill Targeting Accuracy: Fire Jab, Water Whip sering miss
  - Hit rate lebih rendah dari expected
  - 2026-11-13: tambah uji segment vs bounding box; Fire Jab menghitung jarak dari tepi hitbox, Air Blast/Water Whip memakai segment terarah dari eye position dan menolak target yang terhalang blok.
  - Automated: 21 unit test + `test build` lulus; Fire Jab suite 18/18 lulus. Akurasi aktual tetap menunggu uji Minecraft.
  - Action: Uji target tepat di depan, pinggir jarak, sedikit di samping, di belakang, dan terhalang blok.

- [🟠] **HIGH** Earth Pillar Block Visual Missing: Erupsi tidak tampil kolom 3D
  - Damage + knockback ✅, tapi VFX hanya partikel, tidak ada struktur kolom
  - **Status QA 2026-11-18:** `.\gradlew.bat build` lulus (21 tes); suite Python M4 (137/137) dan M6 (45/45) lulus, keduanya simulasi. Pemeriksaan awal mengasumsikan skala unit dan menandai model Java 2.0 blok sebagai mismatch; setelah validator memeriksa base scale 1.0 dan skala Y runtime 1.25, hasilnya 7/7. BBModel/Bedrock/OBJ mencapai 2.5 blok di atas tanah. Preview masih berlabel 42 unit/2.63 m dan tidak menunjukkan detail atlas dengan jelas; visual runtime belum diuji.
  - **2026-11-18:** Packet `S2CSkillPosition` mengirim posisi ground authoritative. Pembersihan `SERVER_POSITIONS` kini mencakup posisi yang langsung diterapkan, recovery/idle, cancel, expiry, cast serial baru, dan reset controller. Build lulus setelah perbaikan; alur packet tetap perlu diuji dalam game.
  - **2026-11-18 (fix):** Non-uniform Y scale 1.25x diterapkan via `VfxTransformUtil.createPillarTransform()` saat spawn ItemDisplayEntity, menghasilkan visual 2.5 blok dari model 2.0 blok tanpa mengubah file model (tetap dalam batas parser -16..32).
  - **Status validasi:** Validator statis Earth Pillar lulus 7/7 setelah mencakup rantai model × base scale × Y scale; belum membuktikan render dalam game.
  - Action: Uji reload/playback in-game untuk target dekat, fallback jarak maksimum, dan observer multiplayer.

- [⚠️] **MEDIUM** Orb 3D Shape: Terlihat piringan tipis, bukan bola sphere
  - **2026-11-18:** Reviewed — `ChargeOrbRenderer` dan `FirstPersonOrbRenderer` sudah menggunakan UV-sphere geometry (12x16 dan 8x12 stacks/slices) dengan inner core + outer shell additive blend. Bug piringan kemungkinan dari missing shader yang sudah diperbaiki sebelumnya. Perlu konfirmasi visual in-game.
  - Action: Verifikasi in-game apakah orb sudah terlihat 3D sphere; jika masih flat, tambah brightness gradient per-vertex.

- [⚠️] **MEDIUM** HUD Layout Not Proportional: Menghalangi gameplay view
  - Action: UI-05 theme tuning, scale/position agar overlay, tidak block center

---

## Tahap 3 — Empat Elemen (Gelombang 1)

- [x] **T3-1** Water Whip: LINE hitbox r6, dmg 3.0, pull knockback, DRIPPING_WATER+SPLASH VFX — keybinding C — BUILD ✅ (belum diuji)
- [x] **T3-2** Earth Boulder: projectile traveling 0.8b/t, dmg 5.0, lifetime 20 tik, no block modify — keybinding B — BUILD ✅ (belum diuji)
- [~] **T3-3** Verifikasi Air Palm/Air Blast: implementasi JSON/handler ada; targeting Air Blast diperketat ke garis pandang, uji in-game nilai/akurasi/slot masih pending
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

- [x] **SC-1** Validasi schema skill dan slot saat load: field wajib/enum, tipe/rentang, duplikasi ID, referensi slot, dan pelaporan sumber/path. Unit test Gradle mencakup bundled config dan kasus invalid; in-game behavior tidak terdampak.
- [x] **SC-2** Rekonsiliasi assignment slot secara konservatif: pertahankan skill yang tersedia dan ubah placeholder berulang menjadi slot kosong (`null`) — WATER/EARTH X–B dan AIR B. Default kerja sementara, belum diverifikasi in-game dan bukan mapping desain final yang dikonfirmasi pengguna.
- [x] **SC-3** Untuk vertical slice, tunda `CHANNEL`, `TOGGLE`, dan chi sustain sampai kontrak W1 disetujui; parser menolak nilai yang belum didukung dan konfigurasi runtime tidak lagi menyatakan sustain yang tidak berjalan. Tes mencakup cast type serta biaya sustain.
- [x] **SC-4** PAL versi `1.1.6+mc.1.21.1` sudah dideklarasikan di Gradle dan `player_animation_library >=1.1.6` di metadata Fabric. Pasang PAL pada instance yang menjalankan mod; metadata PAL kompatibel dengan client/server. Build terverifikasi, launch in-game masih perlu diuji manual.

- [ ] **T3-10** Water Jet: channel skill, tekan+tahan untuk semburan air berkelanjutan

- [x] **T3-11** Earth Pillar: raise column dari bawah target, launch ke atas — Claude Code — 2026-11-11
  - `EarthPillarSkill.java`: cari target terdekat di arah pandang (step 1 blok s/d range 8), snap ke permukaan tanah
  - Damage 5.0 + launch vertikal (velocity Y 1.05) untuk entity di tapak radius 1.6
  - VFX partikel blok tanah aktual (BlockStateParticleEffect) + kolom debu naik selama ACTIVE; tanpa world mutation
  - Slot EARTH C; BUILD ✅ unit test lulus (belum diuji in-game)

- [x] **T3-12** Boulder Launch: hold→release, batu makin besar sesuai charge — Claude Code — 2026-11-11
  - `BoulderLaunchSkill.java` memakai framework hold-release generik (Phase.HOLD, C2SHoldStart/Release)
  - Scaling charge: damage 40–100% dari 8.0, hitbox 0.5–1.2, AOE impact 1.0–2.5, speed 1.0–1.4 b/t, lifetime 24 tik
  - Charge orb tanah terdaftar di `OrbVisualConfig` (WINDUP+HOLD), radius orb mengikuti pola fire_blast
  - Slot EARTH X; BUILD ✅ unit test lulus (belum diuji in-game)

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
- [x] **B-5** Fire Jet rocket flight: sustained flight pada ACTIVE phase, flame thruster trail, foot ignition, fall damage immunity (2026-11-20)
- [x] **B-6** Air Scooter traversal: rapid ground/water glide (0.85b/t), hovering height 0.75b, spinning air vortex VFX, fall damage immunity, vegetation clearing, 6-bone zero-snap PAL clip (2026-11-20)
- [x] **B-7** Emergency Avatar State Survival Reflex: auto-trigger saat health <= 2.0 (lethal/fatal), 100 Chi refill, full heal, Resistance IV, cataclysmic 4-element shockwave 8-block, 5-min cooldown (2026-11-20)
- [x] **B-8** World & Entity Elemental Interactions: Fire Jab/Flame Sweep ground ignition, Air Palm/Air Blast vegetation clearing & deflection, Earth Boulder seismic stagger & vegetation clearing, Water Whip/Jet fire dousing & grass clearing (2026-11-20)
- [x] **B-9** Earth Pillar martial arts manipulation: re-cast C atau left-click/punch saat pillar berdiri langsung kick/strike pillar (15 chi refund 50%), sneak+C raise 3-pillar curved Earth Wall (2026-11-20)

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

Status task diperbarui 2026-11-09; detail `UI_THEME_SPEC.md`. HUD baru adalah irisan visual pertama dan belum diverifikasi in-game.
- [x] UI-01 Audit HUD, data dan konflik input aktual; mode tetap overlay dan screen vanilla/inventory tidak diganti.
- [ ] UI-02 Wireframe menu gulungan, HUD minimal dan tema tribe; buat preview, bukan klaim runtime.
- [ ] UI-03 Komponen scalable/background modular, text, tab, slider, toggle, tooltip dan pencarian.
- [ ] UI-04 Config client berversi, AUTO/manual/minimal, layout preview dan apply/cancel/reset.
- [~] UI-05 Mulai tema HUD Fire/Water/Earth/Air memakai token aksen bersama; tema Nonbender/AUTO manual menunggu konfigurasi UI.
- [ ] UI-06 Ikon chi/stamina/health, cooldown dan charge dari snapshot server; tanpa data dummy live.
- [ ] UI-07 Profil mastery/profesi dan widget material sesudah data terkait tersedia.
- [ ] UI-08 Keyboard, kontras, reduced motion/flash, resolusi dan GUI scale.
- [ ] UI-09 Uji overlap HUD/mod lain, input bocor, close saat charge, SP/MP dan izin server.
- [ ] UI-10 Catat provenance aset dan hasil build/runtime; tidak memasang Essential/RPG-HUD sebagai syarat inti.
- [x] UI-11 Selector elemen radial (G default), navigasi mouse/keyboard, sinkronisasi pilihan langsung melalui server dan validasi ID elemen; R tetap fallback cycle, scroll hotbar tidak diubah. `.\gradlew.bat test build` lulus (29 tes; worker memori dibatasi); uji GUI/in-game dua client masih pending.
- [ ] UI-12 Tetapkan model `benderAffinity`/`unlockedElements` dan aturan lintas-elemen untuk Avatar, progression, serta combo; jangan membatasi akses runtime sebelum keputusan gameplay disepakati.

## Jalur visual martial art & Blockbench

- [x] **VA-01** Mulai satu animasi PAL per `castSerial` dan gunakan nama tulang player `body` untuk clip Fire Jab; Gradle `test build` lulus (15 unit test, 2026-11-11).
- [ ] **VA-02** Uji Fire Jab di client: stance/guard, transfer berat, frame impact, recovery, kulit normal/slim, armor, orang pertama/ketiga, dan observer multiplayer.
- [ ] **VA-03** Integrasikan satu VFX hasil Blockbench melalui format/render pipeline Fabric yang terverifikasi; source `.bbmodel` saat ini belum dirender runtime.
- [ ] **VA-04** Tambahkan rig siku/forearm atau adapter yang terbukti sebelum mengklaim artikulasi pukulan setara studi Blockbench.
- [x] **VA-05** Tahap 4 Canonical Weapons 3D Blockbench Suite: SM_Dual_Swords, SM_Earth_Hammer, SM_War_Fan, SM_Water_Spear lengkap (.bbmodel, .geo.json, .json [-16,32], .obj, .mtl, 64x64 texture atlas, preview isometrik & turntable GIF 360°) — Antigravity (art-producer) — 2026-11-18 — package lengkap; 52/52 pemeriksaan struktural lulus (docs/WEAPONS_SPEC.md). Ini bukan penerimaan visual atau bukti integrasi runtime.
- [x] **VA-06** QA visual senjata: render ulang preview dengan sampling atlas UV tekstur asli dan dynamic fit-to-bounds (tanpa terpotong di tepi atas/bawah); 52/52 pemeriksaan struktural & visual lulus (2026-11-18).
- [x] **VA-07** Integrasikan item senjata ke resource/runtime mod: AvatarItems.java mendaftarkan 4 senjata (DUAL_SWORDS, EARTH_HAMMER, WAR_FAN, WATER_SPEAR), item models & textures dipaketkan ke assets/avatar_elements/, CMD overrides 2001–2004 pada iron_sword.json, teks bahasa en_us/id_id lengkap; 28/28 checks lulus (tests/validate_weapon_runtime_integration.py, 2026-11-18).
