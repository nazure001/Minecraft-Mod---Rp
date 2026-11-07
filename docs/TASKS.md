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

- [ ] **T1-1** Scaffold mod Fabric 1.21.1 (fabric.mod.json, entry point, gradle) — `mod/`
- [ ] **T1-2** Implementasi keybind (skill slots, dodge, element radial, combat mode toggle)
- [ ] **T1-3** Implementasi networking (C2S_SkillInput, S2C_SkillResult, S2C_HudUpdate)
- [ ] **T1-4** Implementasi `PlayerBendingData` (chi, cooldown, mastery, skills) via AttachmentType
- [ ] **T1-5** Implementasi `SkillTimeline` (windup → active → recovery)
- [ ] **T1-6** Implementasi `SkillValidator` server-side
- [ ] **T1-7** Implementasi `ChiManager` (regen, cost, clamp)
- [ ] **T1-8** HUD dasar (chi bar, cooldown, skill aktif)
- [ ] **T1-9** Konfigurasi bersama (JSON loader untuk skill_definitions)
- [ ] **T1-10** Verifikasi berjalan di dedicated server tanpa crash

---

## Tahap 2 — Prototipe Vertikal

- [ ] **T2-1** Fire Jab (tangan kosong): animasi, hitbox, VFX, suara pada 1 timeline
- [ ] **T2-2** Flame Sweep: animasi arc, hitbox arc, VFX, suara
- [ ] **T2-3** Fire Jet: animasi, movement (cek collision), VFX, suara
- [ ] **T2-4** Fire Guard: animasi, block logic, VFX
- [ ] **T2-5** Kombo fire 3 serangan (Jab → Sweep → Jab, dengan combo window)
- [ ] **T2-6** Air Staff basic attack (Tongkat udara): 3 serangan kombo
- [ ] **T2-7** Air Vortex skill pada tongkat udara
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
