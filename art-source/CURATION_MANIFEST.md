# Manifest & Peta Kurasi Aset `art-source` (Avatar Elements)
**Target Platform:** Minecraft Java Edition 1.21.1 (Fabric Loader & Resource Pack)  
**Dokumen Pendamping:** [vfx_texture_and_asset_master_spec.md](file:///d:/repo/Minecraft%20Mod%20&%20Rp/docs/vfx_texture_and_asset_master_spec.md) | [minecraft-vfx-particle-authoring SKILL](file:///d:/repo/Minecraft%20Mod%20&%20Rp/docs/skills/minecraft-vfx-particle-authoring/SKILL.md) | [WEAPONS_SPEC.md](file:///d:/repo/Minecraft%20Mod%20&%20Rp/docs/WEAPONS_SPEC.md) | [ASSET_PRODUCTION_SPEC.md](file:///d:/repo/Minecraft%20Mod%20&%20Rp/docs/ASSET_PRODUCTION_SPEC.md)

---

## 1. Ikhtisar & Taksonomi Folder `art-source`

Folder `art-source` adalah repositori sumber produksi (*authoring workspace*) dan arsip verifikasi visual. Seluruh file di sini dikategorikan ke dalam 7 status integritas:

| Kategori Status | Folder Terkait | Deskripsi & Aturan Penggunaan |
| :--- | :--- | :--- |
| **CANONICAL MASTER** | `asset_pack/`, `asset_pack_t2_vfx/` | Aset yang telah terverifikasi penuh (52/52 structural checks), siap disalin langsung ke runtime mod. |
| **STAGING PRODUCTION**| `models/` | Model Blockbench/Blender yang sedang disiapkan untuk rilis tahapan berikutnya (`air_staff`, `avatar_skills`). |
| **ANIMATION STUDY** | `animation_studies/` | Studi rig, data blocking pose, storyboard, dan keyframe kombo (`fire_jab`, `staff_thrust`). |
| **AUDIO CANDIDATE** | `audio/` | File audio mentah WAV dan hasil konversi Mono OGG 44.1 kHz siap registrasi `sounds.json`. |
| **UI CONCEPTS** | `ui/concepts/` | Mockup antarmuka pengguna yang telah disetujui (`Water Tribe UI Overlook.png`). |
| **TOOLS & AUDIT** | `tools/` | Script headless audit otomatis, screenshot runner Blockbench, dan validasi geometri. |
| **ENTITY STAGING** | `Avatar_Elements_Missing_Assets_Staging/` | Tekstur entity (boss, mob, armor) untuk konten masa depan. Belum diintegrasikan ke mod. |
| **UI ASSETS** | `avatar_elements_assets/` | Badge elemen, ikon skill, partikel trail, GUI frame — aset UI unik belum ada di canonical. |
| **ARCHIVE** | `archive/` | Paket cadangan ZIP historis, arsip review lama, prototipe yang sudah diekstrak (`complete_aaa_suite`, `scratch_asset_expert`, `showcase`, `vfx_prototypes`, `old_versions`). |

---

## 2. Tabel Pemetaan Kurasi: `art-source` → Runtime Mod (`mod/` & Datapack)

Tabel ini digunakan oleh **Coding Agent (Claude Code / Fabric Dev)** untuk mengintegrasikan berkas ke dalam mod runtime:

### 2.1 Model & Tekstur Senjata Kanonikal (Canonical Weapons)

| Sumber di `art-source/` | Target Runtime Mod (`mod/src/main/resources/`) | Target Resource Pack (`assets/minecraft/models/item/`) | Keterangan & Hook Kode |
| :--- | :--- | :--- | :--- |
| `asset_pack/models/SM_Dual_Swords.json`<br>`asset_pack/models/SM_Dual_Swords.png` | `assets/avatar_elements/models/item/dual_swords.json`<br>`assets/avatar_elements/textures/item/dual_swords.png` | Registrasi override CMD pada `iron_sword.json` / `diamond_sword.json` | Register di `AvatarItems.java`: `DUAL_SWORDS = register("dual_swords", ...)` |
| `asset_pack/models/SM_Earth_Hammer.json`<br>`asset_pack/models/SM_Earth_Hammer.png` | `assets/avatar_elements/models/item/earth_hammer.json`<br>`assets/avatar_elements/textures/item/earth_hammer.png` | Override CMD pada `iron_axe.json` / `mace.json` | Register di `AvatarItems.java`: `EARTH_HAMMER = register("earth_hammer", ...)` |
| `asset_pack/models/SM_War_Fan.json`<br>`asset_pack/models/SM_War_Fan.png` | `assets/avatar_elements/models/item/war_fan.json`<br>`assets/avatar_elements/textures/item/war_fan.png` | Override CMD pada `shield.json` / `iron_sword.json` | Register di `AvatarItems.java`: `WAR_FAN = register("war_fan", ...)` |
| `asset_pack/models/SM_Water_Spear.json`<br>`asset_pack/models/SM_Water_Spear.png` | `assets/avatar_elements/models/item/water_spear.json`<br>`assets/avatar_elements/textures/item/water_spear.png` | Override CMD pada `trident.json` | Register di `AvatarItems.java`: `WATER_SPEAR = register("water_spear", ...)` |
| `models/air_staff/air_staff.json`<br>`models/air_staff/air_staff.png` | `assets/avatar_elements/models/item/air_staff.json`<br>`assets/avatar_elements/textures/item/air_staff.png` | Override CMD pada `stick.json` / `iron_sword.json` | Terdaftar aktif di `AvatarItems.AIR_STAFF` |

### 2.2 Model 3D Skill & Konstruksi Dunia (World Constructs)

| Sumber di `art-source/` | Target Runtime Mod (`mod/src/main/resources/`) | Tipe Renderer Java |
| :--- | :--- | :--- |
| `asset_pack/models/earth_pillar.geo.json`<br>`asset_pack/models/earth_pillar.png` | `assets/avatar_elements/geo/earth_pillar.geo.json`<br>`assets/avatar_elements/textures/entity/earth_pillar.png` | BlockEntityRenderer / GeoEntityRenderer |
| `asset_pack/models/boulder_launch_megalith.geo.json`<br>`asset_pack/models/boulder_launch_megalith.png` | `assets/avatar_elements/geo/boulder_megalith.geo.json`<br>`assets/avatar_elements/textures/entity/boulder_megalith.png` | Flying Projectile Entity Renderer |
| `asset_pack/models/air_vortex_funnel.geo.json`<br>`asset_pack/models/air_vortex_funnel.png` | `assets/avatar_elements/geo/air_vortex.geo.json`<br>`assets/avatar_elements/textures/entity/air_vortex.png` | WorldRenderEvents Volumetric Translucent Mesh |
| `asset_pack/models/charge_orb_elemental.geo.json`<br>`asset_pack/models/charge_orb_elemental.png` | `assets/avatar_elements/geo/charge_orb.geo.json`<br>`assets/avatar_elements/textures/entity/charge_orb.png` | Player Hand Attachment Viewmodel Renderer |
| `asset_pack/models/water_whip_stream.geo.json`<br>`asset_pack/models/water_whip_stream.png` | `assets/avatar_elements/geo/water_whip.geo.json`<br>`assets/avatar_elements/textures/entity/water_whip.png` | Bezier Spline Tube Renderer |

### 2.3 Partikel & Sprite Provider (Fabric 1.21.1)

| Sumber di `art-source/` | Target Runtime Mod (`mod/src/main/resources/`) | Pendaftaran Kode Java |
| :--- | :--- | :--- |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/fire_ember.json`<br>`textures/particle/fire_ember_*.png` (0..3) | `assets/avatar_elements/particles/fire_ember.json`<br>`assets/avatar_elements/textures/particle/fire_ember_*.png` | `AvatarParticles.FIRE_EMBER`<br>Factory: `FireEmberParticle.Factory` |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/fire_arc_slash.json`<br>`textures/particle/fire_arc_slash_*.png` (0..3) | `assets/avatar_elements/particles/fire_arc_slash.json`<br>`assets/avatar_elements/textures/particle/fire_arc_slash_*.png` | `AvatarParticles.FIRE_ARC_SLASH`<br>Factory: `FireArcSlashParticle.Factory` |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/air_gust_swirl.json`<br>`textures/particle/air_gust_swirl_*.png` (0..3) | `assets/avatar_elements/particles/air_gust_swirl.json`<br>`assets/avatar_elements/textures/particle/air_gust_swirl_*.png` | `AvatarParticles.AIR_GUST_SWIRL`<br>Factory: `AirGustSwirlParticle.Factory` |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/air_ring.json`<br>`textures/particle/air_ring_*.png` (0..2) | `assets/avatar_elements/particles/air_ring.json`<br>`assets/avatar_elements/textures/particle/air_ring_*.png` | `AvatarParticles.AIR_RING`<br>Factory: `AirRingParticle.Factory` |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/water_droplet.json`<br>`textures/particle/water_droplet_*.png` (0..3) | `assets/avatar_elements/particles/water_droplet.json`<br>`assets/avatar_elements/textures/particle/water_droplet_*.png` | `AvatarParticles.WATER_DROPLET`<br>Factory: `WaterDropletParticle.Factory` |
| `asset_pack_t2_vfx/assets/avatar_elements/particles/earth_chunk.json`<br>`textures/particle/earth_chunk_*.png` (0..2) | `assets/avatar_elements/particles/earth_chunk.json`<br>`assets/avatar_elements/textures/particle/earth_chunk_*.png` | `AvatarParticles.EARTH_CHUNK`<br>Factory: `EarthChunkParticle.Factory` |

### 2.4 Tekstur GUI Skill Icon & Mob Effect

| Sumber di `art-source/` | Target Runtime Mod (`mod/src/main/resources/`) | Pemakaian di HUD / Menu |
| :--- | :--- | :--- |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/fire_jab.png` | `assets/avatar_elements/textures/gui/skills/fire_jab.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/flame_sweep.png` | `assets/avatar_elements/textures/gui/skills/flame_sweep.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/fire_jet.png` | `assets/avatar_elements/textures/gui/skills/fire_jet.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/fire_guard.png` | `assets/avatar_elements/textures/gui/skills/fire_guard.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/air_palm.png` | `assets/avatar_elements/textures/gui/skills/air_palm.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/gui/skills/air_blast.png` | `assets/avatar_elements/textures/gui/skills/air_blast.png` | HUD Skill Slot & Skill Tree |
| `asset_pack_t2_vfx/assets/avatar_elements/textures/mob_effect/*.png` | `assets/avatar_elements/textures/mob_effect/*.png` | Status Effect Vanilla Overlay |

### 2.5 Entitas Bestiary (42 Mobs, Pets, Roaming Sub-Bosses & Prime Bosses)

| Model Sumber (Blockbench `.bbmodel`) | Target Runtime Mod (`mod/src/main/resources/`) | Tipe Registrasi Entity Fabric |
| :--- | :--- | :--- |
| `asset_pack/models/bbmodel/entity/flying_bison.bbmodel` | `geo/flying_bison.geo.json`<br>`textures/entity/flying_bison.png` | `EntityType.Builder.create(FlyingBisonEntity::new, SpawnGroup.CREATURE)` |
| `asset_pack/models/bbmodel/entity/winged_lemur.bbmodel` | `geo/winged_lemur.geo.json`<br>`textures/entity/winged_lemur.png` | `EntityType.Builder.create(WingedLemurEntity::new, SpawnGroup.CREATURE)` |
| `asset_pack/models/bbmodel/entity/polar_bear_dog.bbmodel`| `geo/polar_bear_dog.geo.json`<br>`textures/entity/polar_bear_dog.png`| `EntityType.Builder.create(PolarBearDogEntity::new, SpawnGroup.CREATURE)` |
| `asset_pack/models/bbmodel/entity/shirshu.bbmodel` | `geo/shirshu.geo.json`<br>`textures/entity/shirshu.png` | `EntityType.Builder.create(ShirshuEntity::new, SpawnGroup.MONSTER)` |
| `asset_pack/models/bbmodel/entity/phoenix_king_ozai.bbmodel`| `geo/phoenix_king_ozai.geo.json`<br>`textures/entity/boss/ozai.png` + `_glow.png` | `EntityType.Builder.create(PhoenixKingOzaiEntity::new, SpawnGroup.MONSTER)` |
| `asset_pack/models/bbmodel/entity/vaatu_spirit.bbmodel` | `geo/vaatu.geo.json`<br>`textures/entity/boss/vaatu.png` + `_glow.png` | `EntityType.Builder.create(VaatuSpiritBossEntity::new, SpawnGroup.MONSTER)` |

### 2.6 Antarmuka GUI RPG Skill Tree & Atribut `[K]`

| Aset Konsep di `ui/` | Target Runtime Mod (`mod/src/main/resources/`) | Komponen Screen Java |
| :--- | :--- | :--- |
| `ui/concepts/Water Tribe UI Overlook.png`<br>`ui/parchment_scroll_frame.png` | `assets/avatar_elements/textures/gui/skill_tree/parchment.png` | `SkillTreeScreen.java` (Screen kustom dengan 9-slice scroll background) |
| `ui/attribute_icons/*.png` (Agility, Chi, Vigor, Mastery, Precision) | `assets/avatar_elements/textures/gui/attributes/*.png` | Widget tombol plus (+) dan progress bar atribut di layar `[K]` |

---

## 3. Panduan untuk Blockbench Modeler

1. **Format Proyek:** Selalu simpan file kerja di folder `.bbmodel` (`art-source/asset_pack/models/bbmodel/` atau `art-source/models/`).
2. **Grip Pivot Alignment:**
   - Letakkan origin $(0.0, 0.0, 0.0)$ tepat di pusat pegangan tangan pemain (*handle grip contact*).
   - Pastikan sumbu $Y$ positif mengarah ke bilah atas, sumbu $Z$ mengarah ke depan bilah potong.
3. **Ekspor Java Model (`.json`):**
   - Periksa bahwa setelah offset $+8.0$, batas koordinat kubus tidak melebihi $[-16.0, 32.0]$.
   - Pastikan sudut rotasi elemen kubus hanya memakai: $-45^\circ, -22.5^\circ, 0.0^\circ, +22.5^\circ, +45^\circ$.
4. **Locators (Grup Empty):**
   - Sertakan locator `trail_begin` (pangkal tebasan), `trail_end` (ujung bilah), dan `imbue_emitter` (titik pusat alirah chi).

---

## 4. Panduan untuk Blender Technical Artist

1. **Unit & Skala:** Gunakan Metric System dengan Unit Scale `1.0` (1 Blender meter = 1 Minecraft block = 16 Blockbench units).
2. **Prinsip Non-Destruktif:**
   - Pertahankan modifier (Mirror, Solidify, Bevel, Subsurf) tetap aktif di dalam koleksi `COL_Geo`.
   - Lakukan apply transform (`Ctrl+A` Scale & Rotation) sebelum melakukan UV Unwrap.
3. **Koleksi Wajib:**
   - `COL_Project` → `COL_Reference`, `COL_Blockout`, `COL_Geo`, `COL_Collision`, `COL_Export`.
4. **Pengepakan UV Atlas:**
   - Gunakan resolusi 64×64 atau 128×128 pixel art tanpa interpolasi (*Nearest Neighbor filtering*).
   - Patuhi kuadran UV (Quadrant 0: Bilah/Badan, Quadrant 1: Fitting/Guard, Quadrant 2: Gagang/Tali, Quadrant 3: Ornamen/Rumbai).
