# CLAUDE HANDOFF: SPESIFIKASI STUDI GERAK & KEYFRAME FIRE JAB

Dokumen ini memuat data handoff resmi dari Antigravity untuk Claude terkait implementasi animasi **Fire Jab (tangan kosong)**.

> [!IMPORTANT]
> **Status Integrasi & Batasan Operasional:**
> - **Ready Pose Air Staff Tetap Dibekukan:** Pose tongkat Candidate 2 tetap dibekukan di [`player_staff_thrust_ready_artistic.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready_artistic.bbmodel) dan [`CLAUDE_READY_POSE_HANDOFF.md`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/CLAUDE_READY_POSE_HANDOFF.md).
> - **Pose Tangan Kosong Murni:** Fire Jab adalah jurus pukulan tangan kosong tanpa tongkat.
> - **Direktori `mod/` Tidak Dimodifikasi:** Seluruh modifikasi kode runtime berada di bawah kewenangan Claude.
> - **Tunda Ekspor PAL Final:** Ekspor file animasi runtime final ditunda sampai template rig PAL yang terbukti di dalam game dibagikan oleh Claude.

---

## 1. File Sumber & Dataset

| Item | Path File | Keterangan |
|---|---|---|
| **Model Blockbench Sumber** | [`player_fire_jab_study.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/fire_jab/player_fire_jab_study.bbmodel) | Model rig entity tangan kosong (tanpa staff). |
| **Dataset Keyframe JSON** | [`fire_jab_keyframes.json`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/fire_jab/fire_jab_keyframes.json) | Data diskret keyframe, durasi fase, rotasi Euler, dan telemetri joint. |
| **Preview Realtime (0.45s)** | [`fire_jab_motion_normal.gif`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/fire_jab/fire_jab_motion_normal.gif) | Animasi kecepatan penuh $0.45\,\text{s}$ (18 frame, 40 fps / 9 tick loop). |
| **Preview Slow Annotated** | [`fire_jab_motion_slow_annotated.gif`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/fire_jab/fire_jab_motion_slow_annotated.gif) | Animasi diperlambat $0.25\times$ ($1.80\,\text{s}$) dengan HUD banner penanda tick, fase, dan flame tracking. |

---

## 2. Pemisahan Interval Fase vs Waktu Keyframe Diskret

### A. Interval Fase (Durasi Fase Gameplay)
Total Durasi Jurus: **9 ticks** ($0.45\,\text{s}$ pada 20 tps). Sesuai dengan konfigurasi `SkillTimeline` dan `skill_definitions.json`.

```
Tick:  0         1         2         3         4         5         6         7         8         9
       |---------|---------|---------|---------|---------|---------|---------|---------|---------|
Fase:  [--- Windup: 2t ----][--------- Active: 3t ----------][----------- Recovery: 4t -----------]
Waktu: 0.00s               0.10s     0.15s               0.25s                               0.45s
                                       ^
                                 HITBOX & FLAME BURST
                                 (Tick 1 dalam Active = Tick 3 absolut)
```

1. **Windup / Anticipation:**
   - Interval: Tick $0 \to 2$ (durasi **2 ticks** / $0.10\,\text{s}$).
   - Gerak: *Coiling* torso ke kanan (Yaw $-35^\circ$), tinju kanan ditarik ke rusuk belakang untuk mengumpulkan momentum.
2. **Active / Strike:**
   - Interval: Tick $2 \to 5$ (durasi **3 ticks** / $0.15\,\text{s}$).
   - **Event Hitbox & Pelepasan Api:** Terjadi tepat pada **Tick 1 Active / Tick 3 Absolut** ($t = 0.15\,\text{s}$).
     - Damage: $4.0$, Range: $2.5\,\text{m}$, Knockback: $0.3$.
     - Partikel: `minecraft:flame`, Suara: `minecraft:entity.blaze.shoot`.
   - Tick $3 \to 5$ ($0.10\,\text{s}$): Puncak pukulan ditahan sesaat (*impact / follow-through frame*) sebelum ditarik.
3. **Recovery / Return:**
   - Interval: Tick $5 \to 9$ (durasi **4 ticks** / $0.20\,\text{s}$).
   - Gerak: *Snap-back* tinju kanan, meredam recoil tubuh, kembali seimbang ke sikap siap tangan kosong.

---

### B. Waktu Keyframe Diskret (Discrete Keyframe Timeline)

| Keyframe ID | Waktu Diskret | Nama Fase / Pose | Deskripsi Gerak |
|---|---|---|---|
| **KF0** | $t = 0\,\text{t}$ ($0.00\,\text{s}$) | `Ready_Stance` | Sikap siaga tangan kosong (*orthodox stance*). Tinju kanan di rusuk, tinju kiri guard. |
| **KF1** | $t = 2\,\text{t}$ ($0.10\,\text{s}$) | `Anticipation_Peak` | Puncak windup. Torso memilin maksimal ke kanan (Yaw $-35^\circ$), tinju kanan ditarik paling belakang. |
| **KF2** | $t = 3\,\text{t}$ ($0.15\,\text{s}$) | `Strike_Impact` | Puncak lontaran tinju kanan (ekstensi maksimal $Z = -10.2\,\text{u}$). Hitbox & pelepasan semburan api aktif. |
| **KF3** | $t = 5\,\text{t}$ ($0.25\,\text{s}$) | `Active_End` | Akhir fase active. Pukulan mulai ditarik (*snap back*), pinggul mulai berputar balik. |
| **KF4** | $t = 9\,\text{t}$ ($0.45\,\text{s}$) | `Recovery_End` | **IDENTIK 100% DENGAN KF0 (`Ready_Stance`)**. Animasi loop mulus tanpa jeda/snap. |

---

## 3. Rotasi Euler Lokal Bone (Urutan `"ZYX"`, Derajat)

Hierarki Rig:
- `torso` (Pivot: `[0, 12, 0]`)
  - `head` (Pivot: `[0, 24, 0]`)
  - `right_upper_arm` (Pivot: `[5, 22, 0]`)
    - `right_forearm` (Pivot: `[5, 16, 0]`)
  - `left_upper_arm` (Pivot: `[-5, 22, 0]`)
    - `left_forearm` (Pivot: `[-5, 16, 0]`)
- `right_leg` (Pivot: `[2, 12, 0]`)
- `left_leg` (Pivot: `[-2, 12, 0]`)

### Data Euler Rotasi Per Keyframe

```json
{
  "KF0_Ready_0t": {
    "torso":           [ 0.00, -20.00,   0.00],
    "head":            [ 0.00,  20.00,   0.00],
    "right_upper_arm": [-1.84,  20.59,  37.46],
    "right_forearm":   [29.88,  19.02, -70.75],
    "left_upper_arm":  [32.47,  28.08, -29.67],
    "left_forearm":    [-6.02,  52.84, 113.20],
    "right_leg":       [-12.00, -10.00,  0.00],
    "left_leg":        [ 12.00, -10.00,  0.00]
  },
  "KF1_Anticipation_2t": {
    "torso":           [ 4.00, -35.00,   0.00],
    "head":            [-4.00,  35.00,   0.00],
    "right_upper_arm": [ 8.45,  33.23,  56.13],
    "right_forearm":   [33.12,  21.03, -74.83],
    "left_upper_arm":  [23.20,  38.97, -33.58],
    "left_forearm":    [-5.38,  58.18, 116.08],
    "right_leg":       [-15.00, -15.00,  0.00],
    "left_leg":        [ 15.00, -15.00,  0.00]
  },
  "KF2_Strike_Impact_3t": {
    "torso":           [ 2.00,  12.00,   0.00],
    "head":            [-2.00, -12.00,   0.00],
    "right_upper_arm": [54.75,  -4.93, -13.90],
    "right_forearm":   [ 5.92,  -7.52, -18.06],
    "left_upper_arm":  [19.82,  -6.97, -31.31],
    "left_forearm":    [-26.86, 17.45,  65.05],
    "right_leg":       [-8.00,  10.00,   0.00],
    "left_leg":        [ 16.00,   5.00,  0.00]
  },
  "KF3_Active_End_5t": {
    "torso":           [ 1.00,   5.00,   0.00],
    "head":            [-1.00,  -5.00,   0.00],
    "right_upper_arm": [35.20,   8.40,  12.50],
    "right_forearm":   [18.50,   4.20, -38.20],
    "left_upper_arm":  [24.00,  12.50, -29.00],
    "left_forearm":    [-18.00, 32.00,  88.00],
    "right_leg":       [-10.00,   0.00,  0.00],
    "left_leg":        [ 14.00,   0.00,  0.00]
  },
  "KF4_Recovery_End_9t": {
    "torso":           [ 0.00, -20.00,   0.00],
    "head":            [ 0.00,  20.00,   0.00],
    "right_upper_arm": [-1.84,  20.59,  37.46],
    "right_forearm":   [29.88,  19.02, -70.75],
    "left_upper_arm":  [32.47,  28.08, -29.67],
    "left_forearm":    [-6.02,  52.84, 113.20],
    "right_leg":       [-12.00, -10.00,  0.00],
    "left_leg":        [ 12.00, -10.00,  0.00]
  }
}
```

---

## 4. Konvensi Sumbu Koordinat & Label Kaki Terhadap Arah -Z

Sistem koordinat Three.js / Blockbench / Minecraft:
- Arah **$-Z$** = **Depan (Forward)** menuju arah pandang dan target musuh.
- Arah **$+Z$** = **Belakang (Backward)** menjauhi musuh.
- Rotasi Pitch Kaki:
  - Pitch $> 0$ memutar ujung kaki ke arah $-Z$ (DEPAN).
  - Pitch $< 0$ memutar ujung kaki ke arah $+Z$ (BELAKANG).

### Verifikasi Geometri Kaki
- **Kaki Kiri = Lead Foot (Kaki Depan):**
  - Pitch $+12^\circ \to +16^\circ$.
  - Koordinat tapak kaki di dunia: $Z = -2.49\,\text{u}$ (arah $-Z$, DEPAN).
  - Berfungsi menjejak kokoh menahan hentakan pukulan.
- **Kaki Kanan = Rear Foot (Kaki Belakang):**
  - Pitch $-12^\circ \to -8^\circ$.
  - Koordinat tapak kaki di dunia: $Z = +2.49\,\text{u}$ (arah $+Z$, BELAKANG).
  - Berfungsi mendorong ke lantai dan mentransfer daya putaran pinggul.

---

## 5. Kontrak Anchor Titik Pelepasan Api (*Flame Emit Point*)

1. **Koordinat Lokal Pada Bone `right_forearm`:**
   - Dalam ruang lokal `right_forearm` (origin di siku `[5, 16, 0]`, panjang tulang $6\,\text{unit}$ ke bawah), pergelangan tangan berada di `[0, -6.0, 0]`.
   - Titik pelepasan api (buku jari / knuckles) berada $+2.0\,\text{unit}$ melewati pergelangan tangan:
     $$\mathbf{P}_{\text{local\_flame}} = [0.0, -8.0, 0.0]$$
2. **Koordinat Dunia Sejati Sepanjang Siklus Gerak:**
   - **KF0 (Ready, $t = 0.00\,\text{s}$):** $[+3.29, 11.57, +0.28]$ (merapat di samping rusuk)
   - **KF1 (Anticipation, $t = 0.10\,\text{s}$):** $[+4.24, 11.89, +2.50]$ (ditarik mundur ke $+Z$)
   - **KF2 (Strike Impact, $t = 0.15\,\text{s}$):** $[-0.50, 15.76, -11.77]$ (lontaran maksimal ke $-Z$, melesat sejauh $\Delta Z = 14.27\,\text{unit} \approx 0.89\,\text{blok}$)
   - **KF3 (Followthrough, $t = 0.25\,\text{s}$):** $[+0.49, 15.08, -7.74]$ (mulai snap back)
   - **KF4 (Recovery End, $t = 0.45\,\text{s}$):** $[+3.29, 11.57, +0.28]$ (kembali identik ke KF0)
3. **Vektor Partikel di Runtime:**
   - Arah tembakan semburan api: searah sumbu forearm mengarah ke depan $[-0.04, -0.06, -0.99]$.
   - Kecepatan partikel: $0.4\,\text{blocks/tick}$, cone spread $15^\circ$.

---

## 6. Panduan Transisi Runtime (Blending Contract)

Untuk integrasi ke dalam runtime Player Animation Library (PAL):
1. **Blend-in (Idle $\to$ KF0):**
   - Ketika tombol cast Fire Jab ditekan, lakukan interpolasi transisi cepat ($1\text{--}2$ ticks / $0.05\text{--}0.10\,\text{s}$) dari animasi dasar pemain (vanilla walk/idle) menuju KF0 (`Ready_Stance`).
2. **Eksekusi Jurus (KF0 $\to$ KF4):**
   - Mainkan seluruh keyframe secara sekuensial selama tepat **9 ticks** ($0.45\,\text{s}$).
3. **Blend-out (KF4 $\to$ Idle/Walk):**
   - Pada tick 9, karena pose KF4 sudah $100\%$ identik dengan sikap siap tangan kosong, animasi dapat langsung di-loop jika kombo berlanjut, ATAU di-blend out secara mulus menggunakan *cubic ease-out* selama $2\text{--}3$ ticks ($0.10\text{--}0.15\,\text{s}$) ke animasi vanilla jika pemain sedang berjalan/berlari.
   - Tidak akan terjadi *popping* atau patahan geometri karena kontinuitas posisi sendi terjaga.
