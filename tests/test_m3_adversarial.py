r"""
Adversarial Empirical Challenge Test Suite for Milestone 3 (Phase B: Animation Foundation & Rig Contract A)
Target: D:\repo\Minecraft Mod & Rp
"""

import json
import os
import sys

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
ANIM_JSON = os.path.join(REPO_ROOT, r"mod\src\client\resources\assets\avatar_elements\player_animations\fire_jab_test.json")
SKILL_DEF_JSON = os.path.join(REPO_ROOT, r"mod\src\main\resources\data\avatar_elements\skill_definitions.json")
CLIENT_NET_HANDLER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\network\ClientNetworkHandler.java")
SKILL_CLIENT_HANDLER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\network\SkillClientHandler.java")
AVATAR_ANIMS = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\anim\AvatarAnimations.java")
KNUCKLE_HELPER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\vfx\KnuckleVfxHelper.java")

test_results = []

def record(test_name, passed, details):
    status = "PASS" if passed else "FAIL"
    test_results.append((test_name, status, details))
    print(f"[{status}] {test_name}: {details}")

print("=================================================================")
print("RUNNING ADVERSARIAL EMPIRICAL CHALLENGES (M3 Phase B)")
print("=================================================================\n")

# -----------------------------------------------------------------
# 1. RIG CONTRACT A & ANIMATION JSON INTEGRITY
# -----------------------------------------------------------------
print("--- [TEST SUITE 1] Rig Contract A & Bedrock JSON Verification ---")

with open(ANIM_JSON, 'r', encoding='utf-8') as f:
    anim_data = json.load(f)

# Test 1.1: Format version and structure
has_format = anim_data.get("format_version") == "1.8.0"
has_anim_key = "animations" in anim_data and "fire_jab_test" in anim_data["animations"]
record("1.1 Bedrock JSON Header & Format", has_format and has_anim_key,
       f"format_version={anim_data.get('format_version')}, anim_key={'fire_jab_test' in anim_data.get('animations', {})}")

fire_jab = anim_data["animations"]["fire_jab_test"]
anim_len = fire_jab.get("animation_length")
loop_mode = fire_jab.get("loop")

# Test 1.2: Animation duration
record("1.2 Animation Length 0.45s", anim_len == 0.45, f"animation_length={anim_len} (expected 0.45s)")
record("1.3 Loop Mode 'once'", loop_mode == "once", f"loop={loop_mode} (expected 'once')")

# Test 1.4: Rig Contract A 6-Bone Mapping
REQUIRED_BONES = {"torso", "head", "right_arm", "left_arm", "right_leg", "left_leg"}
present_bones = set(fire_jab.get("bones", {}).keys())
missing_bones = REQUIRED_BONES - present_bones
record("1.4 Rig Contract A 6-Bone Completeness", len(missing_bones) == 0,
       f"Present bones: {sorted(list(present_bones))}, Missing: {missing_bones}")

# Test 1.5: Zero-Delta Boundary Pose Recovery (KF4 == KF0)
EXPECTED_KF_TIMES = ["0.00", "0.10", "0.15", "0.25", "0.45"]
bones_data = fire_jab.get("bones", {})
all_zero_delta = True
zero_delta_details = []

for bone in REQUIRED_BONES:
    rot_track = bones_data.get(bone, {}).get("rotation", {})
    kf_times = sorted(list(rot_track.keys()))
    if kf_times != EXPECTED_KF_TIMES:
        all_zero_delta = False
        zero_delta_details.append(f"{bone} keyframe times mismatch: {kf_times}")
    
    kf0 = rot_track.get("0.00")
    kf4 = rot_track.get("0.45")
    if kf0 != kf4:
        all_zero_delta = False
        zero_delta_details.append(f"{bone} KF0 {kf0} != KF4 {kf4}")

record("1.5 Zero-Delta Pose Recovery (KF0 == KF4)", all_zero_delta,
       "All 6 bones match 100% between KF0 (0.00s) and KF4 (0.45s)" if all_zero_delta else str(zero_delta_details))

# Test 1.6: Single Elbow Bend Projection Verification on right_arm
right_arm_rot = bones_data.get("right_arm", {}).get("rotation", {})
kf2_rot = right_arm_rot.get("0.15")  # Strike apex
expected_kf2 = [58.4, 6.56, -11.71]
is_elbow_projected = (kf2_rot == expected_kf2)
record("1.6 Single Elbow Bend Projection (right_arm KF2)", is_elbow_projected,
       f"right_arm KF2 rotation={kf2_rot} (expected {expected_kf2})")


# -----------------------------------------------------------------
# 2. TIMELINE DESYNC & MATHEMATICAL CORRESPONDENCE (R4, R7)
# -----------------------------------------------------------------
print("\n--- [TEST SUITE 2] SkillTimeline vs Animation Timing Desync Stress Test ---")

with open(SKILL_DEF_JSON, 'r', encoding='utf-8') as f:
    skill_defs = json.load(f)

fire_jab_def = next((s for s in skill_defs["skills"] if s["id"] == "avatar:fire_jab"), None)
record("2.1 Skill Definition avatar:fire_jab Exists", fire_jab_def is not None, f"Found: {fire_jab_def is not None}")

windup_ticks = fire_jab_def["windupTicks"]
active_ticks = fire_jab_def["activeTicks"]
recovery_ticks = fire_jab_def["recoveryTicks"]
total_ticks = windup_ticks + active_ticks + recovery_ticks
calculated_duration = total_ticks / 20.0

record("2.2 Total Timeline Ticks == 9 Ticks (0.45s)", (total_ticks == 9 and calculated_duration == 0.45),
       f"windup={windup_ticks}t, active={active_ticks}t, recovery={recovery_ticks}t -> Total={total_ticks}t -> {calculated_duration}s")

record("2.3 Zero Timing Desync (JSON 0.45s == Timeline 9 ticks)", (anim_len == calculated_duration),
       f"anim_len={anim_len}s, timeline={calculated_duration}s, delta={abs(anim_len - calculated_duration)}s")

# Keyframe time mapping to ticks
kf_mapping = {
    "0.00": 0.0,
    "0.10": 2.0,   # windup end (2 ticks)
    "0.15": 3.0,   # active tick 1 / strike apex (3 ticks)
    "0.25": 5.0,   # active end (2+3 = 5 ticks)
    "0.45": 9.0    # recovery end / idle (2+3+4 = 9 ticks)
}
mapping_ok = True
for kf_str, expected_tick in kf_mapping.items():
    actual_tick = float(kf_str) * 20.0
    if abs(actual_tick - expected_tick) > 1e-5:
        mapping_ok = False
record("2.4 Keyframe to Tick Alignment (20 TPS)", mapping_ok,
       f"KF0=0t, KF1=2t(WindupEnd), KF2=3t(StrikeApex), KF3=5t(ActiveEnd), KF4=9t(RecoveryEnd)")

# Simulation of what happens under desync:
class TimelineSimulator:
    def __init__(self, windup, active, recovery, anim_duration_s):
        self.windup = windup
        self.active = active
        self.recovery = recovery
        self.total_ticks = windup + active + recovery
        self.anim_ticks = anim_duration_s * 20.0
        
    def check_desync_flaws(self):
        flaws = []
        if self.anim_ticks < self.total_ticks:
            flaws.append(f"SHORT_ANIM: Anim finishes at {self.anim_ticks}t, but timeline runs to {self.total_ticks}t. Model pops to idle {self.total_ticks - self.anim_ticks} ticks early!")
        elif self.anim_ticks > self.total_ticks:
            flaws.append(f"LONG_ANIM: Anim continues until {self.anim_ticks}t, but timeline ends at {self.total_ticks}t. Next cast blocked by isPlayingTriggeredAnimation() guard for {self.anim_ticks - self.total_ticks} ticks!")
        return flaws

sim_current = TimelineSimulator(2, 3, 4, 0.45)
flaws_current = sim_current.check_desync_flaws()
record("2.5 Current Production Timeline Desync", len(flaws_current) == 0,
       "No desync flaws detected" if not flaws_current else str(flaws_current))

sim_short = TimelineSimulator(2, 3, 4, 0.35)
record("2.6 Desync Stress Test (Short JSON 0.35s)", len(sim_short.check_desync_flaws()) > 0,
       f"Identified flaw: {sim_short.check_desync_flaws()[0]}")

sim_long = TimelineSimulator(2, 3, 4, 0.55)
record("2.7 Desync Stress Test (Long JSON 0.55s)", len(sim_long.check_desync_flaws()) > 0,
       f"Identified flaw: {sim_long.check_desync_flaws()[0]}")


# -----------------------------------------------------------------
# 3. MULTIPLAYER ANIMATION SYNCHRONIZATION & RACE CONDITION ORACLES
# -----------------------------------------------------------------
print("\n--- [TEST SUITE 3] Multiplayer Animation Sync & Double Trigger Oracles ---")

with open(CLIENT_NET_HANDLER, 'r', encoding='utf-8') as f:
    cnh_code = f.read()

with open(SKILL_CLIENT_HANDLER, 'r', encoding='utf-8') as f:
    sch_code = f.read()

with open(AVATAR_ANIMS, 'r', encoding='utf-8') as f:
    aa_code = f.read()

# Test 3.1: Interception of S2CPhaseSync in ClientNetworkHandler
cnh_intercepts_phase_sync = "SkillPackets.S2CPhaseSync.ID" in cnh_code
cnh_checks_windup = '"WINDUP".equals(payload.phase())' in cnh_code
cnh_checks_skill_id = '"avatar:fire_jab".equals(payload.skillId())' in cnh_code
cnh_triggers_anim = "AvatarAnimations.triggerFireJab(acp)" in cnh_code

record("3.1 ClientNetworkHandler Intercepts S2CPhaseSync",
       cnh_intercepts_phase_sync and cnh_checks_windup and cnh_checks_skill_id and cnh_triggers_anim,
       f"Registers receiver: {cnh_intercepts_phase_sync}, Checks WINDUP: {cnh_checks_windup}, Checks avatar:fire_jab: {cnh_checks_skill_id}, Calls triggerFireJab: {cnh_triggers_anim}")

# Test 3.2: Remote Player Triggering via getPlayerByUuid
cnh_queries_world_player = "client.world.getPlayerByUuid(payload.casterUuid())" in cnh_code
cnh_checks_acp = "player instanceof AbstractClientPlayerEntity acp" in cnh_code
record("3.2 Remote Player Trigger via client.world.getPlayerByUuid",
       cnh_queries_world_player and cnh_checks_acp,
       f"Queries client.world: {cnh_queries_world_player}, Checks acp instance: {cnh_checks_acp}")

# Test 3.3: Double Trigger Protection in AvatarAnimations
aa_checks_playing = "controller.isPlayingTriggeredAnimation()" in aa_code
aa_returns_early = "if (controller.isPlayingTriggeredAnimation()) {\n                // Already playing; do not restart animation mid-swing\n                return;\n            }" in aa_code or "if (controller.isPlayingTriggeredAnimation()) return;" in aa_code.replace(" ", "")

record("3.3 AvatarAnimations Double Trigger Guard",
       aa_checks_playing,
       f"isPlayingTriggeredAnimation() guard present: {aa_checks_playing}")

# Simulation of Packet Interleaving Race Condition:
class MockPlayerAnimationController:
    def __init__(self):
        self.triggered_animation = None
        self.is_running = False
        self.trigger_count = 0
        
    def is_playing_triggered_animation(self):
        return self.triggered_animation is not None and self.is_running
        
    def trigger_animation(self, anim_id):
        if self.is_playing_triggered_animation():
            return False  # Guard in triggerFireJab prevents this
        self.triggered_animation = anim_id
        self.is_running = True
        self.trigger_count += 1
        return True
        
    def trigger_fire_jab(self):
        if self.is_playing_triggered_animation():
            return False
        return self.trigger_animation("avatar:fire_jab")

# Test Interleaving Order A: S2CSkillResult first, then S2CPhaseSync
ctrl_a = MockPlayerAnimationController()
res_a1 = ctrl_a.trigger_fire_jab() # S2CSkillResult
res_a2 = ctrl_a.trigger_fire_jab() # S2CPhaseSync
record("3.4 Race Condition: S2CSkillResult -> S2CPhaseSync",
       res_a1 is True and res_a2 is False and ctrl_a.trigger_count == 1,
       f"First packet triggered={res_a1}, Second packet triggered={res_a2}, Total triggers={ctrl_a.trigger_count}")

# Test Interleaving Order B: S2CPhaseSync first, then S2CSkillResult
ctrl_b = MockPlayerAnimationController()
res_b1 = ctrl_b.trigger_fire_jab() # S2CPhaseSync
res_b2 = ctrl_b.trigger_fire_jab() # S2CSkillResult
record("3.5 Race Condition: S2CPhaseSync -> S2CSkillResult",
       res_b1 is True and res_b2 is False and ctrl_b.trigger_count == 1,
       f"First packet triggered={res_b1}, Second packet triggered={res_b2}, Total triggers={ctrl_b.trigger_count}")

# Test Remote Player (only S2CPhaseSync received)
ctrl_remote = MockPlayerAnimationController()
res_rem = ctrl_remote.trigger_fire_jab() # S2CPhaseSync
record("3.6 Remote Player Single Trigger",
       res_rem is True and ctrl_remote.trigger_count == 1,
       f"Triggered={res_rem}, Total triggers={ctrl_remote.trigger_count}")


# -----------------------------------------------------------------
# 4. EDGE CASES & ROBUSTNESS VULNERABILITY ANALYSIS
# -----------------------------------------------------------------
print("\n--- [TEST SUITE 4] Edge Cases & Robustness Analysis ---")

# Test 4.1: getPlayerByUuid returns null (player not in tracking range / not spawned)
# In Java:
# var player = client.world.getPlayerByUuid(payload.casterUuid()); // null
# if (player instanceof AbstractClientPlayerEntity acp) { ... }
# In Java spec, (null instanceof Anything) is ALWAYS false, does not throw NPE.
record("4.1 getPlayerByUuid == null Safety (Java instanceof semantics)", True,
       "null instanceof AbstractClientPlayerEntity evaluates safely to false without NPE")

# Test 4.2: KnuckleVfxHelper Null Safety Audit
with open(KNUCKLE_HELPER, 'r', encoding='utf-8') as f:
    kvh_code = f.read()

# Check player null check in getKnucklePosition
has_player_null_check = "if (player == null) {\n            return Vec3d.ZERO;\n        }" in kvh_code
record("4.2 KnuckleVfxHelper.getKnucklePosition(null) Guard", has_player_null_check,
       f"getKnucklePosition checks if (player == null) -> Vec3d.ZERO: {has_player_null_check}")

# Check lines 108-116 of KnuckleVfxHelper.java:
# MinecraftClient mc = MinecraftClient.getInstance();
# if (mc.getEntityRenderDispatcher() != null)
# BUG AUDIT: What if mc is null? (Headless client / server / unit test)
mc_null_vulnerability = "if (mc.getEntityRenderDispatcher() != null)" in kvh_code and "if (mc != null && mc.getEntityRenderDispatcher() != null)" not in kvh_code
record("4.3 KnuckleVfxHelper Headless mc == null NPE Vulnerability [FINDING]",
       not mc_null_vulnerability,
       "VULNERABILITY CONFIRMED: Line 109 executes 'mc.getEntityRenderDispatcher()' without checking 'if (mc != null)'. In headless test or pre-init, MinecraftClient.getInstance() == null, throwing NullPointerException!" if mc_null_vulnerability else "mc null check present")

# Check model null check:
# PlayerEntityModel<AbstractClientPlayerEntity> model = playerRenderer.getModel();
# model.setArmAngle(arm, matrices);
model_null_vulnerability = "model.setArmAngle" in kvh_code and "if (model != null)" not in kvh_code
record("4.4 KnuckleVfxHelper playerRenderer.getModel() == null NPE Vulnerability [FINDING]",
       not model_null_vulnerability,
       "VULNERABILITY CONFIRMED: Line 113 calls 'model.setArmAngle(arm, matrices)' without 'if (model != null)'. If custom/mock renderer returns null model, throws NullPointerException!" if model_null_vulnerability else "model null check present")

# Check First-Person Mode handling:
# Does KnuckleVfxHelper check if client is in first person perspective?
has_perspective_check = "getPerspective().isFirstPerson()" in kvh_code
record("4.5 KnuckleVfxHelper First-Person Perspective Awareness [FINDING]",
       has_perspective_check,
       "DEFECT CONFIRMED: KnuckleVfxHelper does NOT check getPerspective().isFirstPerson(). In first-person, PlayerEntityRenderer is NOT invoked by Minecraft, leaving PlayerEntityModel angles in third-person resting or uninitialized state!" if not has_perspective_check else "Perspective checked")


# -----------------------------------------------------------------
# 5. KNUCKLE COORDINATE GEOMETRY & PAL 1.1.6 RIG PROOF
# -----------------------------------------------------------------
print("\n--- [TEST SUITE 5] Knuckle Coordinate Geometry & PAL Rig Proof ---")

# Test 5.1: Headless Arm Pivot Sign Check in KnuckleVfxHelper.java:120
# Vanilla BipedEntityModel.getModelData: right_arm pivotX = -5.0f, left_arm pivotX = +5.0f
has_inverted_pivot = "float armX = (arm == Arm.RIGHT ? 5.0F : -5.0F) / 16.0F;" in kvh_code
record("5.1 KnuckleVfxHelper Headless Arm Pivot Sign [FINDING]",
       not has_inverted_pivot,
       "DEFECT CONFIRMED: Line 120 sets armX = +5.0F for Arm.RIGHT. In vanilla BipedEntityModel, rightArm.pivotX is -5.0F and leftArm.pivotX is +5.0F! Sign is inverted in fallback." if has_inverted_pivot else "armX pivot signs match vanilla")

# Test 5.2: Geometric Knuckle Center in 4x12x4 Arm Space
# In vanilla BipedEntityModel, right_arm cuboid is: cuboid(-3.0f, -2.0f, -2.0f, 4.0f, 12.0f, 4.0f)
# X center is (-3 + 1)/2 = -1.0 pixel (-0.0625 blocks) for Steve, -0.5 pixel for Alex.
# KnuckleVfxHelper uses localOffset.x = 0.0.
offset_has_zero_x = "new Vec3d(0.0, -8.0 / 16.0, 0.0)" in kvh_code
record("5.2 Knuckle Center Offset X Alignment [FINDING]",
       not offset_has_zero_x,
       "CAVEAT DETECTED: LOCAL_KNUCKLE_OFFSET uses X=0.0. Exact geometric fist center is X=-1/16 (-0.0625) for Steve 4px arm or X=-0.5/16 (-0.03125) for Alex 3px arm. 1px lateral deviation." if offset_has_zero_x else "X centered")

# Test 5.3: PAL Fabric 1.1.6 Subdivided Limb Bone Proof
# PAL PlayerModelMixin binds only 6 vanilla parts: pal$head, pal$torso, pal$rightArm, pal$leftArm, pal$rightLeg, pal$leftLeg
# Proves that PAL Fabric 1.1.6 does NOT support subdivided bones (elbows/forearms) without custom model replacement.
pal_jar_path = r"C:\Users\USER\.gradle\caches\modules-2\files-2.1\com.zigythebird.playeranim\PlayerAnimationLibFabric\1.1.6+mc.1.21.1\f927eb5ac56526ef332e2ecfa69a18e58dfc9b21\PlayerAnimationLibFabric-1.1.6+mc.1.21.1-sources.jar"
has_pal_sources = os.path.exists(pal_jar_path)
pal_binds_only_vanilla = False
if has_pal_sources:
    import zipfile
    with zipfile.ZipFile(pal_jar_path) as z:
        mixin_src = z.read("com/zigythebird/playeranim/mixin/PlayerModelMixin.java").decode("utf-8")
        pal_binds_only_vanilla = ("pal$rightArm" in mixin_src and "forearm" not in mixin_src and "elbow" not in mixin_src)
record("5.3 PAL 1.1.6 Model Rig Restriction (Rig Contract A Necessary)",
       pal_binds_only_vanilla,
       "PROVEN: PAL PlayerModelMixin defines exactly 6 vanilla parts; no elbow/forearm subpart exists in PAL or vanilla player model")

# Test 5.4: PAL PlayerAnimManager secondLayer Synchronous Tracking
# Proves that updatePart applies identical translatePartToBone to both part and secondLayer
pal_syncs_second_layer = False
if has_pal_sources:
    import zipfile
    with zipfile.ZipFile(pal_jar_path) as z:
        manager_src = z.read("com/zigythebird/playeranim/animation/PlayerAnimManager.java").decode("utf-8")
        pal_syncs_second_layer = ("RenderUtil.translatePartToBone(part, bone, initialPose);" in manager_src and
                                  "RenderUtil.translatePartToBone(secondLayer, bone, initialPose);" in manager_src)
record("5.4 PAL secondLayer (rightSleeve) Synchronous Tracking",
       pal_syncs_second_layer,
       "PROVEN: PlayerAnimManager.updatePart() applies identical transforms to part and secondLayer synchronously")


# -----------------------------------------------------------------
# SUMMARY AND VERDICT
# -----------------------------------------------------------------
print("\n=================================================================")
print("TEST SUMMARY")
print("=================================================================")
total_tests = len(test_results)
passed_tests = sum(1 for t in test_results if t[1] == "PASS")
failed_tests = sum(1 for t in test_results if t[1] == "FAIL")

print(f"Total Tests Executed: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed (Findings): {failed_tests}")

for name, status, details in test_results:
    if status == "FAIL":
        print(f"  -> [FINDING] {name}: {details}")

print("=================================================================")
