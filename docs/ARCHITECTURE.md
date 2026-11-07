# ARCHITECTURE.md — Arsitektur Teknis

## Pembagian client/server

```
Client (Fabric mod)                Server (Fabric mod)
─────────────────────              ──────────────────────────
Keybind + input buffer             Validasi chi, cooldown, damage
Animasi (Epic Fight)               Validasi hitbox dan proyektil
Partikel VFX (client-side)         Perubahan blok (earth wall, lava)
HUD (chi, stamina, cooldown)       State pemain (mastery, progression)
Sound (positional)                 Aturan Avatar State dan sub-bending
Skill timeline rendering           Batas proyektil dan entitas per pemain
```

## Networking

Paket kustom (Fabric Networking API):
- `C2S_SkillInput` — input skill dari client ke server (keybind + slot aktif)
- `S2C_SkillResult` — hasil validasi server ke client (cast / reject + alasan)
- `S2C_HudUpdate` — update chi, cooldown, status ke client
- `S2C_AnimationTrigger` — trigger animasi ke semua client dalam jangkauan

Server adalah authority. Client tidak langsung menerapkan damage atau perubahan blok.

## Penyimpanan

| Data | Lokasi | Format |
|---|---|---|
| Mastery pemain | `PlayerData` NBT via AttachmentType | JSON-serializable |
| Chi dan cooldown | Scoreboard (sementara) → AttachmentType | Integer |
| Skill yang terbuka | AttachmentType (persistent) | Set\<ResourceLocation\> |
| Konfigurasi server | `config/avatar/server.json` | JSON |
| Konfigurasi client | `config/avatar/client.json` | JSON |

## Konfigurasi bersama (satu sumber data)

Semua nilai gameplay (damage, chi cost, cooldown, range, duration) didefinisikan di:
```
mod/src/main/resources/data/avatar/skill_definitions/
mod/src/main/resources/data/avatar/armor_definitions/
mod/src/main/resources/data/avatar/weapon_definitions/
```

Format JSON. Dibaca oleh: kode server (validasi), HUD (display), tooltip item, dan `docs/CONTENT_SPEC.md` (referensi dokumentasi).

## Skill timeline

Setiap skill punya satu `SkillTimeline`:
```
[windup_ticks] → [active_ticks] → [recovery_ticks]
     ↓                ↓                ↓
  animasi mulai    hitbox aktif     animasi selesai
  chi dikurangi    VFX dipancarkan  cooldown dimulai
  suara windup     suara impact     bisa kombo berikutnya
```

Ini memastikan animasi, hitbox, VFX, dan suara berjalan pada waktu yang sama.

## Dependensi mod

| Mod | Versi | Peran |
|---|---|---|
| Fabric API | 1.21.1 | Base API |
| Epic Fight | 21.17.3.1 | Animasi pertarungan |
| WTHIT/JADE | opsional | Debug overlay |

## Struktur package Java

```
com.avatar.elements/
├── AvatarMod.java
├── client/
│   ├── KeyBindings.java
│   ├── HudRenderer.java
│   └── AnimationHandler.java
├── server/
│   ├── SkillValidator.java
│   ├── ChiManager.java
│   └── CombatHandler.java
├── common/
│   ├── skill/
│   │   ├── SkillDefinition.java
│   │   ├── SkillTimeline.java
│   │   └── SkillRegistry.java
│   ├── element/
│   │   └── Element.java
│   ├── data/
│   │   └── PlayerBendingData.java
│   └── network/
│       ├── C2SSkillInputPacket.java
│       └── S2CSkillResultPacket.java
└── content/
    ├── skills/fire/
    ├── skills/water/
    ├── skills/earth/
    ├── skills/air/
    └── weapons/
```
