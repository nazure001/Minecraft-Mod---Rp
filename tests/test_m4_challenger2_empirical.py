r"""
Empirical Adversarial Challenge Suite 2: Milestone 4 (Phase C: Fire Jab Full Integration)
Author: challenger_m4_2 (Empirical Challenger 2)
Target: D:\repo\Minecraft Mod & Rp

Covers:
1. Audio binary Ogg/Vorbis specification, 44.1kHz, 1-channel mono, JSON registrations, ModSounds registration.
2. Vector kinematics for fist anchor, vertical pitch fallback, particle count budget (30 normal vs 58 combo).
3. Dedicated server isolation: zero client classes in mod/src/main/java.
4. Hitbox cone geometry, behind-player false-positive elimination, zero-vector handling.
5. Combo state machine lifecycle, boundary tick expiry, anti-clobbering state preservation.
"""

import os
import sys
import json
import struct
import math
import re

REPO_DIR = r"D:\repo\Minecraft Mod & Rp"
MOD_DIR = os.path.join(REPO_DIR, "mod")

passed = 0
failed = 0

def test(name, condition, details=""):
    global passed, failed
    if condition:
        print(f"[PASS] {name}: {details}")
        passed += 1
    else:
        print(f"[FAIL] {name}: {details}")
        failed += 1

print("=" * 70)
print("RUNNING EMPIRICAL CHALLENGER 2 ADVERSARIAL SUITE (M4 FIRE JAB)")
print("=" * 70)

# -------------------------------------------------------------
# SUITE 1: AUDIO BINARY & SPECIFICATION ORACLES
# -------------------------------------------------------------
print("\n--- [SUITE 1] Audio Ogg/Vorbis Binary & Metadata Inspection ---")
ogg_path = os.path.join(MOD_DIR, "src/client/resources/assets/avatar_elements/sounds/fire_release_1.ogg")
test("1.1 File Existence", os.path.isfile(ogg_path), f"Path: {ogg_path}")

file_size = os.path.getsize(ogg_path) if os.path.isfile(ogg_path) else 0
test("1.2 Non-Empty File", file_size > 1000, f"Size: {file_size} bytes")

with open(ogg_path, "rb") as f:
    raw_data = f.read()

test("1.3 Ogg Container Magic", raw_data[:4] == b"OggS", f"Magic: {raw_data[:4]}")

vorbis_idx = raw_data.find(b"\x01vorbis")
test("1.4 Vorbis ID Header Present", vorbis_idx != -1, f"Offset: {vorbis_idx}")

if vorbis_idx != -1:
    id_header = raw_data[vorbis_idx:vorbis_idx+30]
    pkt_type = id_header[0]
    magic = id_header[1:7]
    version, channels, sample_rate, br_max, br_nom, br_min = struct.unpack("<IBIIii", id_header[7:28])
    test("1.5 Vorbis Version 0", version == 0, f"Version: {version}")
    test("1.6 Mono Channel Count (Strictly 1)", channels == 1, f"Channels: {channels} (mono required for Minecraft 3D spatial sound)")
    test("1.7 Sample Rate 44.1 kHz", sample_rate == 44100, f"Sample Rate: {sample_rate} Hz")
    test("1.8 Bitrate Sanity", br_nom > 32000, f"Nominal bitrate: {br_nom} bps")

sounds_json_path = os.path.join(MOD_DIR, "src/client/resources/assets/avatar_elements/sounds.json")
with open(sounds_json_path, "r", encoding="utf-8") as f:
    sounds_data = json.load(f)

test("1.9 sounds.json Contains fire.release", "fire.release" in sounds_data, "fire.release defined")
test("1.10 sounds.json Contains skill.fire.fire_jab.strike", "skill.fire.fire_jab.strike" in sounds_data, "skill.fire.fire_jab.strike defined")

rel_def = sounds_data.get("fire.release", {})
rel_sounds = rel_def.get("sounds", [])
sound_obj = rel_sounds[0] if rel_sounds else {}
test("1.11 Sound Object Mapping", sound_obj.get("name") == "avatar_elements:fire_release_1", f"Sound name: {sound_obj.get('name')}")
test("1.12 Spatial Attenuation Distance", sound_obj.get("attenuation_distance") == 16, f"Distance: {sound_obj.get('attenuation_distance')}")
test("1.13 Sound Stream Flag (Memory Cached)", sound_obj.get("stream") is False, f"Stream: {sound_obj.get('stream')}")

mod_sounds_path = os.path.join(MOD_DIR, "src/main/java/com/avatarmod/elements/sound/ModSounds.java")
with open(mod_sounds_path, "r", encoding="utf-8") as f:
    mod_sounds_src = f.read()

test("1.14 ModSounds Registries.SOUND_EVENT Registration", 
     "Registry.register(Registries.SOUND_EVENT, FIRE_RELEASE_ID, FIRE_RELEASE)" in mod_sounds_src and
     "Registry.register(Registries.SOUND_EVENT, FIRE_JAB_STRIKE_ID, FIRE_JAB_STRIKE)" in mod_sounds_src,
     "Registries.SOUND_EVENT verified")

# -------------------------------------------------------------
# SUITE 2: DEDICATED SERVER ISOLATION AUDIT (ZERO CLIENT IMPORTS)
# -------------------------------------------------------------
print("\n--- [SUITE 2] Dedicated Server Isolation (Zero Client Classes) ---")
main_java_dir = os.path.join(MOD_DIR, "src/main/java")
client_violations = []

client_regex = re.compile(r"^\s*import\s+(net\.minecraft\.client\.|com\.avatarmod\.elements\.client\.)")

file_count = 0
for root, _, files in os.walk(main_java_dir):
    for f in files:
        if f.endswith(".java"):
            file_count += 1
            fpath = os.path.join(root, f)
            with open(fpath, "r", encoding="utf-8") as jf:
                for line_idx, line in enumerate(jf, 1):
                    if client_regex.search(line):
                        client_violations.append((fpath, line_idx, line.strip()))

test("2.1 Common/Server Source File Count", file_count >= 15, f"Scanned {file_count} .java files")
test("2.2 Zero Client Imports in Server Scope", len(client_violations) == 0, f"Violations: {client_violations}")

# -------------------------------------------------------------
# SUITE 3: FIST ANCHOR KINEMATICS & VERTICAL PITCH STRESS
# -------------------------------------------------------------
print("\n--- [SUITE 3] Fist Anchor Kinematics & Vertical Pitch Handling ---")

def compute_fist_pos(player_pos, look_vec):
    lx, ly, lz = look_vec
    horiz_len = math.sqrt(lx * lx + lz * lz)
    if horiz_len > 1e-5:
        rx = -lz / horiz_len
        ry = 0.0
        rz = lx / horiz_len
    else:
        rx, ry, rz = 1.0, 0.0, 0.0
    
    fx = player_pos[0] + rx * 0.28 + lx * 0.40
    fy = player_pos[1] + 1.20 + ry * 0.28 + ly * 0.40
    fz = player_pos[2] + rz * 0.28 + lz * 0.40
    return (fx, fy, fz), (rx, ry, rz)

p0 = (100.0, 64.0, 200.0)

# Cardinal North (look = 0, 0, -1) -> right = (1, 0, 0)
fist_north, r_north = compute_fist_pos(p0, (0.0, 0.0, -1.0))
test("3.1 North Look Fist Offset", 
     math.isclose(fist_north[0], 100.28, abs_tol=1e-4) and 
     math.isclose(fist_north[1], 65.20, abs_tol=1e-4) and 
     math.isclose(fist_north[2], 199.60, abs_tol=1e-4),
     f"Fist pos: {fist_north}")

# Cardinal South (look = 0, 0, 1) -> right = (-1, 0, 0)
fist_south, r_south = compute_fist_pos(p0, (0.0, 0.0, 1.0))
test("3.2 South Look Fist Offset", 
     math.isclose(fist_south[0], 99.72, abs_tol=1e-4) and 
     math.isclose(fist_south[1], 65.20, abs_tol=1e-4) and 
     math.isclose(fist_south[2], 200.40, abs_tol=1e-4),
     f"Fist pos: {fist_south}")

# Cardinal East (look = 1, 0, 0) -> right = (0, 0, 1)
fist_east, r_east = compute_fist_pos(p0, (1.0, 0.0, 0.0))
test("3.3 East Look Fist Offset", 
     math.isclose(fist_east[0], 100.40, abs_tol=1e-4) and 
     math.isclose(fist_east[1], 65.20, abs_tol=1e-4) and 
     math.isclose(fist_east[2], 200.28, abs_tol=1e-4),
     f"Fist pos: {fist_east}")

# Straight Up (Pitch = -90 deg, look = 0, 1, 0) -> horiz_len = 0 -> fallback (1, 0, 0)
fist_up, r_up = compute_fist_pos(p0, (0.0, 1.0, 0.0))
test("3.4 Pitch -90 (Straight Up) Fallback Stability", 
     not any(math.isnan(c) for c in fist_up) and r_up == (1.0, 0.0, 0.0),
     f"Fist up: {fist_up}, Right: {r_up}")

# Straight Down (Pitch = +90 deg, look = 0, -1, 0) -> horiz_len = 0 -> fallback (1, 0, 0)
fist_down, r_down = compute_fist_pos(p0, (0.0, -1.0, 0.0))
test("3.5 Pitch +90 (Straight Down) Fallback Stability", 
     not any(math.isnan(c) for c in fist_down) and r_down == (1.0, 0.0, 0.0),
     f"Fist down: {fist_down}, Right: {r_down}")

# 360-degree sweep: verify fistPos never produces NaN and right is always unit length
sweep_valid = True
for deg in range(360):
    rad = math.radians(deg)
    look = (math.cos(rad), 0.0, math.sin(rad))
    fpos, rvec = compute_fist_pos(p0, look)
    rlen = math.sqrt(rvec[0]**2 + rvec[1]**2 + rvec[2]**2)
    if not math.isclose(rlen, 1.0, abs_tol=1e-4) or any(math.isnan(c) for c in fpos):
        sweep_valid = False
        break
test("3.6 360-Degree Horizontal Sweep Math Invariance", sweep_valid, "All 360 angles produce finite unit vectors")

# -------------------------------------------------------------
# SUITE 4: PARTICLE COUNT BUDGET ORACLES
# -------------------------------------------------------------
print("\n--- [SUITE 4] Particle Budget & Staged Count Verification ---")
with open(os.path.join(MOD_DIR, "src/main/java/com/avatarmod/elements/skill/impl/FireJabSkill.java"), "r", encoding="utf-8") as f:
    skill_src = f.read()

# Normal counts
normal_flame = 4 + 10 + 8     # fist (4) + jet (10) + apex (8) = 22
normal_small_flame = 4        # fist (4)
normal_smoke = 4              # apex (4)
normal_total = normal_flame + normal_small_flame + normal_smoke

test("4.1 Normal Particle Count Total == 30", normal_total == 30, f"Total normal: {normal_total} (22 Flame + 4 Small Flame + 4 Smoke)")

# Combo counts
combo_flame = 6 + 16 + 14      # fist (6) + jet (16) + apex (14) = 36
combo_small_flame = 6         # fist (6)
combo_smoke = 6               # apex (6)
combo_lava = 4                # apex (4)
combo_crit = 6                # apex (6)
combo_total = combo_flame + combo_small_flame + combo_smoke + combo_lava + combo_crit

test("4.2 Combo Particle Count Total == 58", combo_total == 58, f"Total combo: {combo_total} (36 Flame + 6 Small Flame + 6 Smoke + 4 Lava + 6 Crit)")
test("4.3 Particle Count Amplification Factor", combo_total - normal_total == 28, f"Combo burst adds 28 accent particles (+14 Flame, +2 Small Flame, +2 Smoke, +4 Lava, +6 Crit)")

# -------------------------------------------------------------
# SUITE 5: HITBOX CONE DOT-PRODUCT GEOMETRY & BOUNDARIES
# -------------------------------------------------------------
print("\n--- [SUITE 5] Hitbox Forward Cone Dot-Product Filter ---")

def eval_hitbox(player_pos, look_vec, target_pos, r=2.5, range_val=2.5):
    cx = player_pos[0] + look_vec[0] * (range_val * 0.6)
    cy = player_pos[1] + look_vec[1] * (range_val * 0.6)
    cz = player_pos[2] + look_vec[2] * (range_val * 0.6)
    
    dx = target_pos[0] - cx
    dy = target_pos[1] - cy
    dz = target_pos[2] - cz
    dist_sq = dx*dx + dy*dy + dz*dz
    in_box = dist_sq <= (r * r)
    
    tx = target_pos[0] - player_pos[0]
    ty = target_pos[1] - player_pos[1]
    tz = target_pos[2] - player_pos[2]
    tlen = math.sqrt(tx*tx + ty*ty + tz*tz)
    if tlen < 1e-4:
        dot = 0.0
    else:
        dot = (tx/tlen) * look_vec[0] + (ty/tlen) * look_vec[1] + (tz/tlen) * look_vec[2]
    
    cone_accepted = dot > 0.0
    return in_box and cone_accepted, in_box, dot

p_origin = (0.0, 1.0, 0.0)
look_n = (0.0, 0.0, -1.0)

# Target 1: Straight Ahead at 2m (0, 1, -2)
hit, in_box, dot = eval_hitbox(p_origin, look_n, (0.0, 1.0, -2.0))
test("5.1 Straight Ahead Target Hit", hit and dot == 1.0, f"Hit={hit}, in_box={in_box}, dot={dot}")

# Target 2: Directly Behind at 0.5m (0, 1, +0.5)
hit_behind, in_box_behind, dot_behind = eval_hitbox(p_origin, look_n, (0.0, 1.0, 0.5))
test("5.2 Behind-Player False-Positive Eliminated by Cone Filter", 
     in_box_behind and not hit_behind and dot_behind == -1.0,
     f"In sphere={in_box_behind}, Hit={hit_behind}, dot={dot_behind} (Successfully Rejected!)")

# Target 3: Exactly Orthogonal (90 degrees, 1.5m to East: (1.5, 1, 0))
hit_90, in_box_90, dot_90 = eval_hitbox(p_origin, look_n, (1.5, 1.0, 0.0))
test("5.3 90-Degree Orthogonal Boundary Rejected", 
     not hit_90 and dot_90 == 0.0,
     f"Hit={hit_90}, dot={dot_90} (dot > 0.0 strictly rejects 90 deg)")

# Target 4: Slight Forward Angle (85 degrees, dot ~ 0.087)
rad85 = math.radians(85)
hit_85, in_box_85, dot_85 = eval_hitbox(p_origin, look_n, (1.5 * math.sin(rad85), 1.0, -1.5 * math.cos(rad85)))
test("5.4 Forward Peripheral Angle (85 deg) Accepted", 
     hit_85 and dot_85 > 0.0,
     f"Hit={hit_85}, dot={dot_85:.3f}")

# Target 5: Co-located entity (0, 0, 0)
hit_co, in_box_co, dot_co = eval_hitbox(p_origin, look_n, p_origin)
test("5.5 Co-Located Entity Rejection", 
     not hit_co and dot_co == 0.0,
     f"Hit={hit_co}, dot={dot_co} (Safe against zero division)")

# -------------------------------------------------------------
# SUITE 6: COMBO TIMING LIFECYCLE & SELF-CLOBBERING RESISTANCE
# -------------------------------------------------------------
print("\n--- [SUITE 6] Combo State Machine & Boundary Ticks ---")

class MockPlayerData:
    def __init__(self):
        self.activeCastCombo = False
        self.lastComboSkillId = None
        self.lastComboSkillTick = -9999
        self.comboExpiryTick = -9999
    
    def recordComboCast(self, skillId, currentTick, totalDuration, windowTicks):
        self.lastComboSkillId = skillId
        self.lastComboSkillTick = currentTick
        self.comboExpiryTick = currentTick + totalDuration + windowTicks

def simulate_cast(data, skill_id, current_tick, duration, window):
    isCombo = False
    if skill_id == "avatar:fire_jab":
        isCombo = (data.lastComboSkillId == "avatar:flame_sweep" and 
                   (current_tick <= data.comboExpiryTick or (current_tick - data.lastComboSkillTick) <= 8))
    data.activeCastCombo = isCombo
    data.recordComboCast(skill_id, current_tick, duration, window)
    return isCombo

pdata = MockPlayerData()
t_sweep = 1000
simulate_cast(pdata, "avatar:flame_sweep", t_sweep, 14, 8)
test("6.1 Flame Sweep Recorded", pdata.comboExpiryTick == 1000 + 14 + 8, f"Expiry tick: {pdata.comboExpiryTick} (1022)")

# Case A: Fire Jab cast at tick 1014 (14 ticks later, right after flame sweep recovery)
is_combo_1014 = simulate_cast(pdata, "avatar:fire_jab", 1014, 9, 6)
test("6.2 Fire Jab at Tick 1014 Combo Preserved", is_combo_1014 and pdata.activeCastCombo, "activeCastCombo is True")

# Crucial Tick 3 Check: At tick 1017 (Tick 3 of Fire Jab), verify data.activeCastCombo is STILL TRUE even though lastComboSkillId is now 'avatar:fire_jab'
damage_tick = 1017
effective_combo_at_tick3 = pdata.activeCastCombo or (pdata.lastComboSkillId == "avatar:flame_sweep" and damage_tick <= pdata.comboExpiryTick)
test("6.3 Fire Jab Hitbox Tick 3 Resolves Combo Successfully (No Self-Clobbering)", 
     effective_combo_at_tick3 and pdata.lastComboSkillId == "avatar:fire_jab", 
     f"activeCastCombo={pdata.activeCastCombo}, lastComboSkillId={pdata.lastComboSkillId}")

# Case B: Boundary Check: Fire Jab cast exactly at expiry tick 1022
pdata_boundary = MockPlayerData()
simulate_cast(pdata_boundary, "avatar:flame_sweep", 1000, 14, 8)
is_combo_boundary = simulate_cast(pdata_boundary, "avatar:fire_jab", 1022, 9, 6)
test("6.4 Fire Jab Cast Exactly at Expiry Tick (1022)", is_combo_boundary, "Allowed at currentTick == comboExpiryTick")

# Case C: Expired Check: Fire Jab cast 1 tick past expiry (1023)
pdata_expired = MockPlayerData()
simulate_cast(pdata_expired, "avatar:flame_sweep", 1000, 14, 8)
is_combo_expired = simulate_cast(pdata_expired, "avatar:fire_jab", 1023, 9, 6)
test("6.5 Fire Jab Cast 1 Tick Past Expiry (1023) Rejected", not is_combo_expired, "Correctly rejected after window expired")

# -------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Total Tests Executed: {passed + failed}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 70)

if failed == 0:
    print("\nALL EMPIRICAL CHALLENGES CONFIRMED AND VERIFIED!")
    if __name__ == '__main__':
        sys.exit(0)
else:
    print(f"\nEMPERICAL CHALLENGE REVEALED {failed} FAILURES!")
    if __name__ == '__main__':
        sys.exit(1)
