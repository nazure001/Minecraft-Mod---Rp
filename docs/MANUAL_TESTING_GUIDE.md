# MANUAL TESTING GUIDE & ACCEPTANCE DOCUMENTATION
## Avatar Elements — Manual Verification Draft
**Document Version:** 1.0.0 (historical checklist; not a completed acceptance record)  
**Target Platform:** Minecraft Java Edition 1.21.1  
**Mod Architecture:** Fabric Loader `0.20.1` (current project version), Fabric API `0.116.17+1.21.1`, Yarn `1.21.1+build.3`  
**Mod ID:** `avatar_elements` | **Namespace:** `com.avatarmod.elements`  
**Compliance Standard:** Requirement R7 (Zero User World Mutation, Zero Auto-Start Servers)

> Status audit 2026-11-08: instruksi dan expected result di bawah adalah checklist historis, bukan klaim telah dijalankan atau lulus pada source saat ini. Sebelum dipakai, cocokkan dengan schema/runtime di `CONTENT_SPEC.md`, mapping aktual Z/X/C/V/B di `element_slots.json`, dan workflow di `TESTING.md`. Jangan memakai command scoreboard/datapack sebagai pengujian state Fabric.

---

## 1. Document Overview & Testing Philosophy

This document is a historical checklist draft for the **Avatar Elements** mod. It is not an authoritative or completed production-acceptance record; use `TESTING.md` for the current verification workflow.

### 1.1 Non-Destructive Testing Guardrails (Requirement R7)
- **Zero Save Mutation:** Testers must **never** load, edit, or execute test commands within existing survival worlds or player saves (`.minecraft/saves`). All procedures must take place in an isolated, newly generated superflat QA world.
- **Zero Auto-Start Servers:** Testers must launch the test environment manually via Gradle client tasks or the approved launcher instance. No automated background server processes are permitted to run unmonitored.
- **Server Authority Compliance:** All gameplay actions (chi spending, cooldown timers, damage calculations, and combo sequences) are strictly verified for server-side authority.

### 1.2 Verification Scope by Phase
| Phase | Milestone | Focus Areas | Key Verification Targets |
|:---|:---:|:---|:---|
| **Phase A** | M2 | Charge Orb Lifecycle & Fire Jet Dash | Hand-anchored visual orb (1st & 3rd person), zero `OrbEntity`, dimension switch purge, tracking sync, pure mobility dash ($2.2f$ impulse, 0 damage). |
| **Phase B** | M3 | Animation Foundation & Rig Contract A | 6-bone player model (`head`, `torso`, `arms`, `legs`), single elbow bend kinematics, 1:1 outer sleeve tracking, zero mesh tearing, $0.45\text{s}$ rest pose return, knuckle VFX matrix. |
| **Phase C** | M4 | Fire Jab Full Integration | 9-tick timeline ($2\text{t}$ windup $\to 3\text{t}$ strike $\to 4\text{t}$ recovery), Tick 3 forward-cone damage ($4.0\text{ HP}$ / $6.0\text{ HP}$ combo), multi-stage knuckle VFX, synchronized OGG SFX (`fire_release_1.ogg`). |
| **Phase D** | M5 | Hold-Release Framework & Fire Blast | 5-slot hotbar (`Z/X/C/V/B`), generic hold-release state machine, hand orb dynamic scaling ($0\text{t} \to 40\text{t}$), instant hand orb dissolution on release, scaling fireball entity, $80\text{t}$ auto-release failsafe, sub-tick taps, GUI interruption guard. |

---

## 2. Environment & Workspace Preparation

### 2.1 Toolchain & System Prerequisites
Before launching the client, verify that your development or testing environment satisfies the following:
1. **Operating System:** Windows 10/11, Linux, or macOS.
2. **Java Runtime:**
   - **Mod Runtime:** Eclipse Temurin JDK 21 (`21.0.5+11` or compatible).
   - **Gradle JVM (if building from source):** JDK 25 (`org.gradle.java.home` in `gradle.properties`) or pre-configured Fabric Loom environment.
3. **Audio Output:** Stereo headphones or speakers enabled (for verifying 3D spatial attenuation and channel separation of sound events).

### 2.2 Safe Client Launch Procedure
Launch the client using either the Gradle development task or PrismLauncher/Modrinth:

#### Option A: Gradle Development Client (Recommended)
```powershell
# Open terminal at repository root
cd "D:\repo\Minecraft Mod & Rp\mod"

# Launch isolated development client
.\gradlew.bat runClient
```
*Note: This command boots into an isolated sandbox environment located at `mod/run/` and will not touch your personal `.minecraft` directory.*

#### Option B: Standalone Launcher (PrismLauncher / Modrinth)
1. Ensure Fabric Loader `0.16.9` or higher (recommended `0.20.1`) is selected for Minecraft `1.21.1`.
2. Verify dependencies installed in the instance `mods/` directory:
   - `fabric-api-0.116.17+1.21.1.jar`
   - `player-animation-lib-fabric-1.1.6+mc.1.21.1.jar`
   - `avatar-elements-0.1.0-alpha.jar` (the compiled mod)
3. Launch the game profile.

---

### 2.3 Creating the Isolated QA World
1. From the Minecraft Title Screen, select **Singleplayer** $\to$ **Create New World**.
2. Configure world parameters:
   - **World Name:** `Avatar_Manual_QA`
   - **Game Mode:** `Creative`
   - **Difficulty:** `Peaceful` (or `Normal` when testing mob combat)
   - **Allow Cheats:** `ON`
   - **World Type:** `Superflat` (Preset: `Redstone Ready` or `Classic Flat`)
3. Click **Create New World**.

### 2.4 Initialization Commands & Testing Stance
Upon loading into the world, open the in-game chat (`T`) and execute the following configuration script:

```mcfunction
# 1. Lock day cycle and clear weather for consistent visibility
/gamerule doDaylightCycle false
/gamerule doMobSpawning false
/gamerule doWeatherCycle false
/time set noon
/weather clear

# 2. Reset player state and inventory
/clear
/effect clear @s
/gamemode creative

# 3. Equip testing stick (for scale) and confirm Chi baseline
/give @s minecraft:stick 1
/scoreboard players get @s avatar_chi
```

### 2.5 Element Selection Verification
1. Use an isolated QA world and press/release `R` once per change. The order must be `FIRE → AIR → WATER → EARTH → FIRE`; wait for the HUD to update from the server before pressing a skill.
2. With each element displayed, try one populated slot and confirm the skill corresponds to the element shown. Repeat several casts without pressing `R`; the HUD element must remain unchanged.
3. Cycle to `FIRE` and verify its current slot mapping:
   - **Slot 1 (`Z`):** `avatar:fire_jab`
   - **Slot 2 (`X`):** `avatar:fire_blast`
   - **Slot 3 (`C`):** `avatar:flame_sweep`
   - **Slot 4 (`V`):** `avatar:fire_guard`
   - **Slot 5 (`B`):** `avatar:fire_jet`
4. In a two-client test, change one player's element several times while the other player casts. Confirm each player's HUD and skill mapping remain independent.
5. If the HUD changes without `R`, capture the latest log and report the last input, displayed element, and skill cast. This result is a blocker; do not mark element sync or multiplayer verification passed.

### 2.6 Directional Hitbox Accuracy
Use only an isolated QA world and a stationary target. Keep the player position fixed and record the element, slot, range, aim point, and whether damage/knockback occurred.

1. For Fire Jab, test the target centered in front at close range and near the configured range. Then test one target behind the player. The front targets should register; the rear target should not.
2. For Air Blast and Water Whip, aim through the center of the target at close and maximum range. Repeat with the target slightly off-axis, clearly outside the visual attack path, and behind a solid block.
3. Confirm only targets intersecting the attack path are affected. If a target is missed, capture the distance and player/target positions; do not compensate by globally increasing range without checking collateral hits.

---

## 3. Phase A: Charge Orb Lifecycle & Fire Jet Pure Mobility

### Test A1: Charge Orb Visual & Perspective Verification
**Objective:** Confirm that the charging orb appears strictly as a hand-anchored client visual in both 1st-person and 3rd-person perspectives, with smooth yaw tracking and zero crosshair occlusion.

#### Step-by-Step Instructions:
1. Switch to **First-Person View** (press `F5` until hands are visible from player viewpoint).
2. Look straight ahead at the horizon (Pitch $0.0^\circ$).
3. Press and hold `X` (Slot 2: `fire_blast`):
   - **Checkpoint 1st-Person:** A glowing orange-red UV sphere appears in the lower-right viewmodel area ($\text{Offset } X=+0.55, Y=-0.45, Z=-0.70$).
   - **Check Crosshair:** Confirm that the center crosshair is completely unobstructed by the orb.
4. Press `F5` twice to switch to **Third-Person Back View**.
5. Press and hold `X`:
   - **Checkpoint 3rd-Person:** The orb is attached directly to the right hand/knuckle.
6. While holding `X`, turn your player in a full $360^\circ$ circle using the mouse:
   - **Checkpoint Yaw Tracking:** The orb smoothly rotates with the player's torso/body yaw (`player.bodyYaw`). It does **not** remain fixed to static cardinal world axes.
7. Switch to **Third-Person Front View** (`F5` again) and repeat step 6 to inspect front alignment.

---

### Test A2: Zero `OrbEntity` Hand Verification
**Objective:** Prove Requirement R3: hand charging orbs are 100% State + Visual rendering (`ChargeOrbClientState` & `ChargeOrbRenderer`). **No entity** is spawned in the world during charging.

#### Step-by-Step Instructions:
1. Summon a test marker armor stand nearby for baseline entity detection:
   ```mcfunction
   /summon armor_stand ~ ~ ~3 {CustomName:'"BaselineTarget"',NoGravity:1b}
   ```
2. Press and hold `X` (Fire Blast charge).
3. While continuously holding `X` with your left hand, open the chat console or check server entity count:
   ```mcfunction
   /execute if entity @e[type=!player,type=!armor_stand]
   ```
4. **Expected Result:**
   - Output must report: `Test failed, count is 0` (or `No entity was found`).
   - Open F3 debug screen $\to$ check the `E: <rendered>/<total>` entity counter on the 2nd line. Total entities must remain constant (e.g. `E: 1/1`).
   - **Conclusion:** There is **no** `OrbEntity`, `FireballEntity`, or rogue projectile entity present in the world while charging in hand.

---

### Test A3: Stale Serial & Rapid Re-cast Protection
**Objective:** Verify that rapid sequential skill triggers and monotonic `castSerial` packet headers prevent older `IDLE` packets from prematurely clearing newer charge visuals.

#### Step-by-Step Instructions:
1. Rapidly tap `Z` (Fire Jab) followed immediately by pressing and holding `X` (Fire Blast) within $< 150\text{ms}$.
2. Observe the right hand visual:
   - **Expected Result:** The `IDLE` reset packet from the completed Fire Jab has a lower `castSerial` than the new Fire Blast cast.
   - The Fire Blast charge orb must **remain visible and expanding** on the hand. It must **not** flicker out or vanish prematurely due to the preceding Jab's completion.

---

### Test A4: Mid-Cast Dimension Switch Test
**Objective:** Confirm that entering a portal or switching dimensions mid-cast instantly cancels the server timeline and purges client orb states without orphaned visuals lingering across worlds.

#### Step-by-Step Instructions:
1. Position yourself in the Overworld flat world.
2. Prepare the dimension teleport command in chat history:
   ```mcfunction
   /execute in minecraft:the_nether run tp @s 0 70 0
   ```
3. Press and hold `X` (Fire Blast charge) to spawn the full hand orb.
4. While continuing to hold `X`, execute the teleport command (press `Enter`).
5. Observe the transition into the Nether:
   - **Expected Result:**
     - The moment the dimension changes, `ServerEntityWorldChangeEvents.AFTER_PLAYER_CHANGE_WORLD` fires on the server, cancelling the timeline and broadcasting `IDLE`.
     - `ClientWorldEvents.AFTER_CLIENT_WORLD_CHANGE` fires on the client, invoking `ChargeOrbClientState.clear()`.
     - Upon rendering in the Nether, the hand is completely clean. No ghost orb or glowing sphere is frozen in mid-air at `(0, 70, 0)` or floating in the Overworld.
6. Teleport back to the Overworld (`/execute in minecraft:overworld run tp @s 0 4 0`) and verify the hand remains completely clear.

---

### Test A5: Mid-Cast Watcher Tracking Sync (Multiplayer / Dual Instance)
**Objective:** Verify that an approaching player entering entity tracking range of a charging player immediately sees the active charge orb without waiting for the next phase packet.

#### Step-by-Step Instructions (Requires 2 clients or test harness):
1. **Player 1 (Caster):** Stands stationary at coordinates `(100, 4, 100)`.
2. **Player 2 (Watcher):** Moves outside tracking range ($> 64\text{ blocks}$, e.g. at `(0, 4, 100)`).
3. **Player 1:** Presses and holds `X` (charging Fire Blast).
4. **Player 2:** Teleports or walks into tracking range:
   ```mcfunction
   /tp @s 90 4 100
   ```
5. **Observation on Player 2's Screen:**
   - `EntityTrackingEvents.START_TRACKING` triggers `SkillNetworking.syncOrbStateToNewWatcher()`.
   - Player 2 immediately sees Player 1 holding the glowing charge orb on their right hand. The orb does **not** require Player 1 to release or re-cast to become visible.

---

### Test A6: Fire Jet Pure Mobility Dash
**Objective:** Verify that Fire Jet (Slot 5: `B`) acts strictly as a mobility propulsion dash with $2.2f$ horizontal velocity, $0.4f$ vertical lift, zero damage, and zero spawned projectile entities.

#### Step-by-Step Instructions:
1. Summon a test zombie with disabled AI directly in front of you:
   ```mcfunction
   /summon zombie ~ ~ ~2 {NoAI:1b,CustomName:'"DashTestTarget"'}
   ```
2. Verify zombie initial health:
   ```mcfunction
   /data get entity @e[name=DashTestTarget,limit=1] Health
   ```
   *(Expected: `20.0f`)*.
3. Aim directly at the zombie's chest (Pitch $0.0^\circ$).
4. Press `B` (Slot 5: `avatar:fire_jet`):
   - **Impulse & Trajectory:** The player is instantly launched forward with powerful velocity ($2.2\text{ blocks/tick}$ horizontal, $0.4\text{ blocks/tick}$ vertical boost), cleanly flying through or past the zombie.
   - **Audio:** `SoundEvents.ENTITY_BLAZE_SHOOT` plays at volume 1.0, pitch 0.7.
   - **Particles:** A trail of 6 `FLAME` and 2 `LARGE_SMOKE` particles spawns at your feet every 2 ticks during the 10-tick dash.
   - **Chi & Cooldown:** 25 Chi is consumed from the HUD pool; a 30-tick (1.5s) cooldown appears on the Slot 5 icon.
5. Re-check the zombie's health:
   ```mcfunction
   /data get entity @e[name=DashTestTarget,limit=1] Health
   ```
   - **Expected Result:** Health remains exactly `20.0f`.
   - **Conclusion:** Fire Jet deals **0.0 damage**, has no attack hitbox, spawns no projectiles, and operates 100% as a pure mobility dash.

---

## 4. Phase B: Animation Foundation & Rig Contract A

### Test B1: Rig Contract A 6-Bone Mapping
**Objective:** Confirm that skill animations map strictly to the 6 standard vanilla player bones via PlayerAnimationLib (`PAL 1.1.6`), ensuring complete compatibility with standard Minecraft player skins.

#### Step-by-Step Instructions:
1. Switch to **Third-Person View** (`F5`).
2. Press `Z` (Slot 1: `avatar:fire_jab`).
3. Observe player model articulation:
   - Identify movement on all 6 canonical bones:
     1. `torso`: Rotates $-35.0^\circ$ yaw during windup, rotates $+12.0^\circ$ forward on strike.
     2. `head`: Counter-rotates $+35.0^\circ$ yaw during windup so player gaze remains locked on the crosshair.
     3. `right_arm`: Draws back slightly, then punches forward with $+58.4^\circ$ pitch at strike apex.
     4. `left_arm`: Rises into a defensive guard stance ($+41.5^\circ$ pitch, $+12.8^\circ$ roll).
     5. `right_leg`: Braces backward ($-15.0^\circ$ pitch, $-15.0^\circ$ yaw).
     6. `left_leg`: Steps forward ($+15.0^\circ$ pitch, $-15.0^\circ$ yaw).
4. Verify that no non-standard sub-bones (e.g. separate `forearm` or `bicep` bones) are required, satisfying Rig Contract A.

---

### Test B2: Single Elbow Bend Kinematics
**Objective:** Verify that the punch motion visually represents a single elbow bend through projected Euler arm kinematics without requiring external skeleton libraries.

#### Step-by-Step Instructions:
1. Stand perpendicular to a wall or orient the camera to the player's side in 3rd-person view (`F5`).
2. Press `Z` (Fire Jab) and carefully watch the right arm trajectory from $t=0.0\text{s}$ to $t=0.15\text{s}$:
   - **At $t=0.10\text{s}$ (Anticipation peak):** Right arm is tucked close to the ribs ($\text{pitch } +3.08^\circ, \text{yaw } -0.20^\circ, \text{roll } +7.28^\circ$).
   - **At $t=0.15\text{s}$ (Strike Apex):** Right arm extends sharply forward ($\text{pitch } +58.40^\circ, \text{yaw } +6.56^\circ, \text{roll } -11.71^\circ$).
   - **Visual Result:** The arm creates the distinct, punchy silhouette of a martial arts jab. The forearm projects forward at chest height ($Y \approx 1.04\text{m}$ relative to feet) rather than swinging in an unbent windmill arc.

---

### Test B3: Synchronous Sleeve & Outer Layer Tracking (Zero Mesh Tearing)
**Objective:** Confirm that outer skin layers (`jacket`, `rightSleeve`, `leftSleeve`, `rightPants`, `leftPants`, `hat`) track 1:1 with base bones without mesh separation, gap tearing, or clipping.

#### Step-by-Step Instructions:
1. Open Minecraft Settings $\to$ **Skin Customization**.
2. Ensure **all** outer skin layers are turned **ON**:
   - `Jacket: ON`, `Right Sleeve: ON`, `Left Sleeve: ON`, `Right Pants Leg: ON`, `Left Pants Leg: ON`, `Hat: ON`.
3. Stand in a brightly lit area in third-person view.
4. Execute `fire_jab` (`Z`) repeatedly while closely inspecting the right shoulder and elbow joints:
   - **Expected Result:**
     - The outer 3D sleeve moves synchronously and locked with the inner arm layer.
     - There is **zero pixel separation**, no hollow voids exposed inside the arm, and no flickering Z-fighting between inner and outer geometry during high-speed rotation ($58.4^\circ$ in $0.05\text{s}$).

---

### Test B4: 0.45s Rest Pose Return (Zero-Delta Recovery)
**Objective:** Prove that the animation returns 100% identically to the player's baseline rest pose upon completion at $t=0.45\text{s}$ (9 ticks), with zero drifting or frozen limbs.

#### Step-by-Step Instructions:
1. Align your player standing completely still on a flat surface in 3rd person.
2. Note the resting arm position alongside the torso.
3. Press `Z` (Fire Jab):
   - Watch the full animation cycle: Windup ($0.10\text{s}$) $\to$ Strike ($0.15\text{s}$) $\to$ Recovery ($0.20\text{s}$ to $0.45\text{s}$).
4. At $t \ge 0.45\text{s}$:
   - Inspect player model angles:
     - Torso yaw returns to baseline.
     - Head alignment returns to neutral forward gaze.
     - Right and left arms return completely to side rest position (`playerAnimLib$setToInitialPose`).
   - Walk forward and backward: confirm vanilla walking swing resumes immediately without stuttering or stuck limb offsets.

---

### Test B5: Knuckle Attachment Point VFX Placement
**Objective:** Verify that `KnuckleVfxHelper` correctly computes the fist matrix $P_{\text{knuckle}} = \text{Matrix}_{\text{right\_arm}} \times [-1.0/16.0, 8.0/16.0, 0.0]^T$ so that flame particles emanate directly from the fist knuckle.

#### Step-by-Step Instructions:
1. Enter third-person front view (`F5`).
2. Press `Z` (Fire Jab) and observe the strike apex ($t=0.15\text{s}$):
   - **Visual Result:** The initial flame flash (`ParticleTypes.FLAME` and `SMALL_FLAME`) spawns directly on the right fist knuckles ($X \approx -0.35\text{m}, Y \approx 1.04\text{m}, Z \approx -0.40\text{m}$).
   - The flame burst does **not** spawn inside the player's head, behind the shoulder, or at ground level.
3. Turn $90^\circ, 180^\circ,$ and $270^\circ$ and repeat: verify the knuckle attachment stays perfectly locked to the fist across all orientations.

---

## 5. Phase C: Fire Jab Complete Integration (Requirement R5)

### Test C1: 9-Tick Chronological Timeline Verification
**Objective:** Verify that Fire Jab strictly adheres to the 9-tick FSM state machine: 2 ticks Anticipation $\to$ 3 ticks Strike $\to$ 4 ticks Recovery.

#### Step-by-Step Instructions:
1. Watch the HUD Chi and Cooldown indicators while tapping `Z`:
   - **Tick 1–2 ($0.00\text{s} - 0.10\text{s}$, WINDUP):**
     - Chi pool immediately deducts 8 Chi ($100 \to 92$).
     - Player right arm pulls back into ready punch chamber.
     - Hand charge orb flickers on the fist.
     - No damage or hitboxes are active yet.
   - **Tick 3 ($0.15\text{s}$, ACTIVE Tick 1):**
     - Strike execution apex occurs.
     - Hitbox detects entities, damage is dealt, knuckle VFX erupts, and SFX plays.
   - **Tick 4–5 ($0.15\text{s} - 0.25\text{s}$, ACTIVE Ticks 2–3):**
     - Arm remains extended in follow-through. Hitbox is no longer active (single-tick trigger).
   - **Tick 6–9 ($0.25\text{s} - 0.45\text{s}$, RECOVERY):**
     - Arm and torso smoothly lerp back to rest pose.
     - Cooldown timer of 6 ticks ($0.3\text{s}$) counts down to 0 on the HUD.
     - Chi regeneration pulses resume ($+1\text{ Chi} / 4\text{ ticks}$).

---

### Test C2: Tick 3 Hitbox & Forward Cone Dot-Product Filter
**Objective:** Verify that Fire Jab deals $4.0\text{ HP}$ base damage strictly on Tick 3, and that entities directly behind the player within the spherical radius take **zero** damage due to forward cone filtering.

#### Step-by-Step Instructions:
1. Spawn two stationary zombies: one directly in front, one directly behind:
   ```mcfunction
   # Front target: 2 blocks in front
   /summon zombie ~ ~ ~2 {NoAI:1b,CustomName:'"FrontTarget"'}

   # Rear target: 1.5 blocks behind
   /summon zombie ~ ~ ~-1.5 {NoAI:1b,CustomName:'"RearTarget"'}
   ```
2. Verify both zombies have full health:
   ```mcfunction
   /execute as @e[type=zombie] run data get entity @s Health
   ```
   *(Both output `20.0f`)*.
3. Stand between them, facing **FrontTarget** directly.
4. Press `Z` (Fire Jab):
   - **FrontTarget:** Flashes red, takes **$4.0\text{ HP}$ damage** (health drops to `16.0f`), and suffers $0.3\text{ blocks}$ knockback.
   - **RearTarget:** Does **not** flash red, takes **$0.0\text{ damage}$** (health remains `20.0f`).
   - **Conclusion:** The spherical bounding box ($r=2.5\text{m}$, center offset $+1.5\text{m}$) correctly enforces the forward dot-product cone filter (`dotProduct(look) > 0.0`), preventing rear hits.

---

### Test C3: Multi-Stage Knuckle VFX Burst
**Objective:** Confirm that Fire Jab deploys the 3-stage particle burst at Tick 3: Knuckle Flash $\to$ Strike Jet Midpoint $\to$ Apex Burst.

#### Step-by-Step Instructions:
1. Ensure Minecraft Video Settings $\to$ **Particles** is set to **ALL**.
2. Stand in third-person view and press `Z` against a dark backdrop or at dusk (`/time set 13000`):
   - **Stage 1 (Knuckle Flash):** 4 `FLAME` and 4 `SMALL_FLAME` particles at the fist knuckle ($P_{\text{fist}}$).
   - **Stage 2 (Strike Jet Midpoint):** 10 `FLAME` particles streaming along the punch vector ($P_{\text{mid}} = P_{\text{fist}} + 0.55 \cdot \mathbf{u}_{\text{look}}$).
   - **Stage 3 (Apex Burst):** 8 `FLAME` and 4 `SMOKE` particles blooming at punch range apex ($P_{\text{apex}} = P_{\text{eye}} + 1.50 \cdot \mathbf{u}_{\text{look}}$).
3. Confirm that particles dissipate naturally within $0.5\text{ seconds}$ without floating indefinitely.

---

### Test C4: Synchronized OGG Sound Event Playback
**Objective:** Confirm that custom sound event `avatar_elements:fire.release` / `skill.fire.fire_jab.strike` triggers synchronously on Tick 3, using transcoded mono OGG audio `fire_release_1.ogg` with proper 3D stereo panning.

#### Step-by-Step Instructions:
1. Open Minecraft Settings $\to$ **Music & Sounds**:
   - Ensure `Master Volume: 100%`, `Players: 100%`, `Subtitles: ON`.
2. Stand still and press `Z`:
   - **Audio Playback:** A crisp, fiery whoosh sound plays exactly when the fist reaches apex extension at Tick 3 ($0.15\text{s}$).
   - **Subtitles Check:** In the bottom-right corner, a subtitle appears:
     `Fire Jab whoosh` (or `subtitles.avatar_elements.fire.release`).
   - **3D Spatial Panning:** Turn your head $90^\circ$ to the left of a target while another player or clone casts Fire Jab: confirm sound pans realistically into your right ear.

---

### Test C5: 3-Hit Combo Sequence Integration
**Objective:** Verify that executing Flame Sweep (`C`, Slot 3) followed by Fire Jab (`Z`, Slot 1) within the 8-tick combo window triggers the empowered final combo strike ($1.5\times$ damage, $1.3\times$ range, Lava & Crit VFX).

#### Step-by-Step Instructions:
1. Spawn a fresh test zombie at $3.0\text{ blocks}$ distance:
   ```mcfunction
   /summon zombie ~ ~ ~3 {NoAI:1b,CustomName:'"ComboTarget"'}
   ```
2. Press `C` (Slot 3: `avatar:flame_sweep`):
   - Arc sweep strikes the zombie for $6.0\text{ HP}$ (zombie health drops from $20.0 \to 14.0$).
   - The combo window opens for 8 ticks ($0.4\text{s}$).
3. Within 8 ticks, immediately press `Z` (Slot 1: `avatar:fire_jab`):
   - **Hitbox Extension:** Fire Jab reaches the target at $3.0\text{ blocks}$ (normal range is $2.5\text{m}$, combo range expands to $3.25\text{m}$).
   - **Empowered Damage:** Target takes **$6.0\text{ HP}$ damage** ($4.0 \times 1.5$, health drops from $14.0 \to 8.0$).
   - **Combo Visual Accents:** In addition to normal flames, 4 `LAVA` sparks and 6 `CRIT` particles explode violently at the apex!
   - **Audio:** `ModSounds.FIRE_RELEASE` plays at full volume $1.0f$ with sharp attack pitch.

---

## 6. Phase D: Hold-Release Framework & Fire Blast (Requirement R6)

### Test D1: 5-Slot Hotbar Keybind Verification
**Objective:** Confirm that all 5 skill slots (`Z`, `X`, `C`, `V`, `B`) operate correctly without slot omissions or key collisions.

#### Step-by-Step Instructions:
1. Open Minecraft Options $\to$ **Controls** $\to$ **Key Binds**:
   - Scroll to category `Avatar: Elements`.
   - Verify all 5 defaults are mapped (all are rebindable in Controls):
     - `Skill Slot 1`: `Z`
     - `Skill Slot 2`: `X`
     - `Skill Slot 3`: `C`
     - `Skill Slot 4`: `V`
     - `Skill Slot 5`: `B`
   - Optional rebind check: change one slot to a comfortable unused key, confirm the new key works and the old one no longer activates it, then restore the setting.
2. In-game, press each key sequentially and verify the Action Bar feedback:
   - Press `Z` $\to$ `[Avatar] avatar:fire_jab — OK`
   - Press `X` $\to$ Enters Fire Blast hold charge
   - Press `C` $\to$ `[Avatar] avatar:flame_sweep — OK`
   - Press `V` $\to$ `[Avatar] avatar:fire_guard — OK`
   - Press `B` $\to$ Fire Jet mobility dash activates

---

### Test D2: Hold-Release Charging State Machine
**Objective:** Verify that `C2SHoldStart` spends Chi upfront and enters the `HOLD` phase, while `C2SHoldRelease` initiates the `ACTIVE` phase and applies cooldown.

#### Step-by-Step Instructions:
1. Ensure your Chi is at $100/100$.
2. Press and hold `X`:
   - **Immediate Action:** 20 Chi is deducted ($100 \to 80$).
   - **State:** Player enters `HOLD` phase.
   - **Cooldown Check:** Notice that the Slot 2 icon does **not** go on cooldown while holding. You can hold and aim indefinitely up to the failsafe.
3. Release `X`:
   - **Release Action:** `C2SHoldRelease` packet is dispatched to the server.
   - **Phase Transition:** Timeline shifts `HOLD \to ACTIVE`.
   - **Cooldown Applied:** A 20-tick ($1.0\text{s}$) cooldown starts immediately upon release.

---

### Test D3: Hand Orb Scaling & Instant Dissolution
**Objective:** Confirm that the hand charge orb dynamically scales in size during the $40\text{t}$ hold, and **dissolves instantaneously** upon release without ghosting.

#### Step-by-Step Instructions:
1. In Third-Person View (`F5`), press and hold `X`:
   - At $t=0\text{t}$ ($0.0\text{s}$): Orb starts at base radius $R = 0.20\text{m}$.
   - At $t=20\text{t}$ ($1.0\text{s}$): Orb reaches intermediate radius $R \approx 0.325\text{m}$.
   - At $t=40\text{t}$ ($2.0\text{s}$): Orb reaches maximum radius $R = 0.45\text{m}$ (dense blazing sphere).
   - From $t=40\text{t}$ to $t=80\text{t}$: Orb stays locked at maximum size.
2. In First-Person View, press and hold `X`:
   - Viewmodel orb expands smoothly from radius $0.06$ to $0.14$.
3. Release `X`:
   - **Instant Dissolution:** The hand orb vanishes on the exact frame of release (`OrbVisualConfig` maps Fire Blast strictly to `WINDUP` and `HOLD`).
   - The fireball projectile entity launches from the hand into the world. There is zero overlap or double-orb visual artifact.

---

### Test D4: Scaling Fireball Projectile Flight & AOE Detonation
**Objective:** Compare minimum-charge tap versus maximum-charge hold for projectile flight, collision damage, AOE explosion radius, and particle effects.

#### Comparison Test Matrix:
| Parameter | Minimum Tap (1–5 ticks) | Maximum Charge (40+ ticks) |
|:---|:---:|:---:|
| **Charge Ratio ($C$)** | $0.10$ | $1.00$ |
| **Projectile Speed** | $1.8\text{ blocks/tick}$ | $1.8\text{ blocks/tick}$ |
| **Flight Trail VFX** | 6 `FLAME`, 3 `SMOKE` | 14 `FLAME`, 3 `SMOKE`, 1 `LAVA` |
| **Direct / AOE Damage** | $2.45\text{ HP}$ ($1.22\text{ hearts}$) | **$7.00\text{ HP}$ ($3.50\text{ hearts}$)** |
| **Blast AOE Radius ($R$)** | $1.0\text{ block}$ | **$3.0\text{ blocks}$** |
| **Knockback** | $0.55$ | **$1.00$** |
| **Explosion VFX** | 1 `EXPLOSION`, 22 `FLAME` | 1 `EXPLOSION`, **45 `FLAME`, 8 `LAVA`, 12 `SMOKE`** |
| **Detonation Audio** | Generic Explode (Pitch 1.27) | Generic Explode (**Deep Pitch 1.00**, Volume 1.2) |

#### Step-by-Step Instructions:
1. **Minimum Charge Test:**
   - Tap `X` rapidly at a target $10\text{ blocks}$ away:
   - Observe fast-flying small fireball.
   - On impact with ground or mob: small pop explosion, target takes $\approx 2.45\text{ HP}$ damage.
2. **Maximum Charge Test:**
   - Hold `X` for $> 2.0\text{ seconds}$ (40+ ticks), then release at a cluster of 3 mobs spaced 2 blocks apart:
   - Fireball launches with blazing lava trail.
   - On impact: massive explosion erupts, all 3 mobs in the $3.0\text{m}$ radius take **$7.0\text{ HP}$ damage** and are violently knocked backward.
   - Deep, resonant explosion boom sounds.

---

### Test D5: 80-Tick Auto-Release Failsafe
**Objective:** Verify that holding the `X` key continuously past 80 ticks ($4.0\text{s}$, $2\times \text{max charge}$) triggers the server-side auto-release failsafe to prevent orphaned hold states.

#### Step-by-Step Instructions:
1. Aim toward an open field.
2. Press and hold `X` and **do not release the key**.
3. Count 4 seconds ($80\text{ ticks}$):
   - At exactly $t = 4.0\text{s}$:
     - The fireball automatically fires from your hand.
     - The hand orb instantly dissolves.
     - Cooldown is applied automatically on the HUD.
   - **Conclusion:** The failsafe prevents stuck charging if a client drops a release packet or experiences a keyup glitch.

---

### Test D6: Sub-Tick Quick Tap (< 50ms) Responsiveness
**Objective:** Confirm that tapping `X` for a fraction of a frame ($< 50\text{ms}$) registers reliably and does not trap the client in a perpetual charging loop.

#### Step-by-Step Instructions:
1. Very quickly click/tap `X` as fast as possible (a momentary key stroke).
2. Observe behavior:
   - `AvatarElementsClient.java` detects `tapped` via `key.wasPressed()` and checks `!pressedNow`.
   - Client sends `C2SHoldStart` immediately followed by `C2SHoldRelease`.
   - The fireball launches cleanly with minimum charge ($C=0.10$).
   - The player does **not** become permanently stuck holding or charging.

---

### Test D7: GUI Screen Open Interruption Guard
**Objective:** Verify that opening an inventory, chat window, or pause menu while holding `X` cleanly terminates the charge without stuck keys.

#### Step-by-Step Instructions:
1. Press and hold `X` (charge begins).
2. While continuing to hold `X`, press `E` (Open Inventory) or `T` (Open Chat) or `Esc`:
   - `client.currentScreen != null` triggers the hold-cancel guard.
   - `slotHolding[slot]` is set to `false`, and `sendHoldRelease` is cleanly dispatched.
   - The fireball fires or cancels safely.
3. Close the GUI screen (`Esc`): confirm the player is not stuck charging and normal controls resume.

---

## 7. Comprehensive Acceptance Matrix (Expected Results)

| Test ID | Feature / Component | Input Trigger | Expected Visual Checkpoint | Expected Audio Event | Expected Server Authority State | Acceptance Status |
|:---:|:---|:---|:---|:---|:---|:---:|
| **A-01** | 1st-Person Charge Orb | Hold `X` (Fire Blast) | Glowing UV sphere at lower-right viewmodel; crosshair 100% clear. | None (charging phase) | `HOLD` phase in timeline; 20 Chi spent upfront. | [ ] PASS |
| **A-02** | 3rd-Person Charge Orb | Hold `X`, rotate view | Orb anchored to right hand; rotates smoothly with body yaw ($360^\circ$). | None | Zero `OrbEntity` in world (`@e` count unchanged). | [ ] PASS |
| **A-03** | Stale Serial Guard | Rapid `Z` $\to$ `X` tap | Fire Blast orb remains visible; not cleared by prior `IDLE` packet. | Sequential SFX | Monotonic `castSerial` increments ($N \to N+1$). | [ ] PASS |
| **A-04** | Dimension Switch Reset | Hold `X` + TP to Nether | Orb immediately cleared on Nether spawn; zero ghost artifacts. | None | Server cancels timeline; broadcasts `IDLE`. | [ ] PASS |
| **A-05** | Watcher Tracking Sync | Approaching player | Observer sees charge orb on caster's hand upon entering render range. | None | `START_TRACKING` packet syncs active state. | [ ] PASS |
| **A-06** | Fire Jet Mobility Dash | Press `B` (Slot 5) | Powerful forward impulse ($2.2f$ look, $0.4f$ up); flame/smoke trail. | `ENTITY_BLAZE_SHOOT` | $0.0\text{ damage}$ dealt; no hitbox query or entities. | [ ] PASS |
| **B-01** | Rig Contract A Bones | Press `Z` (Fire Jab) | 6 vanilla bones articulate (`head`, `torso`, `arms`, `legs`). | Audio at Tick 3 | No custom GeckoLib bone requirements. | [ ] PASS |
| **B-02** | Single Elbow Bend | Press `Z` (Side view) | Arm projects forward at chest height ($Y \approx 1.04\text{m}$, Pitch $+58.4^\circ$). | Audio at Tick 3 | Projected Euler kinematics. | [ ] PASS |
| **B-03** | Sleeve Layer Tracking | Press `Z` (Sleeves ON) | Outer 3D skin layer locked 1:1 with arm; zero tearing or z-fighting. | None | Synchronous PAL model transform. | [ ] PASS |
| **B-04** | Rest Pose Return | $t \ge 0.45\text{s}$ (9 ticks) | 100% zero-delta return to neutral stance; walk animation resumes. | None | `playerAnimLib$setToInitialPose` invoked. | [ ] PASS |
| **B-05** | Knuckle VFX Attachment | Press `Z` (Front view) | Flame flash anchored directly to fist knuckle across all yaw angles. | Audio at Tick 3 | Knuckle matrix transform $[-1/16, 8/16, 0]$. | [ ] PASS |
| **C-01** | Fire Jab 9-Tick FSM | Press `Z` | $2\text{t}$ windup $\to 3\text{t}$ strike $\to 4\text{t}$ recovery. Cooldown 6t. | Sound at Tick 3 | Chi $-8$; timeline advances strictly per tick. | [ ] PASS |
| **C-02** | Tick 3 Hitbox & Cone | Press `Z` facing mob | Front target takes $4.0\text{ HP}$; rear target within radius takes $0\text{ HP}$. | Mob hurt sound | Forward cone dot-product filter enforced. | [ ] PASS |
| **C-03** | Multi-Stage VFX Burst | Press `Z` | Stage 1 (Fist flash) $\to$ Stage 2 (Jet) $\to$ Stage 3 (Apex burst). | Sound at Tick 3 | Particle counts: 8 fist, 10 jet, 12 apex. | [ ] PASS |
| **C-04** | OGG Audio Playback | Press `Z` | Crisp fire release audio with 3D directional stereo panning. | `fire.release` (mono OGG) | Registered in `Registries.SOUND_EVENT`. | [ ] PASS |
| **C-05** | 3-Hit Combo Strike | Press `C` $\to$ Press `Z` | Jab deals $6.0\text{ HP}$ ($1.5\times$); Lava & Crit sparks explode at apex. | `fire.release` (vol 1.0) | Combo window validated; range bonus $1.3\times$. | [ ] PASS |
| **D-01** | 5-Slot Hotbar Mapping | Press `Z, X, C, V, B` | All 5 slots cast their respective Fire skills cleanly. | Respective SFX | Clean `element_slots.json` mapping. | [ ] PASS |
| **D-02** | Hold-Release State | Hold `X` $\to$ Release | Chi deducted on start; Cooldown applied strictly on release. | Launch Blaze Shoot | `C2SHoldStart` & `C2SHoldRelease` protocol. | [ ] PASS |
| **D-03** | Hand Orb Dissolution | Release `X` | Hand orb vanishes on exact frame of projectile launch. | Projectile launch SFX | Hand orb active in `WINDUP/HOLD` only. | [ ] PASS |
| **D-04** | Fireball Scaling | Tap vs. 40t Hold | Damage $2.45 \to 7.0\text{ HP}$; AOE Radius $1.0 \to 3.0\text{m}$; Heavy VFX. | Deep explode boom | `FireBlastProjectileEntity` scaling logic. | [ ] PASS |
| **D-05** | 80t Failsafe Release | Hold `X` for 4 seconds | Fireball auto-launches at $t=4.0\text{s}$; cooldown starts. | Detonation SFX | Auto-release triggered at `ticks >= limit * 2`. | [ ] PASS |
| **D-06** | Sub-Tick Tap (<50ms) | Rapid click `X` | Minimum charge fireball launches cleanly; no hold lockup. | Launch SFX | Key polling catches quick falling edge. | [ ] PASS |
| **D-07** | GUI Interrupt Guard | Hold `X` + Press `E` | Hold cleanly cancels; no stuck key state upon exiting inventory. | None | Screen check releases hold cleanly. | [ ] PASS |

---

## 8. Troubleshooting & Diagnostics Guide

### 8.1 Audio & Sound Event Issues
- **Symptom:** No sound is heard when casting Fire Jab, but visual punch and damage work.
  - **Check 1:** Open Options $\to$ Music & Sounds $\to$ verify **Players** and **Master Volume** are $> 0\%$.
  - **Check 2:** Verify that the audio output device is in **Stereo Mode** (Minecraft spatial audio fails to pan on 7.1 surround virtualizers).
  - **Check 3:** Inspect game log (`mod/run/logs/latest.log`) for `Missing sound event: avatar_elements:fire.release`. If missing, verify `sounds.json` exists in `assets/avatar_elements/` and `ModSounds.init()` was called during mod initialization.

### 8.2 Orb Rendering & Perspective Issues
- **Symptom:** Orb appears in 3rd-person view, but not in 1st-person viewmodel space.
  - **Check 1:** Verify you are not holding a full-screen GUI screen open.
  - **Check 2:** Check F3 debug screen $\to$ verify `mc.options.getPerspective().isFirstPerson()` is true.
  - **Check 3:** Verify that `FirstPersonOrbRenderer.register()` was registered to `WorldRenderEvents.LAST`.
- **Symptom:** Orb in 3rd-person does not rotate when the player turns around.
  - **Check:** Verify `ChargeOrbRenderer.java` incorporates `player.bodyYaw` rotation via `Vec3d.rotateY(yawRad)` on the hand offset.

### 8.3 Keybinding & Hotbar Conflicts
- **Symptom:** Pressing `Z` or `X` does not cast any skill.
  - **Check 1:** Open Options $\to$ Controls $\to$ Key Binds $\to$ `Avatar: Elements`. Defaults are `Z/X/C/V/B` for skill slots and press `R` to cycle elements; all are rebindable. Avoid red conflicts and movement keys unless intentionally replacing their vanilla actions.
  - **Check 2:** Press the element-cycle key (default `R`) once per step until the HUD shows `FIRE`. If active element is `AIR` or `WATER`, slot contents differ.
  - **Check 3:** Check your Chi pool in the HUD. If Chi is $< 8$, Fire Jab will be denied with `Chi tidak cukup`.

### 8.4 Animation Foundation Issues
- **Symptom:** Character arm stays frozen in extended punch pose and does not return to rest pose.
  - **Check 1:** Ensure `PlayerAnimationLibFabric 1.1.6` is loaded in your mod list.
  - **Check 2:** Verify `fire_jab_test.json` has `loop: "once"` and `animation_length: 0.45`.
  - **Check 3:** Verify `AvatarAnimations.java` layer priority is set to `1000`.

### 8.5 Gradle / Toolchain Launch Failures
- **Symptom:** `.\gradlew.bat runClient` fails with `Dependency requires at least JVM runtime version 25`.
  - **Solution:** As documented in `docs/DECISIONS.md (D012)`, Loom 1.19.3 requires JVM 25+ to run Gradle tasks. Ensure `org.gradle.java.home` in `mod/gradle.properties` points to your JDK 25 install (e.g. `C:/Users/USER/.jdks/jdk-25.0.5+8`). The mod itself compiles to Java 21 bytecode via toolchain.

---

## 9. QA Sign-Off Sheet & Final Acceptance

| Milestone | Scope Verified | Lead Tester Signature | Verification Date | Verdict (PASS / FAIL) |
|:---|:---|:---|:---:|:---:|
| **Milestone 2 (Phase A)** | Charge Orb Lifecycle & Fire Jet Pure Mobility | `_________________________` | `____/__/__` | `[   ]` |
| **Milestone 3 (Phase B)** | 6-Bone Rig Contract A & Single Elbow Bend | `_________________________` | `____/__/__` | `[   ]` |
| **Milestone 4 (Phase C)** | Fire Jab 9-Tick Timeline & Combo Integration | `_________________________` | `____/__/__` | `[   ]` |
| **Milestone 5 (Phase D)** | Hold-Release Framework & Fire Blast Projectile | `_________________________` | `____/__/__` | `[   ]` |
| **Milestone 6 (Acceptance)**| Full E2E Integration & Non-Destructive QA | `_________________________` | `____/__/__` | `[   ]` |

**Final Release Recommendation:**
Upon successful execution of all 22 checklist items above with **0 critical defects**, the Avatar Modding System build is certified **Production-Ready** for Minecraft 1.21.1.
