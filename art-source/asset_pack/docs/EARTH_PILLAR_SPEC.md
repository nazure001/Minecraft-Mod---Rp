# 🪨 Earth Pillar 3D Asset Specification & Handoff (Canon v2 — ATLA/LOK)
> **Author:** Antigravity IDE (3D Technical Art Lead)  
> **Consumer:** Claude Code (Runtime Implementer) & User (QA Reviewer)  
> **Target:** Minecraft Fabric 1.21.1 (Client-only VFX Earth Column)  
> **Status:** QA 2026-11-18 - geometri sumber terukur 2.5 blok di atas tanah; tinggi Java runtime belum cocok, cleanup lifecycle packet posisi sudah dibenahi, dan uji visual dalam game masih pending.
> **QA note:** Preview isometrik masih berlabel 42 unit/2.63 m dan tidak menunjukkan detail atlas dengan jelas; preview tersebut bukan bukti render runtime.

---

## 1. Literatur & Landasan Serial Avatar (Canon References)

Model 3D Earth Pillar ini dikalibrasi secara ketat berdasarkan visual art dan koreografi kanonikal seri *Avatar: The Last Airbender* dan *The Legend of Korra*:

1. **Prinsip Bela Diri Hung Gar (洪家) & Koreografi Sifu Kisu:**
   * Di serial animasinya, *Earth Column* dipicu oleh entakan kaki kuda-kuda kokoh (*Ma Bu*) atau pukulan tinju ke atas (*rising fist thrust*).
   * Kolom bumi tidak muncul perlahan, melainkan **meletus dengan akselerasi kinetik eksplosif** dalam hitungan 2–3 frame (0.08–0.12 detik), melontarkan target atau caster ke udara (*catapult launcher*).
2. **Karakteristik Geologis Karst & Tambang Kerajaan Bumi:**
   * Terinspirasi langsung dari formasi karst Guilin dan benteng Omashu/Ba Sing Se.
   * Bukan batu bulat acak, melainkan **monolit batu pahat persegi/oktagonal kokoh** dengan bidang sesar (*fault shears*) vertikal dan lapisan batuan sedimen (*sedimentary rock strata*) horizontal.
3. **Piston Launch Head (Kepala Piston Pelontar):**
   * Sesuai kode `EarthPillarSkill.java` (`LAUNCH_VELOCITY = 1.05f (~4-5 block hop)`), fungsi gameplay pilar adalah **melontarkan entitas ke atas**.
   * Di kanon serial, pilar pelontar memiliki kepala atas yang **datar dan kokoh bersudut beveled** (bukan jarum lancip yang tidak masuk akal untuk dipijak), bertindak sebagai bantalan hidrolik kinetik alami tanah.
4. **Impact Collar (Kerah Patahan Tanah Merekah):**
   * Saat pilar menembus permukaan tanah, tanah di sekelilingnya terdesak dan mencuat membentuk kerah serpihan batuan miring ($25^\circ$).
5. **Palet Warna & Kristal Giok Ba Sing Se:**
   * Menggunakan palet cel-shading hangat Kerajaan Bumi: batu pasir ochre Omashu, granit abu-abu sejuk, lempung tanah liat, dan urat mineral kristal giok (*jade*) khas katakombe Ba Sing Se / Lake Laogai.

---

## 2. Asset Deliverables & File Locations

| Komponen | Lokasi Berkas | Format / Spesifikasi |
| :--- | :--- | :--- |
| **Proyek Blockbench** | `art-source/asset_pack/models/bbmodel/earth_pillar.bbmodel` | Blockbench 4.10, hierarchy 4 grup (`foundation`, `column_lower`, `column_mid`, `launch_head`), UV terpeta, tekstur & animasi erupsi embedded. |
| **Universal 3D Mesh** | `art-source/asset_pack/meshes/vfx/earth_pillar.obj` | Skala 1.0 (1.0 = 1 meter), origin di titik kontak tanah (0, 0, 0); rentang total 2.75 m, dengan 2.5 m di atas tanah. |
| **Material Library** | `art-source/asset_pack/meshes/vfx/earth_pillar.mtl` | Menghubungkan tekstur atlas `earth_pillar.png`. |
| **Bedrock Geometry** | `art-source/asset_pack/models/earth_pillar.geo.json` | Standar Bedrock 1.12.0 (`geometry.earth_pillar`). |
| **Java Display Model** | `art-source/asset_pack/models/earth_pillar.json` | Format item/block display entity vanilla Fabric 1.21.1. |
| **Tekstur Atlas 64x64** | `art-source/asset_pack/assets/avatar_elements/textures/vfx/earth_pillar.png` | 4 kuadran: Karst Strata, Rupture Slabs, Launch Piston Cap, dan Urat Giok Ba Sing Se. |
| **Animasi Erupsi** | `art-source/asset_pack/animations/earth_pillar.animation.json` | Timeline 1.25s: Bawah tanah $ightarrow$ burst catapult overshoot $ightarrow$ ground slam lock $ightarrow$ held stance $ightarrow$ shatter & sink. |
| **Pratinjau Multi-Sudut** | `art-source/asset_pack/previews/earth_pillar/` | `earth_pillar_isometric.png`, `earth_pillar_front.png`, `earth_pillar_top.png`, dan `earth_pillar_turntable.gif`. |

---

## 3. Spesifikasi Geometri & Koordinat

* **Ground Pivot Contact Point:** Origin $(0.0, 0.0, 0.0)$ berada **persis di permukaan kontak tanah**.
* **Tinggi target kolom:** Y=0 sampai Y=40 unit (2.5 blok), sesuai `PILLAR_HEIGHT = 2.5f`. BBModel/Bedrock/OBJ mencapai target ini. Java display model mencapai Y=32 (2.0 blok) pada skala 1.0; runtime memakai base scale 1.0 dan skala Y 1.25 sehingga tinggi efektifnya 2.5 blok.
* **Ukuran Launch Platform:** Platform atas selebar $11	imes 11	ext{ unit}$ ($0.69	ext{m} 	imes 0.69	ext{m}$) dengan landasan sentral $6	imes 6	ext{ unit}$ ($0.38	ext{m}$), sempurna untuk menyangga kaki pemain saat terangkat.
* **Radius Footprint:** Radius radial maksimum serpihan dasar adalah $0.81	ext{ meter}$, berada aman di dalam radius damage skill `FOOTPRINT_RADIUS = 1.6f`.
* **Anti-Clipping Subterranean Root:** Masuk sedalam $0.25	ext{ m}$ ($Y = -4.0$ unit) ke bawah tanah agar tidak bolong saat meletus di tanjakan/lereng.

```
       ▲  Y = +2.50m (40 units)    -- Center Strike Anvil & Piston Launch Cap
       │
       │  Y = +2.31m (37 units)    -- Cornice Bevel Transition Ring
       │
       │  Y = +1.94m (31 units)    -- Upper Monolith & Architectural Belt
       │
       │  Y = +1.06m (17 units)    -- Mid Column + Ba Sing Se Jade Strata Seam
       │
       │  Y = +0.19m ( 3 units)    -- Basal Collar & 4 Flared Rupture Slabs
───────┼────────────────────────── Ground Level (Y = 0.0, Ground Pivot Contact)
       ▼  Y = -0.25m (-4 units)   -- Subterranean Anchor (Anti-Clipping)
```

---

> **Pengukuran QA 2026-11-18:** BBModel/Bedrock membentang Y=-4..40 unit dan OBJ Y=-0.25..2.5 m. Java model membentang Y=-12..32 unit; puncaknya 2.0 blok pada skala 1.0. Client menerapkan base scale 1.0 dan skala Y 1.25, menghasilkan tinggi efektif 2.5 blok. Validator statis memeriksa rantai transform ini dan lulus 7/7; penerimaan visual, posisi, dan multiplayer tetap memerlukan uji dalam game.

## 4. Rekomendasi Integrasi Client-Side (Untuk Claude Code)

1. **Client-Only Display (Tanpa World Mutation):**
   * Spawn entity visual saat server mengumumkan skill `ACTIVE` pada koordinat `Vec3d center`.
2. **Animasi & Fase Kinetik:**
   * $0.00	ext{s} ightarrow 0.12	ext{s}$: Erupsi eksplosif dari $Y = -2.75$ ke $+0.15$ (overshoot pelontaran).
   * $0.12	ext{s} ightarrow 0.18	ext{s}$: Settle kembali ke $Y = 0.0$ dengan partikel debu `minecraft:block` dan suara benturan batu.
   * $0.18	ext{s} ightarrow 0.75	ext{s}$: Diam mengunci posisi di $Y = 0.0$.
   * $0.75	ext{s} ightarrow 1.15	ext{s}$: Merekah dan amblas kembali ke dalam tanah lalu despawn.
