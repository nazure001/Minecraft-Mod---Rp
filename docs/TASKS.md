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
- [x] **T2-2** Flame Sweep: ARC 180°, 3 hit/active, dmg 6.0, +30% combo bonus — BUILD ✅ (belum diuji terpisah)
- [x] **T2-3** Fire Jet: velocity dash 2.2f, flame trail VFX — BUILD ✅ (belum diuji)
- [x] **T2-4** Fire Guard: blok entity damage saat ACTIVE, shield shimmer VFX — BUILD ✅ (belum diuji)
- [x] **T2-5** Kombo Jab→Sweep→Jab: +50% dmg step3, range x1.3, lava particles — BUILD ✅
- [x] **T2-6** Air Staff Attack: 3-hit kombo (H), CLOUD particles — TERVERIFIKASI in-game ✅
- [x] **T2-7** Air Vortex: pull r6, 40 tik, spiral particles (V) — BUILD ✅ (belum diuji)
- [ ] **T2-8** Test sinkronisasi: dua pemain, dedicated server

---

## Tahap 3–8

Lihat `docs/PROJECT_PLAN.md` untuk daftar lengkap per tahap. Tugas akan dipecah saat tahap dimulai.

---

## Backlog (dari audit)

- [ ] **B-1** CIT tier armor: tambah layer definition untuk tier `basic` s/d `veteran` di resourcepack
- [ ] **B-2** Ganti XP vanilla sebagai progression → mastery tracking kustom
- [ ] **B-3** Pack format `pack.mcmeta` — verifikasi format 48 untuk 1.21.1
- [ ] **B-4** `avatar_skill_timer` di armor-datapack sudah tidak dipakai — hapus setelah konfirmasi

---

## Selesai (arsip)

| ID | Deskripsi | Tanggal | Hasil |
|---|---|---|---|
| T0-1 | Audit aset | 2026-11-07 | 4 paket ditemukan, 4 masalah kritis teridentifikasi |
| T0-2 | Identifikasi konflik | 2026-11-07 | Dua sistem skill paralel, chi failsafe, Avatar State tanpa validasi |
| T0-3 | Perbaiki datapack | 2026-11-07 | 5 fix diterapkan, belum diuji di Minecraft |
| T0-4 | Setup workspace | 2026-11-07 | Struktur folder, docs, Git init |
