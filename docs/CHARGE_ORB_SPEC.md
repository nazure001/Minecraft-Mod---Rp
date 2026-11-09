> Revisi desain 2026-11-08: bagian tambahan di akhir dokumen menjadi acuan untuk perluasan W. Status historis tetap dipertahankan; tidak ada implementasi atau uji baru yang diklaim.

# Charge Orb System — Spesifikasi Final

**Status dokumen:** Proposal historis 2026-11-07. Addendum koreksi di bagian akhir mengesampingkan bagian yang bertentangan; implementasi/runtime terbaru harus diverifikasi dari source dan `TASKS.md`.

## Snapshot renderer aktif — 2026-11-08

- Orb ditampilkan hanya untuk skill yang terdaftar di `OrbVisualConfig`: `fire_jab` (WINDUP/ACTIVE), `fire_blast` (WINDUP/HOLD), `fire_jet` (WINDUP/ACTIVE), dan `air_blast` (WINDUP/ACTIVE).
- Third-person mengikuti `KnuckleVfxHelper` untuk client player; fallback player memakai offset berbasis yaw.
- First-person memakai offset relatif kamera dan rotasi yaw/pitch, bukan transform tangan PAL. Ukuran Fire Blast diatur khusus hingga 40 tick.
- Packet phase dan renderer sudah ada di source. Daftar optik lama di bawah merupakan proposal; bukan bukti semua ukuran, tracking, dan lifecycle sudah diuji.

---

## Keputusan Arsitektur (dari ChatGPT)

| Aspek | Keputusan |
|---|---|
| Multiplayer | Orb terlihat pemilik **dan** pemain lain, state disetujui server |
| Kapan muncul | Saat skill masuk fase **WINDUP** (charging), bukan saat idle memilih elemen |
| Posisi | Mengikuti attachment tangan per jurus (dari COMBAT_CONTRACT field 2) |
| Saat dilempar | Transisi per jurus: ditembak / dilebur ke serangan / dipadamkan |
| Saat cancel | Efek menghilang singkat (dissolve), **tidak ada damage** |
| 1st person | **Prioritas tinggi** — harus selesai bersamaan dengan 3rd person |
| Listrik | Kandidat visual sub-elemen; **bukan** elemen playable ke-5 |
| Chi saat cancel | Ikuti aturan cast yang sudah ada di pipeline, tidak ada refund baru |

### Koreksi Arsitektur Penting

**`OrbEntity` TIDAK diperlukan untuk fase charge.**
State charge tersinkron via packet yang sudah ada (`S2CPhaseSync`) + renderer
client-side cukup untuk orb yang menempel di tangan. `OrbEntity` / `OrbProjectile`
hanya dibuat saat orb benar-benar dilepas sebagai objek terbang dengan
collision dan lifetime sendiri.

**1st person dirender di viewmodel space, bukan HUD overlay.**
Orb harus terlihat seperti digenggam di tangan, ukuran dan posisi tidak
menutupi bidikan. Bukan billboard yang ikut cursor.

**Orb tidak universal.**
Fire Jab, Water Whip, dan staff attack punya bahasa visual sendiri.
Tidak semua skill harus diawali bola elemen — orb hanya untuk skill
yang memang punya fase charge.

---

## Visual Per Elemen

| Elemen | Orb Visual |
|---|---|
| **Api** | Bola api berputar, partikel flame melingkar, glow oranye |
| **Udara** | Sphere transparan, cincin angin berputar horizontal, partikel cloud |
| **Listrik** | Bola biru/putih, petir kecil keluar ke segala arah — visual sub-elemen, belum playable |
| **Air** | Bola air, droplet mengorbit, efek riak |
| **Tanah** | Bongkahan batu berputar mengelilingi inti |

---

## Arsitektur Teknis Final

```
SkillTimeline (server)
  WINDUP → kirim S2CPhaseSync(skillId, WINDUP, casterUUID)
  ACTIVE → kirim S2CPhaseSync(skillId, ACTIVE, casterUUID)
  RECOVERY/cancel → kirim S2CPhaseSync(skillId, RECOVERY/IDLE, casterUUID)

ChargeOrbClientState (client)
  per-player map: UUID → OrbState { phase, element, ticksIn }
  update dari S2CPhaseSync packet

ChargeOrbRenderer (client, WorldRenderEvents.AFTER_ENTITIES)
  untuk setiap OrbState yang WINDUP/ACTIVE:
    1. ambil player entity dari UUID
    2. hitung posisi orb dari PAL right_arm bone world pos + tangan offset
    3. render sphere mesh + particle ring sesuai element
    4. scale berdasarkan ticksIn (orb membesar saat charge)

FirstPersonOrbRenderer (client, GameRenderer mixin atau ItemRenderer mixin)
  hanya untuk client player sendiri
  render orb di viewmodel space (ikut tangan kanan, bukan cursor)
  posisi: offset dari kamera + arm transform, natural digenggam
  tidak menutupi crosshair

OrbProjectile extends ProjectileEntity (server + client)
  hanya spawn saat skill cast melempar orb (bukan semua skill)
  punya velocity = player.getRotationVec() * projectile_speed
  punya collision handler → impact VFX packet
```

### Packet yang Dibutuhkan

| Packet | Arah | Isi |
|---|---|---|
| `S2CPhaseSync` | Server→Client | skillId, phase, casterUUID, ticksIn — **sudah ada di TASKS** |
| `S2COrbImpact` | Server→Client | position, element, skill_id — baru |

`S2CPhaseSync` adalah dependency ChargeOrbClientState. Packet dan renderer sudah ada di source saat audit; penyelesaian visual/lifecycle tetap harus diuji di Minecraft.

---

## Urutan Implementasi

```
1. S2CPhaseSync packet (server kirim phase ke semua client nearby; sudah ada)
   → Claude Code

2. ChargeOrbClientState (client-side state dari packet)
   → Claude Code

3. ChargeOrbRenderer 3rd person — Fire element dulu
   → Claude Code (sphere + partikel flame)

4. FirstPersonOrbRenderer — Fire element
   → Claude Code (viewmodel space)

5. Test fire_jab: orb muncul saat WINDUP, held saat ACTIVE, hilang saat RECOVERY
   → User

6. OrbProjectile (opsional per skill, bukan semua)
   → Claude Code setelah langkah 5 verified

7. Visual elemen lain (Air, Water, Earth)
   → Claude Code setelah Fire pipeline terbukti
```

---

## Skill yang Butuh Charge Orb (Prioritas)

| Skill | Orb | Catatan |
|---|---|---|
| `avatar:fire_jab` | Api kecil | Opt-in demo/prototipe; bukan jurus charge wajib |
| `avatar:fire_jet` | Api besar | Entri historis; Fire Jet saat ini adalah dash, bukan projectile |
| `avatar:air_blast` | Udara | Orb sphere transparan |
| `avatar:water_whip` | Air | Bukan orb — whip shape, visual berbeda |
| `avatar:air_staff_attack` | Tidak | Pakai trail angin, tidak perlu orb |

---

## Ketergantungan

- **PAL `right_arm` bone world position** — dibutuhkan untuk posisi orb akurat.
  Saat ini belum ada query API. Perlu dicek apakah PAL expose world matrix bone.
- **Animasi tangan final (Antigravity)** — agar posisi orb sinkron dengan gerakan.
  Bisa diimplementasi tanpa ini, dengan fallback `player.getHandPos()` approximate.
- **`S2CPhaseSync` packet** — sudah ada di source; validasi lifecycle/late-watcher masih perlu dicatat terpisah.

---

## Klarifikasi manipulasi dan utilitas — 2026-11-08

Bagian ini mengoreksi contoh prototipe sebelumnya: Fire Jet adalah dash, bukan projectile besar.
Fire Blast HOLD_RELEASE merupakan kandidat utama charge orb. Orb pada Fire Jab, jika dipakai untuk demo,
berstatus efek prototipe opt-in dan tidak menjadikan Jab jurus charge wajib.
WINDUP/ACTIVE tidak otomatis berarti charging; gunakan visual config dan state kemampuan aktual.

Orb charge yang mengikuti tangan adalah visual client dari state server, bukan entity material baru.
Material terkendali untuk air/tanah/lava harus punya sumber dan ledger sebelum visual ditampilkan sebagai material nyata.
Orb tidak menciptakan persediaan air/lava. Renderer bukan authority damage, resource, atau transaksi world.
Air riding dan konstruksi wall tidak memerlukan orb hanya karena durasinya panjang.
First person gunakan attachment tangan/viewmodel yang terverifikasi; third person gunakan transform player yang sama acuannya.
Saat release/cancel/finish, serial dan lifecycle menghapus efek lama; observer baru tersinkron ketika mulai tracking.
