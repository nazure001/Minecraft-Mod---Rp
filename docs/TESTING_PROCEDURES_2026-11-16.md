# 🎮 Testing Procedures — Avatar Elements Mod (2026-11-16)

## Phase: Integration Testing with Debug Diagnostics

**Status:** Build ready with debug logging + targeting improvements  
**Build Date:** 2026-11-16  
**Test Environment:** Singleplayer + Dedicated Server  
**Expected Duration:** ~60 minutes per tester

---

## 🎯 Test Plan Overview

### Test 1: Element Cycle Bug Verification ⚠️ BLOCKING
- **Scope:** Server-side debounce (Fix #1)
- **Duration:** 5-10 min
- **Critical:** YES (blocks T2-8 multiplayer)

### Test 2: Fire Jab Animation Trigger 🎬 BLOCKING
- **Scope:** PAL animation playback on Z key cast
- **Duration:** 10-15 min
- **Critical:** YES (blocks VA-02 verification)

### Test 3: Air Blast Targeting Accuracy 🎯 HIGH
- **Scope:** Z-skill hit detection at various ranges
- **Duration:** 10-15 min
- **Critical:** YES (blocks T3-3 verification)

### Test 4: T2-8 Multiplayer (After Test 1 passes)
- **Scope:** Two-player independent chi/cooldown
- **Duration:** 15-20 min
- **Critical:** After Test 1

---

## 📋 Test 1: Element Cycle Bug Verification

### Prerequisites
```
✓ Latest build deployed
✓ Client executable ready
✓ Singleplayer world available
```

### Test Steps

**Step 1: Launch Game**
```bash
cd "D:\repo\Minecraft Mod & Rp\mod"
.\gradlew.bat runClient
# Wait for game to load (≈ 30-60s)
```

**Step 2: Verify Game State**
- Confirm world loaded
- Check HUD: Chi bar visible (blue bar above hotbar)
- Check active element shown (flame icon = FIRE)

**Step 3: Element Cycling Test**
1. Stand in clear area (no mobs)
2. Press R key (element wheel)
3. Watch HUD: element should change FIRE → AIR
4. Press R again: AIR → WATER
5. Press R again: WATER → EARTH
6. Press R again: EARTH → FIRE
7. **PASS if:** All 4 elements cycle smoothly, no skipping

**Step 4: Rapid Cast Test (Bug Verification)**
```
1. Set active element: FIRE (press R until FIRE active)
2. Cast Fire Jab: Press Z key 5 times rapidly (< 2 seconds)
3. Watch HUD element bar color: should stay ORANGE (FIRE)
4. Repeat with AIR element: cast Air Staff 5 times, should stay TEAL (AIR)
5. Mix elements: cycle to WATER, cast Water Whip 5x, should stay BLUE
```

**Expected Results:**
- ✅ Element bar does NOT change color during casting
- ✅ Skills use correct element (Fire Jab = FIRE, not switching to AIR)
- ✅ No random element switching observed

**Failure Diagnostics:**
If element switches randomly during casting:
- Check server logs: look for "Element changed to X" messages
- Verify debounce is working: cooldown should show 6 ticks (300ms)
- Check for duplicate packets: any repeated element changes = packet spam

**PASS Criteria:** Element stable over 20+ consecutive casts

---

## 📋 Test 2: Fire Jab Animation Trigger

### Prerequisites
- Test 1 passed (element system stable)
- Latest build with debug logging deployed
- Console output visible

### Test Steps

**Step 1: Launch Client with Console**
```bash
# Keep console window visible during testing
cd "D:\repo\Minecraft Mod & Rp\mod"
.\gradlew.bat runClient
# Console should show [Avatar DEBUG] messages
```

**Step 2: Verify PAL Loaded**
1. Look at console output during game load
2. Search for "player.anim" or "PAL" messages
3. Should see: "player_animation_library" or similar library name

**Step 3: Animation Trigger Test**
```
1. Set element to FIRE (active element = Fire)
2. Cast Fire Jab: Press Z key once
3. Watch player model:
   - Should see martial arts stance (arms positioned)
   - Should see strike motion (jab forward)
   - Should see recovery motion
4. Check console for debug logs:
   - "[Avatar DEBUG] triggerSkillAnimation(avatar:fire_jab, ACTIVE) -> ..."
   - "[Avatar DEBUG] triggerAnimation(...) = true"
```

**Expected Results:**
- ✅ Fire Jab animation plays in 3rd person view
- ✅ Player arms animate (not T-pose vanilla cast)
- ✅ Console shows "triggerAnimation(...) = true"
- ✅ Animation duration ≈ 0.45 seconds

**Failure Diagnostics:**

**If animation NOT playing:**
```
Check console for:
- "[Avatar DEBUG] Failed to resolve animation: avatar:fire_jab"
  → Animation JSON not found or wrong format
  
- "resolveAnimationId: NO MATCH for avatar:fire_jab"
  → PAL animation resource not loaded
  
- "Layer not PlayerAnimationController"
  → PAL not initialized properly
```

**If animation plays but martial arts minimal:**
```
Check console for:
- bone transform logs from PAL
- any animation blend errors
- verify fire_jab.animation.json has bone rotation keyframes
```

**PASS Criteria:**
- Animation visibly plays on Z key cast
- Player martial arts posture visible
- Console shows successful triggerAnimation()

---

## 📋 Test 3: Air Blast Targeting Accuracy

### Prerequisites
- Latest build with targeting improvements deployed
- Test 1 passed (element system stable)

### Test Steps

**Step 1: Setup Test Area**
1. Spawn 5 zombies at various distances
2. Clear area around player (20 block radius)
3. Create lineup: zombie at 2m, 4m, 6m, 8m (max range)

**Step 2: Target At Front**
```
1. Stand facing zombie at 2m distance
2. Align player aim (crosshair on zombie)
3. Cast Air Blast: Press Z key
4. Result: zombie should take 3.0 damage + 2.5 knockback
5. Repeat for zombie at 4m, 6m, 8m
```

**Expected:** All zombies in line of sight → HIT

**Step 3: Target At Edge/Angle**
```
1. Position zombie slightly off to side (< 30° angle from look)
2. Cast Air Blast
3. Expected: HIT (within cone)
```

**Step 4: Block Obstruction**
```
1. Place wood block between player and zombie
2. Position zombie behind block
3. Cast Air Blast
4. Expected: MISS (blocked by wood)
```

**Step 5: Out of Range**
```
1. Position zombie at 12 blocks away (beyond 8m range)
2. Cast Air Blast
3. Expected: MISS (out of range)
```

**Success Metrics:**
- ✅ Zombies at 0-8m all hit (line of sight)
- ✅ Zombies behind walls miss
- ✅ Zombies > 8m miss
- ✅ Knockback applied correctly (2.5 velocity)

**Failure Diagnostics:**
If zombies NOT taking damage:
- Check: Is Air Blast actually casting? (cooldown shows?)
- Check: Are zombies in correct range? (< 8m?)
- Check: Is line of sight blocked by blocks?
- Check: Targeting logic may need adjustment

**PASS Criteria:** 8/10 hits in valid targets, 0/5 hits on blocked targets

---

## 📋 Test 4: T2-8 Multiplayer (After Test 1 Passes)

### Prerequisites
- Test 1 PASSED (element bug fixed)
- Two Minecraft instances or two players
- Dedicated server available

### Test Steps

**Step 1: Start Dedicated Server**
```bash
cd "D:\repo\Minecraft Mod & Rp\mod"
.\gradlew.bat runServer
# Wait for "Done (X.XXs)!" message
# Server running on port 25565
```

**Step 2: Connect Two Players**
```
Player 1:
  - Launch minecraft via ./gradlew.bat runClient
  - Multiplayer → Add Server → localhost:25565
  - Join

Player 2:
  - Same as Player 1
```

**Step 3: Chi Independence Test**
```
1. Player 1: Cast Fire Jab (costs 8 chi)
   - Player 1 HUD: chi decreases 8
   - Player 2 HUD: chi UNCHANGED
   
2. Player 2: Cast Water Whip (costs ?)
   - Player 2 HUD: chi decreases
   - Player 1 HUD: chi UNCHANGED
```

**Expected:** Each player's chi independent

**Step 4: Cooldown Independence Test**
```
1. Player 1: Cast Fire Jab
   - Player 1: Cooldown shows 6 ticks
   - Player 2: No cooldown displayed
   
2. Player 2: Cast same skill immediately
   - Player 2: Cooldown shows 6 ticks
   - Player 1: Cooldown still active
```

**Expected:** Cooldowns per-player

**Step 5: Element Independence Test**
```
1. Player 1: Press R to cycle element → AIR
   - Player 1 HUD: element = AIR
   - Player 2 HUD: element = FIRE (unchanged)
   
2. Player 2: Press R to cycle element → WATER
   - Player 2 HUD: element = WATER
   - Player 1 HUD: element = AIR (unchanged)
```

**Expected:** Element cycles independent per player

**PASS Criteria:** All 3 systems independent, no chi/cooldown/element sharing

---

## 🔍 Debug Logging Guide

### Console Output Examples

#### Animation Trigger Success
```
[Avatar DEBUG] triggerSkillAnimation(avatar:fire_jab, ACTIVE) -> avatar_elements:fire_jab = true
[Avatar DEBUG] triggerAnimation(avatar_elements:fire_jab) = true
```

#### Animation Trigger Failure
```
[Avatar DEBUG] Failed to resolve animation: avatar:fire_jab
[Avatar DEBUG] resolveAnimationId: NO MATCH for avatar:fire_jab
```

#### PAL Not Loaded
```
[Avatar DEBUG] Layer not PlayerAnimationController: null
```

#### Element Debounce Working
```
Server console: [Avatar] Element changed to AIR for player Player925
(no spam = debounce working)
```

---

## ✅ Pass/Fail Summary

| Test | Pass | Fail | Blocker |
|------|------|------|---------|
| T1: Element Bug | Element stable | Random switches | YES |
| T2: Fire Jab Animation | Animation plays | No animation | YES |
| T3: Air Blast Targeting | 8/10 targets | 5/10 targets | YES |
| T4: Multiplayer | Independent | Shared state | NO (after T1) |

---

## 🚀 Next Steps After Testing

**If All Pass:**
- Merge feat/fabric-scaffold → main
- Begin Wave 2 content development
- Unlock new element skills

**If Any Fail:**
- Review DEBUG logs
- Adjust code based on diagnostic output
- Re-test with new build

---

## 📞 Troubleshooting

**Build won't compile:**
```bash
./gradlew.bat clean build  # Clean rebuild
```

**Client won't start:**
- Check Java version: `java -version` (should be JDK 21+)
- Check RAM: game needs ≥ 3GB

**Game crashes on startup:**
- Check Fabric Loader logs
- Look for mod incompatibilities (should only be Avatar Elements + Fabric API)

---

## 🎯 Final Checklist

Before testing:
- [ ] Build successful (`BUILD SUCCESSFUL`)
- [ ] Console visible and logging enabled
- [ ] Singleplayer world ready
- [ ] ~60 minutes available for full testing

During testing:
- [ ] Copy debug output to notepad for reference
- [ ] Document any unexpected behavior
- [ ] Screenshot HUD state at key moments

After testing:
- [ ] Report results to developer
- [ ] Attach console logs from debug output
- [ ] Note any crashes or errors

---

**Generated:** 2026-11-16  
**For:** Avatar Elements Mod Phase Integration Testing  
**Ready for:** Autonomous testing execution

