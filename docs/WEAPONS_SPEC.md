# ⚔️ Canonical Weapons 3D Blockbench Suite Specification & Handoff (Tahap 4 — ATLA/LOK)
> **Author:** Antigravity IDE (3D Technical Art Specialist)  
> **Consumer:** Claude Code / Runtime Agent & User (QA Reviewer)  
> **Target:** Minecraft Fabric 1.21.1 & Avatar Elements Resource Pack  
> **Status:** Production-Ready Asset Deliverables (Blockbench, Bedrock, Java JSON, OBJ/MTL, 64x64 Atlas, 360° Turntable Previews)

---

## 1. Landasan Literatur & Kanon Serial Avatar (*Weaponry in the World of Avatar*)

Seluruh model 3D senjata di Tahap 4 ini dirancang dan dimodelkan secara presisi berdasarkan kanon *Avatar: The Last Airbender* (ATLA) dan *The Legend of Korra* (LOK), mengacu pada dokumentasi resmi [Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar), `docs/armor_weapon_research_spec.md`, dan `docs/design/ASSET_INVENTORY.md`:

### 1.1 `SM_Dual_Swords` (Zuko Dao Broadswords / Shuang Dao)
- **Karakter Ikonik:** Pangeran Zuko (*The Blue Spirit*).
- **Fitur Visual Kanon:**
  - **Sepasang Pedang Lengkung Tunggal (*Twin Curved Dao*):** Dua pedang golok Tiongkok (*Shuang Dao*) bermata tunggal dengan kurva khas di bagian ujung (*flared belly*) dan ujung bilah terpotong (*clipped point*).
  - **Pelindung Tangan Setengah Lingkaran (*Asymmetric Brass Half-Guard*):** Dirancang dengan permukaan bagian dalam yang rata sehingga kedua pedang dapat disatukan secara sempurna ke dalam satu sarung.
  - **Gagang Kayu Berlilit Tali Merah (*Hardwood Handle & Crimson Cord Wrap*):** Pola lilitan berlian (*criss-cross diamond wrap*) khas prajurit Fire Nation dengan cincin pommel kuningan dan rumbai sutra merah (*red silk tassel*).
  - **Sarung Ganda Tunggal (*Twin Sheath Scabbard*):** Sarung kayu rosewood berpernis gelap dengan fitting kuningan bertatah (*locket throat* & *chape tip*) serta gelang suspensi untuk digendong di punggung atau pinggang.

### 1.2 `SM_Earth_Hammer` (Kyoshi Earthbender Warhammer / Palu Perang Batu Gow)
- **Karakter Ikonik:** Pasukan Tempur Kerajaan Bumi, Gow, dan Avatar Kyoshi.
- **Fitur Visual Kanon:**
  - **Kepala Mallet Monolit Batu Pahat (*Monolithic Carved Stone Mallet*):** Kepala palu godam raksasa dari batuan basal/loam gelap dengan pahatan faset beveled tahan benturan seismik.
  - **Sabuk Besi Tempa Penguat (*Reinforced Wrought-Iron Bands & Rivets*):** Tali-tali pelat besi melingkari monolit batu dengan paku keling (*rivets*) baja untuk mencegah batu retak saat menyalurkan *Earthbending Shockwave*.
  - **Gagang Kayu Panjang Berlapis Kulit (*Leather-Wrapped Hardwood Haft*):** Gagang kayu ash/oak tebal dengan lilitan kulit pelana cokelat berikat silang (*cross-lacing*) untuk genggaman dua tangan kokoh.
  - **Pemberat & Ujung Tembus Tanah (*Counterbalance & Iron Earth-Spike*):** Kerah besi bawah dengan paku piramidal runcing untuk menancapkan palu ke dalam tanah atau manuver *Ground Stomp*.
  - **Urat Giok Ba Sing Se (*Ba Sing Se Jade Seam*):** Urat kristal mineral giok hijau alami yang tertanam di faset batu.

### 1.3 `SM_War_Fan` (Kyoshi Warriors War Fan / Shanzi)
- **Karakter Ikonik:** Avatar Kyoshi, Suki, dan Prajurit Kyoshi (*Kyoshi Warriors*).
- **Fitur Visual Kanon:**
  - **Kipas Tempur Baja Lipat (*Japanese Tessen / Chinese Shanzi*):** Struktur kipas tempur yang memadukan keindahan tarian bela diri dengan daya mematikan bilah baja.
  - **Bilah Rusuk Luar Berketajaman Silet (*Sharpened Metallic Outer Razor Ribs / Oya-bone*):** Rusuk terluar berupa bilah baja tebal yang diasah tajam untuk menangkis (*Fan Parry*) dan memotong senjata lawan.
  - **Daun Sutra Hijau Zamrud & Trim Daun Emas (*Emerald Silk & Radiant Gold Leaf Trim*):** Membran kipas berlapis kain sutra hijau Kyoshi dengan lipatan berlipit (*faceted pleats*) dan lis emas imperial di sepanjang lengkungan atas.
  - **Poros Keling Kuningan (*Brass Kaname Pivot Pin*):** Engsel paku keling kuningan kuat di pangkal genggaman dengan simpul cincin, manik giok, dan rumbai sutra merah menjuntai.

### 1.4 `SM_Water_Spear` (Water Tribe Harpoon Spear / Tombak Harpun Suku Air)
- **Karakter Ikonik:** Hakoda, Bato, Sokka, dan Prajurit Suku Air Selatan/Utara.
- **Fitur Visual Kanon:**
  - **Mata Tombak Tulang Paus Kutub & Es Abadi (*Carved Bone / Glacial Ice Spearpoint*):** Mata tombak daun ganda dari tulang paus kutub dengan inti es padat gletser berwarna cyan-frost.
  - **Kait Harpun Ganda (*Dual Downward-Facing Barbed Toggles*):** Kait takik harpun khas Suku Air di bawah mata pisau untuk menembus dan mengunci armor lawan atau berburu di laut Arktik.
  - **Lilitan Tali Urat Otot Hewan (*Rawhide Sinew Socket Binding*):** Ikatan silang tali urat dan getah pinus arktik yang mengunci mata tombak pada leher tongkat kayu apung.
  - **Tongkat Kayu Apung Laut Lapuk (*Weathered Arctic Driftwood Shaft*):** Kayu apung abu-abu perak yang tahan air laut beku dengan lilitan kulit anjing laut biru nila (*indigo leather wrap*).
  - **Pangkal Sirip Ekor Ikan (*Carved Bone Fishtail Counterbalance*):** Penyeimbang ujung bawah berbentuk ekor ikan bertakik dengan taji tanah.

---

## 2. Standar Geometri, Pivot & Skala (Technical Standards)

Seluruh senjata mematuhi aturan standar arsitektur 3D mod:
1. **Skala Satuan Metrik:** $1	ext{ unit Blockbench} = \frac{1}{16}	ext{ meter} = 0.0625	ext{ m}$.
2. **Titik Pivot Genggaman Tangan (*Hand Grip Origin*):** Titik origin $(0.0, 0.0, 0.0)$ berada **persis di pusat pegangan tangan pemain** (*grip point*).
3. **Batas Koordinat Java Model:** Seluruh elemen kubus setelah ditranslasikan $+8.0$ unit pada model Java `.json` berada strictly di dalam batas $[-16.0, 32.0]$ tanpa clipping atau penolakan deserializer Minecraft.
4. **Sudut Rotasi Java Model:** Sudut rotasi pada model Java dibatasi pada sudut legal vanilla: $-45.0^\circ, -22.5^\circ, 0.0^\circ, +22.5^\circ, +45.0^\circ$.
5. **Dukungan Locator Trail & Emitter:** Setiap model dilengkapi locator kanonikal untuk integrasi `item_skins`:
   - `trail_begin`: Pangkal ayunan tebasan bilah.
   - `trail_end`: Ujung bilah terjauh (*weapon tip*).
   - `imbue_emitter`: Titik pusat emisi partikel elemen saat senjata dialiri bending (*Weapon Imbue*).

### Tabel Rentang Koordinat & Dimensi Senjata

| Aset ID | Panjang Total | Dimensi Geometri (Unit) | Rentang Y (Grip Pivot = 0) | Bounds Java (Offset +8) | Locator Trail End |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SM_Dual_Swords` | $1.94	ext{ m}$ (31 unit) | $7.4 	imes 33.0 	imes 7.7$ | $Y = -9.2 	o +23.8$ | $Y \in [-1.2, +31.8]$ | `[1.2, 23.8, -0.6]` |
| `SM_Earth_Hammer`| $2.34	ext{ m}$ (37.4 unit) | $13.6 	imes 37.4 	imes 8.2$ | $Y = -14.2 	o +23.2$ | $Y \in [-6.2, +31.2]$ | `[0.0, 23.2, 0.0]` |
| `SM_War_Fan`     | $1.37	ext{ m}$ (21.9 unit) | $20.0 	imes 21.9 	imes 1.6$ | $Y = -4.5 	o +17.4$ | $Y \in [+3.5, +25.4]$ | `[0.0, 17.4, 0.0]` |
| `SM_Water_Spear` | $2.41	ext{ m}$ (38.6 unit) | $5.0 	imes 38.6 	imes 2.2$ | $Y = -15.0 	o +23.6$ | $Y \in [-7.0, +31.6]$ | `[0.0, 23.6, 0.0]` |

---

## 3. Spesifikasi Tekstur Atlas 64x64 Cel-Shaded

Setiap senjata memiliki tekstur atlas 64×64 PNG unik dengan pembagian 4 kuadran UV terstruktur:

```
+--------------------------------+--------------------------------+
| Quadrant 0 [0..32, 0..32]      | Quadrant 1 [32..64, 0..32]     |
| Permukaan Utama Bilah / Batu /  | Fitting Logam, Guard Kuningan, |
| Tulang & Es Gletser            | Sabuk Besi, Trim Daun Emas     |
+--------------------------------+--------------------------------+
| Quadrant 2 [0..32, 32..64]     | Quadrant 3 [32..64, 32..64]    |
| Lilitan Gagang, Tali Kulit,    | Rumbai Sutra, Manik Giok,      |
| Kayu Apung / Ash Haft          | Sarung Rosewood, Pengait Tali  |
+--------------------------------+--------------------------------+
```

---

## 4. Matriks Berkas Deliverables (File Index)

Semua berkas telah diekspor dan diverifikasi secara otomatis melalui script `art-source/asset_pack/build_weapons_suite.py`:

### 4.1 Proyek Blockbench 4.10 (`.bbmodel`)
- `art-source/asset_pack/models/bbmodel/SM_Dual_Swords.bbmodel`
- `art-source/asset_pack/models/bbmodel/SM_Earth_Hammer.bbmodel`
- `art-source/asset_pack/models/bbmodel/SM_War_Fan.bbmodel`
- `art-source/asset_pack/models/bbmodel/SM_Water_Spear.bbmodel`
- Sub-folder weapons: `art-source/asset_pack/models/bbmodel/weapons/` (termasuk sinkronisasi file legacy `weapon_zuko_dual_dao.bbmodel`, `weapon_earth_war_hammer.bbmodel`, `weapon_kyoshi_war_fans.bbmodel`, `weapon_water_jaw_blade.bbmodel`).

### 4.2 Model Geometri Bedrock 1.12.0 (`.geo.json`)
- `art-source/asset_pack/models/SM_Dual_Swords.geo.json`
- `art-source/asset_pack/models/SM_Earth_Hammer.geo.json`
- `art-source/asset_pack/models/SM_War_Fan.geo.json`
- `art-source/asset_pack/models/SM_Water_Spear.geo.json`

### 4.3 Model Display Item Minecraft Java 1.21.1 (`.json`)
- `art-source/asset_pack/models/SM_Dual_Swords.json`
- `art-source/asset_pack/models/SM_Earth_Hammer.json`
- `art-source/asset_pack/models/SM_War_Fan.json`
- `art-source/asset_pack/models/SM_Water_Spear.json`
- Resource Pack Item Models: `art-source/asset_pack/assets/avatar_elements/models/item/` (tersedia dalam nama kanon `SM_*` dan alias legacy `weapon_*`).

### 4.4 Model Mesh Universal 3D (`.obj` & `.mtl`)
- `art-source/asset_pack/meshes/weapons/SM_Dual_Swords.obj` & `.mtl`
- `art-source/asset_pack/meshes/weapons/SM_Earth_Hammer.obj` & `.mtl`
- `art-source/asset_pack/meshes/weapons/SM_War_Fan.obj` & `.mtl`
- `art-source/asset_pack/meshes/weapons/SM_Water_Spear.obj` & `.mtl`
- Mirror di `art-source/asset_pack/meshes/vfx/` untuk kemudahan akses shader VFX.

### 4.5 Tekstur Atlas PNG 64x64
- `art-source/asset_pack/assets/avatar_elements/textures/weapons/` (`SM_Dual_Swords.png`, `SM_Earth_Hammer.png`, `SM_War_Fan.png`, `SM_Water_Spear.png`)
- Mirror di `textures/item/`, `textures/vfx/`, `models/`, dan `meshes/weapons/`.

### 4.6 Pratinjau Visual & Turntable GIF 360°
- `art-source/asset_pack/previews/SM_Dual_Swords/` (`SM_Dual_Swords_isometric.png`, `SM_Dual_Swords_turntable.gif`, `_front.png`, `_side.png`)
- `art-source/asset_pack/previews/SM_Earth_Hammer/` (`SM_Earth_Hammer_isometric.png`, `SM_Earth_Hammer_turntable.gif`, `_front.png`, `_side.png`)
- `art-source/asset_pack/previews/SM_War_Fan/` (`SM_War_Fan_isometric.png`, `SM_War_Fan_turntable.gif`, `_front.png`, `_side.png`)
- `art-source/asset_pack/previews/SM_Water_Spear/` (`SM_Water_Spear_isometric.png`, `SM_Water_Spear_turntable.gif`, `_front.png`, `_side.png`)
- Root preview mirror di `art-source/asset_pack/previews/`.

---

## 5. Panduan Integrasi Runtime (Untuk Claude Code / Runtime Agent)

1. **CustomModelData (CMD) Overrides:**
   - Gunakan predicate `minecraft:custom_model_data` pada item dasar Minecraft:
     * `SM_Dual_Swords` -> pada `iron_sword` atau `netherite_sword` (misal CMD `2001`)
     * `SM_Earth_Hammer` -> pada `mace` atau `iron_axe` (misal CMD `2002`)
     * `SM_War_Fan` -> pada `shield` atau `iron_sword` (misal CMD `2003`)
     * `SM_Water_Spear` -> pada `trident` atau `diamond_sword` (misal CMD `2004`)
2. **Definisi Swing Trail (`item_skins`):**
   - Senjata telah memiliki titik koordinat presisi `trail_begin` dan `trail_end`.
   - Konfigurasi `assets/avatar_elements/item_skins/` dapat langsung mengadopsi file tekstur trail `assets/avatar_elements/textures/vfx/trail_*_128x32.png` yang telah ada.
3. **Weapon Imbue VFX:**
   - Saat pemain memicu jurus kombo elemen (contoh: *Flame Sweep* untuk Dual Swords atau *Earth Stomp* untuk Warhammer), partikel bending dapat dispawn pada posisi locator `imbue_emitter`.
