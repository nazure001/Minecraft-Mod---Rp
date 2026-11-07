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

---

## D009 — Mod ID dan package Java
**Tanggal:** 2026-11-07  
**Keputusan:** Mod ID = `avatar_elements`, Maven group = `com.avatarmod`, package root = `com.avatarmod.elements`. Archives base name = `avatar-elements`.  
**Alasan:** Placeholder yang dipakai saat scaffold T1-1. Jika nama mod berubah, update `gradle.properties` (mod_id, maven_group, archives_base_name) dan rename package — catat di sini.

---

## D010 — JDK: Java 17 dipertahankan sebagai JAVA_HOME sistem, JDK 21 Temurin side-by-side
**Tanggal:** 2026-11-07  
**Keputusan:** JDK 21 (Eclipse Temurin 21.0.5+11) diinstal di `C:\Users\USER\.jdks\jdk-21.0.5+11`. JAVA_HOME sistem tetap JDK 17. Gradle Java Toolchain di `build.gradle` mengarah ke Java 21; Gradle mendeteksi Temurin otomatis dari `~/.jdks`.  
**Alasan:** Instruksi eksplisit: jangan ubah JAVA_HOME/PATH global. Toolchain Gradle menangani pemilihan JDK per-project tanpa mengubah sistem.

---

## D012 — JDK 25 side-by-side untuk JVM Gradle (bukan compile target mod)
**Tanggal:** 2026-11-07  
**Keputusan:** JDK 25 (Temurin 25.0.5+8) di-install di `C:\Users\USER\.jdks\jdk-25.0.5+8` dan diset via `org.gradle.java.home` di `gradle.properties`. Mod compile target tetap Java 21 (via `options.release = 21` dan toolchain JDK 21).

**Fakta terverifikasi (dari error aktual):**
- Loom ≥ 1.18.x: `Dependency requires at least JVM runtime version 25` — butuh JVM 25 untuk MENJALANKAN Gradle/Loom
- Loom 1.7.4 + Gradle 9.8.2: `'Problems.forNamespace()' method changed` — Gradle API berubah di 9.x, loom lama tidak kompatibel
- Loom 1.17.21 + Gradle 9.8.2: `Could not find method mappings()` — Groovy DSL timing issue (konfigurasi belum register)
- Loom 1.19.3: `requires at least Gradle 9.8.0` (dari error saat coba Gradle 9.3.1)

**Pembedaan JVM (instruksi ChatGPT poin 4):**
- JVM Gradle: `org.gradle.java.home` → JDK 25 (loom butuh ini untuk jalan)
- Toolchain kompilasi mod: `java.toolchain.languageVersion = 21` → JDK 21 (dari `~/.jdks/jdk-21.0.5+11`)
- Runtime Minecraft 1.21.1: Java 21 (tidak berubah)

**Alasan pilihan:** Jangan ubah JAVA_HOME global (constraint eksplisit). JDK 25 di-install side-by-side.

---

## D011 — Versi dependency Fabric scaffold (diperbarui dari diagnostik aktual)
**Tanggal:** 2026-11-07  
**Sumber:** `github.com/FabricMC/fabric-example-mod` branch `1.21.1` (awal), dikoreksi dari error aktual  
**Keputusan:**
- Minecraft: `1.21.1`
- Fabric Loader: `0.20.1`
- Fabric Loom: `1.19.3` (pinned; loom 1.19.3 requires Gradle ≥ 9.8.0 — terverifikasi)
- Fabric API: `0.116.17+1.21.1`
- Gradle: `9.8.2` (minimum yang dibutuhkan loom 1.19.3)
- Mappings: `Yarn 1.21.1+build.3` via `loom.layered { it.mappings("net.fabricmc:yarn:...") }`
- Java toolchain (mod): `21`; JVM Gradle: `25`
- **Plugin ID**: `fabric-loom` (bukan `net.fabricmc.fabric-loom`)

**Root cause utama T1-1 (terverifikasi dari decompile LoomGradleExtensionImpl):**
`net.fabricmc.fabric-loom` → `LoomNoRemapGradlePlugin` (environment non-obfuscated, tidak bisa pakai mappings).
`fabric-loom` → `LoomGradlePlugin` (standard remapping, benar untuk Fabric mod).
Semua error "non-obfuscated environment" dan "mappings() not found" berasal dari plugin ID yang salah.

**Alasan:** Versi awal dari template resmi Fabric. Loom, Gradle, JVM version, dan plugin ID dikoreksi dari error aktual selama diagnostik T1-1. BUILD SUCCESSFUL terverifikasi 2026-11-07.
