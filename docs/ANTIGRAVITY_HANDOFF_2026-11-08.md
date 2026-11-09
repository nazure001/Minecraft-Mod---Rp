> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# Handoff: Claude Code → Antigravity IDE
- **Tanggal:** 2026-11-08
- **Branch aktif:** `feat/fabric-scaffold`
- **Dikerjakan oleh:** Claude Code

> Snapshot handoff historis, bukan daftar tugas terkini. Source saat audit sudah memuat handler Air Palm/Air Blast; verifikasi tertunda dilacak di `TASKS.md` T3-3. Mapping Fire aktif adalah Z=Jab, X=Blast, C=Sweep, V=Guard, B=Jet. Jangan memakai prioritas implementasi lama di bawah tanpa membandingkan branch/source saat ini.

---

## Ringkasan pekerjaan session ini

Session ini menyelesaikan **Charge Orb VFX System** (T3-5) dan mendokumentasikan
**skill list lengkap** dari Avatar: TLA + LoK sebagai dasar roadmap implementasi.

---

## Yang sudah selesai (siap di branch)

### 1. Charge Orb System — semua file baru/berubah

| File | Perubahan |
|---|---|
| `mod/src/main/java/.../network/SkillPackets.java` | `S2CPhaseSync` record + `castSerial` field |
| `mod/src/main/java/.../network/SkillNetworking.java` | `castSerials` map, `broadcastPhaseSync()`, `broadcastOrbReset()`, `syncOrbStateToNewWatcher()` |
| `mod/src/main/java/.../network/AvatarServerEvents.java` | `AFTER_RESPAWN` → cancel + reset orb; `JOIN` → sync state ke watcher baru |
| `mod/src/main/java/.../skill/SkillDispatcher.java` | **Tick timeline di sini** (dipindah dari PlayerBendingData), detect transisi IDLE, broadcast semua phase change |
| `mod/src/main/java/.../data/PlayerBendingData.java` | `tickTimeline()` tidak lagi panggil `timeline.tick()`; tambah `clearTimeline()` |
| `mod/src/client/java/.../client/orb/ChargeOrbClientState.java` | State map UUID→OrbState, `interpolatedTicks()`, stale-serial guard |
| `mod/src/client/java/.../client/orb/ChargeOrbRenderer.java` | WorldRenderEvents.AFTER_ENTITIES; UV-sphere; additive blend; skip self hanya saat 1st person |
| `mod/src/client/java/.../client/orb/FirstPersonOrbRenderer.java` | WorldRenderEvents.LAST; `ctx.matrixStack()` + player yaw/pitch rotation; additive blend |
| `mod/src/client/java/.../client/orb/OrbVisualConfig.java` | Opt-in registry: fire_jab WINDUP+ACTIVE, fire_jet WINDUP+ACTIVE, air_blast WINDUP+ACTIVE |
| `mod/src/client/java/.../client/network/ClientNetworkHandler.java` | Receiver untuk S2CPhaseSync → update ChargeOrbClientState |
| `mod/src/client/java/.../client/AvatarElementsClient.java` | Register orb renderers; DISCONNECT+JOIN → clear state |

### 2. Dokumentasi diperbarui

- `docs/CONTENT_SPEC.md` — skill list lengkap semua elemen, cast type definitions, stat JSON untuk fire_blast/fire_stream/lightning_strike/combustion_beam
- `docs/TASKS.md` — T3-5 s/d T3-12 ditambahkan

---

## Status sistem yang perlu verifikasi ulang

Orb terlihat in-game (screenshot dikonfirmasi user), namun dua hal belum diverifikasi
setelah fix terakhir:

1. **Orb hilang setelah skill selesai** — IDLE broadcast fix sudah diapply, belum di-test
2. **Shape glowing sphere** — additive blend sudah diapply, belum di-screenshot

Build terakhir: **BUILD SUCCESSFUL** (semua source 08:41-08:42 sudah masuk JAR 08:43).

Jalankan `.\gradlew runClient` dari `mod/` untuk test.

---

## Task berikutnya yang direkomendasikan

### Prioritas 1: T3-6 — Fire Blast (hold→release)

Ini adalah skill hold-and-release pertama. Arsitektur yang dibutuhkan:

```
Client tekan Z (hold) → C2SHoldStart { skillId } → Server
Server mulai charge state (charge_ticks++/tick)
Client release Z     → C2SHoldRelease { skillId } → Server
Server spawn FireBallEntity ke arah pandang
  - speed = 1.8 blok/tick
  - damage = 7.0 × (charge_ticks / max_charge_ticks)
  - radius = 1.0 + 2.0 × (charge_ticks / max_charge_ticks)
Client: orb membesar via interpolatedTicks() yang sudah ada di ChargeOrbClientState
```

File yang perlu dibuat:
- `SkillPackets.java` — tambah `C2SHoldStart`, `C2SHoldRelease`
- `HoldTimeline.java` — server-side charge state (charge_ticks, max_charge, skillId)
- `FireBallEntity.java` — projectile entity, extends `ProjectileEntity`
- `ElementSlotMap.java` — register fire_blast ke slot X (saat ini slot Z=fire_jab, X=kosong)

### Prioritas 2: T3-9 — Air Blast handler

JSON sudah ada di `config/avatar_elements/skill_definitions.json`.
Hanya perlu tambah case di `SkillDispatcher.dispatch()`:
```java
case "avatar:air_blast" -> AirBlastSkill.tick(player, def);
```
Dan buat `AirBlastSkill.java` (knockback LINE hitbox, mirip FireJabSkill).

### Prioritas 3: T2-8 — Test sinkronisasi dua pemain

Belum pernah diuji. Butuh dedicated server + 2 client untuk verifikasi
chi/cooldown independen dan kombo tidak tertukar antar pemain.

---

## Arsitektur sistem (snapshot)

```
Client presses Z/X/C/V
  → SkillClientHandler.sendSlotCast(slot)
  → C2SSlotCast packet
  → SkillNetworking.registerSlotCastReceiver()
  → ElementSlotMap.getSkillId(element, slot)
  → SkillValidator.validate() + apply()
  → SkillTimeline starts (windup → active → recovery)
  → broadcastPhaseSync() ke semua watcher
  → SkillDispatcher.tick() setiap server tick:
      timeline.tick() → detect phase transition → broadcast
      dispatch() → skill-specific effects (hitbox, particles, SFX)
      timeline.isIdle() → clearTimeline() → broadcast IDLE

Client receives S2CPhaseSync:
  → ChargeOrbClientState.update() (dengan stale-serial guard)
  → ChargeOrbRenderer / FirstPersonOrbRenderer membaca state
  → Orb render berdasarkan OrbVisualConfig.shouldShow(skillId, phase)
```

---

## Konvensi kode

- **SkillId format:** `avatar:skill_name` (lowercase, underscore)
- **Packet naming:** C2S = client→server, S2C = server→client
- **Chi cost** deduct di `SkillValidator.apply()` via `PlayerBendingData`
- **VFX** server-side via `world.spawnParticles()`, client-side via WorldRenderEvents
- **Tidak ada** database, persistence, atau file I/O selain `SkillConfigLoader` (JSON dari jar)
- **Branch policy:** jangan push ke `main`, semua lewat PR

---

## File referensi penting

| File | Isi |
|---|---|
| `docs/CONTENT_SPEC.md` | Semua nilai stat skill (sumber kebenaran) |
| `docs/TASKS.md` | Status task per ID |
| `docs/COMBAT_CONTRACT.md` | Kontrak pengujian per skill |
| `docs/CHARGE_ORB_SPEC.md` | Spesifikasi lengkap sistem orb |
| `docs/DECISIONS.md` | Keputusan arsitektur dan alasannya |
| `mod/src/main/resources/assets/.../models/item/air_staff.json` | Model item air staff |

---

## Yang JANGAN dilakukan

- Jangan push ke `main` atau merge PR tanpa review
- Jangan hapus folder `legacy/` atau `reference/`
- Jangan jalankan server Minecraft atau modify world data
- Jangan commit file world/save
- Jangan hardcode nilai skill — selalu rujuk `CONTENT_SPEC.md`
- Jangan ubah `AGENTS.md` tanpa konfirmasi user

---

## Addendum mandat dan roadmap W — 2026-11-08

Dokumen ini mempertahankan laporan historis Claude; addendum tidak memverifikasi source terbaru atau hasil runtime.
Antigravity kini lead implementasi dan integrasi; ChatGPT review kontrak/source/bukti yang dikirim.
Larangan historis mod/ tidak berlaku untuk mandat A–D. Larangan merusak save, mengubah environment global,
reset perubahan lokal, dan push/merge main tetap berlaku.

Selesaikan A–D dahulu; Fire Blast baru setelah fondasi dan Fire Jab lengkap. Framework hold-release
merupakan prasyarat Fire Blast, bukan sistem yang dibuat ulang per skill. Audit slot aktif sebelum migrasi.
JOIN tidak mencakup seluruh peristiwa mulai tracking; verifikasi watcher yang mendekat saat skill berjalan.
Skill config loader override dan persistence aktual harus diaudit; jangan memakai klaim snapshot “tidak ada persistence”
sebagai batas untuk sistem material/profesi berikutnya.

Sesudah A–D ikuti W1–W7 pada PROJECT_PLAN dan W-01–W-15 pada TASKS.
Dunia dimanipulasi dengan ledger material; utilitas bisa memberi dampak PvP eksplisit; profesi merupakan pilihan latihan.
Kerusakan terrain default, biaya sustain dan profession cap masih TBD, jangan diputuskan diam-diam.
Tiap checkpoint: HEAD/branch, diff, config, build, runtime SP/MP, persistence, visual dan gap.

---

## Addendum UI gulungan — 2026-11-08

Arah pengguna: GUI gulungan dengan aksen tribe, Essential referensi navigasi dan RPG-HUD referensi HUD.
Baca UI_THEME_SPEC.md. Implementasi belum dilakukan pada update dokumen ini.
Prioritas A–D dan roadmap W tetap; jalur UI dasar bisa menyusul setelah checkpoint aktif tanpa menunggu semua profesi.
Lead menjaga data server/client terpisah, config satu sumber, aset original dan tidak menambah dependency reference.
Gabungkan addendum ini dengan perubahan agent terbaru; jangan menimpa diff lokal atau status pengujian.
