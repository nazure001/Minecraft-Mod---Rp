# ASSET_INVENTORY.md — Inventaris Aset Proyek Avatar: Elements

Dokumen ini mencatat seluruh aset lokal proyek yang tersedia di direktori `D:\repo\Minecraft Mod & Rp`, memisahkan aset asli milik proyek dengan aset referensi pihak ketiga, serta memetakan format, fungsi, status penggunaan, ketergantungan, dan hasil pemeriksaannya.

---

## 1. Zirah (Armor)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Icon Item Zirah 4 Elemen (112 buah) | `avatar-armor-resourcepack/assets/avatar/textures/item/*.png` | PNG (16×16) | Ikon tampilan zirah di inventory & GUI untuk 4 elemen (Fire, Water, Earth, Air) × 7 tier × 4 slot | Proyek sendiri (dihasilkan script Python prosedural) | Aktif | CustomModelData (CMD) formula `NTPP` | Lengkap 112 file tekstur unik, valid PNG RGBA, palet warna bergradasi sesuai tier. |
| Model Item Helm 3D (28 buah) | `avatar-armor-resourcepack/assets/avatar/models/item/headwear/*.json` | JSON | Model geometri 3D kubus untuk hiasan kepala/mahkota saat helm dipakai | Proyek sendiri | Aktif | Minecraft 1.21.1 item model loader | Sintaks valid, kubus terdefinisi rapi, tekstur mengarah ke `textures/item/headwear/`. |
| Tekstur Helm 3D (28 buah) | `avatar-armor-resourcepack/assets/avatar/textures/item/headwear/*.png` | PNG (16×16 / 32×32) | Tekstur permukaan model 3D hiasan kepala helm | Proyek sendiri | Aktif | Model headwear JSON | File valid PNG, cocok dengan mapping UV model 3D headwear. |
| Tekstur Zirah Badan (Entity Equipment Layer 1 & 2) | `avatar-armor-resourcepack/assets/avatar/textures/entity/equipment/humanoid/*.png` & `humanoid_leggings/*.png` | PNG (64×32 / 64×64) | Tampilan zirah saat terpasang pada badan dan kaki karakter pemain | Proyek sendiri | Aktif sebagian | Vanilla Trim Engine & CIT Resewn | 8 file tekstur utama per elemen ada, tetapi tier 1–5 masih berbagi tekstur seragam; variasi visual dominan dari trim material. |
| Definisi CIT Armor Resewn (16 file) | `avatar-armor-resourcepack/assets/minecraft/citresewn/cit/armor/*.properties` | `.properties` | Pengait CIT agar zirah custom terpasang visualnya pada badan karakter | Proyek sendiri | Aktif | Mod `citresewn` (Fabric 1.21.1) | 16 konfigurasi layer 1 & 2 mengaitkan item custom ke tekstur PNG. Bekerja untuk tier tertinggi/nama khusus, belum memetakan tiap tier secara mandiri (Backlog B-1). |
| Definisi CIT OptiFine (16 file) | `avatar-armor-resourcepack/assets/minecraft/optifine/cit/armor/*.properties` | `.properties` | Kompatibilitas mundur bagi pengguna OptiFine CIT | Proyek sendiri | Aktif (Opsional) | OptiFine / EMF / ETF | Duplikat dari konfigurasi CIT Resewn untuk kompatibilitas multi-client. |
| Override Model Vanilla Item (21 file) | `avatar-armor-resourcepack/assets/minecraft/models/item/*.json` | JSON | Mengarahkan item zirah vanilla (`leather_helmet`, `diamond_chestplate`, dll.) ke model custom berdasarkan CMD | Proyek sendiri | Aktif | Komponen native `minecraft:custom_model_data` 1.21.1 | Sintaks valid, pemetaan predikat CMD `1101` s/d `4704` tepat sasaran tanpa merusak zirah vanilla. |

---

## 2. Senjata & Item (Weapons & Items)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Ikon Gulungan Elemen (Scrolls, 5 buah) | `avatar-skill-resourcepack/assets/avatar_skills/textures/item/scroll_*.png` | PNG (16×16) | Ikon item gulungan jurus (`fire`, `water`, `earth`, `air`, `mastery`) | Proyek sendiri | Aktif (Legacy Datapack) | Model item CMD | Valid PNG 16×16, representasi visual gulungan kulit berikat pita elemen. |
| Ikon Relik & Fokus Sub-Bending (8 buah) | `avatar-skill-resourcepack/assets/avatar_skills/textures/item/focus_*.png`, `avatar_relic.png`, `chi_orb.png` | PNG (16×16) | Ikon item katalis sub-bending (Lava, Metal, Blood, Lightning, Combustion, Healing, Flight) dan Orb Chi | Proyek sendiri | Aktif (Legacy Datapack) | Model item CMD | Valid PNG 16×16 pixel art, warna distingtif per sub-elemen. |
| Model Override Katalis Tongkat (2 file) | `avatar-skill-resourcepack/assets/minecraft/models/item/carrot_on_a_stick.json` & `warped_fungus_on_a_stick.json` | JSON | Mengalihkan model item tongkat vanilla ke tekstur scroll dan relik | Proyek sendiri | Aktif (Legacy Datapack) | Vanilla Item Predicate CMD | Valid JSON, memetakan 14 item skill ke slot pemicu klik kanan. |
| Model Item Skill Relik (15 file) | `avatar-skill-resourcepack/assets/avatar_skills/models/item/*.json` | JSON | Model datar (generated item) untuk masing-masing gulungan dan relik | Proyek sendiri | Aktif | Vanilla Model Loader | Sintaks valid `item/generated` standar Minecraft. |
| **Tongkat Udara (Air Staff)** | *Belum ada file lokal* | — | Senjata utama Pengendali Udara (tusuk, putar, sapu, terbang) | — | **Belum tersedia** | Dibutuhkan untuk Prototipe Tahap 2 | **GAP:** Tidak ditemukan model 3D maupun tekstur 2D untuk tongkat udara di paket aset proyek saat ini. |
| **Senjata Melee Lainnya** (Pedang Tunggal/Ganda, Tombak, Palu, Kipas) | *Belum ada file lokal* | — | Senjata pertarungan elemen lanjutan | — | **Belum tersedia** | Rencana Tahap 4 | Belum ada model/tekstur. |
| Model/Tekstur Senjata Bedrock | Di dalam `reference/Avatar-Addon-1.3.2-Beta.mcaddon` | `.geo.json`, PNG | Referensi visual senjata di versi Bedrock | Pihak ketiga (Bedrock Addon) | Referensi studi saja | Bedrock Engine | Format geometri Bedrock, tidak bisa langsung dibaca Fabric Java tanpa konversi manual. Asal/lisensi: **Belum diketahui**. |

---

## 3. Partikel & Efek Visual (VFX)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Partikel Aura Zirah Sovereign & Tier | `avatar-armor-datapack/data/avatar/function/particles/*.mcfunction` | mcfunction | Menampilkan partikel aura hidup di tubuh pemain saat memakai set lengkap | Proyek sendiri | Aktif | Vanilla Particle Engine (`flame`, `dust`, `cloud`, dll.) | Berjalan melalui logika server tick. Beban partikel rendah (2–5 partikel/detik per pemain), aman untuk TPS. |
| Partikel Bending Prosedural | `avatar-skill-datapack/data/avatar_skills/function/particles/*.mcfunction` & `cast/*.mcfunction` | mcfunction | Membentuk geometri serangan: Water Whip spiral, Dragon Flame Slash arc, Concentric Air Rings, Tectonic Wave | Proyek sendiri | Aktif (Legacy Datapack) | Vanilla Particle Engine + Notasi Caret (`^ ^ ^`) | Dibangun murni dengan kalkulasi koordinat polar/trigonometri vanilla. Belum ada tekstur partikel kustom baru. |
| Tekstur Partikel Trail Sabetan (*Swing Trail*) | Di dalam `reference/WOLegendaryMonsters-1.1.0-forge-1.20.1.jar` (`assets/wolm/textures/particle/swing_trail/vanillafied.png`) | PNG | Referensi lembaran busur visual sabetan senjata | Pihak ketiga (WOLM Mod) | Referensi studi visual saja | Forge 1.20.1 | Tekstur trail horizontal transparan. Asal/lisensi: **Belum diketahui**. Jangan didistribusikan langsung. |
| Definisi Partikel Bedrock | Di dalam `reference/Avatar-Addon-1.3.2-Beta.mcaddon` (`*.particle.json`) | JSON | Efek partikel elemen versi Bedrock | Pihak ketiga (Bedrock Addon) | Referensi visual saja | Bedrock Particle Emitter | Menggunakan kurva matematika MOLANG Bedrock, tidak kompatibel langsung dengan sistem partikel Minecraft Java. Asal/lisensi: **Belum diketahui**. |
| Tekstur Partikel Kustom Java (Mod) | *Belum ada file lokal di mod/ atau RP* | — | Sprite efek api, cipratan air, debu tanah, dan distorsi angin khusus mod | — | **Belum tersedia** | Dibutuhkan untuk presentasi visual tinggi (Tahap 6) | Proyek saat ini 100% menggunakan partikel bawaan vanilla Minecraft (`minecraft:flame`, `minecraft:dust`, dsb.). |

---

## 4. Animasi (Animations)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Gerakan Serangan Datapack | `avatar-skill-datapack/data/avatar_skills/function/cast/*.mcfunction` | mcfunction | Animasi gerak berbasis momentum dorongan teleport (`tp @s ^ ^0.1 ^0.5`) | Proyek sendiri | Aktif (Legacy Datapack) | Command vanilla | Bukan animasi skeletal karakter; hanya pergerakan translasi posisi pemain bersamaan dengan ayunan tangan vanilla (*hand swing*). Kaku untuk pertarungan dinamis. |
| API & Logika Animasi Pertarungan | Di dalam `reference/epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` (`yesman/epicfight/api/animation/*`) | Java Class & JSON | Kerangka kerja pembacaan animasi pergerakan tulang, interpolasi, dan collider hitbox | Pihak ketiga (Epic Fight Project) | Referensi arsitektur API | NeoForge 1.21.1 | Digunakan oleh Claude/arsitek untuk memetakan alur `SkillTimeline` (windup, active, recovery). **Peringatan:** File ini berformat NeoForge; tidak bisa dijalankan langsung di lingkungan runtime Fabric. Lisensi: All Rights Reserved / Mod API. |
| Animasi Karakter Bedrock (30+ file) | Di dalam `reference/Avatar-Addon-1.3.2-Beta.mcaddon` (`RP/animations/*.json`) | JSON (Bedrock Animation) | Pose pukulan bela diri, tendangan elemen, dan gerakan jurus versi Bedrock | Pihak ketiga (Bedrock Addon) | Referensi keyframe gerak saja | Bedrock Animation Controller | Berisi koordinat rotasi tulang rig Bedrock (`root`, `waist`, `rightArm`, dll.). **Tidak kompatibel langsung dengan Fabric Java/Epic Fight** tanpa proses re-targeting rig atau konversi manual. Asal/lisensi: **Belum diketahui**. |
| File Animasi Kustom Milik Proyek Sendiri | *Belum ada di repositori* | — | Animasi jurus Fire Jab, Flame Sweep, Tusukan/Putaran Tongkat | — | **Belum tersedia** | Dibutuhkan untuk Prototipe Tahap 2 | **GAP:** Belum ada file animasi format Java/Fabric yang siap pakai. |

---

## 5. Efek Suara (Sound Effects / SFX)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Suara Jurus Bawaan Vanilla | Dipanggil via `/playsound` di fungsi datapack | Vanilla Sound Event | Efek suara letupan api, ledakan, hembusan angin, dan hantaman batu | Mojang (Vanilla Minecraft) | Aktif | Minecraft Engine | Menggunakan sound vanilla (`entity.blaze.shoot`, `item.firecharge.use`, `entity.breeze.wind_burst`, `block.stone.break`, dll.). Suara berfungsi tetapi terasa generik, belum memiliki kekhasan magis audio Avatar. |
| Audio Bending Autentik (37 file) | Di dalam `reference/Avatar-Addon-1.3.2-Beta.mcaddon` (`*.ogg` & `sounds.json`) | OGG Vorbis | Suara sabetan api, pusaran angin, deburan air, dan benturan tanah khas serial Avatar | Pihak ketiga (Bedrock Addon) | Referensi pendengaran saja | Bedrock Addon / OGG player | Kualitas audio jernih dan autentik sesuai anime/serial. **Status Lisensi: Belum diketahui.** Sesuai batas tugas, file ini **TIDAK diekstrak** ke folder mod/resourcepack aktif sebelum status hak ciptanya terverifikasi. |
| Audio Senjata & Dampak Serangan (49 file) | Di dalam `reference/epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` (`assets/epicfight/sounds/*.ogg`) | OGG Vorbis | Suara desingan bilah pedang, ayunan tumpul, dan benturan zirah | Pihak ketiga (Epic Fight) | Referensi saja | Epic Fight Mod | Suara pertarungan berkualitas tinggi. Lisensi milik pembuat Epic Fight; tidak boleh di-redistribusi secara langsung tanpa izin. |
| File SFX Kustom Milik Proyek Sendiri | *Belum ada di resourcepack proyek* | — | Bank suara resmi proyek di `assets/avatar/sounds/` | — | **Belum tersedia** | Dibutuhkan untuk Tahap 2 & 6 | Resourcepack proyek saat ini belum memiliki folder `sounds/` maupun file `sounds.json`. |

---

## 6. Musik Latar & Suasana (Backsound / BGM)

| Nama Aset | Path Relatif | Format | Fungsi | Asal | Status Penggunaan | Ketergantungan | Hasil Pemeriksaan |
|---|---|---|---|---|---|---|---|
| Musik Latar / BGM Khusus Avatar | *Tidak ada file di seluruh repositori* | — | Musik atmosferik 4 negara, musik pertarungan, tema Avatar State | — | **Belum tersedia** | Direncanakan Tahap 6 | Seluruh repositori (baik proyek sendiri maupun arsip referensi) tidak memiliki file trek musik latar (BGM). Saat ini sepenuhnya bergantung pada musik latar vanilla Minecraft. |

---

## 7. Ringkasan Status Kesiapan Inventaris

```
[████████████████████] 100%  Zirah Item 2D (112 Icon Selesai & Lengkap)
[████████████████████] 100%  Helm 3D (28 Model & Tekstur Terpasang)
[██████████████░░░░░░]  70%  Zirah Layer Badan (8 Tekstur Dasar Aktif; Backlog B-1 Tiering)
[███████████████░░░░░]  75%  Item Skill/Katalis (14 Tekstur & Model Scroll/Fokus Lengkap)
[░░░░░░░░░░░░░░░░░░░░]   0%  Senjata Prototipe (Tongkat Udara & Model Tangan Kosong Belum Ada)
[████████████░░░░░░░░]  60%  Partikel/VFX (Geometri Vanilla Selesai; Belum Ada Sprite Custom)
[░░░░░░░░░░░░░░░░░░░░]   0%  Animasi Fabric Java (Hanya Ada Referensi NeoForge & Bedrock)
[████████░░░░░░░░░░░░]  40%  Efek Suara (Memakai Suara Vanilla; Belum Ada SFX Kustom Proyek)
[░░░░░░░░░░░░░░░░░░░░]   0%  Backsound / Musik Latar (Belum Tersedia)
```
