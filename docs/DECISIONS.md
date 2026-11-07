# DECISIONS.md — Keputusan Teknis

Format: `[YYYY-MM-DD] DXXX — Judul — Keputusan — Alasan`

---

## D001 — Platform: Fabric bukan Forge/NeoForge
**Tanggal:** 2026-11-07  
**Keputusan:** Mod dikembangkan di Fabric 1.21.1.  
**Alasan:** Epic Fight mod tersedia untuk Fabric 1.21.1. Fabric lebih ringan dan update lebih cepat. File referensi NeoForge (`epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`) di `reference/` hanya untuk studi API animasi.

---

## D002 — Server authority untuk semua validasi gameplay
**Tanggal:** 2026-11-07  
**Keputusan:** Server memvalidasi chi, cooldown, damage, hitbox, dan langkah kombo. Client hanya mengirim input dan menerima hasil.  
**Alasan:** Mencegah cheating di multiplayer. Client yang cepat atau dimodifikasi tidak bisa bypass cooldown atau spam chi.

---

## D003 — Chi dan stamina sebagai dua bar terpisah
**Tanggal:** 2026-11-07  
**Keputusan:** Chi untuk bending, stamina untuk gerakan fisik dan senjata.  
**Alasan:** Memisahkan resource mencegah konflik antara bending dan gerakan. Harus diuji agar kontrol tidak terasa terlalu rumit; bisa disederhanakan jika terlalu kompleks.

---

## D004 — Dua sistem skill datapack disatukan lewat bridge
**Tanggal:** 2026-11-07  
**Keputusan:** `avatar-armor-datapack/skill/cast_*` sekarang hanya menjadi bridge yang set `avatar_used_c=1`, mendelegasikan ke router `avatar-skill-datapack`.  
**Alasan:** Dua sistem yang berjalan paralel tidak bisa dikoordinasikan. Satu router sebagai authority mencegah duplikasi logika dan state yang tidak konsisten.

---

## D005 — Avatar State memerlukan semua 4 mastery + 50 chi + cooldown = 0
**Tanggal:** 2026-11-07  
**Keputusan:** Avatar State tidak bisa diaktifkan sembarangan. Syarat: `av_mast_all >= 1`, `avatar_chi >= 50`, `avatar_cd = 0`. Cooldown 200 ticks setelah habis.  
**Alasan:** Tanpa syarat, Avatar State bisa diexploit di multiplayer (spam Resistance 3 + Speed 3). Efek diturunkan dari level 2→1 untuk keseimbangan.

---

## D006 — Lunge menggunakan block check sebelum tp
**Tanggal:** 2026-11-07  
**Keputusan:** `tp @s ^ ^0.1 ^0.5` hanya dieksekusi jika blok destinasi adalah air. Fallback jarak lebih pendek untuk Fire Jet.  
**Alasan:** `tp` di datapack tidak memeriksa collision. Tanpa check, pemain bisa menembus dinding atau jatuh ke void di tepi jurang. Keterbatasan: check satu blok tidak mencakup semua geometri; ini perlu diganti velocity API saat migrasi ke Fabric mod.

---

## D007 — Chi failsafe dihapus
**Tanggal:** 2026-11-07  
**Keputusan:** Baris `if score @s avatar_chi matches ..0 run scoreboard players set @s avatar_chi 100` dihapus dari `tick.mcfunction` dan `cast/router.mcfunction`.  
**Alasan:** Failsafe ini membuat seluruh sistem resource tidak bermakna — skill paling mahal pun tidak ada konsekuensinya karena chi selalu refill. Diganti dengan clamp floor 0 dan pesan feedback ke pemain.

---

## D008 — Sumber kebenaran nilai gameplay
**Tanggal:** 2026-11-07  
**Keputusan:** Semua nilai skill, armor, weapon didefinisikan di `docs/CONTENT_SPEC.md` (selama masih datapack) dan akan dimigrasikan ke `data/avatar/skill_definitions/*.json` saat Tahap 1 Fabric mod dimulai.  
**Alasan:** Mencegah nilai berbeda antara kode, HUD, tooltip, dan dokumentasi.
