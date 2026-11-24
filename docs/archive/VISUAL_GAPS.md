# VISUAL_GAPS.md — Analisis Kesenjangan Visual & Aset Prototipe

Dokumen ini memetakan perbandingan antara **aset yang tersedia di proyek saat ini** dengan **kebutuhan visual konkret untuk Prototipe Vertikal (Tahap 2)** sebagaimana ditetapkan dalam `docs/CONTENT_SPEC.md` dan `docs/PROJECT_PLAN.md`.

---

## 1. Lingkup Prototipe Vertikal (Tahap 2)

Sesuai dokumen rencana proyek, prototipe difokuskan pada dua alur pertarungan (*moveset*):
1. **Fire Bending Tangan Kosong**:
   * Kombo 3 Serangan Dasar: **Fire Jab** $\rightarrow$ **Flame Sweep** (busur 180°) $\rightarrow$ **Fire Jab / Finisher**.
   * 1 Skill Khas: **Fire Jet** (mobilitas lunge ke depan) atau **Fire Guard** (perisai api).
2. **Tongkat Udara (Air Staff)**:
   * Kombo 3 Serangan Dasar: **Tusuk (Thrust)** $\rightarrow$ **Putar (Spin)** $\rightarrow$ **Sapu (Sweep)**.
   * 1 Skill Khas: **Air Vortex** (pusaran angin sentrifugal).

Prinsip mutlak yang ditetapkan dalam arsitektur: **Satu Serangan = Satu Timeline** (*windup* $\rightarrow$ *active* $\rightarrow$ *recovery*), di mana animasi, hitbox, VFX, dan suara harus terpicu pada frame yang sama.

---

## 2. Analisis Moveset 1: Fire Bending Tangan Kosong

### A. Aset yang Sudah Tersedia
* **Logika Server & Definisi Gameplay**:
  * Nilai `windup_ticks`, `active_ticks`, `recovery_ticks`, `damage`, dan `range` sudah terdefinisi secara resmi di `docs/CONTENT_SPEC.md`.
  * Parameter hitbox: `SPHERE` (radius 2.5 blok) untuk Jab, dan `ARC` (radius 5.0 blok, 180°) untuk Flame Sweep.
* **Efek Partikel / VFX Dasar**:
  * Prosedur partikel vanilla di `avatar-skill-datapack/data/avatar_skills/function/cast/fire_blast.mcfunction`: menggunakan `minecraft:flame`, `minecraft:small_flame`, `minecraft:lava`, dan `minecraft:smoke` dengan notasi Caret (`^ ^ ^`).
* **Efek Suara (Vanilla)**:
  * Suara vanilla Mojang `minecraft:item.firecharge.use`, `minecraft:entity.blaze.shoot`, dan `minecraft:entity.generic.explode`.
* **Ikon GUI/Katalis**:
  * Ikon 2D `scroll_fire.png` (16×16) dan `carrot_on_a_stick.json` predikat CMD.

### B. Kesenjangan Aset (Aset yang Kurang / GAP)
1. **Animasi Pemain (Kritis)**:
   * **Belum ada file animasi**: Tidak ada klip animasi pukulan lurus cepat (*Jab* Shaolin), tendangan/ayunan menyapu memutar (*Sweep*), maupun pose dorongan kaki meluncur (*Jet*).
   * Kondisi saat ini hanya mengandalkan ayunan lengan standar vanilla Minecraft (*hand swing*), yang terlihat kaku dan tidak memancarkan rasa seni bela diri Avatar.
2. **VFX Busur Tebasan Api (*Flame Slash Arc*)**:
   * Partikel vanilla saat ini hanya berupa semprotan titik api acak.
   * Belum ada tekstur lembaran busur api (*mesh ribbon / slash trail*) yang membentuk lengkungan 180° yang solid dan terbaca jelas oleh pemain saat melakukan *Flame Sweep*.
3. **Efek Suara Autentik (*Bending SFX*)**:
   * Suara tembakan Blaze vanilla terdengar mekanis dan tidak memiliki desiran udara terbakar (*woosh combustion*) khas serial animasi.
   * Belum ada file `.ogg` terdaftar di proyek untuk suara pukulan api, benturan impact, dan deru jet api.
4. **Representasi Visual Tangan Kosong**:
   * Saat berada dalam mode tangan kosong (*unarmed bending*), hotbar pemain saat ini masih mengharuskan memegang item tongkat/wortel wortel pancingan atau gulungan kertas, bukan postur tangan kosong bertarung.

### C. Batasan Teknis
* **Keterbatasan Datapack**: Datapack tidak dapat memodifikasi animasi rig tubuh pemain (tulang tangan, kaki, kepala) secara selektif.
* **Kebutuhan Fabric Mod**: Memerlukan integrasi sistem animasi client-side (seperti Fabric Epic Fight API) untuk memutar klip animasi `windup_ticks` $\rightarrow$ `active_ticks` $\rightarrow$ `recovery_ticks` yang sinkron dengan client lain via paket `S2C_AnimationTrigger`.

---

## 3. Analisis Moveset 2: Tongkat Udara (Air Staff)

### A. Aset yang Sudah Tersedia
* **Logika Server & Definisi Gameplay**:
  * Nilai skill udara dasar (`air_palm`, `air_blast`) terdaftar di `docs/CONTENT_SPEC.md`. Rencana kombo tusuk-putar-sapu telah dicatat di `docs/PROJECT_PLAN.md`.
* **Efek Partikel / VFX Dasar**:
  * Prosedur partikel hembusan angin di `avatar-skill-datapack/data/avatar_skills/function/cast/air_blast.mcfunction`: menggunakan `minecraft:cloud`, `minecraft:poof`, `minecraft:sweep_attack`, dan partikel Breeze (`minecraft:breeze_wind`, `minecraft:gust_emitter_small`).
* **Efek Suara (Vanilla)**:
  * Suara vanilla `minecraft:entity.breeze.wind_burst` dan `minecraft:entity.breeze.slide`.
* **Ikon GUI/Katalis**:
  * Ikon 2D `scroll_air.png` (16×16).

### B. Kesenjangan Aset (Aset yang Kurang / GAP)
1. **Model & Tekstur Tongkat Udara (Sangat Kritis / Hilang Total)**:
   * **Tidak ditemukan model 3D item**: Proyek sama sekali belum memiliki model geometri tongkat (`air_staff.json`) maupun tekstur kayu/sayap glider (`air_staff.png`).
   * Tanpa model ini, prototipe senjata tongkat udara tidak dapat ditampilkan secara visual di tangan karakter.
2. **Animasi Senjata Dua Tangan (*Two-Handed Staff Animation*)**:
   * Belum ada data animasi untuk gerakan menusuk lurus (*Thrust*), memutar tongkat melingkar di depan dada (*Spinning Deflection*), dan menyabetkan tongkat horizontal (*Low Sweep*).
   * Animasi memegang tongkat dengan dua tangan saat berlari dan diam (*idle/walk pose*) belum tersedia di repositori.
3. **VFX Pusaran Udara (*Air Vortex*)**:
   * Belum ada model/tekstur corong tornado atau lingkaran angin memutar bertekanan tinggi untuk skill khas Air Vortex (saat ini hanya semprotan partikel awan datar).
4. **Efek Suara Khusus Tongkat & Pusaran**:
   * Belum ada suara sabetan kayu berdesing di udara dan raungan pusaran angin sentrifugal.

### C. Batasan Teknis
* **Display Transformasi Model**: Model tongkat panjang membutuhkan pengaturan `display` JSON khusus (posisi `thirdperson_righthand`, `firstperson_righthand`, `gui`, dan `ground`) agar tongkat dipegang di tengah dan memiliki panjang yang proporsional, tidak terlihat seperti pedang pendek biasa.
* **Integrasi Rig Dua Tangan**: Gerakan memutar tongkat membutuhkan kontrol kedua lengan pemain (tangan kiri dan kanan menyatu memegang tongkat), yang hanya bisa dicapai melalui animator khusus di Fabric mod.

---

## 4. Matriks Komparasi Kesiapan Visual Prototipe

| Komponen Prototipe | Kebutuhan Spesifikasi | Aset Tersedia Saat Ini | Status Kesiapan | Kekurangan yang Harus Dibuat (GAP) |
|---|---|---|---|---|
| **Fire: Fire Jab** | Pukulan lurus cepat (windup 2t, active 3t, recovery 4t, sphere 2.5m) | Partikel `flame` + suara `blaze.shoot` vanilla | 🟡 Parsial (35%) | 1. Animasi pukulan tinju<br>2. SFX pukulan api instan<br>3. Flash partikel saat tinju melesat |
| **Fire: Flame Sweep** | Sapuan api busur 180° (windup 3t, active 8t, recovery 6t, arc 5.0m) | Geometri polar partikel `flame` via caret | 🟡 Parsial (40%) | 1. Animasi tebasan/ayunan memutar<br>2. Tekstur/mesh slash trail api melengkung<br>3. SFX sabetan api menyala |
| **Fire: Fire Jet** | Lunge mobilitas cepat ke depan dengan semburan api | Semburan partikel di kaki + `tp` velocity check | 🟡 Parsial (40%) | 1. Animasi pose meluncur lunge<br>2. Suara deru api jet kontinu<br>3. Partikel thrust api di telapak kaki |
| **Staff: Tusuk (Thrust)** | Serangan tusukan lurus tongkat ke depan | Tidak ada | 🔴 Kosong (0%) | 1. Model 3D tongkat (`air_staff.json`)<br>2. Tekstur tongkat (`air_staff.png`)<br>3. Animasi tusukan dua tangan<br>4. Suara desingan dorongan |
| **Staff: Putar (Spin)** | Putaran tongkat vertikal/horizontal menangkis proyektil | Partikel sweep vanilla | 🔴 Kosong (10%) | 1. Animasi memutar tongkat kontinu<br>2. VFX lingkaran angin melingkar di ujung tongkat<br>3. SFX desiran kayu berputar |
| **Staff: Sapu (Sweep)** | Sabetan busur angin mendatar | Partikel gust/sweep vanilla | 🔴 Kosong (10%) | 1. Animasi sabetan tongkat mendatar<br>2. VFX sabit angin tajam<br>3. SFX angin kencang menghempas |
| **Staff: Air Vortex** | Pusaran angin menyedot musuh | Lingkaran partikel awan konsentris di datapack | 🟡 Parsial (25%) | 1. Animasi membanting/memutar tongkat ke tanah<br>2. Mesh/geometri partikel corong tornado<br>3. SFX raungan pusaran udara |

---

## 5. Kesenjangan Sistemik Pendukung (Audio & Bank Suara)

Selain kebutuhan spesifik per moveset, ditemukan kesenjangan struktural pada aset pendukung:

1. **Ketiadaan Struktur Audio Resmi**:
   * Repositori proyek belum memiliki direktori `assets/avatar/sounds/` maupun file registrasi `sounds.json`.
   * Akibatnya, seluruh efek suara saat ini masih menumpang (*hardcoded*) pada event suara bawaan Minecraft vanilla.
2. **Keberadaan Aset Referensi yang Belum Terverifikasi**:
   * Arsip `reference/Avatar-Addon-1.3.2-Beta.mcaddon` memiliki 37 file suara `.ogg` autentik dan animasi Bedrock, namun:
     * **Izin & Lisensi belum jelas** (tercatat sebagai referensi pihak ketiga).
     * Format animasi Bedrock (`.animation.json`) tidak kompatibel langsung dengan Fabric Java/Epic Fight.
     * Sesuai mandat perlindungan proyek, file ini **tidak boleh diekstrak ke paket rilis** sebelum ada konfirmasi resmi.

---

## 6. Usulan Solusi Teknis (Tanpa Mengubah Kode yang Ada)

Sebagai rekomendasi terpisah untuk tim desain dan pengembang:

1. **Penyediaan Model Tongkat Udara (Prioritas 1)**:
   * Buat model item 3D kubus sederhana (`air_staff.json`) menggunakan software Blockbench dengan tekstur kayu 16×16 atau 32×32 piksel, disesuaikan dengan proporsi tangan pemain Minecraft Java.
2. **Pembuatan Bank Suara Resmi Proyek (Prioritas 2)**:
   * Sediakan file audio orisinal bebas royalti (Creative Commons 0 / buatan sendiri) untuk 4 efek dasar:
     * `fire_whoosh.ogg` (ayunan api)
     * `fire_hit.ogg` (ledakan benturan api)
     * `air_whoosh.ogg` (ayunan tongkat angin)
     * `air_vortex.ogg` (pusaran angin)
   * Daftarkan di `mod/src/main/resources/assets/avatar_elements/sounds.json`.
3. **Pemanfaatan Animasi Kompatibel Fabric**:
   * Saat Claude Code menyelesaikan scaffold Fabric mod, integrasikan format animasi yang didukung mod animasi Java (misal: JSON pose Epic Fight untuk Fabric atau animasi berbasis GeckoLib/PlayerAnimator) yang dirancang khusus untuk kombo 3 langkah.
