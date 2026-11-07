# Combat Contract — Avatar: Elements Mod

Dokumen ini mendefinisikan kontrak visual combat untuk setiap skill.
Semua timing mengacu pada `SkillTimeline` (tick = 1/20 detik).
Pipeline ini harus terbukti berfungsi pada satu skill lengkap sebelum diperluas.

---

## Format Kontrak Per Skill

Setiap skill harus mendefinisikan 7 field berikut:

| Field | Deskripsi |
|---|---|
| **1. animation_id & timing** | Clip ID animasi + durasi fase (windup/active/recovery dalam tick) |
| **2. weapon_attachment** | Bone Tool_R offset (posisi & rotasi relatif terhadap Hand_R) |
| **3. trail_points** | Dua titik lokal pada model untuk membentuk trail (tip & base) |
| **4. trail_window** | Tick mulai/berhenti trail relatif terhadap fase ACTIVE + durasi fade (tick) |
| **5. damage_window** | Tick awal & akhir hitbox aktif relatif terhadap fase ACTIVE (server-side) |
| **6. impact_vfx_sfx** | Particle type, suara, dan kondisi trigger saat hit |
| **7. finish_cancel_rules** | Kondisi selesai normal, kondisi pembatalan, state reset |

---

## Referensi Format Trail (dari EFMCompat audit)

Format yang diadopsi dari `EFMCompat item_skin + per-animation trail`:

```json
// Dalam skill_definitions.json atau file terpisah, per skill:
"trail": {
    "begin_pos": [0.0, 0.5, 0.0],
    "end_pos":   [0.0, -0.3, 0.0],
    "start_tick": 0,
    "end_tick": 2,
    "fade_ticks": 3,
    "color": [255, 100, 20],
    "texture": "avatar_elements:textures/particle/fire_trail.png"
}
```

- `begin_pos` / `end_pos` — titik lokal pada bone referensi (Tool_R atau Hand_R)
- `start_tick` / `end_tick` / `fade_ticks` — relatif dari awal fase ACTIVE

---

## Catatan Arsitektur Pose (dari avatarmod audit)

avatarmod Fabric tidak memakai PAL. Ia memakai `Rig` wrapper + `BendingPoses.apply()`:

```
BipedEntityModelMixin @Inject TAIL
  └── BendingPoses.apply(rig, entity, phase, ticksIn)
        └── dispatch per technique (airBlast, airBall, fireJab, ...)
              └── rig.rightArm(pitch, yaw, roll, weight)
                  rig.twist(angle, weight)
                  rig.finish()
```

AnimPhase mapping ke SkillTimeline proyek:
- avatarmod `WINDUP` → proyek `WINDUP`
- avatarmod `SUSTAIN` → proyek `ACTIVE`
- avatarmod `RELEASE` → proyek `RECOVERY`

PAL tetap tersedia untuk animasi keyframe halus di fase berikutnya (sudah ada di build.gradle).
Untuk fire_jab PoC: pakai Rig pattern, bukan PAL.

---

## STATUS IMPLEMENTASI

Legenda:
- `[ ]` Belum ada — perlu dibuat
- `[~]` Ada sebagian — definisi ada, belum ada animasi/trail/VFX
- `[x]` Selesai dan terverifikasi di game

---

## avatar:fire_jab — PRIORITAS 1 (Prove first)

> Fire Jab adalah skill yang harus dibuktikan lengkap sebelum skill lain ditambahkan.
> Semua 7 field harus `[x]` sebelum lanjut ke Staff Thrust.

### 1. Animation ID & Timing

```
clip_id    : avatar:fire_jab
windup     : 2 tick  → SkillTimeline.WINDUP  (frames 0–2)
active     : 3 tick  → SkillTimeline.ACTIVE  (frames 2–5)
recovery   : 4 tick  → SkillTimeline.RECOVERY (frames 5–9)
total      : 9 tick  (0.45 detik)
```

Keyframes Blender/Blockbench:
- Frame 0 (neutral): pose idle
- Frame 2 (cocked): rightArm pitch –1.2 rad (~70°), elbow bend –0.6 rad
- Frame 3 (strike): rightArm pitch –0.1 rad, elbow extend 0, body yaw +0.15 rad
- Frame 9 (return): kembali ke neutral

Status animasi: `[~]` PAL pipeline terbukti (fire_jab_test.json bergerak di game 2026-11-07). Animasi final menunggu Antigravity.

### 2. Weapon Attachment

Untuk fire_jab: tidak ada senjata di tangan. Attachment bola api muncul di
posisi `Hand_R` bone.

```
bone       : Hand_R  (tidak ada Tool_R untuk skill ini)
vfx_anchor : posisi world Hand_R tip saat frame 3 (strike)
```

Status: `[ ]` Hand_R world position query belum diimplementasi (PAL terpasang dan terverifikasi)

### 3. Trail Points

Fire Jab tidak menghasilkan trail fisik. Sebagai gantinya, impact flash pada hit.

```
trail_tip  : Hand_R tip (offset: [0, 0.5, 0] dari Hand_R pivot)
trail_base : Elbow_R (offset: [0, 0, 0])
```

Status: `[ ]`

### 4. Trail Window

```
start_tick : ACTIVE + 0  (tick ke-2 dari awal skill)
stop_tick  : ACTIVE + 2  (tick ke-4 dari awal skill)
fade_ticks : 3
```

Status: `[ ]`

### 5. Damage Window (server-side)

Dari `skill_definitions.json`:
```
phase      : ACTIVE
start_tick : ACTIVE + 0  (server authoritative)
end_tick   : ACTIVE + 3  (= activeTicks)
hitbox     : SPHERE, radius 2.5 blok di depan player
damage     : 4.0
knockback  : 0.3
```

Status: `[~]` SkillDispatcher sudah ada, hitbox SPHERE sudah ada. Timing
sudah mengikuti `activeTicks` dari JSON. Yang belum: sync ke animasi frame.

### 6. Impact VFX / SFX

```
particle   : minecraft:flame (burst 8–12 partikel)
particle_pos: posisi Hand_R tip saat hit
sound      : entity.blaze.shoot (pitch 1.4, volume 0.6)
trigger    : setiap entity yang terkena dalam damage_window
no_hit     : tidak ada VFX jika tidak ada target
```

Status: `[ ]` belum ada impact particle dan suara

### 7. Finish & Cancel Rules

```
finish     : recoveryTicks habis → kembali ke IDLE, chi dikurangi
cancel     : player di-stagger (damage diterima > 2.0) selama WINDUP/ACTIVE
             → potong animasi ke frame recovery-start, skip sisa active
cancel_chi : tidak dikembalikan jika sudah masuk ACTIVE
reset      : mati → reset semua phase ke IDLE, bersihkan trail
```

Status: `[~]` IDLE/WINDUP/ACTIVE/RECOVERY state machine ada.
Cancel on stagger belum diimplementasi.

---

## avatar:air_staff_attack — PRIORITAS 2 (Staff Thrust)

> Dikerjakan setelah fire_jab semua field `[x]`.

### 1. Animation ID & Timing

```
clip_id    : avatar:air_staff_thrust
windup     : 1 tick
active     : 2 tick
recovery   : 3 tick
total      : 6 tick (0.3 detik)
```

Keyframes: staff thrust ke depan, body lean +10°, kembali ke ready pose.

Status: `[ ]`

### 2. Weapon Attachment

```
bone       : Tool_R (custom bone, perlu ditambah ke armature PAL)
offset_pos : [0, -0.5, 0.8]  — ujung staff di depan tangan
offset_rot : [0, 0, 0]       — align dengan sumbu lengan
```

Ini adalah migrasi dari `thirdperson_righthand` display transform JSON ke
bone attachment yang di-animate. Saat PAL terpasang, display transform
JSON menjadi fallback saja.

Status: `[ ]`

### 3. Trail Points

```
trail_tip  : Tool_R tip  (offset: [0, 0, 1.2] dari Tool_R pivot)
trail_base : Tool_R base (offset: [0, 0, -0.3] dari Tool_R pivot)
```

Status: `[ ]`

### 4. Trail Window

```
start_tick : ACTIVE + 0
stop_tick  : ACTIVE + 2
fade_ticks : 4
trail_color: 0xAAAAFF (abu-abu udara)
```

Status: `[ ]`

### 5. Damage Window

```
phase      : ACTIVE
start_tick : ACTIVE + 0
end_tick   : ACTIVE + 2
hitbox     : SPHERE, radius 2.0 blok
damage     : 3.0
knockback  : 0.4
```

Status: `[~]`

### 6. Impact VFX / SFX

```
particle   : minecraft:cloud (burst 6 partikel)
particle_pos: Tool_R tip saat hit
sound      : entity.player.attack.sweep (pitch 1.2)
trigger    : setiap entity terkena dalam damage_window
```

Status: `[ ]`

### 7. Finish & Cancel Rules

```
finish     : kembali ke ready pose (Sikap Siaga mixin aktif kembali)
cancel     : tidak bisa cancel selama ACTIVE (terlalu singkat)
reset      : sama dengan fire_jab
```

Status: `[~]`

---

## Skill Lain (belum boleh dikerjakan)

Skill berikut belum boleh ditambah kontrak atau diimplementasi sampai
`fire_jab` dan `air_staff_attack` sudah `[x]` semua field.

- `avatar:flame_sweep`
- `avatar:fire_jet`
- `avatar:fire_guard`
- `avatar:air_palm`
- `avatar:air_blast`
- `avatar:water_whip`
- `avatar:earth_boulder`
- `avatar:air_vortex`

---

## Referensi Arsitektur

- **EFMCompat** (tidak ada di reference/) — konfigurasi weapon type dan trail.
  Perlu dikonfirmasi lokasi file ke ChatGPT/User.
- **Sword Soaring** (tidak ada di reference/) — contoh skill dengan entity,
  animation, collider, networking, berbasis Epic Fight.
- **Epic Fight JAR** (`reference/epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`) —
  NeoForge only, hanya referensi konsep armature. Jangan install ke Fabric.
- **PAL** (`com.zigythebird.playeranim:PlayerAnimationLibFabric:1.1.6+mc.1.21.1`) —
  library animasi terpilih, belum ditambah ke `build.gradle`.

---

## Catatan Pipeline

Urutan implementasi yang wajib diikuti:

```
1. Tambah PAL ke build.gradle + verifikasi build
2. Buat armature JSON: Head, Body, Arm_R/L, Elbow_R/L, Hand_R/L
3. Buat animasi fire_jab di Blockbench (3 keyframe, 9 tick)
4. Hubungkan ke SkillTimeline → semua 7 field fire_jab [x]
5. Tambah Tool_R bone ke armature
6. Buat animasi air_staff_thrust di Blockbench
7. Hubungkan → semua 7 field air_staff_attack [x]
8. Baru boleh lanjut ke skill lain
```
