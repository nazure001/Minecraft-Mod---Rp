# ARMOR_WEAPON_RESEARCH_SPEC — Riset Armor & Senjata Kanon Avatar + Analisis Mod/Custom Equipment

Tanggal: 2026-11-09

Target: Minecraft Java 1.21.1 (Fabric)

Status: **Dokumen Riset & Arsitektur Desain untuk Diskusi Sebelum Produksi Aset**

## 1. Katalog Lengkap Senjata & Armor Kanon (*Avatar: The Last Airbender* & *The Legend of Korra*)

Berdasarkan dokumentasi kanon [Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar) dan [Fashion in the World of Avatar](https://avatar.fandom.com/wiki/Fashion_in_the_World_of_Avatar), perlengkapan tempur di dunia Avatar terbagi menjadi **senjata penyalur elemen (*Weapon-Enhanced Bending*)**, **senjata khusus Nonbender**, dan **armor faksi/militer**.

### 1.1 Tabel Armor Kanon per Faksi / Elemen

| Faksi / Elemen | Nama Armor Kanon | Ciri Visual & Material Kanon | Fungsi / Efek Sinergi Gameplay (`CONTENT_SPEC.md` & Kanon) | 
| ----- | ----- | ----- | ----- | 
| **Water Tribe** ([Southern Water Tribe](https://avatar.fandom.com/wiki/Southern_Water_Tribe)) | **Wolf Armor (Armor Serigala)** | Helm kepala serigala kutub putih-abu, mantel kulit berlapis tulang, pelindung lengan (*bracers*) & tulang kering (*greaves*) biru-putih ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | +10% efisiensi pertahanan air, regenerasi chi saat hujan/air, resistansi dingin/es | 
| **Water Tribe** ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | **Hexagonal Notched Shield** | Perisai heksagonal biru berbingkai tulang putih berbentuk bumerang dengan takik samping untuk tombak | Pertahanan arah depan sambil tetap bisa menusukkan tombak | 
| **Earth Kingdom** ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | **Earthbender Military Armor & Conical Hat** | Lapisan pelindung hijau-emas-cokelat, topi kerucut lebar berujung runcing (melindungi dari semburan api), **tanpa alas kaki (bertelanjang kaki)** untuk menjaga kontak *Seismic Sense* | +20% resistansi *knockback*, bonus *guard*, mengaktifkan pasif *Seismic Sense* di tanah | 
| **Earth Kingdom** ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | **Beifong Academy Chainmail** | Jubah rantai pelat logam kecil fleksibel di balik pakaian (dirancang Sokka & murid akademi Toph) | Kekebalan/resistansi terhadap serangan *Chi-Blocking* jarak dekat | 
| **Earth Kingdom / Kyoshi** ([War Fans](https://avatar.fandom.com/wiki/War_fans)) | **Kyoshi Warrior Armored Kimono & Wrist-Shield** | Kimono hijau tua berlapis pelat logam bahu/dada, riasan wajah kabuki, dan perisai bundar lipat di lengan bawah | Membuka jurus *Shield Wall* (perisai lipat tahan api) & *Counter Parry* | 
| **Earth / Metal Clan** ([Metal Clan](https://avatar.fandom.com/wiki/Metal_Clan), [Earth Empire](https://avatar.fandom.com/wiki/Earth_Empire)) | **Zaofu / Kuvira Metal Strip Armor** | Pelat logam perak-baja minimalis dengan bilah-bilah logam di bahu/lengan yang siap dilontarkan | Menyimpan amunisi keping logam (*Metal Strips*) untuk mengikat/menyerang lawan tanpa mengambil blok dunia | 
| **Republic City** ([Republic City Police](https://avatar.fandom.com/wiki/Republic_City_Police)) | **Metalbending Police Armor** | Helm topi logam berpelindung leher, pelat dada bersegmen dengan **2 gulungan kabel hitam di punggung**, sarung tangan bilah lipat (*Lin's blades*), dan sepatu bot lutut kubah | Syarat wajib untuk menembakkan *Metal Cable* / *Metal Whip* dari punggung tangan tanpa menghabiskan blok dunia | 
| **Fire Nation** ([Fire Army](https://avatar.fandom.com/wiki/Fire_Army)) | **Fire Nation Infantry & Bender Skull-Mask Armor** | Pelat baja merah-hitam dengan bahu melengkung tajam ke atas, helm jambul emas, dan topeng tengkorak putih khusus pengendali api | +10% efisiensi chi jurus api, resistansi panas/terbakar | 
| **Fire Nation** ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | **Aang's Overloaded Shu Jing Armor (*Wind Sword Armor*)** | Armor ekstrem penuh tanduk, rantai, dan duri dari toko senjata Shu Jing (kosmetik/meme kanon) | Sangat berat (*slowness* tinggi), tetapi memiliki referensi kanon gagang *Wind Sword* | 
| **Air Nomads** ([Fashion in the World of Avatar](https://avatar.fandom.com/wiki/Fashion_in_the_World_of_Avatar)) | **Traditional Air Nomad Monk Robes** | Jubah biksu kuning-jingga-cokelat berlapis selendang ringan | \-15% biaya chi mobilitas, pengurangan *fall damage* | 
| **Air Nation** ([Airbender Wingsuit](https://avatar.fandom.com/wiki/Airbender_wingsuit)) | **Future Industries Airbender Wingsuit** | Setelan merah-kuning buatan Asami Sato dengan membran sayap lipat di antara lengan dan kaki | Terbang melayang (*gliding* seperti Elytra + kendali angin) tanpa perlu memegang tongkat glider di tangan | 
| **Nonbender / Equalist** ([Equalists](https://avatar.fandom.com/wiki/Equalists)) | **Equalist Chi-Blocker Uniform & Goggles** | Seragam taktis gelap dengan pelindung bahu ringan, kacamata *goggles*, dan sarung tangan khusus | +10% stamina/kecepatan gerak, meningkatkan durasi *Chi-Blocking* & kelincahan akrobatik | 

### 1.2 Tabel Senjata Kanon & *Weapon-Enhanced Bending*

| Kategori / Faksi | Nama Senjata Kanon | Karakter Ikonik | Mekanika Tempur & Sinergi Bending ([Weaponry in the World of Avatar](https://avatar.fandom.com/wiki/Weaponry_in_the_World_of_Avatar)) | 
| ----- | ----- | ----- | ----- | 
| **Master Swordsman** | [**Sokka's Meteorite "Space Sword"**](https://avatar.fandom.com/wiki/Sokka%27s_sword) | Sokka | Pedang lurus (*Jian*) bermata dua dari bijih meteorit hitam dengan ukiran [Order of the White Lotus](https://avatar.fandom.com/wiki/Order_of_the_White_Lotus) di gagangnya; mampu membelah logam dan batu keras (*Armor Negation* tinggi) | 
| **Master Swordsman** | [**Steel Jian (Piandao's Blade)**](https://avatar.fandom.com/wiki/Sokka%27s_weapons) | Piandao, Sokka | Pedang lurus baja presisi tinggi untuk tebasan cepat, *parry*, dan serangan balik | 
| **Fire Nation / Blue Spirit** | [**Dual Broadswords (Twin Dao)**](https://avatar.fandom.com/wiki/Dual_broadswords) | Zuko (Blue Spirit) | Sepasang golok melengkung yang digabungkan dalam satu sarung; dapat dipakai Nonbender (gaya Blue Spirit) **atau** disaluri *Firebending* untuk *Flame Sweep* & pusaran api | 
| **Air Nomads** | [**Airbender Glider Staff**](https://avatar.fandom.com/wiki/Airbender_staff) | Aang, Tenzin, Korra | Tongkat kayu lipat dengan sayap glider merah/biru; memperkuat *Air Staff Attack* (jejak angin *tip-to-base*), *Air Vortex*, dan membuka mode terbang saat sayap dibuka | 
| **Earth / Kyoshi / Air** | [**War Fans (Shanzi)**](https://avatar.fandom.com/wiki/War_fans) | Avatar Kyoshi, Suki, Jesa | Sepasang kipas besi lipat; dipakai Kyoshi Warriors untuk *Fan Throw* (lintasan elips kembali), *Fan Parry*, & *Dance of Fans*, serta oleh bender untuk memperbesar busur *Air/Fire/Earth Wave* | 
| **Water Tribe** | [**Boomerang**](https://avatar.fandom.com/wiki/Sokka%27s_weapons) | Sokka | Senjata lempar logam berbentuk L yang kembali ke tangan; dapat memantul antar-target (*Trick Shot*) dan menginterupsi konsentrasi (*Combustion Beam* / *Charge*) jika mengenai kepala | 
| **Water Tribe** | [**Wolf-Tail Battle Club & Jaw Blade**](https://avatar.fandom.com/wiki/Sokka%27s_weapons) | Sokka, Kuruk | Gada tulang paha beruang kutub dengan bola pemberat biru & takik pengait senjata lawan; belati rahang serigala (*Jaw Blade*) dapat ditancapkan ke tanah untuk mendeteksi getaran musuh | 
| **Earth Kingdom** | **Twin War Hammers (Stone Hammers)** | Gow | Sepasang palu godam berat (juga dapat dihubungkan rantai) yang memperkuat *Earthbending* untuk menghancurkan tanah dan melontarkan batu berkecepatan tinggi | 
| **Earth Kingdom / Dai Li** | [**Rock Gloves (Sarung Tangan Batu)**](https://avatar.fandom.com/wiki/Rock_gloves) | Agen [Dai Li](https://avatar.fandom.com/wiki/Dai_Li), Yun | Sarung tangan keping batu tanah yang ditembakkan sebagai proyektil tangan pencengkeram (mengikat tangan/kaki target atau menarik pemakai ke dinding/langit-langit) | 
| **Freedom Fighters** | [**Hook Swords (Pedang Kait Kembar)**](https://avatar.fandom.com/wiki/Hook_swords) | Jet, Tokuga | Sepasang pedang dengan ujung kait bulan sabit, pelindung tangan tajam, dan pangkal belati; kedua ujung kait dapat disambungkan untuk menggandakan jangkauan tebasan | 
| **Fire Nation** | [**Mai's Stiletto Darts & Throwing Knives**](https://avatar.fandom.com/wiki/Mai%27s_weapons) | Mai | Pisau lempar dan anak panah *stiletto* tersembunyi di lengan baju yang dapat memaku pakaian lawan ke dinding/tanah (*Pin/Root effect*) | 
| **Equalists** | [**Electrified Glove**](https://avatar.fandom.com/wiki/Electrified_glove) **& Kali Sticks** | Asami Sato, The Lieutenant | Sarung tangan kejut listrik dan tongkat ganda beraliran listrik dari generator punggung; melumpuhkan target (*Stun/Chi-Block*) dan menembus armor logam polisi | 

## 2. Audit Teknis dari 9 Berkas Referensi yang Anda Unggah

Kami telah mengekstrak dan menganalisis struktur internal dari ke-9 arsip ZIP yang Anda lampirkan untuk memetakan praktik terbaik yang bisa diadopsi langsung ke proyek **Avatar Elements (Minecraft 1.21.1 Fabric)**:

| Arsip Referensi | Arsitektur Armor, Senjata & VFX yang Ditemukan | Pelajaran Penting untuk Proyek Kita | 
| ----- | ----- | ----- | 
| **`avatarmod-0.3.0.zip`** | Memiliki sistem **Swordsman & Kyoshi Warrior** lengkap (`meteorite_sword`, `steel_jian`, `war_fans`, `boomerang`, `glider_staff`), wadah sumber (`water_pouch`, `earth_pouch`), serta **Metalbending Police Armor** (`police_helmet`, `police_chestplate`, `cable_leggings`, `police_boots`) dan teknik armor aktif (`earth_armor`, `metal_armor`, `enhanced_earth_armor`). | **Sangat relevan!** Menunjukkan mekanika di mana *Metal Cable* membutuhkan `police_chestplate` (gulungan kabel di punggung), *Earth/Metal Armor* memiliki *tier* (mis. *Academy Chainmail* anti-*chi-block*, *Comet-Proof* tahan api), dan *Glider Staff* punya 2 model (`glider_staff.png` tertutup & `glider_staff_sail.png` terbuka). | 
| **`avatar-legend-reforged-1.3.0.zip`** | Menggunakan model geometri Bedrock/GeckoLib `.geo.json` (`glider.geo.json` dengan 16 variasi warna *dyeable*, `stone_hammer.geo.json`, `water_pouch.geo.json`, `bison_saddle.geo.json`), mesh `.obj` (`cone`, `torus`, `cylinder`, `isosphere`), serta *custom shader* GLSL (`fresnel`, `edge_dissolve`, `stylised_fire/water/air`). | Menunjukkan cara memisahkan model tongkat glider (`staff_main` bone) dengan kain layar yang dapat diwarnai (*dyeable*) dan cara *Stone Hammer* dipakai sebagai penyalur *Earth Smash*. | 
| **`avatar-skill-datapack.zip` & `avatar-skill-resourcepack.zip`** | Menggunakan item fokus (`chi_orb`, `avatar_relic`, `scroll_fire/water/earth/air/mastery`, `focus_lightning/metal/lava/blood/healing/flight/combustion`) dan 4 pohon atribut pasif (`potency`, `resilience`, `agility`, `chi` level 1–5). | Memberikan referensi desain *item scroll* dan *focus* untuk membuka *sub-bending* di *Skill Tree*. | 
| **`epic-fight-21.17.3.1-mc1.21.1-neoforge.zip` & `EFMCompat 2.0.zip`** | Memisahkan **visual jejak tebasan (`assets/<mod>/item_skins/<weapon>.json`)** dari **atribut tempur (`data/<mod>/capabilities/weapons/<weapon>.json`)** dan menyediakan `VanillaModelTransformer` / `AnimatedArmorTextureEvent` untuk melipat tekstur armor mengikuti sendi animasi pemain. | Kita harus mengadopsi skema `item_skins` milik Epic Fight: setiap senjata mendefinisikan `begin_pos` (pangkal bilah), `end_pos` (ujung bilah), `lifetime`, `interpolations`, `color`, dan `texture_path` untuk *swing trail*! | 
| **`WOLegendaryMonsters-1.1.0-forge-1.20.1.zip`** | Mendefinisikan atribut armor (`stun_armor`, `weight` pada `annihilator_chestplate.json`) serta atribut senjata satu tangan vs dua tangan (`impact`, `armor_negation`, `max_strikes`, `speed_bonus` pada `axe_of_lightning.json`) dan *Weapon Innate Skill*. | Sangat cocok untuk membedakan senjata ringan (Kipas Kyoshi / Belati Mai: `speed_bonus` tinggi, `weight` rendah) vs senjata berat (Palu Batu Gow / Pedang Meteorit: `armor_negation` & `impact` tinggi). | 
| **`sword_soaring-21.14.2.5-mc1.21.1-neoforge.zip`** | Mengimplementasikan entitas senjata melayang/telekinetik (`FlySwordEntity`, `ScreenSwordEntity`, `BabylonEntity`) di mana pemain dapat menaiki pedang terbang atau mengendalikan banyak bilah di udara. | Arsitektur ini sangat mirip dengan cara kerja **Metal Strips (Keping Logam Zaofu/Kuvira)** dan **Air Scooter / Glider**! | 
| **`epicfight-skilltree-neoforge-21.3.3-1.21.1.zip`** | Sistem *Skill Tree* berbasis halaman (`TreePage`), simpul status (`NodeState`: *locked/available/unlocked*), konversi XP ke *Ability Points*, dan *radial icon compatibility*. | Selaras dengan sistem GUI *Skill Tree* perkamen dan `skill_node_*` yang sudah kita bangun di paket aset. | 

## 3. Analisis Sumber Eksternal ([MythicCraft](https://mythiccraft.io/) & [ResourcePack AI](https://resourcepack.ai/docs))

1. **Ekosistem [MythicCraft](https://mythiccraft.io/) ([MythicCrucible](https://mythiccraft.io/index.php?resources/mythiccrucible.2/), [Custom Armor](https://mythiccraft.io/index.php?tags/custom-armor/), [Custom Weapons](https://mythiccraft.io/index.php?tags/weapons/), [ModelEngine](https://wiki.mythiccraft.io/modelengine/Modeling/Importing-a-Model))**:

   * **Pola Desain**: Memisahkan sebuah *Equipment Set* menjadi **(a) 2D Inventory Icon**, **(b) 3D Wearable/Held Blockbench Model (`.bbmodel`)**, **(c) Custom Trail/VFX**, dan **(d) Skill Triggers** (`onSwing`, `onRightClick`, `onBlock`, `Full Set Bonus`).

   * **Penerapan di Fabric 1.21.1**: Karena kita menggunakan Fabric murni tanpa plugin server Paper/Spigot, kita tidak memakai plugin MythicCrucible/ModelEngine secara langsung, melainkan menerapkan **pola arsitektur datanya**: setiap senjata/armor memiliki model 3D `.bbmodel` / `.geo.json`, definisi *swing trail* (`begin_pos` → `end_pos`), dan *hook* ke sistem jurus (`Weapon Imbue` & `Armor Set Bonus` sesuai `CONTENT_SPEC.md`).

2. **Ekosistem [ResourcePack AI](https://resourcepack.ai/docs) ([VFX Docs](https://resourcepack.ai/docs/vfx), [Exporting Docs](https://resourcepack.ai/docs/exporting), [RP Engine Skills](https://resourcepack.ai/docs/rp-engine/skills))**:

   * **Pola Desain**: Menyediakan pembuatan tekstur item 2D, model 3D blok/item Java, dan sekuens VFX (*buildup → loop → fade*).

   * **Batasan Penting**: Ekspor VFX otomatisnya mengandalkan *RP Engine* (1.21.4+), sedangkan untuk **Minecraft Java 1.21.1 Fabric**, semua model item 3D dan tekstur armor harus diekspor sebagai **model JSON/geometri 1.21.1 standar + tekstur PNG RGBA** yang dirender oleh *custom renderer* Fabric kita.

## 4. Rancangan Paket Aset Armor & Senjata untuk Didiskusikan

Agar pembuatan aset berikutnya tepat sasaran dan tidak melebar tanpa arah, berikut usulan **Katalog Produksi Armor & Senjata Tahap Selanjutnya**:

### A. Kandidat Set Armor (5 Set Utama + 2 Set Spesialis)

1. **Fire Nation Military Set** (*Skull-Mask Helmet, Pauldron Chestplate, Imperial Greaves, Boots*) — Bonus: +10% efisiensi chi Api, tahan panas.

2. **Water Tribe Wolf Warrior Set** (*Wolf-Head Hood/Helmet, Fur-Trimmed Tunic, Bracers/Leggings, Mukluk Boots*) — Bonus: +10% pertahanan Air, regen chi di air/hujan.

3. **Earth Kingdom / Dai Li / Kyoshi Set** (*Conical Hat / Kyoshi Headdress, Armored Tunic, Leggings, Barefoot Ankle Wraps*) — Bonus: +20% *knockback resistance*, bonus *guard* & *Seismic Sense*.

4. **Air Nomad Monk / Wingsuit Set** (*Monk Headband/Hood, Saffron Robe / Future Industries Wingsuit Chestplate, Robe Leggings, Light Boots*) — Bonus: -15% biaya chi mobilitas, fitur *Wingsuit Gliding*.

5. **Nonbender Equalist / Kyoshi Tactical Set** (*Equalist Goggle Mask, Tactical Vest, Chi-Blocker Leggings, Silent Boots*) — Bonus: +10% stamina, bonus kecepatan & *Chi-Blocking*.

6. **Republic City Metalbending Police Set** (*Police Cap, Dual-Spool Cable Chestplate, Plated Skirt Leggings, Knee-Guard Boots*) — Membuka teknik *Metal Cable* & *Retractable Arm Blades*.

7. **Zaofu Metal Clan / Beifong Chainmail Set** (*Zaofu Pauldrons & Metal Strip Bracers / Anti-Chi-Block Chainmail*).

### B. Kandidat Senjata Kanon & *Weapon-Enhanced Bending* (10 Senjata Ikonik)

 1. **Airbender Glider Staff** (2 state: *Closed Combat Staff* + *Open Glider Wings* dengan 16 variasi warna kain & locator *wind trail*).

 2. **Sokka's Meteorite "Space Sword" (Black Jian)** + **Piandao's Steel Jian** (lengkap dengan *swing trail* hitam-ungu/perak & *armor negation*).

 3. **Zuko's Dual Broadswords (Twin Dao)** (bisa mode *Nonbender Blue Spirit* atau *Fire-Imbued Twin Blades*).

 4. **Kyoshi Warrior War Fans (Shanzi)** + **Collapsible Wrist-Shield** (mendukung *Fan Throw*, *Fan Parry*, dan *Air/Fire Wave amplification*).

 5. **Water Tribe Boomerang** + **Wolf-Tail Battle Club** + **Arctic Wolf Jaw Blade**.

 6. **Gow's Twin Earth War Hammers** (memperkuat *Earth Smash*, *Ground Stomp*, dan *Earth Bullet*).

 7. **Jet's Twin Hook Swords** (mendukung mode kait ganda jangkauan panjang).

 8. **Dai Li Rock Gloves** (gauntlet batu yang bisa ditembakkan sebagai proyektil penangkap).

 9. **Equalist Electrified Glove** + **Lieutenant's Kali Sticks** (senjata kejut listrik anti-armor logam).

10. **Mai's Throwing Knives & Stiletto Darts** (senjata lempar presisi dengan efek *pin/slow*).

## 5. Pertanyaan Diskusi sebelum Eksekusi Pembuatan Aset

1. **Format Visual Armor**: Apakah untuk ke-5/7 set armor di atas Anda menginginkan **(a) Tekstur Armor Humanoid Vanilla/2-Layer (`textures/models/armor/*_layer_1.png` & `_layer_2.png`) + Ikon Inventori**, atau **(b) Model 3D Berlapis di Blockbench (`.bbmodel` / `.geo.json`)** dengan bahu, jubah, topi kerucut, dan gulungan kabel 3D yang menonjol? (Atau keduanya sekaligus?)

2. **Prioritas Batch Senjata**: Dari 10 senjata kanon di atas, apakah kita buat **semuanya sekaligus** dalam satu batch (Ikon 2D + Model 3D `.bbmodel`/`.json` + Tekstur *Swing Trail* ala `EFMCompat` + konfigurasi `item_skins`), atau Anda ingin fokus pada daftar tertentu terlebih dahulu?

3. **Sistem *Weapon Imbue* & *Swing Trail***: Apakah Anda ingin setiap senjata juga dilengkapi tekstur *Swing Trail* khusus (seperti di `EFMCompat 2.0.zip`: jejak api untuk Dual Dao, jejak meteor hitam untuk Space Sword, jejak angin untuk Glider Staff & Kipas Kyoshi, dan jejak listrik untuk Equalist Glove)?


---

## 6. Panduan Audit & Integrasi untuk Coding/Runtime Agent (Status: Aset Siap Integrasi)

Seluruh aset untuk **7 Set Armor (28 item)**, **16 Senjata Kanon**, **8 Tekstur Swing Trail**, dan **12 Skill Kombo Aktif (Weapon + Full Set + Bender Element)** telah dibangun dan disertakan di dalam `Avatar_Elements_Asset_Pack_2026-11-08.zip`. Berikut daftar lokasi berkas dan aturan kontrak server untuk diaudit oleh Agent:

### 6.1 Lokasi Berkas di Dalam Paket Aset
- **Atlas Baru (`atlases/`) & Manifest (`docs/asset_manifest.json` — Total 31 Atlas, 320 Aset)**:
  - `atlases/23_armor_sets_icons.png` → 28 ikon armor (`individual/armor_<set>_<slot>.png` & `individual/runtime32/armor_*_32.png`).
  - `atlases/24_canonical_weapons.png` → 16 ikon senjata kanon (`individual/weapon_*.png` & `individual/runtime32/weapon_*_32.png`).
  - `atlases/25_weapon_swing_trails.png` → 8 tekstur *swing trail* *tileable* (`individual/trail_*.png` 128×128 & `assets/avatar_elements/textures/vfx/trail_*_128x32.png`).
  - `atlases/26_weapon_combo_icons.png` → 12 ikon skill kombo sinergi (`individual/combo_*.png` & `individual/runtime32/combo_*_32.png`).
- **Tekstur Armor Humanoid 2-Layer & Model 3D Blockbench**:
  - `assets/avatar_elements/textures/models/armor/<set>_layer_1.png` & `<set>_layer_2.png` (7 set × 2 layer = 14 tekstur humanoid 64×32).
  - `models/bbmodel/armor/armor_<set>_3d.bbmodel` (7 model armor 3D dengan locator `back_spool_left/right` & `wrist_emitter_left/right`).
  - `models/bbmodel/weapons/weapon_*.bbmodel` (16 model senjata 3D dengan locator `trail_begin`, `trail_end`, dan `imbue_emitter`).
- **Skema Data Sinergi, Capabilities & Item Skins (Siap Diaudit Agent)**:
  - `data/avatar_elements/synergies/weapon_armor_element_combos.json` → Matriks deklaratif yang memetakan `combo_id`, `required_weapon`, `required_armor_set`, `required_bender_element`, `animation`, dan `trail_override`.
  - `assets/avatar_elements/item_skins/weapon_*.json` → Definisi koordinat *swing trail* (`begin_pos`, `end_pos`, `lifetime`, `interpolations`) beserta `elemental_imbue_overrides` (`FIRE`, `BLUE_FIRE`, `AIR`, `WATER`, `EARTH`, `LIGHTNING`).
  - `data/avatar_elements/capabilities/weapons/weapon_*.json` & `armors/armor_*.json` → Atribut `impact`, `armor_negation`, `max_strikes`, `speed_bonus`, `stun_armor`, dan `weight`.
  - `animations/pal/combos/combo_*.animation.json` → 12 animasi *keyframe* kombo untuk [Player Animation Library (PAL)](https://docs.zigythebird.com/pal/intro/).

### 6.2 Kontrak Non-Negosiasi untuk Runtime Agent
1. **Otoritas Server Penuh**: Klien hanya merender *swing trail* (`item_skins`) dan memutar animasi PAL (`combo_*.animation.json`) setelah server memvalidasi bahwa pemain memegang `required_weapon`, mengenakan `required_armor_set` (atau memenuhi syarat elemen `required_bender_element`), dan memiliki cukup `chi_cost`.
2. **Zero Double-Damage Handler**: Sesuai `CONTENT_SPEC.md`, *Weapon Imbue* dan *Active Combo* memodifikasi proyektil/hitbox kemampuan melalui satu jalur validasi damage tunggal di server, bukan menumpuk dua *damage handler* terpisah.
3. **Kabel & Keping Logam Berbasis Equipment**: Kombo `avatar:combo_beifong_cable_grapple_slash` memeriksa keberadaan `armor_metal_police_chestplate` (gulungan kabel punggung) atau `armor_zaofu_clan_chestplate` (keping logam) sebelum mengizinkan tembakan kabel/keping tanpa mengambil blok dunia.
