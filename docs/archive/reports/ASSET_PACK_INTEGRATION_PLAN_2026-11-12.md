# Avatar Elements Asset Pack — Integration Plan 2026-11-12

**Asset pack location:** `art-source/asset_pack/` (dipindahkan dari `reference/` agar terlacak Git)  
**Status:** Production-ready, but needs runtime integration + verification  
**Target:** Minecraft Java 1.21.1 Fabric  

---

## 🎯 Asset Inventory & Integration Status

### 1. **PAL Animations** ⭐ **CRITICAL FOR VA-02**

**Available (15 animations):**
```
fire_jab.animation.json         ✅ READY (0.45s, full keyframes)
fire_blast.animation.json       ✅ READY
flame_sweep.animation.json      ✅ READY
fire_jet.animation.json         ✅ READY
fire_guard.animation.json       ✅ READY

air_staff_attack.animation.json ✅ READY
air_vortex.animation.json       ✅ READY
air_scooter.animation.json      ✅ READY

water_whip.animation.json       ✅ READY

earth_boulder.animation.json    ✅ READY
earth_wall.animation.json       ✅ READY

lightning_strike.animation.json ✅ READY
lightning_redirect.animation.json ✅ READY

octopus_form.animation.json     ✅ READY (water sub-bending)
```

**Fire Jab breakdown (from animation.json):**
```
Timeline (0.45s = 9 ticks @ 20 TPS):
  0.0s (tick 0)    → Neutral stance (body, arms at 0° rotation)
  0.10s (tick 2)   → Guard ready (right_arm: -35°, body: +4°, left_arm ready)
  0.18s (tick 3.6) → **IMPACT PEAK** (right_arm: -92°, body: +8°, left_arm: -42°)
  0.45s (tick 9)   → Return to neutral

Bones animated:
  - right_arm: primary punch motion
  - body: weight shift (stance twist)
  - left_arm: counter-balance
```

**Integration status:** ❌ **NOT INTEGRATED**
- Files exist but NOT loaded in mod
- Animation JSON format = PAL standard ✅
- Bone naming = Vanilla player model ✅
- Serial sync mechanism exists but animation not triggered

**Action:** Load fire_jab.animation.json into PAL layer `fire_jab_test` + verify serial match with server phase broadcast

---

### 2. **VFX Procedural Meshes** ⭐ **FOR ORB & EFFECTS POLISH**

**Available (9 meshes, both .bbmodel + .obj):**
```
vfx_sphere_shell.bbmodel   → For 3D orb (replace current flat piringan)
vfx_ring.bbmodel           → For charge aura rings
vfx_dome.bbmodel           → For impact dome/shockwave
vfx_cone.bbmodel           → For fire/air cone blast
vfx_arc.bbmodel            → For sweeping arc (Flame Sweep)
vfx_tube.bbmodel           → For stream/jet trail
vfx_funnel.bbmodel         → For vortex/whirlpool
vfx_wave_sheet.bbmodel     → For water ripple/ground slam
vfx_octopus_tentacle.bbmodel → For water sub-bending
```

**Current orb issue:** Charge orb terlihat piringan 2D tipis (ChargeOrbRenderer geometry simple)

**Solution:** 
- Use `vfx_sphere_shell.bbmodel` geometry (proper 3D sphere with UV mapping)
- Implement renderer to load this mesh + animate it during charge phase
- Apply additive blend + brightness gradient per vertex

**Integration status:** ❌ **NOT INTEGRATED**
- `.bbmodel` format = Blockbench 4.10 ✅
- `.obj` format available for custom Java renderer ✅
- But rendering code not in mod yet

**Action:** 
1. Render `vfx_sphere_shell` geometry in `ChargeOrbRenderer`
2. Optionally add `vfx_ring` as rotating aura overlay
3. Swap flat QUADS with proper mesh vertices

---

### 3. **2D Artwork & Texture Atlases** (27 atlases, 256 entries)

**Status:** ❌ **PARTIALLY USED**
- Fire particles (flame, ember, smoke) — used in particle effects ✅
- UI elements — not integrated (HUD layout pending)
- Status icons — available but not used
- Skill icons — available but not used

**Available categories:**
- Particles (flame, water, earth, air, smoke, sparks)
- UI panels, buttons, toggles
- Status badges (cooldown, buff, debuff)
- Skill icons (128px and downsampled 32px versions)
- Trail textures (flipbook animations)

**Integration:** Texture pack `assets/avatar_elements/` already provides particle textures ✅

---

### 4. **Audio Files** (17 source WAV + Vorbis OGG)

**Status:** ⚠️ **PARTIAL**
- SFX OGG files in `assets/avatar_elements/sounds/` ready ✅
- Java integration class `AvatarSounds.java` available in `fabric_src/` 

**Action:** Import `AvatarSounds.java` from asset pack → integrate with current skill SFX playback

---

### 5. **Java Integration Classes** (Fabric 1.21.1)

**Asset pack includes (in `fabric_src/`):**
```
AvatarParticles.java          → Particle system initialization
AvatarSounds.java            → Sound registry
ProceduralVfxMeshes.java     → VFX mesh loading + rendering
VfxLifecycleManager.java     → Mesh lifecycle (spawn, tick, despawn)
```

**Status:** ❌ **NOT INTEGRATED** but ready-to-use
- Format = Java 1.21.1 Fabric compatible ✅
- Should be copied to `mod/src/client/java/com/avatarmod/elements/`

**Action:** Copy + adapt these classes to current mod structure

---

## 🔴 **CRITICAL: Fire Jab Animation Why Minimal?**

Animation file exists ✅ and is properly formatted ✅, but appears vanilla-like in-game.

**Diagnostic checklist:**

1. **Is PAL layer registered?**
   - Server broadcasts phase → `S2CPhaseSync` packet sent ✅ (from testing, orb visible)
   - Client receives it → `ChargeOrbClientState` updated ✅
   - **BUT:** Does PAL animation layer activate on phase broadcast?

2. **Serial sync issue?**
   - `CastAnimationGate.java` checks if `castSerial` matches
   - If serial mismatch → animation gate closed, animation skipped
   - Check: Server serial increments? Client receives same serial in S2CPhaseSync?

3. **Bone naming mismatch?**
   - Animation JSON uses: `right_arm`, `body`, `left_arm`
   - Vanilla player model bones: same names ✅
   - **BUT:** Is PAL correctly mapping animation bones to player bones?

4. **Timeline phase mapping?**
   - Animation = 0.45s (9 ticks)
   - Current timeline: windup 2, active 3, recovery 4 = 9 ticks ✅
   - **BUT:** When does animation start? At WINDUP tick 0? Or somewhere else?

**Quick fix hypothesis:**
- Fire Jab animation file is correct
- Issue = serial sync or PAL layer trigger logic
- Recommend: Check `CastAnimationGate.java` + `S2CPhaseSync` broadcast

---

## 📋 Integration Priority (Post-Element-Bug-Fix)

### Phase 1: **Immediate** (VA-02 animation fix)
- [ ] Debug fire_jab.animation.json trigger (serial, layer activation)
- [ ] Verify PAL layer registration in client event listener
- [ ] Test with `fire_jab.animation.json` from asset pack

### Phase 2: **High** (Martial arts quality)
- [ ] Load remaining 14 animations (fire_blast, flame_sweep, air_staff, etc.)
- [ ] Verify all animations sync with server timelines
- [ ] Test animation blending during combo transitions

### Phase 3: **High** (VFX polish)
- [ ] Import `ProceduralVfxMeshes.java` + `VfxLifecycleManager.java`
- [ ] Replace orb flat QUADS with `vfx_sphere_shell` mesh
- [ ] Add `vfx_ring` aura overlay for charge phase
- [ ] Test sphere rendering + additive blend

### Phase 4: **Medium** (SFX + extras)
- [ ] Import `AvatarSounds.java` → SFX registry
- [ ] Integrate 2D particle atlases for additional VFX layers
- [ ] Add skill icons to HUD (from 32px texture pack)

### Phase 5: **Low** (UI polish)
- [ ] Extract UI panels from 2D atlases
- [ ] Integrate with Essential HUD (if chosen)
- [ ] Implement theme color per element (Fire orange, Air cyan, etc.)

---

## 📁 Recommended Folder Structure

```
mod/
├── src/client/java/com/avatarmod/elements/
│   ├── client/vfx/
│   │   ├── ProceduralVfxMeshes.java       [COPY from asset_pack fabric_src/]
│   │   ├── VfxLifecycleManager.java        [COPY from asset_pack fabric_src/]
│   │   ├── AvatarParticles.java            [COPY from asset_pack fabric_src/]
│   │   └── ChargeOrbRenderer.java          [MODIFY to use vfx_sphere_shell]
│   ├── sound/
│   │   └── AvatarSounds.java               [COPY from asset_pack fabric_src/]
│   └── ...
├── src/main/resources/
│   ├── data/player_animation_library/
│   │   └── animation/
│   │       ├── fire_jab.json               [COPY from asset_pack animations/pal/]
│   │       ├── fire_blast.json             [...]
│   │       └── ...
│   ├── assets/avatar_elements/
│   │   ├── textures/
│   │   │   ├── particle/                   [Already in place ✅]
│   │   │   └── vfx/                        [Particle flipbooks, trails]
│   │   └── sounds/                         [OGG files from asset_pack]
│   └── ...
└── ...
```

---

## ⚡ Epic Fight Movement Adoption (Non-Framework)

User note: "Epic Fight movement keren, bisa adopt ke mod" (bukan framework dependency).

**What to adopt (animation concept, not code):**
1. **Multi-frame hit detection:** Epic Fight breaks punches into 3–5 impact frames
   - Implement in `FireJabSkill.tick()`: check hitbox at frame tick 3–4 (not full ACTIVE phase)
   - Current: entire ACTIVE phase hits; better: specific impact frame only

2. **Swing arc trajectory:** Epic Fight calculates weapon path (elbow→wrist)
   - For Fire Jab: simulate punch trajectory (shoulder→fist) for better hit feedback
   - Implement as raycast from player eye toward impact point

3. **Knockback direction:** Epic Fight uses velocity.y += jump_multiplier based on impact height
   - Current implementation already does this ✅

**Implementation:** Add to `FireJabSkill.java`:
```java
// Only deal damage during specific impact frames (tick 3-4 of ACTIVE phase)
if (timeline.phase() == ACTIVE && timeline.ticksInPhase() >= 2 && timeline.ticksInPhase() <= 3) {
    // Hit detection here
}
// Instead of current: entire ACTIVE phase is a hitbox
```

---

## ✅ Checklist for Integration

### Before committing to mod:
- [ ] Verify animation JSON format (version 1.8.0 PAL standard)
- [ ] Check bone names match player model (right_arm, body, left_arm)
- [ ] Confirm timing (0.45s = 9 ticks @ 20 TPS)
- [ ] Test serial sync mechanism with current S2CPhaseSync

### Before rendering meshes:
- [ ] Load `.bbmodel` or `.obj` from asset pack
- [ ] Verify vertex count / polygon budget (don't exceed ~500 verts per frame)
- [ ] Test UV mapping (texture coordinates in .bbmodel must match Minecraft UV scale)
- [ ] Confirm additive blend works with mesh (not just QUADS)

### Before audio integration:
- [ ] Verify Vorbis OGG format (mono, 44.1kHz)
- [ ] Test spatial attenuation (is there a `distance` field in sounds.json?)
- [ ] Check subtitle localization (en_us, id_id available)

---

## 🎬 Epic Fight Reference: Animation Concepts to Adopt

Without Framework dependency, borrow design patterns:

| Epic Fight Pattern | Adopt to Avatar | Impl Location |
|---|---|---|
| **Multi-frame impact** | Hit detection only on frames 3–4 | `FireJabSkill.ticksInPhase() check` |
| **Swing arc path** | Raycast punch trajectory | `FireJabSkill.hitbox()` method |
| **Jump multiplier knockback** | Already implemented ✅ | Current knockback vector ✅ |
| **Recovery pause** | Animation freeze last frame | PAL animation `0.45s → 0.45s` (no change) |
| **Combo chain transitions** | Blend next animation on last frame | PAL layer trigger on phase transition |

---

## Summary: What Needs to Happen

1. **Fire Jab animation trigger** (VA-02 blocker)
   - Debug serial sync or PAL layer registration
   - Confirm animation loads from asset pack JSON ✅

2. **Adopt 14 ready-made animations**
   - Copy PAL `.json` files from asset pack → mod resourcepack
   - Register each in `CastAnimationGate` + serial trigger logic

3. **Enhance orb with 3D mesh**
   - Replace flat QUADS with `vfx_sphere_shell` geometry
   - Import `ProceduralVfxMeshes.java` + `VfxLifecycleManager.java`

4. **Adopt Epic Fight movement concepts** (not framework)
   - Add multi-frame hit detection (tick 3–4 only)
   - Implement swing arc raycast for better feedback

5. **Polish with remaining assets**
   - Import sounds, particle atlases, UI textures
   - Integrate `AvatarSounds.java` for SFX registry

---

**Est. effort for Phase 1–3:** 8–12 hours (animation debug + mesh integration + testing)

Once element bug fixed, start with fire_jab.animation.json integration ASAP (highest ROI for VA-02).
