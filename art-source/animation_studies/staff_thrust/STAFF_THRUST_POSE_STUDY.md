# STUDI GERAKAN: TUSUKAN TONGKAT DUA TANGAN (STAFF THRUST POSE STUDY)

> **Dokumentasi Pre-Produksi Studi Gerak (Pre-Production Motion Study)**  
> **Mod:** Avatar Elements (Minecraft Java Edition 1.21.1)  
> **Aset Terkait:** Air Nomad Staff (`air_staff.json` / `air_staff.bbmodel` v0.2) — Panjang tetap 30.0 unit (1.875 blok / ~1.875 m)  
> **Fokus Kajian:** Kinematika Rig Pemain Komunitas, Titik Kontak Satu Tongkat, dan Lintasan Tusukan Linier  
> **Status:** Studi Gerak (DCC Motion Study) — *Bukan Animasi Runtime Siap Pakai Vanilla*

---

## 1. TUJUAN & RUANG LINGKUP STUDI

Studi ini bertujuan menganalisis kinematika gerakan **Tusukan Linier Tongkat Dua Tangan (*Staff Thrust*)** menggunakan rig karakter pemain Minecraft standar komunitas (Biped recreation Steve/Alex di Blockbench; bukan rig resmi dari Mojang). 

Sebagai senjata beladiri tradisi Pengembara Udara (*Air Nomads*), tongkat staf tidak sekadar dipukul seperti pentungan (*club*), melainkan digunakan dengan prinsip beladiri tongkat (*Bojutsu / Northern Shaolin Gunshu*) yang mengandalkan:
1. Tuas mekanis dua tangan (*dual-hand fulcrum & piston mechanics*) pada **satu batang tongkat tunggal**.
2. Penetrasi garis lurus horizontal (*linear piercing vector*) ke arah ulu hati sasaran.
3. Transmisi gaya pegas rotasi panggul dan dorongan kuda-kuda busur (*bow stance / Gong Bu*).

---

## 2. SPESIFIKASI 4 POSE UTAMA

Berikut adalah dekonstruksi 4 fase kinematika tusukan tongkat yang telah dimodelkan dan dirender:

```
[Pose 1: Sikap Awal] ---> [Pose 2: Persiapan / Windup] ---> [Pose 3: Dorongan / Strike] ---> [Pose 4: Pemulihan / Reset]
(Kuda-kuda seimbang)      (Pegas panggul ditarik)          (Tusukan lurus meledak)          (Redaman & kembali siaga)
```

### Pose 1: Sikap Awal Dua Tangan (*Two-Handed Ready Stance*)
- **Timing:** Frame 0 – 5 (0.00s – 0.21s)
- **Kuda-kuda & Distribusi Bobot:** 
  - Kuda-kuda serang atletis seimbang (*Zhan Zhuang / Bo Guard*).
  - Kaki kiri (lead) sedikit melangkah maju (+Z), lutut sedikit lentur. Kaki kanan (rear) di belakang menyudut 35° untuk stabilitas tumpuan.
  - Distribusi beban: 50% kaki depan, 50% kaki belakang. Ketinggian pelvis turun sedikit ke Y = 11.5 (dari Y = 12.0 standar berdiri tegak).
- **Torso & Kepala:**
  - Torso berotasi Yaw +22° (menghadap serong kanan), mempersempit siluet target tubuh (*blade profile*) terhadap musuh.
  - Kepala mengompensasi rotasi torso dengan Yaw -22°, sehingga pandangan mata tetap mengunci lurus ke arah target (+Z).
- **Genggaman & Orientasi Tongkat:**
  - Tangan kanan (belakang) memegang bagian bawah tongkat pada koordinat `[-3.2, 14.0, 1.2]` di samping panggul.
  - Tangan kiri (depan) memegang bagian selubung wrap tengah pada `[1.8, 16.5, 7.8]` di depan dada.
  - Ujung tongkat membidik koridor dada sasaran pada elevasi `Y = 19.2`, `Z = +14.9`.

---

### Pose 2: Persiapan / Tarikan (*Anticipation / Windup*)
- **Timing:** Frame 6 – 11 (0.25s – 0.46s)
- **Kuda-kuda & Distribusi Bobot:**
  - Pemadatan pegas tubuh (*kinetic coiling*): pelvis ditarik mundur ke `Z = -1.0`, turun ke `Y = 10.8`.
  - Bobot bertumpu 70% di kaki belakang (kanan), lutut kanan tertekuk dalam (-26° pitch). Kaki depan (kiri) bertumpu ringan pada ujung telapak kaki.
- **Torso & Kepala:**
  - Torso berotasi lebih dalam ke Yaw +42° dan Pitch +6°, memuntir otot inti tubuh (*core torque*).
  - Kepala mempertahankan *aim-lock* ketat (Yaw -42°) mengarah ke sasaran.
- **Genggaman & Orientasi Tongkat:**
  - Tangan kanan menarik tongkat mundur jauh ke belakang pinggul kanan pada `[-5.6, 13.2, -3.4]`.
  - Tangan kiri menggeser cengkeraman penuntun di sepanjang wrap pada `[-0.4, 16.2, 3.8]`.
  - Tutup bawah tongkat (*butt cap*) menonjol ke belakang pada `[-8.4, 11.6, -7.2]`.
  - Ujung tongkat (*tip*) mundur ke `Z = +10.8` (retraksi bersih 4.1 unit dari sikap awal), siap melesat lurus ke depan.

---

### Pose 3: Dorongan / Tusukan (*Thrust Strike - Apex Penetration*)
- **Timing:** Frame 12 – 17 (0.50s – 0.71s)
- **Kuda-kuda & Distribusi Bobot:**
  - Kuda-kuda busur dinamis meledak (*Gong Bu / Deep Forward Lunge*).
  - Kaki belakang mendorong lantai dengan gaya dorong maksimal (ekstensi lurus -35° pitch), panggul melesat maju ke `Z = +3.8`.
  - Kaki depan (kiri) menancap kokoh dengan lutut tertekuk 90° (+32° pitch) menopang 75% bobot tubuh.
- **Torso & Kepala:**
  - Torso berputar cepat dari +42° kembali menghadap sasaran (Yaw +8°), melepaskan seluruh torsi rotasi tubuh. Torso condong maju (Pitch +12°) untuk menambah daya tusuk.
  - Kepala fokus tajam mengiringi sumbu penetrasi.
- **Genggaman & Orientasi Tongkat:**
  - Tangan kanan (piston) menghantam maju lurus ke depan pada `[-1.4, 17.5, 9.2]`.
  - Tangan kiri (selongsong) meluruskan jangkauan ke `[1.2, 19.0, 16.8]`.
  - Ujung tongkat mencapai ekstensi jangkauan maksimum pada `[3.4, 20.3, 27.6]` (+27.6 unit di depan titik pusat pemain!).
  - Ketinggian penetrasi tepat berada pada `Y = 20.3` (titik ulu hati musuh setinggi 1.27 meter).

---

### Pose 4: Pemulihan (*Recovery & Guard Reset*)
- **Timing:** Frame 18 – 24 (0.75s – 1.00s)
- **Kuda-kuda & Distribusi Bobot:**
  - Penyerapan hentakan balik (*recoil absorption*): panggul ditarik surut sedikit ke `Z = +1.5`, elevasi kembali ke `Y = 11.6`.
  - Kuda-kuda kembali lentur dan seimbang (55% depan / 45% belakang).
- **Torso & Kepala:**
  - Torso mereda ke posisi netral bertahan (Yaw +18°, Pitch +4°).
- **Genggaman & Orientasi Tongkat:**
  - Tongkat ditarik surut secara terkendali sejauh 10.4 unit dari titik penetrasi puncak (ujung tongkat berada di `Z = +17.2`).
  - Posisi kedua tangan kembali rileks melindungi tubuh tengah, siap menyambung ke kombo tebasan memutar (*whirlwind sweep*) atau tangkisan atas.

---

## 3. CATATAN TEKNIS TITIK KONTAK PADA SATU TONGKAT UTUH

Dalam studi ini, model tongkat yang digunakan adalah **satu batang fisik tunggal dan kaku (rigid single body)** dengan panjang konstan **30.0 unit** (setara 1.875 blok / meter). Penggunaan dua objek tongkat terpisah untuk menyamarkan masalah pergeseran genggaman tidak diperkenankan.

```
[Butt Cap: 0u] === (5.5u) === [Rear Grip: R-Hand] === (Grip Span: 7.9u - 9.4u) === [Lead Sleeve: L-Hand] === (Tip Offset) === [Tip Cap: 30u]
```

1. **Tangan Kanan / Belakang (*Rear Power Hand / Piston*):**
   - **Titik Kontak:** Terkunci stabil pada jarak konstan **5.5 unit** (0.34 blok) di atas tutup bawah (*butt cap*).
   - **Fungsi Mekanis:** Piston penekan utama (*linear thruster*). Tangan ini menggenggam kayu poros bawah secara kaku dan mendorong seluruh batang tongkat sepanjang sumbu serang.
2. **Tangan Kiri / Depan (*Lead Guide Hand / Fulcrum Sleeve*):**
   - **Titik Kontak:** Bertindak pada zona lilitan selubung kain (*crimson wrap*, segmen unit 12.0 hingga 18.0).
   - **Mekanika Pergeseran (*Slide Sleeve Mechanic*):** Pada teknik tusukan tongkat nyata, tangan depan tidak mencengkeram mati pada titik koordinat beku, melainkan menjadi selongsong penuntun (*loose sliding sleeve*). Tongkat meluncur maju menembus telapak tangan kiri.
3. **Koreksi Rentang Genggam & Fenomena Drift:**
   - **Bukan Rentang Konstan:** Pada sistem animasi Forward Kinematics (FK) bebas, jarak linier antar kedua pergelangan tangan berfluktuasi dari **7.9 unit hingga 9.4 unit** (mengalami pergeseran/drift sebesar **1.5 unit / ~9.4 cm**).
   - Fenomena ini membuktikan bahwa animasi dua tangan pada senjata dua tangan kaku (*two-handed rigid polearm*) secara mutlak memerlukan mekanisme constraint (IK constraint atau slot attachment terdefinisi), agar telapak tangan depan tidak menembus atau terlepas dari badan tongkat saat pemutaran animasi in-game.

---

## 4. LINTASAN UJUNG TONGKAT (*THRUST TRAJECTORY*)

Di Minecraft, rasio skala geometris adalah: **16 model unit = 1.0 blok dunia = 1.0 meter**.

| Parameter Kinematika | Nilai Model | Konversi Skala Minecraft | Keterangan Evaluasi |
| :--- | :--- | :--- | :--- |
| **Panjang Tongkat Utuh** | `30.0 unit` | **1.875 blok (~1.875 m)** | Panjang fisik tetap (*rigid length*), tidak berubah antar pose. |
| **Rentang Ketinggian (Y)** | `Y = 19.2 s.d. 20.3` | **Elevasi dada (1.20 - 1.27 m)** | Deviasi vertikal hanya **1.1 unit (6.8 cm)**; tusukan horizontal stabil. |
| **Jangkauan Ekstensi (Z)** | `Z = +10.8 s.d. +27.6`| **1.05 blok (1.05 meter)** | Jarak luncur bersih **16.8 unit** dari titik tarikan awal ke penetrasi puncak. |
| **Penyimpangan Samping (X)**| `X = -1.2 s.d. +1.4` | **< 0.16 blok (< 16 cm)** | Jalur lurus menuju garis tengah sasaran (*combat center-line*). |

---

## 5. TABEL LENGKAP ROTASI SENDI (*JOINT EULER MATRIX*)

Semua rotasi sendi disajikan dalam format Euler Degree (Pitch-X, Yaw-Y, Roll-Z) berbasis konvensi Blockbench / Minecraft:

| Bone / Sendi | Pose 1 (Sikap Awal) | Pose 2 (Windup) | Pose 3 (Thrust Strike) | Pose 4 (Recovery) |
| :--- | :--- | :--- | :--- | :--- |
| **Pelvis Root (Posisi)** | `[0.0, 11.5, 0.0]` | `[-0.5, 10.8, -1.0]` | `[0.2, 11.2, 3.8]` | `[0.0, 11.6, 1.5]` |
| **Torso (Rotasi)** | `[4.0, 22.0, 0.0]` | `[6.0, 42.0, -2.0]` | `[12.0, 8.0, 0.0]` | `[4.0, 18.0, 0.0]` |
| **Head (Rotasi)** | `[-2.0, -22.0, 0.0]` | `[0.0, -42.0, 2.0]` | `[4.0, -8.0, 0.0]` | `[-1.0, -18.0, 0.0]` |
| **Right Arm (Piston)** | `[-16.0, -10.0, -8.0]` | `[10.0, -24.0, -14.0]` | `[-62.0, -6.0, -6.0]` | `[-24.0, -12.0, -8.0]` |
| **Left Arm (Guide)** | `[-48.0, 26.0, 18.0]` | `[-36.0, 40.0, 24.0]` | `[-76.0, 10.0, 12.0]` | `[-50.0, 22.0, 15.0]` |
| **Right Leg (Rear)** | `[-14.0, -18.0, 6.0]` | `[-26.0, -26.0, 8.0]` | `[-35.0, -10.0, 6.0]` | `[-18.0, -14.0, 4.0]` |
| **Left Leg (Lead)** | `[10.0, 12.0, -4.0]` | `[18.0, 16.0, -2.0]` | `[32.0, 4.0, -4.0]` | `[14.0, 8.0, -3.0]` |

---

## 6. BATASAN ARSITEKTUR & PENETAPAN KONTRAK MENDATANG

> [!IMPORTANT]
> **PEMBATAS ARSITEKTUR & PENETAPAN FRAMEWORK:**
> 1. Dokumen ini adalah **studi kinematika gerak pre-produksi**, bukan implementasi runtime.
> 2. Model JSON item vanilla Minecraft tidak dapat menganimasikan tubuh pemain.
> 3. **Penetapan Framework Animasi:** Sesuai arahan, Antigravity **TIDAK MEMILIH** framework animasi runtime dan tidak mengubah kode pada `mod/`.
> 4. **Lingkup Claude Code (Checkpoint Berikutnya):** Claude Code yang akan menetapkan kontrak animasi pemain resmi (spesifikasi rig/bone, format ekspor model/animasi, metode item attachment, konvensi satuan/koordinat, serta mekanisme pemutaran dan sinkronisasi gameplay) serta membuktikannya dengan satu animasi sederhana terlebih dahulu.

---

## 7. INVENTARIS FILE HASIL STUDI

Semua file studi tersimpan rapi dan terisolasi di folder:  
[`art-source/animation_studies/staff_thrust/`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust)

1. **`staff_thrust_motion.gif`** (Animasi Siklus Penuh 24-Frame @ 15 FPS):  
   Menampilkan tampak depan dan tampak samping berdampingan dengan SATU TONGKAT UTUH 30 unit konstan, memperlihatkan pergerakan kedua tangan dan posisi meluncurnya tongkat.
2. **`preview_storyboard_side.png`** & **`preview_storyboard_front.png`** (Storyboard 4 Pose Kunci):  
   Tampak samping ortografis dan tampak depan ortografis resolusi tinggi dengan telemetri koordinat kedua tangan terhadap satu tongkat.
3. **`staff_grip_contact_analysis.png`** (Grafik Diagnostik Titik Kontak):  
   Plot pergeseran posisi tangan kanan (terkunci di 5.5u) vs tangan kiri yang meluncur (13.4u s.d. 15.5u) di sepanjang 24 frame.
4. **`player_staff_thrust_study.bbmodel`** (Format Blockbench 4.10 `modded_entity` biped standard).
5. **`pose_data.json`** & skrip generator (`generate_thrust_motion_preview.py`).

---

## 8. ASPEK YANG BELUM DIUJI (*UNTESTED ASPECTS*)

1. **Sinkronisasi Kamera First-Person (FPV):**  
   Studi ini berfokus pada sudut pandang orang ketiga (Third-Person View / TPV) dan interaksi siluet luar. Penyesuaian FOV dan pemotongan jangkauan tongkat saat dilihat dari kamera mata pemain pertama belum diuji.
2. **Variasi Kulit Ramping Alex (Slim 3-pixel Arms):**  
   Rig yang digunakan saat ini adalah model standar Steve (lengan 4 pixel). Untuk model Alex, posisi cengkeraman tangan kiri dan kanan perlu sedikit penyesuaian offset X sebesar 0.5 unit ke dalam.
3. **Collision / Hitbox Raycast di Dalam Ruang Sempit Minecraft:**  
   Jangkauan ujung tongkat sebesar +27.6 unit (~1.72 blok dari pivot pemain) belum diuji terhadap sistem deteksi tubrukan balok sempit (1x1 atau lorong sempit pertambangan), di mana ujung tongkat berpotensi menembus dinding jika tidak dibatasi oleh *bounding box raycasting*.
