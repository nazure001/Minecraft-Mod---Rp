# Prosedur Verifikasi Wave 2 — In-Game Testing

Tanggal: 2026-11-12. Tujuan: verifikasi tiga blocker sebelum gelombang 2 (Wave 2) — animasi Fire Jab (VA-02), Air Blast (T3-3), dan sinkronisasi 2 pemain (T2-8).

## Build & Launch

```bash
cd mod
./gradlew runClient  # Launch Fabric dev client dengan mod + PAL (PAL harus sudah di instance)
```

Instance diasumsikan:
- Fabric 1.21.1 loader + Fabric API
- Player Animation Library (PAL) 1.1.6+mc.1.21.1 (critical; tanpa ini Fire Jab tidak ada animasi)
- Avatar: Elements mod JAR (output dari `./gradlew build`)

## VA-02 — Fire Jab Animation Client Test

**File:** Animasi memakai `fire_jab_test` layer PAL di `data/player_animation_library/animation/fire_jab.json` (lihat [anim_library_audit.md](../memory/anim_library_audit.md)).

**Checklist:**

1. **Tekan Z (fire_jab keybinding)** saat melihat ke suatu target atau kosong.
   - [ ] Animasi body bone bergeser/punch visible (stance → transfer berat → impact → recovery)?
   - [ ] Atau hanya vanilla attack animation (tanda PAL layer tidak trigger)?
   
2. **Stance & weight transfer:**
   - [ ] Kaki tetap anchored atau bergeser?
   - [ ] Punch frame clearly at peak?
   
3. **1st person vs 3rd person:**
   - [ ] Pose terlihat normal di 1st person (kamera)?
   - [ ] Observer/3rd person melihat animasi full juga (multiplayer prep)?
   
4. **Armor/slim skin:**
   - [ ] Pose tidak broken untuk armor pakaian atau alex slim skin?
   
5. **Charge orb:**
   - [ ] Orb api WINDUP (2t) + ACTIVE (3t) terlihat ≈ 5 ticks total?
   - [ ] Warna orange-red, additive glow (tidak fully opaque)?
   
**Hasil expected:**
- Animasi visible = PASS VA-02
- Hanya vanilla attack = FAIL (investigate PAL layer trigger atau PAL not loaded)

---

## T3-3 — Air Blast Verification

**File:** `avatar:air_blast` JSON di `skill_definitions.json` (damage 3.0, range 8, knockback 2.5, hitbox LINE, instant cast).

**Keybinding:** Slot AIR X (tombol X saat element AIR aktif; set elemen dengan keybinding yang sudah ada, atau mod terpisah).

**Checklist:**

1. **Setup element:** Ubah active element ke AIR (jika belum ada UI untuk ini, skip atau hardcode di testing).
   
2. **Tekan X — cast Air Blast:**
   - [ ] Chi berkurang sesuai `chiCost: 12`?
   - [ ] Cooldown HUD menunjukkan `cooldownTicks: 10` (blue bar)?
   - [ ] Tidak ada error console?
   
3. **Hitbox & damage:**
   - [ ] Summon target dummy di jarak <8 blok di depan.
   - [ ] Air Blast mengenai dummy?
   - [ ] Damage ≈ 3.0 (dummy lost ~3 hearts)?
   - [ ] Knockback = 2.5 (target terdorong jauh)?
   
4. **VFX/SFX:**
   - [ ] Ada efek visual (air particle, wind burst, atau hanya vanilla)?
   - [ ] Ada suara?
   
5. **hitbox shape LINE (cone-like?):**
   - [ ] Damage area melebar ke depan atau hanya garis menyempit?
   
**Hasil expected:**
- Chi cost + cooldown + damage + knockback ✅ = PASS T3-3
- Chi cost atau damage tidak berubah = FAIL (investigate SkillDispatcher.dispatch() untuk case air_blast)

---

## T2-8 — 2-Player Sync Test (Dedicated Server)

**Tujuan:** Verifikasi chi/cooldown independen per pemain, kombo tidak tertukar antara pemain, broadcast phase sync akurat.

### Setup: Local Dedicated Server

```bash
# Terminal 1: Launch dedicated server
cd mod
./gradlew runServer

# Terminal 2: Launch client 1 (Player A)
cd mod
./gradlew runClient

# Terminal 3 (atau manual via launcher): Launch client 2 (Player B)
cd mod
./gradlew runClient
```

Server akan bind ke `localhost:25565`. Kedua client connect dengan username berbeda (misal: `PlayerA`, `PlayerB`).

### Checklist

#### A. Chi/Cooldown Independen

1. **Player A: Tekan Z (fire_jab)**
   - [ ] A: chi berkurang 8, cooldown jadi 6 tik
   - [ ] B: chi tetap penuh, tidak ada cooldown?
   - [ ] B bisa cast jab langsung tanpa menunggu A selesai?
   
2. **Player B: Tekan Z sambil A masih dalam recovery**
   - [ ] B: chi berkurang, cooldown dimulai (independen dari A)
   - [ ] A: cooldown countdown tidak terpengaruh?
   
**Hasil:** Kedua cooldown bar terpisah pada HUD masing-masing = PASS chi independence

#### B. Kombo Tidak Tertukar

1. **Player A: Z (jab) → X (blast/sweep)**
   - [ ] Combo counter pada A naik?
   - [ ] Damage multiplier diterapkan ke A?
   
2. **Player B: Tekan Z sementara A sedang di fase combo X**
   - [ ] B: hit registrar sebagai kombo baru B (counter = 1)?
   - [ ] Atau hit A malah? (BUG — kombo tertukar)
   
**Hasil:** Masing-masing player combo independen = PASS

#### C. Phase Sync Broadcast Akurat

1. **Player A: Tekan Z**
   - [ ] Di layar A: jab animasi/orb tampil (lokal)
   - [ ] Di layar B: A's character melakukan jab animasi, orb tampil di tangan A? (sync)
   - [ ] Atau B hanya lihat vanilla attack? (BUG — phase broadcast gagal)
   
2. **Server log:** Cari line `broadcastPhaseSync` atau `S2CPhaseSync`:
   - [ ] Paket terkirim ke kedua client?
   - [ ] Serial (`castSerial`) tracking ?
   
**Hasil:** Animasi/VFX A terlihat di B = PASS broadcast

#### D. Network Stability

- [ ] Tidak ada timeout/disconnect saat test?
- [ ] Console tidak ada `ERROR` atau `NullPointerException`?

**Hasil:** No crash = PASS network stability

---

## Hasil Pelaporan

Setelah testing, update `TASKS.md`:

```markdown
- [ ] **T2-8** Test sinkronisasi: dua pemain, dedicated server
  - [x] Chi/cooldown independen — PASS / FAIL (log)
  - [x] Kombo tidak tertukar — PASS / FAIL (log)
  - [x] Phase broadcast akurat — PASS / FAIL (log)
  - [x] Network stability — PASS / FAIL (log)
  - Status: ______ (3-4/4 PASS → LANJUT Wave 2; ada FAIL → investigate & fix)

- [x] **VA-02** Uji Fire Jab di client
  - [x] Animasi visible — PASS / FAIL
  - [x] Stance/weight transfer — OK / degraded / missing
  - [x] Multiplayer pose — OK / broken
  - [x] Armor compatibility — OK / broken
  - [x] Charge orb visible & glow — PASS / FAIL
  - Status: ______ (semua OK → VA-02 PASS; ada degraded → VA-02 PARTIAL)

- [x] **T3-3** Verifikasi Air Blast
  - [x] Chi cost + cooldown — PASS / FAIL
  - [x] Damage + knockback — ✅ / ❌ (value: ___)
  - [x] hitbox shape LINE — PASS / FAIL
  - Status: ______ (semua PASS → T3-3 COMPLETE)
```

---

## Troubleshooting

### Fire Jab animasi tidak muncul
- [ ] PAL di instance?
  - Cek `/mods` folder → harus ada `player_animation_library-1.1.6+mc.1.21.1.jar` atau later
- [ ] `fire_jab_test` layer tidak trigger?
  - Cek console log: ada line `fire_jab_test` atau error?
  - Investigate `CastAnimationGate.java` → apakah cast serial mismatch?

### Air Blast damage 0 atau tidak mengenai
- [ ] Dispatcher.dispatch() ada case `"avatar:air_blast"`?
  - Cek `SkillDispatcher.java` line 75 — harus ada `case "avatar:air_blast" -> ...`
- [ ] Handler `AirBlastSkill.tick()` ada?
  - Cek `AirBlastSkill.java` — harus ada hitbox LINE logic

### Sync gagal (B tidak lihat A punya animasi)
- [ ] Paket `S2CPhaseSync` terkirim?
  - Cek server log: `broadcastPhaseSync` line
  - Cek client B console: `S2CPhaseSync received` atau error?
- [ ] Serial mismatch?
  - Cek `ChargeOrbClientState` — apakah serial konsisten dengan server broadcast?

---

## Timeline

- [ ] Setup & launch server: ~5 menit
- [ ] VA-02 test: ~10 menit (pose, 1st/3rd person, armor, orb)
- [ ] T3-3 test: ~5 menit (chi, cooldown, damage, knockback)
- [ ] T2-8 test: ~15 menit (chi indep, kombo, sync, stability)
- **Total:** ~35 menit untuk semua tiga

Setelah testing 3/3 PASS, Wave 2 (T3 gelombang 2: water_surge, earth_wall, lightning, ice_prison, dsb.) siap dikerjakan.
