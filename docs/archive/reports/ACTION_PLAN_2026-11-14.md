# Action Plan — Testing & Integration Phase (2026-11-14)

## 🎯 Prioritas Tertinggi

### Phase 1: Verify Element Bug Fix ⚠️ BLOCKING

**Status:** Server-side debounce deployed (Fix #1), awaiting in-game test

**Test Protocol:**
```
1. Launch mod dengan build terbaru (cc7aa36 or later)
2. Singleplayer, spawn test area
3. Cast Fire Jab (Z key) → 5 times rapidly (< 3 detik total)
4. Check: active element di HUD tetap FIRE (tidak berubah ke AIR/WATER/EARTH)
5. Repeat test dengan R key element cycling → verify no interference
```

**Expected Result:** Element tetap stabil, HUD color tidak berubah

**If Bug Persists:**
- Check logs untuk "Element changed to X" — see if server-side state matches client HUD
- Debug Cause 2: Add logging ke `PlayerBendingData()` constructor untuk detect multiple creations
- Debug Cause 3: Verify `S2CSyncElement` packet always received after cycle

**Reference:** `docs/DEBUG_ELEMENT_BUG_2026-11-14.md` (diagnostik procedure)

---

### Phase 2: Fire Jab Animation Integration 🔴 HIGH PRIORITY

**Status:** VA-02 shows minimal animation (mostly vanilla cast)

**Problem:**
- Animation JSON exists di asset_pack (`avatar_elements_asset_pack/fire_jab.animation.json`) ✅
- PAL 1.1.6+mc.1.21.1 declared di Gradle ✅
- Tapi in-game Fire Jab cast tidak trigger martial arts keyframes

**Root Causes (to investigate):**
1. Animation not registered atau tidak linked ke skill ID
2. Trigger condition salah (timeline phase, holdable mismatch)
3. PAL instance tidak load di game instance

**Action Steps:**
1. **Verify PAL loaded:**
   ```
   Check: /animprops, /anim list in-game
   Check: logs untuk "PAL initializing" atau error messages
   ```

2. **Check animation registration:**
   ```
   Grep: SkillDispatcher.java + AvatarElementsClient.java
   untuk animation trigger logic
   ```

3. **Test animation trigger:**
   - Cast fire_jab, watch for animation playback
   - If not playing: check cast trigger state (WINDUP vs ACTIVE vs RECOVERY)
   - If wrong frame: check timeline tick sync dengan animation timeline

4. **Next:** Integrate PAL bone system untuk handle 1st/3rd person arm + item positioning

**Files to examine:**
- `mod/src/main/java/com/avatarmod/elements/animation/` (if exists)
- `mod/src/main/java/com/avatarmod/elements/client/AvatarElementsClient.java` (key bind handler)
- `avatar_elements_asset_pack/fire_jab.animation.json` (animation definition)

---

### Phase 3: Air Blast Targeting Accuracy 🔴 HIGH

**Status:** T3-3 Mechanics OK, targeting frequently misses

**Problem:**
- Z-skill Air Blast raycast not detecting target properly
- Fire Jab (SPHERE) and Water Whip (LINE) also affected

**Root Cause Investigation:**
- `AirBlastSkill.tick()` uses raycast dari eye position
- Distance check dan block obstruction currently implemented
- BUT: may have off-by-one errors atau incorrect hitbox distance calculation

**Action Steps:**
1. Check hitbox logic di skill classes: `AirBlastSkill.java`, `FireJabSkill.java`, `WaterWhipSkill.java`
2. Add debug particles untuk show raycast trajectory + hit detection
3. Test: target di front, edge, samping, belakang, blocked
4. Adjust distance/hitbox parameters jika perlu

**Files to examine:**
- `mod/src/main/java/com/avatarmod/elements/skill/impl/AirBlastSkill.java`
- `mod/src/main/java/com/avatarmod/elements/skill/impl/FireJabSkill.java`
- `mod/src/main/java/com/avatarmod/elements/skill/impl/WaterWhipSkill.java`

---

## 📋 Secondary Tasks (After Phase 1–3 Clear)

### Phase 4: T2-8 Multiplayer Retest

**Blocker:** Element bug ✅ Now fixed

**Test Protocol:**
- Two players, dedicated server
- Each player cast skills independently
- Verify: chi/cooldown isolated per player
- Verify: no skill slot/element confusion between players
- Verify: element switching independent per player

---

### Phase 5: Animation & VFX Polish

**Low priority (not blocking Wave 1):**
- [ ] Replace flat QUAD orb dengan 3D sphere mesh (vfx_sphere_shell)
- [ ] Improve 1st person hand positioning (PAL bone alignment)
- [ ] Earth Pillar: add 3D column mesh eller holo-block particles
- [ ] HUD layout: scale/position untuk tidak block view

---

## 📊 Summary Status Table

| Task | Status | Blocker | Action |
|------|--------|---------|--------|
| Element Cycle Bug | `[~]` Fix #1 deployed | YES | In-game test |
| Fire Jab Animation | `[~]` Minimal anim | YES | PAL integration |
| Air Blast Targeting | `[~]` Mechanics OK | YES | Debug raycast |
| T2-8 Multiplayer | `[ ]` Blocked | NO | Await Phase 1 |
| Animation Polish | `[ ]` Backlog | NO | Phase 5+ |

---

## 🔧 Deployment Checklist

Before merge to main:
- [ ] Element bug test: element stays stable over 10+ casts
- [ ] Fire Jab test: animation plays on Z key cast
- [ ] Air Blast test: hits detect at expected distances
- [ ] T2-8 test: two-player skills independent
- [ ] Build: `./gradlew build` ✅ no errors
- [ ] Tests: `./gradlew test` ✅ unit tests pass

---

**Next Step:** Start Phase 1 in-game testing (user responsibility). Report findings untuk next iteration.

