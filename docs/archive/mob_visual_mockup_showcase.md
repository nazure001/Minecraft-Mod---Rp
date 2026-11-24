# Showcase Mockup 3D Kinematik Entitas (Avatar: Elements)

Dokumen ini memaparkan hasil perombakan total pasca-penerapan prinsip **ATM (Amati, Tiru, Modifikasi)** dari referensi kanonikal studio-grade (`avatar-legend-reforged-1.3.0` dan GeckoLib 1.12.0) guna mengeliminasi seluruh kesan kaku (*stiff box syndrome*) pada model entitas.

Tiga entitas perwakilan kategori telah berhasil dirombak penuh:
1. **Pet / Mount**: **Flying Bison (Sky Bison / Appa)** — 71 Tulang Bersendi & 8 Set Animasi
2. **Wild Creature / Mob**: **Platypus Bear (Beruang Berparuh)** — 21 Tulang Artikulasi & 3 Set Animasi
3. **Prime Boss**: **Phoenix King Ozai (Raja Api Ozai)** — 22 Tulang Biped Martial Arts & 3 Set Animasi

---

## 1. Mengapa Model Sekarang Luwes & Tidak Kaku?

| Parameter | Sebelum (Statis Kaku) | Sesudah (ATM Studio-Grade) | Dampak Visual di Dalam Game |
| :--- | :--- | :--- | :--- |
| **Hierarki Tulang** | 1 Tulang `root` kaku tunggal | **21 s/d 71 Tulang Bersarang** (*Parent-Child*) | Bagian tubuh dapat meliuk, menoleh, dan berayun secara independen. |
| **Pose Istirahat (*Resting Stance*)** | Kaki tegak lurus $90^\circ$ (kotak) | **Kuda-kuda Natural Berengsel** (Paha $12^\circ$, betis $-10^\circ$) | Mob berdiri dengan bobot gravitasi realistis, bukan seperti patung museum. |
| **Kelengkungan Organik** | Balok patah siku-siku | **Rantai Bersambung Bertingkat** (Tanduk 5 segmen, ekor 6 segmen) | Tanduk melengkung aerodinamis dan ekor beaver mendayung luwes. |
| **Kain & Jubah** | Badan balok datar | **Flowing Robe Skirt Quad-Layer** (sudut luar $10^\circ$) | Jubah kaisar berkibar saat melangkah atau menembakkan api. |
| **Resolusi Tekstur** | $128 \times 128$ (Piksel besar) | **$256 \times 256$ s/d $512 \times 512$** Pixel Art Halus | Serat bulu shaggy, sisik leathery ekor, dan sulaman emas naga tampak tajam. |
| **Pustaka Animasi** | 0 Animasi | **Siklus Keyframe GeckoLib 1.8.0** | Idle napas dada, langkah berbobot (*weight shift*), dan ayunan ekor inersia. |

---

## 2. Galeri Render 3D Mockup Isometrik Kinematik

### A. Kategori Pet / Mount: Flying Bison (Appa / Sky Bison)
- **Status Rig:** **71 Articulated Bones** (Diadopsi langsung dari referensi studio)
- **Fitur Kinematika:**
  - Torso fleksibel 3 segmen (`hump` $\to$ `body_segment` $\to$ `body_segment2`).
  - Tanduk melengkung mulus 5 segmen bertingkat (`right_horn` s/d `right_horn5` dengan rotasi inkremental $22.5^\circ$).
  - 6 Kaki berotot 3 sendi (paha, betis, telapak, dan 3 jari cakar independen).
  - Rantai ekor dayung beaver 6 segmen yang lentur melambai.
- **Pustaka Animasi:** 8 Animasi (`walk`, `idle` napas dada, `roar`, `jump_slam`, `hover`, `flying` mendayung, `land`, `liftoff`).
- **Tekstur:** $512 \times 512$ Atlas Kanonikal berbulu shaggy cream dengan tanda panah chevron cokelat.

Berkas Mockup: [mockup_flying_bison.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/art-source/showcase/mockup_flying_bison.png)

---

### B. Kategori Wild Creature / Mob: Platypus Bear
- **Status Rig:** **21 Articulated Bones** (Kombinasi quadruped beruang + paruh bebek leathery + ekor pipih bersisik)
- **Fitur Kinematika:**
  - Punggung bungkuk berotot dengan mantel bulu pundak lebat berlapis (`inflate: 0.5`).
  - Moncong paruh bebek platypus leathery teal-olive dengan rahang bawah (`jaw`) terpisah yang dapat membuka $35^\circ$ saat mengaum.
  - 4 Kaki bertapak lebar dengan cakar penggali tajam gading (`claws`).
  - Ekor platypus pipih 3 segmen fleksibel (`tail_base` $\to$ `tail_mid` $\to$ `tail_tip`) untuk efek hempasan tanah (*earth slam*).
- **Pustaka Animasi:** 3 Animasi (`idle` goyang ekor dan napas, `walk` langkah beruang berat, `slam_attack` berdiri dua kaki lalu menghantam tanah).
- **Tekstur:** $256 \times 256$ Grizzly fur texturing + sisik crosshatch ekor platypus.

Berkas Mockup: [mockup_platypus_bear.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/art-source/showcase/mockup_platypus_bear.png)

---

### C. Kategori Prime Boss: Phoenix King Ozai (Raja Api Ozai)
- **Status Rig:** **22 Articulated Bones** (Biped humanoid dengan kuda-kuda bela diri Agni Kai)
- **Fitur Kinematika:**
  - Tulang belakang melengkung atletis (`chest` condong ke depan $-3^\circ$ dalam kuda-kuda siaga).
  - Jubah sutra kaisar terbagi 4 panel (`robe_skirt_front`, `back`, `left`, `right`) yang mekar $10^\circ$ keluar dan bergerak mengikuti inersia langkah kaki.
  - Pauldron pundak emas runcing bertingkat terpasang independen di bahu kiri dan kanan.
  - Lengan 2 sendi dengan gelang bracer emas pemancar api chi di pergelangan tangan.
  - Mahkota api topknot trisula emas di atas sanggul kepala.
- **Pustaka Animasi:** 3 Animasi (`idle` thermal updraft jubah, `walk` langkah anggun intimidatif, `lightning_strike` putaran chi dua jari).
- **Tekstur & Emissive:** $256 \times 256$ Sutra scarlet bordir naga emas + [phoenix_king_ozai_glow.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/textures/entity/boss/phoenix_king_ozai_glow.png) untuk mata amber chi menyala di malam hari.

Berkas Mockup: [mockup_phoenix_king_ozai.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/art-source/showcase/mockup_phoenix_king_ozai.png)

---

## 3. Berkas Runtime yang Telah Diterapkan

Seluruh model dan animasi telah aktif di dalam pohon aset runtime mod:

1. **Geometri Model (`.geo.json`):**
   - [flying_bison.geo.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/models/entity/flying_bison.geo.json) (71 tulang)
   - [platypus_bear.geo.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/models/entity/platypus_bear.geo.json) (21 tulang)
   - [phoenix_king_ozai.geo.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/models/entity/phoenix_king_ozai.geo.json) (22 tulang)

2. **Animasi GeckoLib (`.animation.json`):**
   - [flying_bison.animation.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/animations/entity/flying_bison.animation.json) (8 animasi)
   - [platypus_bear.animation.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/animations/entity/platypus_bear.animation.json) (3 animasi)
   - [phoenix_king_ozai.animation.json](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/animations/entity/phoenix_king_ozai.animation.json) (3 animasi)

3. **Tekstur Resolusi Tinggi:**
   - [flying_bison.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/textures/entity/pet/flying_bison.png) ($512 \times 512$)
   - [platypus_bear.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/textures/entity/mobs/platypus_bear.png) ($256 \times 256$)
   - [phoenix_king_ozai.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/textures/entity/boss/phoenix_king_ozai.png) ($256 \times 256$)
   - [phoenix_king_ozai_glow.png](file:///d:/repo/Minecraft%20Mod%20&%20Rp/mod/src/main/resources/assets/avatar_elements/textures/entity/boss/phoenix_king_ozai_glow.png) ($256 \times 256$)
