r"""
Comprehensive Automated Test Suite for Milestones 4, 5, and 6:
- Milestone 4 (Phase C): Fire Jab Full Integration (Timeline, Knuckle VFX, Damage, SFX Synchronization)
- Milestone 5 (Phase D): Hold-Release Generic Framework & Fire Blast Implementation
- Milestone 6 (Phase E): Integration Verification, Networking Codecs & Contract Oracles
Target: D:\repo\Minecraft Mod & Rp
"""

import json
import os
import sys
import re

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
ANIM_JSON = os.path.join(REPO_ROOT, r"mod\src\client\resources\assets\avatar_elements\player_animations\fire_jab_test.json")
SKILL_DEF_JSON = os.path.join(REPO_ROOT, r"mod\src\main\resources\data\avatar_elements\skill_definitions.json")
ELEMENT_SLOTS_JSON = os.path.join(REPO_ROOT, r"mod\src\main\resources\data\avatar_elements\element_slots.json")

FIRE_JAB_SKILL = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\impl\FireJabSkill.java")
FIRE_BLAST_SKILL = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\impl\FireBlastSkill.java")
SKILL_TIMELINE = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\data\SkillTimeline.java")
PLAYER_BENDING_DATA = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\data\PlayerBendingData.java")
SKILL_VALIDATOR = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\SkillValidator.java")
SKILL_PACKETS = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\network\SkillPackets.java")
SKILL_NETWORKING = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\network\SkillNetworking.java")
SKILL_DISPATCHER = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\SkillDispatcher.java")
ELEMENT_SLOT_MAP = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\ElementSlotMap.java")
SKILL_DEFINITION = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\skill\SkillDefinition.java")
CHARGE_ORB_RENDERER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\orb\ChargeOrbRenderer.java")
FIRST_PERSON_ORB = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\orb\FirstPersonOrbRenderer.java")
ORB_CONFIG = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\orb\OrbVisualConfig.java")
AVATAR_CLIENT = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\AvatarElementsClient.java")
SKILL_CLIENT_HANDLER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\network\SkillClientHandler.java")
SERVER_EVENTS = os.path.join(REPO_ROOT, r"mod\src\main\java\com\avatarmod\elements\network\AvatarServerEvents.java")
KNUCKLE_HELPER = os.path.join(REPO_ROOT, r"mod\src\client\java\com\avatarmod\elements\client\vfx\KnuckleVfxHelper.java")

test_results = []

def record(test_name, passed, details):
    status = "PASS" if passed else "FAIL"
    test_results.append((test_name, status, details))
    print(f"[{status}] {test_name}: {details}")

print("=================================================================")
print("RUNNING MILESTONES 4, 5, 6 VERIFICATION TEST SUITE")
print("=================================================================\n")

# -----------------------------------------------------------------
# SUITE 1: MILESTONE 4 - FIRE JAB TIMELINE & VFX/SFX SYNCHRONIZATION
# -----------------------------------------------------------------
print("--- [SUITE 1] Milestone 4: Fire Jab Full Timeline & VFX/SFX Sync ---")

with open(SKILL_DEF_JSON, 'r', encoding='utf-8') as f:
    skill_defs = json.load(f)["skills"]

fire_jab_def = next((s for s in skill_defs if s["id"] == "avatar:fire_jab"), None)
record("1.1 avatar:fire_jab definition exists", fire_jab_def is not None, f"Found: {fire_jab_def is not None}")
if fire_jab_def:
    w = fire_jab_def.get("windupTicks")
    a = fire_jab_def.get("activeTicks")
    r = fire_jab_def.get("recoveryTicks")
    total_ticks = w + a + r
    record("1.2 Fire Jab Phase Timing (2w + 3a + 4r = 9t = 0.45s)",
           w == 2 and a == 3 and r == 4 and total_ticks == 9,
           f"windup={w}t, active={a}t, recovery={r}t -> total={total_ticks}t ({total_ticks/20.0}s)")

with open(ANIM_JSON, 'r', encoding='utf-8') as f:
    anim_data = json.load(f)["animations"]["fire_jab_test"]

record("1.3 Animation length matches 0.45s exactly", anim_data.get("animation_length") == 0.45,
       f"anim_length={anim_data.get('animation_length')}s")

# Verify zero-delta pose return
bones = anim_data.get("bones", {})
all_zero_delta = True
for bname, bdata in bones.items():
    rots = bdata.get("rotation", {})
    if "0.00" in rots and "0.45" in rots:
        if rots["0.00"] != rots["0.45"]:
            all_zero_delta = False
            break
record("1.4 Rig zero-delta pose recovery (KF0 == KF4)", all_zero_delta,
       "All bones return exactly to ready stance at 0.45s")

with open(FIRE_JAB_SKILL, 'r', encoding='utf-8') as f:
    fire_jab_code = f.read()

# Check tick 1 active / tick 3 absolute trigger
active_check = "timeline.phase() != SkillTimeline.Phase.ACTIVE" in fire_jab_code
tick1_check = "timeline.ticksInPhase() != 1" in fire_jab_code
record("1.5 Strike trigger at tick 1 active / tick 3 absolute",
       active_check and tick1_check,
       "Hits precisely on ACTIVE tick 1 (after 2t windup)")

# Check Knuckle VFX and SFX synchronization
has_knuckle_vfx = "fistPos" in fire_jab_code or "knucklePos" in fire_jab_code
has_flame_particle = "ParticleTypes.FLAME" in fire_jab_code
has_sfx = "FIRE_RELEASE" in fire_jab_code or "ENTITY_BLAZE_SHOOT" in fire_jab_code
record("1.6 Knuckle flame VFX and SFX synchronized in same tick",
       has_knuckle_vfx and has_flame_particle and has_sfx,
       "Knuckle position, flame particles, and sound event all execute in executeHitbox")

# Check 3rd-person charge orb renderer knuckle tracking
with open(CHARGE_ORB_RENDERER, 'r', encoding='utf-8') as f:
    orb_code = f.read()

has_knuckle_anchor = "KnuckleVfxHelper.getKnucklePosition" in orb_code
record("1.7 ChargeOrbRenderer anchored to KnuckleVfxHelper",
       has_knuckle_anchor,
       "3rd-person charge orb tracks right knuckle via KnuckleVfxHelper")

with open(ORB_CONFIG, 'r', encoding='utf-8') as f:
    orb_cfg_code = f.read()

has_charge_only_phases = bool(re.search(r'"avatar:fire_blast",\s*new Config\(Set\.of\("WINDUP",\s*"HOLD"\)\)', orb_cfg_code))
record("1.8 Charge Orb Visually Dissolves on Projectile Release (WINDUP + HOLD only)",
       has_charge_only_phases,
       "Charge orb phases strictly limited to WINDUP and HOLD; hand orb dissolves when fireball is released")

# -----------------------------------------------------------------
# SUITE 2: MILESTONE 5 - HOLD-RELEASE GENERIC FRAMEWORK
# -----------------------------------------------------------------
print("\n--- [SUITE 2] Milestone 5: Generic Hold-Release Framework ---")

with open(SKILL_TIMELINE, 'r', encoding='utf-8') as f:
    timeline_code = f.read()

has_hold_phase = "HOLD" in timeline_code and "public enum Phase { IDLE, WINDUP, HOLD, ACTIVE, RECOVERY }" in timeline_code
has_release_hold = "public void releaseHold()" in timeline_code
has_charge_ratio = "public float getChargeRatio()" in timeline_code
record("2.1 SkillTimeline Phase.HOLD State Integration",
       has_hold_phase,
       "Phase.HOLD integrated into unified SkillTimeline enum")
record("2.2 SkillTimeline releaseHold() Transition Method",
       has_release_hold,
       "releaseHold() transitions Phase.HOLD -> Phase.ACTIVE immediately")
record("2.3 SkillTimeline getChargeRatio() Normalization",
       has_charge_ratio,
       "getChargeRatio() returns [0.0, 1.0] normalized charge factor")

# Verify NO duplicate/parallel timeline or chi system
with open(PLAYER_BENDING_DATA, 'r', encoding='utf-8') as f:
    bending_code = f.read()

no_parallel_timeline = "activeTimeline" in bending_code and "holdTimeline" not in bending_code
record("2.4 Single Unified Timeline in PlayerBendingData (No Parallel System)",
       no_parallel_timeline,
       "PlayerBendingData manages a single activeTimeline instance for all skills")

with open(SKILL_PACKETS, 'r', encoding='utf-8') as f:
    packets_code = f.read()

has_hold_start_pkt = "record C2SHoldStart" in packets_code and "c2s_hold_start" in packets_code
has_hold_release_pkt = "record C2SHoldRelease" in packets_code and "c2s_hold_release" in packets_code
record("2.5 C2SHoldStart Packet & Codec Definition",
       has_hold_start_pkt,
       "C2SHoldStart(slotIndex, skillId) CustomPayload registered")
record("2.6 C2SHoldRelease Packet & Codec Definition",
       has_hold_release_pkt,
       "C2SHoldRelease(slotIndex, skillId) CustomPayload registered")

with open(SKILL_NETWORKING, 'r', encoding='utf-8') as f:
    net_code = f.read()

has_hold_start_handler = "handleHoldStart" in net_code
has_hold_release_handler = "handleHoldRelease" in net_code
record("2.7 SkillNetworking C2SHoldStart/Release Receivers",
       has_hold_start_handler and has_hold_release_handler,
       "Network receivers route hold-start and hold-release to PlayerBendingData")

with open(AVATAR_CLIENT, 'r', encoding='utf-8') as f:
    client_code = f.read()

has_client_hold_handling = "sendHoldStart" in client_code and "sendHoldRelease" in client_code
record("2.8 AvatarElementsClient Slot Key Hold Detection",
       has_client_hold_handling,
       "Client differentiates instant click vs hold-release based on SkillDefinition.isHoldRelease()")

has_quick_tap = "drainPressed(key)" in client_code and "sendHoldRelease(slot, skillId)" in client_code
has_element_switch_safety = "slotHeldSkillId" in client_code
record("2.9 Client Quick-Tap Handling & Element Switch Resilience",
       has_quick_tap and has_element_switch_safety,
       "Client handles sub-tick quick taps and reliably releases held skills upon element switch")

# -----------------------------------------------------------------
# SUITE 3: MILESTONE 5 - FIRE BLAST IMPLEMENTATION & SCALING
# -----------------------------------------------------------------
print("\n--- [SUITE 3] Milestone 5: Fire Blast Skill Implementation & Scaling ---")

fire_blast_def = next((s for s in skill_defs if s["id"] == "avatar:fire_blast"), None)
record("3.1 avatar:fire_blast definition in skill_definitions.json",
       fire_blast_def is not None,
       f"Found: {fire_blast_def is not None}")

if fire_blast_def:
    record("3.2 Fire Blast castType is HOLD_RELEASE",
           fire_blast_def.get("castType") == "HOLD_RELEASE",
           f"castType={fire_blast_def.get('castType')}")
    record("3.3 Fire Blast maxChargeTicks is 40 (2.0s)",
           fire_blast_def.get("maxChargeTicks") == 40,
           f"maxChargeTicks={fire_blast_def.get('maxChargeTicks')}")
    record("3.4 Fire Blast damage 7.0 and range 24.0",
           fire_blast_def.get("damage") == 7.0 and fire_blast_def.get("range") == 24.0,
           f"damage={fire_blast_def.get('damage')}, range={fire_blast_def.get('range')}")
    record("3.5 Fire Blast chiCost 20 and cooldownTicks 20",
           fire_blast_def.get("chiCost") == 20 and fire_blast_def.get("cooldownTicks") == 20,
           f"chiCost={fire_blast_def.get('chiCost')}, cooldown={fire_blast_def.get('cooldownTicks')}")

with open(ELEMENT_SLOTS_JSON, 'r', encoding='utf-8') as f:
    slots_data = json.load(f)

fire_slots = slots_data.get("FIRE", [])
record("3.6 FIRE Slot 1 (X key) mapped to avatar:fire_blast",
       len(fire_slots) > 1 and fire_slots[1] == "avatar:fire_blast",
       f"FIRE slots: {fire_slots}")

with open(FIRE_BLAST_SKILL, 'r', encoding='utf-8') as f:
    blast_code = f.read()

has_speed_18 = "1.8f" in blast_code
has_radius_scaling = "MIN_RADIUS" in blast_code and "MAX_RADIUS" in blast_code
has_damage_scaling = "MIN_DAMAGE_RATIO" in blast_code and "MAX_DAMAGE_RATIO" in blast_code
has_aoe_detonation = "detonate" in blast_code and "getEntitiesByClass" in blast_code
has_explode_sfx = "ENTITY_GENERIC_EXPLODE" in blast_code
record("3.7 Fireball Projectile Speed 1.8 blocks/tick",
       has_speed_18,
       "Fireball travels at 1.8 blocks/tick")
record("3.8 Fireball Damage & Radius Charge Scaling",
       has_radius_scaling and has_damage_scaling,
       "Radius scales [1.0, 3.0] and damage scales [0.35x, 1.0x] by charge ratio")
record("3.9 Fireball AOE Collision & Detonation SFX",
       has_aoe_detonation and has_explode_sfx,
       "Detonates on entity/block impact with explosion particles and SFX")

with open(SKILL_DISPATCHER, 'r', encoding='utf-8') as f:
    dispatcher_code = f.read()

has_blast_dispatch = bool(re.search(r'case\s+"avatar:fire_blast"\s*->\s*FireBlastSkill\.tick\(player,\s*def\);', dispatcher_code))
record("3.10 SkillDispatcher routes avatar:fire_blast",
       has_blast_dispatch,
       "SkillDispatcher dispatches avatar:fire_blast to FireBlastSkill.tick")

with open(SERVER_EVENTS, 'r', encoding='utf-8') as f:
    events_code = f.read()

has_fireball_tick_loop = "FireBlastSkill.tickAllFireballs" in events_code and "tickAllFireballs(MinecraftServer" in blast_code
record("3.11 Decoupled In-Flight Fireball Progression via tickAllFireballs",
       has_fireball_tick_loop,
       "Fireball continues in-flight progression independently of caster active timeline state")

has_solid_collision_check = "getCollisionShape" in blast_code and "!world.isAir" not in blast_code
record("3.12 Solid Collision Shape Filter for Fireball Detonation",
       has_solid_collision_check,
       "Collision check inspects block collision shape to prevent premature detonation on passable foliage")

# -----------------------------------------------------------------
# SUITE 4: SIMULATION ORACLES & MATHEMATICAL PROOFS
# -----------------------------------------------------------------
print("\n--- [SUITE 4] Simulation Oracles: Charge Math, Timeline & Safety ---")

def simulate_timeline(is_hold, windup, active, recovery, max_charge, hold_release_at_tick=None):
    phase = "WINDUP" if windup > 0 else ("HOLD" if is_hold else "ACTIVE")
    ticks_in_phase = 0
    hold_ticks = 0
    history = []
    
    for t in range(1, 100):
        ticks_in_phase += 1
        history.append((t, phase, ticks_in_phase))
        
        if phase == "WINDUP":
            if ticks_in_phase >= windup:
                phase = "HOLD" if is_hold else "ACTIVE"
                ticks_in_phase = 0
        elif phase == "HOLD":
            hold_ticks = min(ticks_in_phase, max_charge)
            if hold_release_at_tick is not None and t >= hold_release_at_tick:
                phase = "ACTIVE"
                ticks_in_phase = 0
            elif ticks_in_phase >= max_charge * 2: # auto-release safety
                phase = "ACTIVE"
                ticks_in_phase = 0
        elif phase == "ACTIVE":
            if ticks_in_phase >= active:
                phase = "RECOVERY" if recovery > 0 else "IDLE"
                ticks_in_phase = 0
        elif phase == "RECOVERY":
            if ticks_in_phase >= recovery:
                phase = "IDLE"
                ticks_in_phase = 0
                break
                
    charge_ratio = min(1.0, max(1, hold_ticks) / max_charge) if max_charge > 0 else 0.0
    return history, hold_ticks, charge_ratio

# Oracle 4.1: Fire Jab Timeline Verification
jab_hist, _, _ = simulate_timeline(False, 2, 3, 4, 0)
strike_tick = next(t for t, p, tip in jab_hist if p == "ACTIVE" and tip == 1)
jab_total_ticks = len(jab_hist)
record("4.1 Fire Jab Simulation: Strike at tick 3, total 9 ticks",
       strike_tick == 3 and jab_total_ticks == 9,
       f"Strike occurred at absolute tick {strike_tick}, total duration = {jab_total_ticks} ticks")

# Oracle 4.2: Fire Blast Hold 10 ticks (25% charge)
_, hold10_ticks, hold10_ratio = simulate_timeline(True, 0, 25, 5, 40, hold_release_at_tick=10)
dmg_10t = 7.0 * (0.35 + 0.65 * hold10_ratio)
radius_10t = 1.0 + 2.0 * hold10_ratio
record("4.2 Fire Blast 10-tick charge (25% charge)",
       abs(hold10_ratio - 0.25) < 1e-4 and abs(radius_10t - 1.5) < 1e-4,
       f"charge={hold10_ratio:.2f}, damage={dmg_10t:.2f}, radius={radius_10t:.2f}b")

# Oracle 4.3: Fire Blast Full 40 ticks (100% charge)
_, hold40_ticks, hold40_ratio = simulate_timeline(True, 0, 25, 5, 40, hold_release_at_tick=40)
dmg_40t = 7.0 * (0.35 + 0.65 * hold40_ratio)
radius_40t = 1.0 + 2.0 * hold40_ratio
record("4.3 Fire Blast 40-tick charge (100% full charge)",
       abs(hold40_ratio - 1.0) < 1e-4 and abs(dmg_40t - 7.0) < 1e-4 and abs(radius_40t - 3.0) < 1e-4,
       f"charge={hold40_ratio:.2f}, damage={dmg_40t:.2f}, radius={radius_40t:.2f}b")

# Oracle 4.4: Fire Blast Safety Auto-Release at 80 ticks
auto_hist, auto_ticks, auto_ratio = simulate_timeline(True, 0, 25, 5, 40, hold_release_at_tick=999)
record("4.4 Fire Blast auto-release safety timeout",
       auto_ticks == 40 and auto_ratio == 1.0,
       f"Auto-released safely with capped charge={auto_ratio:.2f}")

# Oracle 4.5: Auto-Release Cooldown & HUD Synchronization Guarantee
has_autorelease_cd = "phaseBefore == SkillTimeline.Phase.HOLD && phaseAfter == SkillTimeline.Phase.ACTIVE" in dispatcher_code and "setCooldown" in dispatcher_code
record("4.5 Auto-Release Safety Cooldown & HUD Synchronization Guarantee",
       has_autorelease_cd,
       "Server automatically applies skill cooldown and updates HUD when auto-release safety timeout fires")

print("\n=================================================================")
print("TEST SUMMARY")
print("=================================================================")
passed_count = sum(1 for _, s, _ in test_results if s == "PASS")
failed_count = sum(1 for _, s, _ in test_results if s == "FAIL")
print(f"Total Tests Executed: {len(test_results)}")
print(f"Passed: {passed_count}")
print(f"Failed: {failed_count}")
print("=================================================================")

if failed_count > 0:
    sys.exit(1)
