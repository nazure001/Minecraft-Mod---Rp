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
