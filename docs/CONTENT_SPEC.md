# CONTENT_SPEC.md — Spesifikasi Gameplay (Sumber Kebenaran)

> Semua nilai di dokumen ini menjadi referensi untuk kode server, HUD, tooltip, dan dokumentasi.
> Perubahan nilai harus disetujui dan dicatat di `DECISIONS.md`.

## Struktur setiap skill

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | ResourceLocation | `avatar:fire_jab` |
| `element` | Enum | FIRE / WATER / EARTH / AIR |
| `mastery_required` | int | Level mastery minimum (0–5) |
| `chi_cost` | int | Chi saat cast |
| `chi_per_tick` | int | Chi per tick saat channeling (0 jika tidak ada) |
| `cooldown_ticks` | int | Cooldown setelah cast |
| `windup_ticks` | int | Ticks sebelum hitbox aktif |
| `active_ticks` | int | Ticks hitbox aktif |
| `recovery_ticks` | int | Ticks setelah active sebelum bisa kombo |
| `damage` | float | Damage base |
| `range` | float | Jangkauan hitbox (blok) |
| `hitbox_shape` | Enum | SPHERE / ARC / LINE / CONE |
| `knockback` | float | Kekuatan dorongan |
| `cancel_on_hit` | bool | Apakah dibatalkan saat terkena serangan |
| `combo_window_ticks` | int | Ticks setelah recovery di mana kombo berikutnya bisa masuk |

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
  "mastery_required": 1,
  "chi_cost": 25,
  "cooldown_ticks": 30,
  "windup_ticks": 1,
  "active_ticks": 1,
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

## Air (Air)

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
  "chi_cost": 20,
  "cooldown_ticks": 20,
  "windup_ticks": 6,
  "active_ticks": 1,
  "recovery_ticks": 10,
  "damage": 10.0,
  "range": 12.0,
  "hitbox_shape": "SPHERE",
  "knockback": 1.5,
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

## Air (Water)

### Water Whip
```json
{
  "id": "avatar:water_whip",
  "element": "WATER",
  "mastery_required": 0,
  "chi_cost": 12,
  "cooldown_ticks": 10,
  "windup_ticks": 3,
  "active_ticks": 5,
  "recovery_ticks": 5,
  "damage": 5.0,
  "range": 6.0,
  "hitbox_shape": "LINE",
  "knockback": 0.8,
  "combo_window_ticks": 8
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
  "active_ticks": 60,
  "recovery_ticks": 8,
  "damage": 7.0,
  "range": 24.0,
  "hitbox_shape": "SPHERE",
  "knockback": 1.0,
  "combo_window_ticks": 0,
  "cast_type": "HOLD_RELEASE",
  "max_charge_ticks": 40,
  "projectile_speed": 1.8
}
```

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
