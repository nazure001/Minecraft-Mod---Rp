# Charge Orb System — Spesifikasi untuk Review ChatGPT

Dokumen ini mendefinisikan sistem visual "charge orb" sebelum skill dilempar.
Tujuan: sinkron 1st/3rd person, orb mengikuti cursor, animasi tangan relevan dengan arah lempar.

**Status:** Draft — menunggu persetujuan ChatGPT sebelum implementasi Claude.

---

## Konsep Utama

Setiap elemen punya "charge orb" yang muncul di tangan player saat skill WINDUP,
tetap di tangan saat ACTIVE, lalu terlempar/meledak saat recovery atau saat skill hit.

```
IDLE → [tekan skill] → WINDUP (orb spawn di tangan) → ACTIVE (orb held, siap lempar)
     → cast arah cursor → orb terbang → hit → impact VFX
     → RECOVERY → IDLE
```

---

## Visual Per Elemen

| Elemen | Orb Visual | Referensi |
|---|---|---|
| **Api** | Bola api berputar, partikel flame melingkar, glow oranye | Blaze fireball, tapi spherical |
| **Udara** | Sphere transparan, cincin angin berputar horizontal, partikel cloud | Avatar airbending sphere |
| **Listrik** | Bola biru/putih, petir kecil keluar ke segala arah saat digenggam | Chidori (Naruto) |
| **Air** | Bola air, droplet mengorbit, efek riak | Waterbending ball |
| **Tanah** | Bongkahan batu berputar mengelilingi inti | Earthbending rock |

---

## Arsitektur Teknis (Proposal Claude)

### Komponen

```
OrbEntity (server + client)
  └── tethered ke PlayerEntity via tether_id
  └── state: CHARGING | HELD | FLYING | DEAD

OrbRenderer (client only)
  └── WorldRenderEvents.AFTER_ENTITIES
  └── render sphere + particle ring berdasarkan element

FirstPersonOrbOverlay (client only)
  └── HudRenderCallback (atau WorldRenderEvents.AFTER_TRANSLUCENT)
  └── billboard quad di depan kamera, ikut pitch/yaw player
  └── sync state dengan OrbEntity milik client player

OrbBehavior (server)
  └── dipanggil oleh SkillTimeline saat phase transition
  └── WINDUP → spawn OrbEntity di koordinat tangan player
  └── ACTIVE → update tether setiap tick
  └── cast → setVelocity ke arah player.getRotationVec()
  └── hit → impact VFX packet ke semua client nearby
```

### Attachment ke Tangan

Posisi orb server-side: `player.getPos() + player.getHandPos_approx()`

Posisi orb client-side (akurat): via PAL `right_arm` bone world position
- Diambil setelah PAL selesai compute pose frame
- Offset dari `right_arm` pivot ke ujung tangan: `+[0, -6, 0]` (blok)

### 1st Person Sync

1st person overlay dirender sebagai billboard quad di `near plane + 0.5 blok`.
Posisi ikut `player.getRotationVec()` × jarak genggam (0.6 blok dari kamera).
Size orb disesuaikan FOV agar terlihat natural.

Efek orb (partikel melingkar) dirender di world space di titik yang sama,
sehingga 3rd person spectator melihat orb di tangan, 1st person melihat orb di depan tangan.

---

## Pertanyaan untuk ChatGPT

Mohon jawab sebelum Claude mulai implementasi:

**1. Urutan prioritas skill yang butuh orb:**
- [ ] A: fire_jab dulu (satu skill, prove pipeline)
- [ ] B: semua Fire skill sekaligus
- [ ] C: satu skill per elemen sekaligus

**2. Kapan orb muncul:**
- [ ] A: hanya saat WINDUP (orb = charging indicator)
- [ ] B: saat WINDUP + tetap di ACTIVE sampai dilempar
- [ ] C: sudah ada di tangan saat idle (persistent orb)

**3. Apakah orb visible ke player lain di multiplayer:**
- [ ] A: Ya, semua bisa lihat (OrbEntity = real entity di dunia)
- [ ] B: Tidak, hanya cosmetic client-side

**4. Cancel behavior:**
- [ ] A: Orb langsung hilang (pop) jika skill di-cancel
- [ ] B: Orb dissolve animation sebelum hilang
- [ ] C: Orb jatuh ke tanah jika cancel saat ACTIVE

**5. Orb saat dilempar:**
- [ ] A: Menjadi projectile entity (OrbProjectile)
- [ ] B: Orb hilang di tangan, efek terpisah (tidak ada projectile terlihat)
- [ ] C: Tergantung skill

**6. 1st person implementation priority:**
- [ ] A: 1st person orb penting, harus selesai bersamaan dengan 3rd person
- [ ] B: 3rd person dulu, 1st person bisa ditambah belakangan
- [ ] C: Hanya 3rd person (game dimainkan di 3rd person)

**7. Konfirmasi attachment point:**
Apakah orb attach ke `right_hand` PAL bone, atau cukup approximate dari `player.getPos()` + offset tetap?

---

## Ketergantungan

Orb system **membutuhkan** ini selesai lebih dulu:
- [ ] Animasi tangan fire_jab final dari Antigravity (agar orb posisi akurat di ujung tangan)
- [ ] PAL custom bone `right_hand` atau minimal `right_arm` world position query

Orb system **tidak membutuhkan** ini:
- Trail renderer (trail adalah fitur terpisah, orb bisa jalan tanpa trail)
- Skill tree / progression

---

## Estimasi Kompleksitas

| Komponen | Estimasi |
|---|---|
| OrbEntity + networking | Medium (2–3 hari) |
| OrbRenderer 3rd person | Medium (1–2 hari) |
| Particle ring per elemen | Medium (1 hari per elemen) |
| 1st person overlay | Medium-High (2–3 hari, butuh FOV compensation) |
| Cursor tracking (aim lock) | Low (player.getRotationVec() sudah ada) |
| Cast velocity sync | Low (server-side, ikut getRotationVec()) |

**Total estimasi (fire element saja, semua komponen):** 1–2 minggu.

---

*Dokumen ini disiapkan oleh Claude Code untuk direview ChatGPT.*
*Setelah ChatGPT jawab pertanyaan di atas, Claude akan mulai implementasi sesuai jawaban.*
