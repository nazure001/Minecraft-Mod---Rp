# Testing Report — 2026-11-12 In-Game Verification

**Tester:** User (singleplayer + multiplayer)  
**Date:** 2026-11-12  
**Build:** commit a0b06e7 (T3-11/T3-12) + commit d31a7d2 (testing doc)

---

## Ringkasan Hasil

**Damage/mechanics:** ✅ Working (chi cost, cooldown, knockback, damage register)  
**VFX:** ⚠️ Partial (Fire/Air particles OK, orb shape issue, Earth Pillar block visual missing)  
**Animation/martial arts:** ❌ Minimal (mostly vanilla cast, martial arts motion belum ada)  
**Element selection:** ❌ CRITICAL BUG (element berubah random setelah beberapa cast)  
**HUD layout:** ⚠️ Not proportional (menghalangi view)  
**Multiplayer:** Same issues as singleplayer

---

## Findings Detail

### 🔴 CRITICAL — Element Switching Bug

**Issue:** Setelah cast skill beberapa kali, active element tiba-tiba berubah ke elemen lain tanpa user input.

**Observed:**
- Cast FIRE skill 2–3x → element jadi WATER/AIR/EARTH
- HUD bar berubah warna
- Skill yang di-cast menjadi elemen lain (misal: cast Fire Jab tapi keluar Air skill)

**Impact:** Gameplay broken — user tidak bisa konsisten pilih elemen  
**Priority:** 🔥 **HIGHEST** — harus di-fix sebelum testing lanjutan

**Suspect code:** `ElementSlotMap.setActiveElement()` atau server-side element tracking di `PlayerBendingData`

**Action:** Investigate element state management. Cek apakah ada race condition di network sync atau HUD update logic.

---

### ⚠️ HIGH — Targeting & Accuracy

**Issue:** Skill Z (instant attack) semua elemen sering **miss** meskipun target jelas di depan.

**Observed:**
- Fire Jab: cast ke target dummy, tapi damage 0 (miss)
- Water Whip: similar, sering tidak mengenai
- Air Staff Attack: lebih konsisten tapi masih ada miss

**Expected:** Hitbox SPHERE r2.5–3.0, harus selalu hit target di depan jika range OK

**Suspect:** Hitbox calculation di server skill handler; mungkin:
- Calculation posisi eye vs hitbox center offset
- Tidak ada server-side raycast/distance check
- Timeline phase timing (WINDUP terlalu pendek?)

**Action:** Verifikasi `FireJabSkill.tick()` + `AirPalmSkill.tick()` hitbox logic. Tambah server-side distance/raycast validation.

---

### ⚠️ HIGH — Earth Pillar Block Visual Missing

**Issue:** Earth Pillar erupsi tidak menampilkan kolom batu 3D. User hanya lihat:
- Partikel blok tanah berterbangan
- Damage applied ✅
- Knockback applied ✅
- Tapi **tidak ada visual kolom/wall yang muncul**

**Expected:** BlockStateParticleEffect layer demi layer (VFX kolom naik) atau minimal blok temporary yang spawn di lokasi

**Current behavior:** `spawnColumnParticles()` hanya spawn partikel individual, tidak ada struktur/outline kolom

**Action:** Enhance Earth Pillar VFX:
- Opsi 1: Spawn temporary entity (ArmorStand dengan block texture) sebagai kolom visual
- Opsi 2: Render-side holo-column (client-side particle mesh)
- Opsi 3: Lebih banyak partikel grid pattern untuk "feel" kolom solid

---

### ⚠️ HIGH — Martial Arts Animation Minimal

**Issue:** Cast animation terlihat hanya vanilla attack motion, **martial arts gerakan belum ada** atau very basic.

**Observed (dari screenshot):**
1. Stance/guard pose → tidak ada
2. Transfer berat badan → tidak terlihat
3. Punch/kick impact frame → vanilla hit animation only
4. Recovery pose → generic

**Expected:** Fire Jab harus punya:
- Open guard stance (fire ready)
- Weight shift (kanan ke kiri)
- Punch peak frame (impact)
- Cooldown recovery pose

**Suspect:** PAL layer `fire_jab_test` trigger, tapi animasi definition di `.bbmodel` / JSON tidak lengkap atau tidak di-load client-side

**Status:** VA-02 = **PARTIAL FAIL** (animasi ada tapi sangat minimal)

**Action:** Review PAL animation JSON dan Blockbench `.bbmodel` untuk Fire Jab. Pastikan:
- Pose sequence (stance → punch → recovery) tersedia di rig
- Client-side render dapat akses pose data per frame
- Serial/timing sync antara server phase dan client animation frame

---

### ⚠️ MEDIUM — Orb/Sphere Shape Issue

**Issue:** Charge orb Fire Blast & Boulder Launch **terlihat piringan tipis 2D**, bukan bola 3D (sphere) seperti blockbench result.

**Current:**
- Additive blend: ✅ (glow effect bagus)
- Color: ✅ (orange/earth tones OK)
- Shape: ❌ Piringan datar, tidak ada depth/3D feel

**Expected:** UV-sphere dengan shading depth atau minimal ring/torus pattern untuk 3D perception

**Suspect:** `ChargeOrbRenderer.renderOrb()` → QUADS mode dengan normal sphere geometry, tapi:
- Lighting/shading tidak ada (flat color)
- Oder tidak ada perspective distortion
- Atau geometry terlalu simple (sedikit segments)

**Action:** Enhance orb visual:
- Tambah lebih banyak sphere segments (64 instead of 32?)
- Implementasi per-vertex brightness gradient (center bright, edge dim) untuk 3D feel
- Atau tambah inner/outer layer (nested sphere) dengan warna berbeda

---

### ⚠️ MEDIUM — 1st Person Item Animation Missing

**Issue:** Saat cast skill di 1st person:
- Tangan **tidak bergerak**
- Item (staff) **tetap statis**
- Hanya player view yang animated (body/weapon jab)

**Expected:** 1st person → player hand/item gerak ke arah skill (punch forward, staff swing, dsb.)

**Current:** 3rd person punya movement (walau martial arts belum ada), 1st person tidak ada.

**Suspect:** PAL layer hanya ter-apply ke `body` bone (3rd person), tidak ke `hand` / `item` bone untuk 1st person.

**Action:** Extend PAL animation untuk 1st person hand/item bones. Atau custom 1st person arm animation layer di `FirstPersonOrbRenderer` area.

---

### ⚠️ MEDIUM — HUD Layout Not Proportional

**Issue:** HUD elements (chi bar, cooldown text, skill name) **menghalangi gameplay view**, tidak proporsional dengan screen size.

**Current:**
- Chi bar terlalu besar?
- Cooldown text overlapping?
- Element indicator tidak jelas posisinya

**Expected:** HUD minimal, overlay corner atau small sidebar, tidak block center screen

**Action:** UI-05 theme tuning (dari kontrak UI_THEME_SPEC). Sesuaikan HUD size/position agar tidak invasive. Atau implementasikan UI scale config di client settings.

---

### ✅ WORKING

**Damage & mechanics:**
- Chi cost applied ✅
- Cooldown tracking ✅ (HUD bar countdown)
- Knockback direction & magnitude ✅
- Combo bonus (jika implemented) ✅

**VFX:**
- Fire particle trail: ✅ (flame burst, lava drops, smoke)
- Air spiral: ✅ (vortex particles)
- Water splash: ✅

**Network (multiplayer):** Same issue as singleplayer (element bug, targeting, animation)

---

## Priority Fix List

| Priority | Issue | Owner | Est. Effort |
|----------|-------|-------|------------|
| 🔥 1 | **Element switching bug** | Debug server state | 1–2 hours |
| 🔥 2 | **Targeting accuracy** (Z skill miss) | Hitbox logic review | 1–2 hours |
| 🟠 3 | **Earth Pillar block visual** | VFX enhancement | 1–2 hours |
| 🟠 4 | **Martial arts animation** (VA-02) | PAL layer investigation | 2–4 hours |
| 🟠 5 | **Orb 3D shape** (sphere quality) | Renderer enhancement | 1 hour |
| 🟡 6 | **1st person item animation** | PAL hand/item bones | 1–2 hours |
| 🟡 7 | **HUD layout proportional** | UI scale/position tuning | 1 hour |

---

## Recommendations

1. **Element bug blocker:** Jangan lanjut skill baru sampai element state fix. Ini akan corrupt testing.
2. **Animation gap:** Investigate PAL layer trigger di client. Fire Jab animation ada tapi minimal — perlu full martial art sequence (stance, weight, impact, recovery).
3. **VFX polish:** Earth Pillar dan orb shape sudah mechanics-OK tapi visual kurang impact. Prioritas rendah untuk gameplay, tapi penting untuk feel/feedback.
4. **Testing restart:** Setelah element bug fix, re-test satu elemen lengkap (Fire) dengan checklist VA-02 + T3-3 + T2-8 sebelum wave 2.

---

## Test Coverage Summary

| Test Case | Status | Notes |
|-----------|--------|-------|
| **VA-02** Fire Jab animation | ⚠️ PARTIAL | Animasi ada, martial arts minimal |
| **T3-3** Air Blast mechanics | ✅ PASS | Damage/knockback/chi OK |
| **T2-8** 2-player sync | ⚠️ PARTIAL | Element bug makes testing unreliable |
| **T3-11** Earth Pillar damage | ✅ PASS | Damage applied, knockback OK |
| **T3-12** Boulder Launch | ✅ PASS | Scaling charge working |
| **All Z-skill accuracy** | ❌ FAIL | Targeting miss rate high |
| **Element consistency** | ❌ FAIL | **CRITICAL** |
| **HUD layout** | ⚠️ OK-ISH | Functional but not optimal |

---

## Next Steps

1. **Commit this report** to docs/
2. **Assign element bug to debug** (likely Antigravity IDE or server-state audit)
3. **Pause wave 2 implementation** until element bug cleared
4. **Schedule re-test** post-fix (estimate 2–3 hours fix + test cycle)
5. **Animation audit:** Parallelize PAL investigation untuk VA-02/VA-03 while element bug is being fixed
