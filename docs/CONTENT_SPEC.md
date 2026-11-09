> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# CONTENT_SPEC.md — Spesifikasi Gameplay dan Snapshot Runtime

> Kontrak desain dan katalog masa depan ada di dokumen ini. Untuk skill aktif, data runtime kanonis adalah `mod/src/main/resources/data/avatar_elements/skill_definitions.json`, yang dapat ditimpa oleh `config/avatar_elements/skill_definitions.json`. Perubahan gameplay harus merekonsiliasi JSON aktif, implementasi, dan dokumen ini serta dicatat di `DECISIONS.md`.

## Schema yang benar-benar dibaca runtime

Loader membaca objek JSON dengan properti `skills` berupa array. Properti yang dibaca dan ejaan kanonisnya ditunjukkan di bawah; field opsional ditandai:

| JSON key | Tipe | Keterangan |
|---|---|---|
| `id` | string | Kunci skill; runtime saat ini memakai prefix `avatar:` meski mod ID adalah `avatar_elements` |
| `element` | string/enum | `FIRE`, `WATER`, `EARTH`, atau `AIR` |
| `masteryRequired` | int | Mastery minimum |
| `chiCost` | int | Chi saat cast |
| `chiPerTick` | int | Dibaca ke definisi, tetapi belum dikonsumsi oleh jalur runtime saat ini |
| `cooldownTicks` | int | Cooldown |
| `windupTicks` | int | Windup |
| `activeTicks` | int | Durasi fase active |
| `recoveryTicks` | int | Durasi recovery |
| `damage` | float | Damage dasar |
| `range` | float | Jangkauan dalam blok |
| `knockback` | float | Opsional; default `0` |
| `hitboxShape` | string/enum | Opsional; default `SPHERE`; nilai yang dikenal: `SPHERE`, `ARC`, `LINE`, `CONE` |
| `cancelOnHit` | boolean | Flag definisi |
| `comboWindowTicks` | int | Jendela kombo |
| `castType` | string/enum | Opsional; default `INSTANT`; nilai enum `INSTANT`, `HOLD_RELEASE`, `CHANNEL`, `TOGGLE` |
| `maxChargeTicks` | int | Opsional; default `0`, dipakai bersama `HOLD_RELEASE` |

Loader menerima alias snake_case hanya untuk `cast_type` dan `max_charge_ticks`; field lain harus memakai ejaan camelCase di atas. Field tambahan seperti `projectile_speed`, `explosion_radius`, atau `block_duration_ticks` tidak dibaca oleh `SkillConfigLoader` dan tidak boleh dianggap konfigurasi runtime.

Walaupun enum mendeklarasikan `CHANNEL` dan `TOGGLE`, jalur validasi/timeline saat ini hanya mengaktifkan perilaku khusus `HOLD_RELEASE`; chi sustain dari `chiPerTick` belum diterapkan. Jangan mendeskripsikan field enum/data tersebut sebagai fitur runtime yang sudah berfungsi.

Jika file override ada tetapi JSON/schema-nya malformed, loader tidak menjamin fallback ke bundled resource: parse/konversi terjadi di dalam blok yang hanya menangkap `IOException`. Validasi startup dan pelaporan error yang jelas masih menjadi follow-up.

### Snapshot definisi dan slot aktif

Daftar ID di bawah adalah isi `skill_definitions.json` yang diaudit. Nilai numerik persis untuk versi kerja selalu dibaca dari file JSON tersebut; blok katalog di bawah bukan salinan runtime yang dijamin mutakhir.

| Elemen | Skill ID yang dimuat |
|---|---|
| FIRE | `avatar:fire_jab`, `avatar:fire_blast`, `avatar:flame_sweep`, `avatar:fire_jet`, `avatar:fire_guard` |
| AIR | `avatar:air_palm`, `avatar:air_blast`, `avatar:air_staff_attack`, `avatar:air_vortex` |
| WATER | `avatar:water_whip` |
| EARTH | `avatar:earth_boulder` |

`element_slots.json` dan `ElementSlotMap` menggunakan lima slot (0–4; tombol Z/X/C/V/B). Mapping saat ini menempatkan Fire Jab/Blast/Sweep/Guard/Jet pada lima slot FIRE; slot AIR kelima mengulang Air Staff Attack, sedangkan seluruh slot WATER mengulang Water Whip dan seluruh slot EARTH mengulang Earth Boulder. Pengulangan ini adalah keadaan data saat audit, bukan rekomendasi desain; jangan menggantinya tanpa keputusan pemetaan gameplay.

Contoh stat di bagian berikut merupakan katalog desain historis. Contoh yang tidak hadir di daftar runtime di atas masih direncanakan; jika nilai contoh berbeda dari JSON aktif, JSON aktif menang sampai nilai tersebut secara eksplisit direkonsiliasi.

## Api (Fire)

### Fire Jab
```json
{
  "id": "avatar:fire_jab",
  "element": "FIRE",
  "mastery_required": 0,
  "chi_cost": 8,
  "cooldown_ticks": 6,
  "windup_ticks": 2,
  "active_ticks": 3,
  "recovery_ticks": 4,
  "damage": 4.0,
  "range": 2.5,
  "hitbox_shape": "SPHERE",
  "knockback": 0.3,
  "combo_window_ticks": 6
}
```

### Flame Sweep (arc, 180°)
```json
{
  "id": "avatar:flame_sweep",
  "element": "FIRE",
  "mastery_required": 0,
  "chi_cost": 15,
  "cooldown_ticks": 12,
  "windup_ticks": 3,
  "active_ticks": 8,
  "recovery_ticks": 6,
  "damage": 6.0,
  "range": 5.0,
  "hitbox_shape": "ARC",
  "knockback": 0.5,
  "combo_window_ticks": 8
}
```

### Fire Jet (mobilitas)
```json
{
  "id": "avatar:fire_jet",
  "element": "FIRE",
  "mastery_required": 0,
  "chi_cost": 25,
  "cooldown_ticks": 30,
  "windup_ticks": 1,
  "active_ticks": 10,
  "recovery_ticks": 10,
  "damage": 0.0,
  "range": 0.0,
  "hitbox_shape": "SPHERE",
  "knockback": 0.0,
  "combo_window_ticks": 0
}
```

### Fire Guard
```json
{
  "id": "avatar:fire_guard",
  "element": "FIRE",
  "mastery_required": 0,
  "chi_cost": 10,
  "chi_per_tick": 2,
  "cooldown_ticks": 8,
  "windup_ticks": 2,
  "active_ticks": 60,
  "recovery_ticks": 5,
  "damage": 0.0,
  "range": 0.0,
  "hitbox_shape": "SPHERE",
  "knockback": 0.0,
  "combo_window_ticks": 0
}
```

### Fire Blast (hold → charge → release projectile)
```json
{
  "id": "avatar:fire_blast",
  "element": "FIRE",
  "mastery_required": 0,
  "chi_cost": 20,
  "cooldown_ticks": 20,
  "windup_ticks": 0,
  "active_ticks": 25,
  "recovery_ticks": 5,
  "damage": 7.0,
  "range": 24.0,
  "hitbox_shape": "SPHERE",
  "knockback": 1.0,
  "combo_window_ticks": 0,
  "cast_type": "HOLD_RELEASE",
  "max_charge_ticks": 40
}
```

`projectile_speed` in older examples was not part of the parsed skill schema; projectile motion is currently implemented by the skill handler.

### Fire Ring
```json
{
  "id": "avatar:fire_ring",
  "element": "FIRE",
  "mastery_required": 1,
  "chi_cost": 25,
  "cooldown_ticks": 18,
  "windup_ticks": 3,
  "active_ticks": 2,
  "recovery_ticks": 6,
  "damage": 5.0,
  "range": 5.0,
  "hitbox_shape": "SPHERE",
  "knockback": 0.8,
  "combo_window_ticks": 0
}
```

### Fire Stream (channel)
```json
{
  "id": "avatar:fire_stream",
  "element": "FIRE",
  "mastery_required": 1,
  "chi_cost": 5,
  "chi_per_tick": 3,
  "cooldown_ticks": 10,
  "windup_ticks": 2,
  "active_ticks": 60,
  "recovery_ticks": 5,
  "damage": 2.0,
  "range": 8.0,
  "hitbox_shape": "LINE",
  "knockback": 0.1,
  "combo_window_ticks": 0,
  "cast_type": "CHANNEL"
}
```

### Lightning Strike (sub-bending)
```json
{
  "id": "avatar:lightning_strike",
  "element": "FIRE",
  "mastery_required": 4,
  "chi_cost": 50,
  "cooldown_ticks": 60,
  "windup_ticks": 0,
  "active_ticks": 1,
  "recovery_ticks": 15,
  "damage": 20.0,
  "range": 32.0,
  "hitbox_shape": "LINE",
  "knockback": 2.0,
  "combo_window_ticks": 0,
  "cast_type": "HOLD_RELEASE",
  "max_charge_ticks": 60
}
```

### Combustion Beam (sub-bending)
```json
{
  "id": "avatar:combustion_beam",
  "element": "FIRE",
  "mastery_required": 5,
  "chi_cost": 40,
  "cooldown_ticks": 30,
  "windup_ticks": 0,
  "active_ticks": 1,
  "recovery_ticks": 10,
  "damage": 15.0,
  "range": 48.0,
  "hitbox_shape": "SPHERE",
  "knockback": 3.0,
  "combo_window_ticks": 0,
  "cast_type": "HOLD_RELEASE",
  "max_charge_ticks": 40,
  "explosion_radius": 3.0
}
```


## Udara (AIR)

### Air Palm
```json
{
  "id": "avatar:air_palm",
  "element": "AIR",
  "mastery_required": 0,
  "chi_cost": 6,
  "cooldown_ticks": 5,
  "windup_ticks": 2,
  "active_ticks": 2,
  "recovery_ticks": 4,
  "damage": 2.0,
  "range": 3.0,
  "hitbox_shape": "CONE",
  "knockback": 1.2,
  "combo_window_ticks": 6
}
```

### Air Blast
```json
{
  "id": "avatar:air_blast",
  "element": "AIR",
  "mastery_required": 0,
  "chi_cost": 12,
  "cooldown_ticks": 10,
  "windup_ticks": 3,
  "active_ticks": 4,
  "recovery_ticks": 6,
  "damage": 3.0,
  "range": 8.0,
  "hitbox_shape": "LINE",
  "knockback": 2.5,
  "combo_window_ticks": 8
}
```

## Tanah (Earth)

### Earth Boulder
```json
{
  "id": "avatar:earth_boulder",
  "element": "EARTH",
  "mastery_required": 0,
  "chi_cost": 15,
  "cooldown_ticks": 15,
  "windup_ticks": 3,
  "active_ticks": 20,
  "recovery_ticks": 6,
  "damage": 5.0,
  "range": 10.0,
  "hitbox_shape": "SPHERE",
  "knockback": 1.0,
  "combo_window_ticks": 0
}
```

### Earth Wall
```json
{
  "id": "avatar:earth_wall",
  "element": "EARTH",
  "mastery_required": 0,
  "chi_cost": 18,
  "cooldown_ticks": 25,
  "windup_ticks": 4,
  "active_ticks": 1,
  "recovery_ticks": 8,
  "damage": 0.0,
  "range": 4.0,
  "hitbox_shape": "LINE",
  "knockback": 0.0,
  "combo_window_ticks": 0,
  "block_duration_ticks": 140
}
```

## Air (WATER)

### Water Whip
```json
{
  "id": "avatar:water_whip",
  "element": "WATER",
  "mastery_required": 0,
  "chi_cost": 10,
  "cooldown_ticks": 8,
  "windup_ticks": 2,
  "active_ticks": 2,
  "recovery_ticks": 4,
  "damage": 3.0,
  "range": 6.0,
  "hitbox_shape": "LINE",
  "knockback": 0.8,
  "combo_window_ticks": 8
}
```

---

## Skill List Lengkap — Referensi Desain

> Bagian ini adalah katalog semua teknik dari Avatar: TLA dan LoK yang akan
> diimplementasi secara bertahap. Status: `planned` / `in_progress` / `done`.
> Nilai stat akan diisi saat task implementasi dibuat di TASKS.md.

### 🔥 Firebending

| Skill ID | Nama | Cast Type | Status | Prioritas |
|---|---|---|---|---|
| `avatar:fire_jab` | Fire Jab | instant | done | — |
| `avatar:flame_sweep` | Flame Sweep | instant | done | — |
| `avatar:fire_jet` | Fire Jet (dash) | instant | done | — |
| `avatar:fire_guard` | Fire Guard | channel | done | — |
| `avatar:fire_blast` | Fire Blast | hold→release | planned | T3 |
| `avatar:fire_stream` | Fire Stream | channel | planned | T3 |
| `avatar:fire_ring` | Fire Ring | instant | planned | T3 |
| `avatar:fire_whip` | Fire Whip | instant | planned | T3 |
| `avatar:fire_arc` | Fire Arc | instant | planned | T3 |
| `avatar:fire_wall` | Fire Wall | instant | planned | T4 |
| `avatar:fire_shield` | Fire Shield | toggle | planned | T4 |
| `avatar:fire_breath` | Fire Breath | channel | planned | T4 |
| `avatar:jet_propulsion` | Jet Propulsion | channel | planned | T4 |
| `avatar:flame_vortex` | Flame Vortex | channel | planned | T4 |
| `avatar:lightning_strike` | Lightning Strike | hold→release | planned | T5 |
| `avatar:lightning_redirect` | Lightning Redirect | instant/counter | planned | T5 |
| `avatar:combustion_beam` | Combustion Beam | hold→release | planned | T5 |
| `avatar:blue_fire` | Blue Fire | passive modifier | planned | T5 |

### 💨 Airbending

| Skill ID | Nama | Cast Type | Status | Prioritas |
|---|---|---|---|---|
| `avatar:air_palm` | Air Palm | instant | planned | T3 |
| `avatar:air_blast` | Air Blast | instant | in_progress | T3 |
| `avatar:air_staff_attack` | Air Staff Attack | instant/combo | done | — |
| `avatar:air_vortex` | Air Vortex | channel | done | — |
| `avatar:air_swipe` | Air Swipe | instant | planned | T3 |
| `avatar:air_wave` | Air Wave | instant | planned | T3 |
| `avatar:air_funnel` | Air Funnel | hold | planned | T4 |
| `avatar:air_shield` | Air Shield | toggle | planned | T4 |
| `avatar:air_cushion` | Air Cushion | instant | planned | T4 |
| `avatar:air_spout` | Air Spout | hold | planned | T4 |
| `avatar:air_scooter` | Air Scooter | hold | planned | T4 |
| `avatar:breath_of_wind` | Breath of Wind | instant | planned | T4 |
| `avatar:true_flight` | True Flight | channel | planned | T5 |
| `avatar:sound_vibration` | Sound Vibration | instant | planned | T5 |
| `avatar:air_suffocation` | Air Suffocation | channel | planned | T5 |

### 💧 Waterbending

| Skill ID | Nama | Cast Type | Status | Prioritas |
|---|---|---|---|---|
| `avatar:water_whip` | Water Whip | instant | done | — |
| `avatar:water_jet` | Water Jet | channel | planned | T3 |
| `avatar:ice_spear` | Ice Spear | instant | planned | T3 |
| `avatar:ice_disk` | Ice Disk | instant | planned | T3 |
| `avatar:ice_shield` | Ice Shield | instant | planned | T3 |
| `avatar:water_wave` | Water Wave | hold | planned | T4 |
| `avatar:ice_prison` | Ice Prison | hold→release | planned | T4 |
| `avatar:water_arms` | Water Arms | hold | planned | T4 |
| `avatar:octopus_form` | Octopus Form | channel | planned | T4 |
| `avatar:steam_cloud` | Steam Cloud | instant | planned | T4 |
| `avatar:ice_path` | Ice Path | instant | planned | T4 |
| `avatar:healing` | Healing | channel | planned | T5 |
| `avatar:bloodbending` | Bloodbending | channel | planned | T5 |
| `avatar:plantbending` | Plantbending | hold | planned | T5 |

### 🪨 Earthbending

| Skill ID | Nama | Cast Type | Status | Prioritas |
|---|---|---|---|---|
| `avatar:earth_wall` | Earth Wall | instant/construct actions | planned | W3 |
| `avatar:earth_boulder` | Earth Boulder | instant | done | — |
| `avatar:earth_bullet` | Earth Bullet | instant | planned | T3 |
| `avatar:earth_pillar` | Earth Pillar | instant | planned | T3 |
| `avatar:earth_rampart` | Earth Rampart | instant | planned | T3 |
| `avatar:ground_stomp` | Ground Stomp | instant | planned | T3 |
| `avatar:boulder_launch` | Boulder Launch | hold→release | planned | T3 |
| `avatar:earth_armor` | Earth Armor | instant | planned | T4 |
| `avatar:rock_cage` | Rock Cage | instant | planned | T4 |
| `avatar:earth_surf` | Earth Surf | hold | planned | T4 |
| `avatar:earth_tunnel` | Earth Tunnel | hold | planned | T4 |
| `avatar:seismic_sense` | Seismic Sense | toggle | planned | T5 |
| `avatar:metalbending_whip` | Metalbending Whip | instant | planned | T5 |
| `avatar:metal_cable` | Metal Cable | instant | planned | T5 |
| `avatar:lavabending` | Lavabending | hold→release | planned | T5 |

### Cast Type Definitions

| Tipe | Deskripsi | Mekanisme |
|---|---|---|
| `instant` | Tekan → langsung cast | Satu C2S packet, timeline windup→active→recovery |
| `channel` | Tahan → terus aktif → lepas | C2S hold start + hold release, chi per tick |
| `hold→release` | Tahan → charge (orb membesar) → lepas → aksi | C2S hold start + release, charge time → power scaling |
| `toggle` | Tekan aktif / tekan lagi nonaktif | C2S toggle packet |
| `instant/counter` | Timing-based, reaktif terhadap input musuh | C2S instant, server cek window |

---

## Avatar State

```json
{
  "chi_cost": 50,
  "cooldown_ticks_after": 200,
  "duration_ticks": 600,
  "mastery_all_required": true,
  "effects": {
    "resistance": {"amplifier": 1, "duration_ticks": 600},
    "speed": {"amplifier": 1, "duration_ticks": 600},
    "strength": {"amplifier": 1, "duration_ticks": 600},
    "regeneration": {"amplifier": 1, "duration_ticks": 600}
  }
}
```

## Chi sistem

| Parameter | Nilai default |
|---|---|
| Chi max base | 100 |
| Chi regen base | 5/detik |
| Chi regen saat meditasi | +20/detik tambahan |
| Chi regen bonus (Chi mastery 1–5) | +2/+4/+7/+10/+15 per detik |

## Armor bonus (ringkasan)

| Set | Bonus utama |
|---|---|
| Fire Nation | +10% efisiensi skill api, resistansi panas |
| Water Tribe | +10% efisiensi pertahanan air, regenerasi chi saat hujan/air |
| Earth Kingdom | Resistansi knockback +20%, guard bonus |
| Air Nomad | -15% chi cost mobilitas, fall damage reduction |
| Nonbender | +10% stamina, resistansi fisik |

Nilai lengkap per tier ada di `data/avatar/armor_definitions/` (di-generate saat Tahap 4).

---

## Manipulasi Elemen, Utilitas, dan Profesi — Rancangan 2026-11-08

Status: **spesifikasi desain untuk implementasi berikutnya**, bukan fitur runtime selesai.
Tidak mengubah nilai balance JSON di atas. Urutan A–D aktif tetap dipertahankan.

### Kontrak kemampuan bersama

Combat dan utilitas memakai definisi kemampuan, validasi server, resource, dan state yang sama.
Utilitas dapat berdampak pada PvP hanya melalui efek gameplay yang didefinisikan; VFX tidak pernah menentukan damage.

| Dimensi | Ketentuan |
|---|---|
| activation / cast_type | INSTANT, HOLD_RELEASE, CHANNEL, TOGGLE, COUNTER; normalisasi nama lama dilakukan saat migrasi schema |
| duration_policy | FIXED, WHILE_HELD, UNTIL_INTERRUPTED; durasi terpisah dari cara aktivasi |
| sustain | Biaya awal/berjalan, syarat konsentrasi, batas material; angka belum ditetapkan |
| interruption | Batal manual, knock/stagger sesuai aturan skill, chi habis, mati, disconnect, pindah dimensi |
| material_source | Lingkungan, wadah, material terkendali, atau produksi internal sesuai elemen |
| manipulation | Ambil, pindahkan, bentuk, panaskan/dinginkan, dorong, lepaskan, reklamasi |
| entity_effects | Damage, panas, knockback, angkat, atau pembatas gerak yang secara eksplisit didukung |
| world_effects | Pengambilan, penempatan, perubahan kondisi blok; mengikuti izin wilayah dan ledger material |
| progression | Elemen, mastery minimum, teknik dipelajari, prasyarat latihan dan profesi |
| presentation | Animation ID, attachment, event cast/release/impact, trail, SFX, first/third person |

Field baru di atas adalah rancangan schema, **belum boleh dimasukkan ke konfigurasi aktif sebelum loader mendukungnya**.
`hold` lama harus dipetakan per skill ke CHANNEL atau HOLD_RELEASE; bukan tipe ambigu tersendiri.

### Durasi berkelanjutan dan mobilitas udara

Menunggangi angin dirancang sebagai TOGGLE + UNTIL_INTERRUPTED: tidak berhenti hanya karena timer tetap habis.
Knock/stagger yang memenuhi aturan skill membuyarkan kendaraan angin. Tetap ada collision; tidak menembus medan.
Biaya sustain, ambang interrupt, kecepatan, dan perlindungan jatuh masih TBD; unlimited durasi bukan keputusan unlimited resource.
Jangan mengubah Fire Jet dasar: tetap dash singkat; rocket flight/jet propulsion teknik terpisah.

### Sumber material per elemen

| Elemen | Aturan desain |
|---|---|
| AIR | Udara lingkungan; tanpa inventori material padat |
| FIRE | Api diproduksi bender menggunakan chi; pemanasan benda mengikuti teknik |
| WATER | Air dunia atau wadah; volume diambil dan dipindahkan, bukan digandakan |
| EARTH | Material bertag bendable dari dunia; pengambilan meninggalkan perubahan medan |
| METAL | Sub-bending dengan tag material dan unlock tersendiri; bukan semua logam otomatis valid |
| LAVA | Lava dunia atau wadah kompatibel; mengubah tanah menjadi lava merupakan teknik lanjut terpisah |
| ICE | Es tersedia atau air yang dibekukan; konversi mempertahankan ledger material |

Kapasitas wadah merupakan properti item. Level membuka kapasitas kendali, laju transfer, teknik, atau wadah tingkat lanjut;
level tidak memperbesar bucket vanilla diam-diam. Unit volume cairan dan konversi source/flowing fluid ditetapkan sebelum implementasi.

### Konservasi material dan perubahan dunia

Alur: sumber dunia/wadah → material terkendali → konstruksi/proyektil → endapan/pecahan → reklamasi.
Setiap jumlah material hanya mempunyai satu representasi yang dapat dipakai atau dijatuhkan sebagai item.
Debris visual tidak menghasilkan item tambahan. Pecahan dekoratif tidak dihitung sebagai material baru.
Transaksi harus menangani kegagalan sebagian, cancel, restart, chunk unload, dan dua pemain mengambil sumber sama.
Blok dengan inventory/block entity dan blok terlindungi ditolak pada prototipe awal.

Arah desain yang direkomendasikan adalah material benar-benar berpindah. **Default kerusakan permanen vs restore otomatis belum dikonfirmasi final oleh pengguna**.
Sediakan kebijakan server: PERMANENT, TEMPORARY_RESTORE, dan pembatasan AREA. Jangan mengaktifkan perubahan dunia pada world pengguna secara otomatis.
Reklamasi berarti membawa material yang tersisa kembali; bukan mengisi lokasi asal dari ketiadaan.
Restore otomatis adalah kebijakan server/arena. Jangan memulihkan sumber sekaligus meninggalkan material/drop salinannya.
Restore tidak boleh menimpa perubahan pemain lain; konflik dicatat dan diselesaikan dengan kebijakan eksplisit.

### Earth Wall — prototipe manipulasi dunia

1. Server memvalidasi izin sumber, tujuan, material, volume, chi, dan ruang entity.
2. Raise mengambil material nyata dan membentuk wall; lokasi asal meninggalkan bekas.
3. Wall merupakan konstruksi yang dapat menerima benturan, bertahan, atau direklamasi.
4. Kick/Launch meluncurkan **seluruh wall sebagai satu massa**, bukan hanya efek atau satu blok.
5. Server menguji collision sepanjang lintasan dan membatasi damage ulang per target.
6. Impact mengendapkan material atau memecahnya sesuai aturan yang dipilih; tidak otomatis selalu menghancurkan seluruh wall.
7. Reclaim memindahkan material tersisa; kerusakan/fragmentasi tidak boleh menghapus atau menggandakan item tanpa kebijakan eksplisit.

Aksi wall dan kendali konstruksi lanjutan tidak disamakan dengan timeline cast pertama: cast dapat selesai sementara wall tetap ada.
Maksimum volume, jumlah konstruksi, jarak kontrol, kecepatan, ketahanan, hasil impact, dan drop masih TBD.
Barrage sebagian wall adalah variasi backlog; bukan pengganti perilaku launch seluruh wall.
`block_duration_ticks: 140` pada Earth Wall lama adalah parameter prototipe FIXED, bukan aturan penghapusan material untuk desain baru.

### Utilitas dan dampak PvP

| Kemampuan kandidat | Utilitas | Dampak PvP yang perlu didefinisikan |
|---|---|---|
| Heat Control | Menyalakan api, memasak daging di tangan, pemanasan terkontrol | Panas terarah/ignition; memasak bukan aura damage otomatis |
| Water Transfer / Flow | Mengisi wadah, irigasi | Dorongan; damage hanya bila tekanan/teknik mendukung |
| Earth Shaping | Menggemburkan, menaikkan fondasi | Penghalang, angkat, atau massa diluncurkan; tidak spawn di dalam tubuh |
| Ore Extraction | Mengambil ore material valid | Hanya efek tabrakan/serangan yang eksplisit; bukan bypass seluruh aturan mining |
| Air Flow / Ride | Hembusan dan transportasi | Dorongan dan interrupt, sesuai teknik |

Server memeriksa friendly fire, PvP, kepemilikan konstruksi, wilayah, line of sight, jarak, collision,
frekuensi hit, dan intensitas. Label utility tidak membypass aturan combat.
Memasak mengonsumsi bahan dan menghasilkan resep yang valid. Ekstraksi ore menetapkan aturan tool/tier, loot,
Silk Touch/Fortune dan XP sebelum aktif; tidak otomatis menghasilkan ingot atau reward berulang.

### Tribe, mastery, latihan, dan profesi

Tribe/latar dan elemen disimpan terpisah. Pilihan awal menghubungkannya tanpa menganggap semua anggota tribe pasti bender.
Unlock = elemen sesuai + mastery minimum + teknik dipelajari + latihan/prasyarat profesi.
Mastery mengatur kendali umum; latihan teknik mengatur aksi spesifik; profesi memberikan jalur pekerjaan.
XP combat tidak otomatis membuka seluruh teknik pekerjaan. Master Earth tidak otomatis menjadi ahli semua profesi.

| Elemen | Kandidat jalur profesi |
|---|---|
| FIRE | Memasak, pengrajin panas |
| WATER | Penyedia air, irigasi, penyembuh |
| EARTH | Pertanian, pertambangan, konstruksi |
| AIR | Kurir, navigasi, angkut ringan |

Satu spesialisasi utama dengan pelatihan tambahan adalah rekomendasi, bukan batas karakter final.
Biaya pindah profesi, jumlah profesi, XP, mastery gate, dan kapasitas belum ditetapkan.
Latihan harus relevan dan mencegah farming lewat target sendiri, bangun-hancurkan berulang, atau transfer bolak-balik.

### Konstruksi master dan terraforming

Tahapan: petak tanah → fondasi → dinding/tangga → struktur → medan mengikuti kontur.
Pembangunan menggunakan preview, konfirmasi pemain, material tersedia, validasi server, dan budget volume/waktu.
Tidak menimpa blok/entity, inventory, bangunan, atau claim tanpa aturan izin.
Terraforming membagi pekerjaan besar ke batch terukur; berhenti aman jika material/izin berubah.

### Integrasi ide tambahan — backlog, bukan unlock otomatis

| Kelompok | Cakupan dan keputusan |
|---|---|
| Weapon imbue | Modifikasi moveset/efek serangan yang ada; tanpa handler damage ganda; syarat item dan stacking eksplisit |
| Interaksi elemen | Matriks server: air–api steam, angin–batu deflect, listrik–air konduksi terbatas; tidak instant kill berdasarkan elemen korban |
| Air Leap / Dash | Mobilitas terarah; fall protection terpisah; tidak menambah key per skill |
| Water Ribbon / Spikes | Kandidat pertahanan berarah/kontrol area; bedakan air bertekanan dan es |
| Water Arms Mobility | Perluasan water_arms aktif, bukan sistem paralel |
| Healing / Spirit | Healing sudah planned; Spirit Bending terpisah dan belum lengkap |
| Chi Blocking | Jalur combat Nonbender setelah melee stabil; durasi disable dan resist harus terbatas |
| Earth Tunnel / Dust Step | Tunnel sudah planned; izin/pemulihan terrain diperlukan; Dust Step backlog mobilitas lanjut |
| Bloodbending resist | Escape/resist sebelum kontrol pemain diaktifkan; QTE bukan keputusan final |
| Lightning QoL | Creeper, rod, cuaca, redirect reward: opsi terpisah dan anti-farming; angka usulan belum disahkan |
| Crafting / Traits | Carving Mat dan talent opsional; kondisi fisik karakter tidak dipaksakan secara acak |
| Bloodlines / Avatar succession | Perlu keputusan mode server, persistence dan cap; tidak mengubah Avatar State sekarang |
| Past lives / Boss / Voice chat | Tahap akhir, dependency opsional dan scope tersendiri |
| Tidak masuk gameplay | Patreon adalah distribusi; pink bears/detail pesan terhapus belum cukup spesifikasi |

### Pelaporan status

Pisahkan implemented/build, runtime singleplayer, visual/audio, multiplayer dan persistence.
Label `done` di katalog lama adalah catatan historis implementasi, bukan bukti semua dimensi di atas lolos.

---

## HUD dan GUI — tema gulungan (2026-11-08)

Arah desain disetujui: GUI gulungan perkamen, tinta gelap dan aksen tribe; navigasi modern terinspirasi Essential.
HUD ringkas terinspirasi modularitas RPG-HUD. Kedua mod referensi bukan dependency wajib.
Tema utama AUTO mengikuti tribe; elemen aktif mengubah aksen jurus. Manual/minimal tersedia sebagai preferensi client.
Profil menampilkan tribe, elemen, mastery, profesi dan latihan dari server; tema tidak memberi bonus/unlock.
Material/charge/konstruksi ditampilkan kontekstual saat fiturnya didukung runtime.
Detail tunggal: `UI_THEME_SPEC.md`. Tidak mengubah stat, slot/keybinding atau inventory vanilla.
