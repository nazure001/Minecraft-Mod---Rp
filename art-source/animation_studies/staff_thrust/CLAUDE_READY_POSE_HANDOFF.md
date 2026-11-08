# CLAUDE_READY_POSE_HANDOFF.md
## Kontrak Integrasi Pose Siaga (Ready Pose - Kandidat Integrasi) Pemain & Tongkat

Dokumen ini adalah spesifikasi resmi penyerahan pose statis siaga (**Ready Pose Candidate**) dari Antigravity untuk Claude, sebagai acuan verifikasi implementasi satu pose dalam runtime Minecraft (aktif lalu kembali normal) sebelum pengembangan rangkaian animasi lanjutan.

---

### 1. Sumber File & Referensi Tangkapan Layar
* **File Sumber Model:** [`player_staff_thrust_ready_artistic.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_ready_artistic.bbmodel)
  - Versi revisi yang menghasilkan seluruh tangkapan layar bersih dan terverifikasi di editor.
  - Seluruh kubus tongkat memiliki `origin` tersinkronisasi dengan origin grup `staff_assembly` (`[10.5953, 7.6933, 12.6588]`), bebas dari anomali translasi ganda (*double-translation*).
* **File Checkpoint Pendukung:**
  - Checkpoint Netral (Pose 0): [`player_staff_thrust_neutral.bbmodel`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/player_staff_thrust_neutral.bbmodel)
* **Tangkapan Layar Acuan Visual:**
  - Tampak Depan Bersih: [`ready_clean_front.png`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/ready_clean_front.png)
  - Tampak Samping Bersih: [`ready_clean_side.png`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/ready_clean_side.png)
  - Perspektif Bersih: [`ready_clean_perspective.png`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/ready_clean_perspective.png)
  - Perspektif Diagnostik (dengan Marker Attachment): [`ready_diagnostic_perspective.png`](file:///D:/repo/Minecraft%20Mod%20&%20Rp/art-source/animation_studies/staff_thrust/ready_diagnostic_perspective.png)

---

### 2. Standar Koordinat, Satuan, dan Urutan Rotasi
* **Satuan Dimensi:** $1.0\,\text{u} = 1\,\text{pixel model} = \frac{1}{16}\,\text{blok} = 0.0625\,\text{meter}$.
* **Orientasi Sumbu Dunia (World Axis):**
  - Depan (*Forward*): $-Z$
  - Atas (*Upward*): $+Y$
  - Kanan Pemain (*Model Right*): $+X$
  - Kiri Pemain (*Model Left*): $-X$
* **Urutan Rotasi Euler:**
  - **`"ZYX"`** (Roll $Z \to$ Yaw $Y \to$ Pitch $X$, sudut dalam **derajat**).
  - Matriks rotasi lokal: $R = R_z(\theta_z) \cdot R_y(\theta_y) \cdot R_x(\theta_x)$.

---

### 3. Hierarki, Pivot (Origin), dan Transform Lokal Bone

Semua nilai rotasi merupakan rotasi lokal relatif terhadap parent bone:

```
root
├── torso (origin: [0.0, 12.0, 0.0], rot: [5.0000, -25.0000, 0.0000])
│   ├── head (origin: [0.0, 24.0, 0.0], rot: [-5.0000, 25.0000, 0.0000])
│   ├── right_upper_arm (origin: [5.0, 22.0, 0.0], rot: [6.1848, 24.6837, 36.4963])
│   │   └── right_forearm (origin: [5.0, 16.0, 0.0], rot: [23.8474, 6.6770, -55.4314])
│   └── left_upper_arm (origin: [-5.0, 22.0, 0.0], rot: [14.6024, 25.4543, -10.0438])
│       └── left_forearm (origin: [-5.0, 16.0, 0.0], rot: [-2.8481, 13.8242, 57.1256])
├── right_leg (origin: [2.0, 12.0, 0.0], rot: [14.0000, -15.0000, 0.0000])
├── left_leg (origin: [-2.0, 12.0, 0.0], rot: [-18.0000, -15.0000, 0.0000])
└── staff_assembly (origin: [10.5953, 7.6933, 12.6588], rot: [-59.6530, 18.1792, 31.1840])
```

#### Dimensi Anggota Tubuh (Konstan)
* Lengan Atas (Kanan/Kiri): $6.0000\,\text{u}$
* Lengan Bawah (Kanan/Kiri): $6.0000\,\text{u}$
* Tongkat Kaku Utuh: $30.0000\,\text{u}$ (Kandidat 2)

---

### 4. Definisi Attachment dalam Ruang Lokal

Untuk menghindari ambiguitas ruang koordinat, titik attachment didefinisikan secara tegas dalam ruang lokal masing-masing komponen:

#### A. Ruang Lokal Lengan Bawah (Forearm Local Space)
Pivot lengan bawah berada di siku (`[0, 0, 0]` lokal). Tulang membujur ke arah $-Y$:
* **Attachment Pergelangan Tangan Kanan (`wrist_right_local`):** `[0.0, -6.0, 0.0]`
* **Attachment Pergelangan Tangan Kiri (`wrist_left_local`):** `[0.0, -6.0, 0.0]`

#### B. Ruang Lokal Tongkat (Staff Local Space)
Pivot grup `staff_assembly` berada di pangkal tongkat / *butt* (`[0, 0, 0]` lokal). Tongkat membujur lurus sepanjang sumbu $+Y$ dari $u = 0$ hingga $u = 30$:
* **Attachment Genggaman Belakang (`grip_rear_local`):** `[0.0, 13.0, 0.0]` (pada area grip wrap)
* **Attachment Genggaman Depan (`grip_lead_local`):** `[0.0, 21.5, 0.0]` (pada area shaft depan)

#### C. Hubungan Relatif Antar Attachment (Telemetri Dunia)
* Jarak pusat pergelangan tangan ke sumbu batang tongkat:
  - Tangan Belakang (Kanan): **$1.5000\,\text{u}$**
  - Tangan Depan (Kiri): **$1.5000\,\text{u}$**
* **Jarak Pendekatan Radius Penampang Tongkat:**
  - Belakang: **$0.5000\,\text{u}$** ($R_{\text{wrap}} \approx 1.0\,\text{u}$)
  - Depan: **$0.7500\,\text{u}$** ($R_{\text{shaft}} \approx 0.75\,\text{u}$)
  - *Catatan Metrik:* Jarak $1.5\,\text{u}$ dari pusat pergelangan ke sumbu tongkat merefleksikan posisi pergelangan tangan terhadap permukaan batang silinder/kubus (setengah tebal telapak tangan Minecraft $\approx 2\,\text{u}$).

---

### 5. Titik Lokal Pembentuk Trail VFX (Ribbon Generation)

Untuk menghasilkan efek bilah angin / sapuan (*weapon trail ribbon*) pada animasi ayunan/tusukan, renderer VFX membutuhkan dua titik acuan lokal pada tongkat:
1. **Titik Luar Trail (Outer Edge / Tip):**
   - Lokasi lokal: `[0.0, 30.0, 0.0]` (Ujung terluar tongkat pada `staff_upper_cap`)
2. **Titik Dalam Trail (Inner Edge / Base of Tip):**
   - Lokasi lokal: `[0.0, 21.5, 0.0]` (Batas genggaman depan / shaft atas) atau `[0.0, 29.0, 0.0]` (Pangkal cap ujung tongkat, untuk trail tipis terkonsentrasi).

---

### 6. Klarifikasi Bounding Box (AABB)
* Bounding box (AABB) Three.js yang dilaporkan pada audit sebelumnya adalah **indikator batas volume global** untuk membuktikan bahwa mesh batang tidak lagi melorot ke area kaki akibat translasi ganda.
* AABB **bukan bukti kontak permukaan mesh presisi** (*mesh-accurate contact*). Kontak genggaman sebenarnya dijamin oleh vektor jarak attachment pergelangan terhadap sumbu tongkat ($1.5000\,\text{u}$) dan pendekatan radius penampang di atas.

---

### 7. Pemetaan Alternatif Vanilla 6-Bone (Zero-Dependency PoC)

Bila Claude menguji satu pose ini pada `PlayerEntityModel` bawaan Minecraft tanpa library tambahan:
* `body` (torso): Yaw $= -25.0^\circ$, Pitch $= +5.0^\circ$
* `head`: Yaw $= +25.0^\circ$, Pitch $= -5.0^\circ$
* `rightArm` (vektor bahu $\to$ pergelangan):
  - $\vec{V}_{\text{kanan}} = [+0.867, -9.186, -0.738]$
  - Euler ekuivalen: Pitch $\approx +4.6^\circ$, Yaw $\approx -5.4^\circ$, Roll $\approx +5.4^\circ$
* `leftArm` (vektor bahu $\to$ pergelangan):
  - $\vec{V}_{\text{kiri}} = [+3.666, -8.159, -2.741]$
  - Euler ekuivalen: Pitch $\approx +17.0^\circ$, Yaw $\approx +24.1^\circ$, Roll $\approx -22.5^\circ$

---

### 8. Rencana Tahap Berikutnya
1. **Status:** Seluruh penyetelan pose siaga **dihentikan**; checkpoint dibekukan menunggu feedback runtime dari Claude.
2. **Koordinasi:** Menyepakati kontrak rig pemain bersama Claude.
3. **Fire Jab:** Setelah format runtime dipastikan, pekerjaan berlanjut ke animasi **Fire Jab** (*anticipation $\to$ strike $\to$ recovery*) mengikuti durasi dan kurva *tick* aktual dari `SkillTimeline`.
4. **Batasan:** Direktori `mod/` tidak dimodifikasi oleh Antigravity.
