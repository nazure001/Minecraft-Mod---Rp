# Art Source — Avatar Elements (Minecraft Java 1.21.1 Fabric)

Ruang kerja produksi visual (*authoring workspace*), studi teknis, dan bukti verifikasi aset untuk mod **Avatar: Elements**.

> [!IMPORTANT]
> Seluruh isi folder ini merupakan sumber kreasi dan arsip verifikasi, **bukan otomatis bagian dari runtime mod aktif**.
> Untuk integrasi ke dalam runtime mod atau resource pack, lihat panduan pemetaan resmi di **[CURATION_MANIFEST.md](CURATION_MANIFEST.md)** dan spesifikasi master di **[docs/vfx_texture_and_asset_master_spec.md](../docs/vfx_texture_and_asset_master_spec.md)**.

---

## 1. Struktur Folder & Taksonomi Kerja

| Folder / Berkas | Status Integritas | Deskripsi Isi & Peran Produksi |
| :--- | :--- | :--- |
| **`CURATION_MANIFEST.md`** | **Manifest Resmi** | Tabel pemetaan jalur berkas `art-source` ke target runtime `mod/src/main/resources/` dan `assets/minecraft/`. |
| **`asset_pack/`** | **Canonical Master** | Paket aset master terverifikasi: model Java `.json`, Bedrock `.geo.json`, proyek Blockbench `.bbmodel`, animasi rig PAL, dan atlas tekstur 64×64 cel-shaded. |
| **`asset_pack_t2_vfx/`** | **Canonical Master** | Paket master VFX T2 volumetrik: frame partikel PNG 16×16 (`fire_ember`, `air_gust_swirl`, `water_droplet`, dll.), JSON definisi partikel Fabric 1.21.1, ikon GUI skill 32×32, dan mob effect 18×18. |
| **`models/`** | **Staging Production** | Sumber model produksi dalam persiapan rilis:<br>• `models/air_staff/`: Model, tekstur, skrip render, dan berkas serah-terima Air Staff kanonikal.<br>• `models/avatar_skills/`: Builder Blender otomatis (`blender_avatar_skills_builder.py`) dan model 3D skill (`earth_boulder`, `water_whip`, `avatar_relic_3d`). |
| **`air_staff/`** | **Staging Glider** | Sumber model Blockbench sayap terbuka (`air_staff_glider.bbmodel`), tekstur kanvas, dan ekspor OBJ/MTL untuk mekanisme gliding Pengembara Udara. |
| **`animation_studies/`** | **Animation Study** | Studi rig pemain dan kombo gerak berbasis bela diri kanon ATLA:<br>• `fire_jab/`: Keyframe JSON, data blocking, storyboard, dan GIF animasi Fire Jab (*Northern Shaolin*).<br>• `staff_thrust/`: Studi gerak tusukan tongkat Pengembara Udara (*Air Staff Thrust*). |
| **`audio/`** | **Audio Spatial** | Aset efek suara spasial:<br>• `audio/candidates/`: Master audio uncompressed (WAV) dan Vorbis OGG mono.<br>• `audio/prototype/`: Audio prototipe terintegrasi. |
| **`ui/`** | **UI Concepts** | Mockup antarmuka pengguna kanonikal: `ui/concepts/Water Tribe UI Overlook.png` (layar HUD, skill tree, dan profil bergaya gulungan perkamen suku air). |
| **`tools/`** | **Tools & Audit** | Skrip verifikasi geometri (`verify_assets.py`) dan test-runner interaktif headless Blockbench (`tools/blockbench_interactive/`). |
| **`scratch_asset_expert/`** | **Scratchpad** | Area eksperimen sementara dan prototipe kode renderer (`FireJabRenderer.java`, `air_staff.png`). Bukan jalur runtime. |
| **`archive/`** | **Archive** | Paket cadangan ZIP historis (`avatar_elements_t2_vfx_assets.zip`, `src.rar`, dll.) serta catatan review lama. |

---

## 2. Aturan & Protokol Integrasi bagi Agent & Technical Artist

1. **Jalur Runtime Kanonis:**
   - Jalur runtime mod tetap strictly berada di: `mod/src/main/resources/` (common & data) dan `mod/src/client/resources/` (client rendering).
2. **Kesesuaian Target Minecraft 1.21.1:**
   - DILARANG menyalin sintaks atau komponen 1.21.2+ / 1.21.4+ (seperti `minecraft:equippable` atau `minecraft:item_model`).
   - Gunakan native component 1.21.1: `minecraft:custom_data`, `minecraft:custom_model_data`, `minecraft:trim`.
3. **Standar Model Blockbench:**
   - Titik putar pegangan (*grip pivot*) berada persis di `(0.0, 0.0, 0.0)`.
   - Koordinat Java Model setelah offset $+8.0$ unit WAJIB strictly di dalam batas `[-16.0, 32.0]`.
   - Sudut rotasi kubus dibatasi pada: `-45.0°`, `-22.5°`, `0.0°`, `+22.5°`, `+45.0°`.
4. **Standar Model Blender:**
   - Unit Metric Scale `1.0`.
   - Hirarki koleksi: `COL_Project` → `COL_Reference`, `COL_Blockout`, `COL_Geo`, `COL_Collision`, `COL_Export`.
   - Pertahankan modifier non-destruktif di `COL_Geo` dan lakukan apply transform sebelum ekspor.
5. **Standar Partikel Fabric Client:**
   - Class partikel client wajib meng-extend `SpriteBillboardParticle` dan memanggil `this.setSpriteForAge(this.spriteProvider)` di setiap `tick()`.
   - Alokasi budget partikel idle maksimal 2–5 partikel/detik per pemain untuk menjaga kestabilan TPS server.
