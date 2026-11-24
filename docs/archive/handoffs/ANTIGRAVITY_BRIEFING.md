> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# Briefing untuk Antigravity — Pipeline Animasi & VFX

Dokumen ini adalah panduan kolaborasi dari Claude Code untuk Antigravity,
berdasarkan hasil audit library dan referensi mod (Epic Fight, avatarmod, EFMCompat, Sword Soaring).

---

## Keputusan Arsitektur

### Runtime animasi: Player Animation Library (PAL)
- Library: `com.zigythebird.playeranim:PlayerAnimationLibFabric:1.1.6+mc.1.21.1`
- **Sudah terpasang** di `build.gradle`
- PAL memainkan file animasi `.animation.json` Blockbench/Bedrock langsung di player model
- Ini artinya: animasi dibuat di Blender → export ke Blockbench → `.animation.json` → PAL memainkannya di Minecraft

### VFX: 100% custom Fabric
- Trail ribbon, impact flash, aura elemen, partikel bending — semua dibuat dari nol
- Format trail mengacu pada EFMCompat (dua titik lokal pada bone + jendela waktu)
- Tidak ada dependency eksternal untuk VFX

### Target kualitas: setara atau melebihi Epic Fight
Epic Fight tampak premium karena kualitas animasinya, bukan engine-nya. Pipeline kita secara teknis setara — hasilnya ditentukan oleh kualitas animasi Blender dan kerapian VFX.

---

## Hierarki Bone yang Dibutuhkan

Vanilla Minecraft hanya punya 6 bone (head, body, rightArm, leftArm, rightLeg, leftLeg).
PAL memungkinkan bone kustom. Hierarki yang dibutuhkan:

```
root
├── torso
│   ├── head
│   ├── right_upper_arm
│   │   └── right_forearm
│   │       └── right_hand
│   │           └── Tool_R          ← attachment point senjata/efek
│   └── left_upper_arm
│       └── left_forearm
│           └── left_hand
│               └── Tool_L
├── right_leg
│   └── right_shin
└── left_leg
    └── left_shin
```

**Prioritas minimum untuk fire_jab:**
`torso`, `right_upper_arm`, `right_forearm`, `right_hand` sudah cukup.

**Untuk staff thrust:**
Tambah `Tool_R` sebagai child dari `right_hand` — ini yang menggantikan display transform statis di `air_staff.json`.

---

## Format Animasi

### Export dari Blender → Blockbench → `.animation.json`
PAL menggunakan format animasi Bedrock (sama dengan yang sudah dipakai di Blockbench).

Contoh struktur file:
```json
{
  "format_version": "1.8.0",
  "animations": {
    "animation.avatar.fire_jab": {
      "animation_length": 0.45,
      "bones": {
        "right_upper_arm": {
          "rotation": {
            "0.00": [0, 0, 0],
            "0.10": [-35, 10, 5],
            "0.25": [15, -5, 0],
            "0.45": [0, 0, 0]
          }
        },
        "right_forearm": {
          "rotation": {
            "0.00": [0, 0, 0],
            "0.10": [-20, 0, 0],
            "0.25": [10, 0, 0],
            "0.45": [0, 0, 0]
          }
        }
      }
    }
  }
}
```

**Timing yang sudah ditetapkan** (dari `SkillTimeline` + `skill_definitions.json`):
| Fase | Durasi | Catatan |
|---|---|---|
| Windup | 2 tick = 0.10 detik | Antisipasi, lengan ke belakang |
| Active | 3 tick = 0.15 detik | Strike, impact di tick ke-2 |
| Recovery | 4 tick = 0.20 detik | Kembali ke idle |
| Total | 9 tick = 0.45 detik | |

---

## Spesifikasi per Animasi (Prioritas)

### 1. Fire Jab (`animation.avatar.fire_jab`) — PRIORITAS 1

**Karakter gerakan:** Jab cepat khas bending api — bukan pukulan karate. Bertumpu pada pinggul, bahu, diakhiri lecutan pergelangan.

**3 fase:**
- **Windup (0.00–0.10s):** Bahu kanan tarik ke belakang ~35°, torso putar -15° (kanan), siku bengkok masuk
- **Strike (0.10–0.25s):** Lengan lepas ke depan, pergelangan snap, torso ikut +20° ke kiri, kaki belakang tekan tanah
- **Recovery (0.25–0.45s):** Kembali smooth ke ready pose (bukan idle)

**Titik impact VFX:** posisi `right_hand` tip saat frame strike (0.15s).

**Catatan pose:** Setelah recovery selesai, kembali ke **Sikap Siaga** (ready pose yang sudah ada di handoff), bukan idle Minecraft.

---

### 2. Staff Thrust (`animation.avatar.air_staff_thrust`) — PRIORITAS 2

Dikerjakan setelah fire_jab terverifikasi di game.

**Karakter gerakan:** Tusukan dengan tongkat airbender — bukan tikaman pedang. Tubuh lean ke depan, kedua tangan mendorong tongkat seperti tombak, ada momen "lock" sebelum kembali.

**Timing:**
| Fase | Durasi |
|---|---|
| Windup | 1 tick = 0.05s |
| Active | 2 tick = 0.10s |
| Recovery | 3 tick = 0.15s |

**Tool_R attachment:** Tongkat harus bergerak bersama `right_hand` → `Tool_R`. Pivot `Tool_R` = di area grip pergelangan kanan. Ujung tongkat adalah trail tip.

**Trail:** Dua titik pada `Tool_R` — tip (`[0, 30, 0]`) dan base grip (`[0, 21.5, 0]`), aktif selama fase Active, fade 4 tick.

---

## Spesifikasi VFX (untuk referensi koordinasi)

Antigravity tidak perlu implement VFX — tapi perlu menyediakan titik attachment-nya:

| Animasi | VFX | Attachment point |
|---|---|---|
| fire_jab | Burst partikel api saat hit | `right_hand` tip |
| fire_jab | Lecutan api kecil saat strike | `right_forearm` |
| air_staff_thrust | Trail abu-abu angin | `Tool_R` tip & base |
| air_staff_thrust | Impact "pop" angin | `Tool_R` tip |

Format trail yang akan dipakai Claude Code:
```json
"trail": {
  "begin_pos": [0.0, 30.0, 0.0],
  "end_pos":   [0.0, 21.5, 0.0],
  "start_tick": 0,
  "end_tick": 2,
  "fade_ticks": 4,
  "color": [170, 170, 255]
}
```

---

## Yang TIDAK perlu dikerjakan Antigravity

- Collider / hitbox (Claude Code yang handle, berbasis `SkillTimeline`)
- Networking / sync (sudah ada di `SkillNetworking.java`)
- Item model `air_staff.json` display transform (sudah selesai, posisi grip terkonfirmasi)
- Skill tree / progression system
- Render pipeline / shader

---

## Alur Handoff

```
Antigravity selesai animasi fire_jab (.animation.json)
  → letakkan di: art-source/animations/fire_jab.animation.json
  → Claude Code mengintegrasikan ke PAL + SkillTimeline
  → User uji di game
  → Jika OK → lanjut ke staff_thrust
  → Jika perlu revisi → Antigravity adjust timing/rotation
```

**File yang sudah ada sebagai referensi:**
- `art-source/animation_studies/staff_thrust/CLAUDE_READY_POSE_HANDOFF.md` — data bone yang sudah divalidasi
- `art-source/animation_studies/staff_thrust/player_staff_thrust_ready_artistic.bbmodel` — model terbaru
- `docs/COMBAT_CONTRACT.md` — spesifikasi lengkap 7 field per skill

---

## Catatan Teknis Penting

1. **Rotasi order:** ZYX (sesuai handoff) untuk konsistensi dengan Blockbench
2. **Satuan waktu:** detik (bukan tick) di file `.animation.json`, tapi desain dalam tick lalu konversi (÷20)
3. **Kecepatan animasi:** PAL bisa disesuaikan `speed` multiplier saat runtime — desain di kecepatan natural, Claude Code akan menyesuaikan ke `SkillTimeline` tick
4. **Idle/ready pose:** Jangan bake idle animation ke file animasi skill — ready pose dihandle oleh mixin terpisah
5. **Smooth lerp:** PAL punya blending otomatis — tidak perlu pose transisi manual antara idle dan skill start

---

## Mandat terbaru dan scope — 2026-11-08

Antigravity mengambil alih implementasi karena Claude sementara berhenti. Pembatasan historis
jangan mengubah mod/ dicabut untuk scope A–D; jangan mengubah environment global, save pengguna atau main.
Lead memegang file bersama/networking/dispatcher/Gradle/config; agent paralel memiliki modul/worktree terpisah.
A orb lifecycle → B rig/runtime → C Fire Jab lengkap → D hold-release + Fire Blast tetap prioritas.

PAL adalah kandidat yang dilaporkan dipasang, bukan bukti bahwa hierarki siku di atas otomatis didukung.
Buktikan bending/skin/sleeve, attachment, blending dan reset sebelum ekspor final. Blender opsional.
Fire Jab tangan kosong memakai ready tersendiri, bukan staff ready. Bedakan pivot model-space, rotasi parent-local,
dan attachment local/world. Tool_R pada grip memerlukan konversi titik trail lama dari pangkal tongkat.
Timing dinyatakan absolut sejak cast dan relatif fase secara eksplisit; jangan menggeser damage agar cocok preview tanpa review.

Agent motion boleh merapikan blocking Fire Jab sambil runtime dibuktikan. Agent orb menangani cleanup/tracking.
Desain W (material, utilitas PvP, profesi) dapat dicatat; implementasi setelah gate A–D, bukan perluasan diam-diam.
Tidak ada izin menyalin aset reference atau mengklaim fitur selesai hanya karena build sukses.

---

## Brief UI tambahan — 2026-11-08

Arah visual baru: gulungan perkamen bertema tribe, bukan panel gelap Essential sebagai tema utama.
Essential hanya referensi navigasi/settings; RPG-HUD referensi HUD modular. Keduanya bukan dependency wajib.
Baca UI_THEME_SPEC.md, UI-01–UI-10 pada TASKS dan acceptance UI pada TESTING.
Jangan menggeser A–D. Agent desain boleh membuat wireframe/aset original dengan kepemilikan file jelas;
implementasi UI setelah checkpoint aktif dan kontrak data tersedia. Theme AUTO/manual/minimal satu sistem.
Tidak mengubah inventory/keybind combat atau menambah fitur sosial/account Essential.
