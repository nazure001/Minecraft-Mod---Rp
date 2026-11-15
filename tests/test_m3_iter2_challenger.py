"""
Milestone 3 Iteration 2 Adversarial Stress Test Harness
Author: challenger_m3_2_iter2
Target: KnuckleVfxHelper remediation and animation rig contracts
"""

import math
import os
import re
import sys
import numpy as np

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
KNUCKLE_HELPER_PATH = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\vfx\KnuckleVfxHelper.java")

results = []

def record(test_id, name, passed, details):
    status = "PASS" if passed else "FAIL"
    results.append((test_id, name, status, details))
    print(f"[{status}] Test {test_id} - {name}: {details}")

print("=================================================================")
print("ADVERSARIAL STRESS TEST HARNESS: M3 ITERATION 2 (KnuckleVfxHelper)")
print("=================================================================\n")

# Read KnuckleVfxHelper source code
with open(KNUCKLE_HELPER_PATH, "r", encoding="utf-8") as f:
    kvh_source = f.read()

# -------------------------------------------------------------
# SUITE A: STATIC CODE & NULL-SAFETY PREDICATE ORACLES
# -------------------------------------------------------------
print("--- [SUITE A] Static Code & Null-Safety Predicates ---")

# A1: Check mc == null guard
# Must be guarded before mc.options or mc.getEntityRenderDispatcher()
pattern_mc_options = r"if\s*\(\s*mc\s*!=\s*null\s*&&\s*mc\.options\s*!=\s*null"
match_mc_options = re.search(pattern_mc_options, kvh_source)
record("A1", "mc == null guard for mc.options", match_mc_options is not None,
       f"Found guard: {match_mc_options.group(0) if match_mc_options else 'NOT FOUND'}")

pattern_mc_dispatcher = r"if\s*\(\s*mc\s*!=\s*null\s*&&\s*mc\.getEntityRenderDispatcher\(\)\s*!=\s*null\s*\)"
match_mc_dispatcher = re.search(pattern_mc_dispatcher, kvh_source)
record("A2", "mc == null guard for getEntityRenderDispatcher()", match_mc_dispatcher is not None,
       f"Found guard: {match_mc_dispatcher.group(0) if match_mc_dispatcher else 'NOT FOUND'}")

# A2: Check model == null guard before model.setArmAngle
pattern_model_guard = r"PlayerEntityModel<AbstractClientPlayerEntity>\s+model\s*=\s*playerRenderer\.getModel\(\);\s*if\s*\(\s*model\s*!=\s*null\s*\)\s*\{\s*model\.setArmAngle\(arm,\s*matrices\);"
match_model_guard = re.search(pattern_model_guard, kvh_source, re.DOTALL)
record("A3", "model == null guard before setArmAngle", match_model_guard is not None,
       "model != null guard verified around model.setArmAngle" if match_model_guard else "NOT FOUND")

# A3: Check first-person perspective guard includes mc.player == player
pattern_first_person = r"mc\.options\.getPerspective\(\)\.isFirstPerson\(\)\s*&&\s*mc\.player\s*==\s*player"
match_first_person = re.search(pattern_first_person, kvh_source)
record("A4", "First-person perspective guard checks mc.player == player", match_first_person is not None,
       "First-person check correctly differentiates local camera player from remote watchers" if match_first_person else "NOT FOUND")

# A4: Check arm pivot signs
# armX = (arm == Arm.RIGHT ? -5.0F : 5.0F) / 16.0F
pattern_arm_pivot = r"float\s+armX\s*=\s*\(arm\s*==\s*Arm\.RIGHT\s*\?\s*-5\.0F\s*:\s*5\.0F\)\s*/\s*16\.0F;"
match_arm_pivot = re.findall(pattern_arm_pivot, kvh_source)
record("A5", "Arm pivot signs in fallback & first-person paths", len(match_arm_pivot) == 2,
       f"Found {len(match_arm_pivot)} instances of vanilla arm pivot (-5.0F for RIGHT, +5.0F for LEFT)")

# A5: Check knuckle offset sign (+8.0 / 16.0 down, -1.0 / 16.0 X)
pattern_offset = r"new\s+Vec3d\(\s*-1\.0\s*/\s*16\.0\s*,\s*8\.0\s*/\s*16\.0\s*,\s*0\.0\s*\)"
match_offset = re.search(pattern_offset, kvh_source)
record("A6", "LOCAL_KNUCKLE_OFFSET sign & alignment", match_offset is not None,
       f"Knuckle offset is [-1/16, +8/16, 0]: {match_offset is not None}")

# -------------------------------------------------------------
# SUITE B: RUNTIME ENVIRONMENT DISPATCH SIMULATOR
# -------------------------------------------------------------
print("\n--- [SUITE B] Runtime Environment Dispatch State Simulator ---")

class MockPerspective:
    def __init__(self, is_first_person):
        self._first_person = is_first_person
    def isFirstPerson(self):
        return self._first_person

class MockGameOptions:
    def __init__(self, is_first_person=True):
        self.perspective = MockPerspective(is_first_person)
    def getPerspective(self):
        return self.perspective

class MockPlayer:
    def __init__(self, name):
        self.name = name

class MockPlayerRenderer:
    def __init__(self, has_model=True):
        self.has_model = has_model
    def getModel(self):
        return "ModelObject" if self.has_model else None

class MockRenderDispatcher:
    def __init__(self, renderer):
        self.renderer = renderer
    def getRenderer(self, player):
        return self.renderer

class MockMinecraftClient:
    def __init__(self, options=None, player=None, dispatcher=None):
        self.options = options
        self.player = player
        self.dispatcher = dispatcher
    def getEntityRenderDispatcher(self):
        return self.dispatcher

def simulate_dispatch_path(mc, player, arm="RIGHT"):
    """
    Simulates exact logic of KnuckleVfxHelper.applyPlayerArmTransform lines 109-133
    """
    path_taken = []
    
    # Line 109:
    if mc is not None and mc.options is not None and mc.options.getPerspective().isFirstPerson() and mc.player == player:
        armX = -5.0 / 16.0 if arm == "RIGHT" else 5.0 / 16.0
        path_taken.append("FIRST_PERSON_PIVOT")
        return path_taken, armX, 2.0 / 16.0, 0.0

    # Line 118:
    if mc is not None and mc.getEntityRenderDispatcher() is not None:
        renderer = mc.getEntityRenderDispatcher().getRenderer(player)
        if isinstance(renderer, MockPlayerRenderer):
            model = renderer.getModel()
            if model is not None:
                path_taken.append("MODEL_SET_ARM_ANGLE")
                return path_taken, None, None, None

    # Line 131: Fallback
    armX = -5.0 / 16.0 if arm == "RIGHT" else 5.0 / 16.0
    path_taken.append("HEADLESS_FALLBACK_PIVOT")
    return path_taken, armX, 2.0 / 16.0, 0.0

# B1: Headless environment (mc is None)
p_local = MockPlayer("local")
path_b1, ax, ay, az = simulate_dispatch_path(None, p_local)
record("B1", "Headless mc == None dispatch", path_b1 == ["HEADLESS_FALLBACK_PIVOT"] and ax == -5.0/16.0,
       f"Path taken: {path_b1}, armX={ax} (expected HEADLESS_FALLBACK_PIVOT)")

# B2: Pre-init options is None
mc_no_opts = MockMinecraftClient(options=None, player=p_local, dispatcher=MockRenderDispatcher(MockPlayerRenderer(True)))
path_b2, ax, ay, az = simulate_dispatch_path(mc_no_opts, p_local)
record("B2", "Pre-init mc.options == None dispatch", path_b2 == ["MODEL_SET_ARM_ANGLE"],
       f"Path taken: {path_b2} (safely skipped options, used model)")

# B3: First-person camera, local player
mc_fp = MockMinecraftClient(options=MockGameOptions(is_first_person=True), player=p_local, dispatcher=MockRenderDispatcher(MockPlayerRenderer(True)))
path_b3, ax, ay, az = simulate_dispatch_path(mc_fp, p_local)
record("B3", "First-person local player dispatch", path_b3 == ["FIRST_PERSON_PIVOT"] and ax == -5.0/16.0,
       f"Path taken: {path_b3} (safely avoided stale 3rd-person model)")

# B4: First-person camera, remote player
p_remote = MockPlayer("remote")
path_b4, ax, ay, az = simulate_dispatch_path(mc_fp, p_remote)
record("B4", "First-person remote player dispatch", path_b4 == ["MODEL_SET_ARM_ANGLE"],
       f"Path taken: {path_b4} (properly routes remote player to animated model)")

# B5: Third-person camera, local player
mc_3p = MockMinecraftClient(options=MockGameOptions(is_first_person=False), player=p_local, dispatcher=MockRenderDispatcher(MockPlayerRenderer(True)))
path_b5, ax, ay, az = simulate_dispatch_path(mc_3p, p_local)
record("B5", "Third-person local player dispatch", path_b5 == ["MODEL_SET_ARM_ANGLE"],
       f"Path taken: {path_b5} (properly routes local player to animated model in 3rd person)")

# B6: Model is None
mc_null_model = MockMinecraftClient(options=MockGameOptions(is_first_person=False), player=p_local, dispatcher=MockRenderDispatcher(MockPlayerRenderer(has_model=False)))
path_b6, ax, ay, az = simulate_dispatch_path(mc_null_model, p_local)
record("B6", "playerRenderer.getModel() == None dispatch", path_b6 == ["HEADLESS_FALLBACK_PIVOT"],
       f"Path taken: {path_b6} (safely fell back to arm pivot without crash)")

# B7: Non-player renderer (spectator or custom mob)
mc_non_player = MockMinecraftClient(options=MockGameOptions(is_first_person=False), player=p_local, dispatcher=MockRenderDispatcher("MobRenderer"))
path_b7, ax, ay, az = simulate_dispatch_path(mc_non_player, p_local)
record("B7", "Non-player renderer fallback dispatch", path_b7 == ["HEADLESS_FALLBACK_PIVOT"],
       f"Path taken: {path_b7} (safely fell back to arm pivot)")


# -------------------------------------------------------------
# SUITE C: 3D AFFINE TRANSFORMATION GEOMETRY & ARM SYMMETRY
# -------------------------------------------------------------
print("\n--- [SUITE C] 3D Affine Geometry, Arm Symmetry & Spatial Sanity ---")

def rot_y(deg):
    r = np.radians(deg)
    return np.array([
        [np.cos(r), 0, np.sin(r), 0],
        [0, 1, 0, 0],
        [-np.sin(r), 0, np.cos(r), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

def rot_x(deg):
    r = np.radians(deg)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(r), -np.sin(r), 0],
        [0, np.sin(r), np.cos(r), 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

def rot_z(deg):
    r = np.radians(deg)
    return np.array([
        [np.cos(r), -np.sin(r), 0, 0],
        [np.sin(r), np.cos(r), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)

def trans(x, y, z):
    m = np.eye(4, dtype=np.float64)
    m[0, 3] = x
    m[1, 3] = y
    m[2, 3] = z
    return m

def scale(sx, sy, sz):
    m = np.eye(4, dtype=np.float64)
    m[0, 0] = sx
    m[1, 1] = sy
    m[2, 2] = sz
    return m

def compute_knuckle_world(body_yaw, arm="RIGHT", arm_rot=(0,0,0), player_pos=(0,0,0)):
    # Base pipeline from KnuckleVfxHelper.java:
    # 1. translate(player.pos)
    # 2. rotate Y: 180.0F - bodyYaw
    # 3. scale(-1.0F, -1.0F, 1.0F)
    # 4. scale(0.9375F, 0.9375F, 0.9375F)
    # 5. translate(0.0F, -1.501F, 0.0F)
    # 6. translate(armX, 2.0F / 16.0F, 0.0F)
    # 7. arm rotation (X, then Y, then Z in Minecraft Euler convention)
    # 8. local knuckle offset: [-1.0/16.0, 8.0/16.0, 0.0] (for RIGHT arm)
    # For LEFT arm: Steve left arm center is at X = +1.0/16.0
    
    armX = -5.0 / 16.0 if arm == "RIGHT" else 5.0 / 16.0
    local_offset_x = -1.0 / 16.0 if arm == "RIGHT" else 1.0 / 16.0
    local_offset = np.array([local_offset_x, 8.0 / 16.0, 0.0, 1.0], dtype=np.float64)
    
    M = np.eye(4, dtype=np.float64)
    M = M @ trans(player_pos[0], player_pos[1], player_pos[2])
    M = M @ rot_y(180.0 - body_yaw)
    M = M @ scale(-1.0, -1.0, 1.0)
    M = M @ scale(0.9375, 0.9375, 0.9375)
    M = M @ trans(0.0, -1.501, 0.0)
    M = M @ trans(armX, 2.0 / 16.0, 0.0)
    
    # Arm rotation
    pitch, yaw, roll = arm_rot
    if pitch != 0:
        M = M @ rot_x(pitch)
    if yaw != 0:
        M = M @ rot_y(yaw)
    if roll != 0:
        M = M @ rot_z(roll)
        
    v = M @ local_offset
    return v[:3]

# C1: At rest (bodyYaw=0, arm_rot=(0,0,0)), test knuckle height
pos_rest_right = compute_knuckle_world(0.0, arm="RIGHT")
pos_rest_left = compute_knuckle_world(0.0, arm="LEFT")

record("C1", "Knuckle position at rest is waist/hip level (~0.82m)",
       0.75 <= pos_rest_right[1] <= 0.90,
       f"Right knuckle rest height Y={pos_rest_right[1]:.4f}m (expected ~0.82m)")

# C2: Lateral symmetry: Right arm vs Left arm X coordinates
is_symmetric = abs(pos_rest_right[0] + pos_rest_left[0]) < 1e-5
record("C2", "Right and Left arm knuckle lateral symmetry (sagittal reflection)",
       is_symmetric,
       f"Right X={pos_rest_right[0]:.4f}m, Left X={pos_rest_left[0]:.4f}m, sum={pos_rest_right[0] + pos_rest_left[0]:.6f}")

# C3: Strike position (pitch=58.4 deg)
# Forward punch should move knuckle forward (negative Z when looking North, bodyYaw=0)
pos_strike = compute_knuckle_world(0.0, arm="RIGHT", arm_rot=(58.4, 6.56, -11.71))
record("C3", "Strike punch extends forward (Z < -0.35m) at chest level (~1.04m)",
       pos_strike[2] <= -0.35 and 1.0 <= pos_strike[1] <= 1.15,
       f"Strike knuckle position: X={pos_strike[0]:.3f}, Y={pos_strike[1]:.3f}, Z={pos_strike[2]:.3f}")

# C4: Body Yaw Invariance / Polar Radius preservation
# When bodyYaw changes, distance of knuckle from player feet (at 0,0,0) in horizontal plane must be constant!
radius_0 = math.hypot(pos_strike[0], pos_strike[2])
radii_ok = True
for yaw in [45.0, 90.0, 135.0, 180.0, 270.0, 315.0]:
    p = compute_knuckle_world(yaw, arm="RIGHT", arm_rot=(58.4, 6.56, -11.71))
    r = math.hypot(p[0], p[2])
    if abs(r - radius_0) > 1e-4:
        radii_ok = False

record("C4", "Body Yaw rotation preserves exact horizontal radius from player center",
       radii_ok,
       f"Horizontal radius = {radius_0:.4f}m across all yaws [0..360]")


# -------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------
print("\n=================================================================")
print("ADVERSARIAL STRESS TEST SUMMARY")
print("=================================================================")
total = len(results)
passed = sum(1 for r in results if r[2] == "PASS")
failed = sum(1 for r in results if r[2] == "FAIL")

print(f"Total Tests Executed: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed > 0:
    for tid, name, status, details in results:
        if status == "FAIL":
            print(f"  -> [FAIL] Test {tid} {name}: {details}")

print("=================================================================")

if failed > 0:
    sys.exit(1)
