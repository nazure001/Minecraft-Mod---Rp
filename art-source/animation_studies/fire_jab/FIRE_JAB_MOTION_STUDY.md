# Studi Gerak & Blocking Fire Jab (Empty-Handed)

Dokumen ini memuat spesifikasi kinematika, pemisahan interval fase vs waktu keyframe diskret, konvensi kaki terhadap sumbu $-Z$, titik pelacak partikel api, dan preview bergerak untuk jurus **Fire Jab** (pukulan tinju api tangan kosong).

---

## 1. Status & Batasan Kerja

1. **Staff Ready Pose Tetap Dibekukan:**
   - Model ready pose tongkat Candidate 2 tetap dibekukan di [`player_staff_thrust_ready_artistic.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready_artistic.bbmodel) dan spesifikasi di [`CLAUDE_READY_POSE_HANDOFF.md`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/CLAUDE_READY_POSE_HANDOFF.md).
   - Tidak ada modifikasi atau regenerasi aset tongkat.
2. **Pose Tangan Kosong Murni (*Empty-Handed*):**
   - Fire Jab adalah jurus pukulan tangan kosong; tidak memegang tongkat atau alat bantu.
   - Model kerja: [`player_fire_jab_study.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/fire_jab/player_fire_jab_study.bbmodel).
3. **Disiplin Mod:**
   - Direktori `mod/` tidak diubah (Claude adalah pemilik implementasi runtime).
4. **Tunda Ekspor Final:**
   - Ekspor format animasi runtime final ditunda sampai template rig Player Animation Library (PAL) yang terbukti di dalam game dibagikan oleh Claude.

---

## 2. Pemisahan Interval Fase vs Waktu Keyframe Diskret

### A. Interval Fase (Durasi Fase Gameplay)
Total Durasi Jurus: **9 ticks** ($0.45\,\text{s}$ pada $20\,\text{tps}$). Sesuai dengan konfigurasi `SkillTimeline` dan `skill_definitions.json`.

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

## 3. Konvensi Sumbu Koordinat & Label Kaki Terhadap Arah -Z

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

## 4. Spesifikasi Kinematika & Rotasi Euler Bone (ZYX, Derajat)

Rotasi diekstrak menggunakan urutan Euler standar Blockbench Three.js (`"ZYX"`: Roll $Z \to$ Yaw $Y \to$ Pitch $X$, derajat):

| Bone | KF0: Ready (0t) | KF1: Anticipation (2t) | KF2: Strike Impact (3t) | KF3: Active End (5t) | KF4: Recovery End (9t) |
|---|---|---|---|---|---|
| **torso** | `[0.0, -20.0, 0.0]` | `[4.0, -35.0, 0.0]` | `[2.0, 12.0, 0.0]` | `[1.0, 5.0, 0.0]` | `[0.0, -20.0, 0.0]` |
| **head** | `[0.0, 20.0, 0.0]` | `[-4.0, 35.0, 0.0]` | `[-2.0, -12.0, 0.0]` | `[-1.0, -5.0, 0.0]` | `[0.0, 20.0, 0.0]` |
| **right_upper_arm** | `[-1.84, 20.59, 37.46]` | `[8.45, 33.23, 56.13]` | `[54.75, -4.93, -13.90]` | `[35.20, 8.40, 12.50]` | `[-1.84, 20.59, 37.46]` |
| **right_forearm** | `[29.88, 19.02, -70.75]` | `[33.12, 21.03, -74.83]` | `[5.92, -7.52, -18.06]` | `[18.50, 4.20, -38.20]` | `[29.88, 19.02, -70.75]` |
| **left_upper_arm** | `[32.47, 28.08, -29.67]` | `[23.20, 38.97, -33.58]` | `[19.82, -6.97, -31.31]` | `[24.00, 12.50, -29.00]` | `[32.47, 28.08, -29.67]` |
| **left_forearm** | `[-6.02, 52.84, 113.20]` | `[-5.38, 58.18, 116.08]` | `[-26.86, 17.45, 65.05]` | `[-18.00, 32.00, 88.00]` | `[-6.02, 52.84, 113.20]` |
| **right_leg** | `[-12.0, -10.0, 0.0]` | `[-15.0, -15.0, 0.0]` | `[-8.0, 10.0, 0.0]` | `[-10.0, 0.0, 0.0]` | `[-12.0, -10.0, 0.0]` |
| **left_leg** | `[12.0, -10.0, 0.0]` | `[15.0, -15.0, 0.0]` | `[16.0, 5.0, 0.0]` | `[14.0, 0.0, 0.0]` | `[12.0, -10.0, 0.0]` |

---

## 5. Kontrak Anchor Titik Pelepasan Api (*Flame Emit Point*)

1. **Koordinat Lokal Pada Bone `right_forearm`:**
   $$\mathbf{P}_{\text{local\_flame}} = [0.0, -8.0, 0.0]$$
   ($+2.0\,\text{unit}$ melewati pergelangan tangan sepanjang sumbu lengan bawah).
2. **Koordinat Dunia Sejati Sepanjang Siklus Gerak:**
   - **KF0 (Ready, $0.00\,\text{s}$):** $[+3.29, 11.57, +0.28]$ (merapat di samping rusuk)
   - **KF1 (Anticipation, $0.10\,\text{s}$):** $[+4.24, 11.89, +2.50]$ (ditarik mundur ke $+Z$)
   - **KF2 (Strike Impact, $0.15\,\text{s}$):** $[-0.50, 15.76, -11.77]$ (lontaran maksimal ke $-Z$)
   - **KF3 (Followthrough, $0.25\,\text{s}$):** $[+0.49, 15.08, -7.74]$ (mulai snap back)
   - **KF4 (Recovery End, $0.45\,\text{s}$):** $[+3.29, 11.57, +0.28]$ (kembali identik ke KF0)

---

## 6. Pratinjau Visual Bergerak & Artefak Render

### Animasi GIF 3D
- **Preview Realtime (0.45s / 9 ticks):** [`fire_jab_motion_normal.gif`](file:///C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71/fire_jab_motion_normal.gif)
- **Preview Slow Motion (1.80s, 0.25x) Berpenanda Waktu:** [`fire_jab_motion_slow_annotated.gif`](file:///C:/Users/USER/.gemini/antigravity/brain/54a80670-a4c4-4299-bd5f-db191f100d71/fire_jab_motion_slow_annotated.gif)
