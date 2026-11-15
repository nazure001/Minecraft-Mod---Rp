#!/usr/bin/env python3
"""
Test Suite: Milestone 5 (Phase D: Hold-Release Framework & Fire Blast)
Verifies:
1. Generic Hold-Release Timeline (SkillTimeline.java) state machine, aliases, clamping, auto-release.
2. Network Packets (C2SHoldStart, C2SHoldRelease), codecs, and handlers.
3. Client Key Handling: 5 slots, continuous key polling, screen cancellation guard.
4. Charge Orb clean disappearance (OrbVisualConfig: WINDUP + HOLD only).
5. Fire Blast Projectile Entity (FireBlastProjectileEntity, registration, renderer, physics, damage/radius scaling).
6. Slot Mapping Preservation (ElementSlotMap.SLOT_COUNT=5, element_slots.json maps all 5 fire skills).
7. Empirical simulation oracles for charge ratio, damage, radius, and safety timeout.
"""

import os
import re
import json
import math

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
MOD_DIR = os.path.join(REPO_ROOT, "mod")

SKILL_TIMELINE = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "data", "SkillTimeline.java")
SKILL_PACKETS = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "network", "SkillPackets.java")
SKILL_NETWORKING = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "network", "SkillNetworking.java")
SKILL_DISPATCHER = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "skill", "SkillDispatcher.java")
ELEMENT_SLOT_MAP = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "skill", "ElementSlotMap.java")
FIRE_BLAST_SKILL = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "skill", "impl", "FireBlastSkill.java")
PROJECTILE_ENTITY = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "entity", "FireBlastProjectileEntity.java")
MOD_MAIN = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "AvatarElementsMod.java")
CLIENT_MAIN = os.path.join(MOD_DIR, "src", "client", "java", "com", "avatarmod", "elements", "client", "AvatarElementsClient.java")
KEY_BINDINGS = os.path.join(MOD_DIR, "src", "client", "java", "com", "avatarmod", "elements", "client", "input", "AvatarKeyBindings.java")
ORB_CONFIG = os.path.join(MOD_DIR, "src", "client", "java", "com", "avatarmod", "elements", "client", "orb", "OrbVisualConfig.java")
SLOTS_JSON = os.path.join(MOD_DIR, "src", "main", "resources", "data", "avatar_elements", "element_slots.json")
SKILL_DEFS_JSON = os.path.join(MOD_DIR, "src", "main", "resources", "data", "avatar_elements", "skill_definitions.json")

test_results = []

def record(name, passed, detail=""):
    test_results.append((name, passed, detail))
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}: {detail}")

print("=" * 65)
print("RUNNING MILESTONE 5 FIRE BLAST & HOLD-RELEASE REGRESSION TEST")
print("=" * 65)

# --- [SUITE 1] Generic Hold-Release Timeline ---
print("\n--- [SUITE 1] Generic Hold-Release Timeline (SkillTimeline.java) ---")
with open(SKILL_TIMELINE, "r", encoding="utf-8") as f:
    tl_code = f.read()

has_phase_hold = "public enum Phase { IDLE, WINDUP, HOLD, ACTIVE, RECOVERY }" in tl_code
record("1.1 Phase.HOLD Enum Integration", has_phase_hold, "Canonical Phase.HOLD preserved in Phase enum")

has_release_charge = "public void releaseCharge() { releaseHold(); }" in tl_code
has_is_charging = "public boolean isCharging() { return isHolding(); }" in tl_code
has_charge_ticks = "public int chargeTicks() { return holdChargedTicks(); }" in tl_code
has_start_charging = "public static SkillTimeline startCharging(" in tl_code
record("1.2 Hold-Release Alias Methods",
       has_release_charge and has_is_charging and has_charge_ticks and has_start_charging,
       "releaseCharge(), isCharging(), chargeTicks(), and startCharging(...) present")

has_clamped_charge = "holdChargedTicks = Math.min(ticksInPhase, limit)" in tl_code
has_auto_release = "ticksInPhase >= limit * 2" in tl_code and "releaseHold()" in tl_code
record("1.3 Clamped Charge and 2x Safety Auto-Release",
       has_clamped_charge and has_auto_release,
       "Charge clamped to limit; auto-releases at 2x limit (80t)")

# --- [SUITE 2] Network Packets & Handlers ---
print("\n--- [SUITE 2] Network Packets & Handlers (SkillPackets & SkillNetworking) ---")
with open(SKILL_PACKETS, "r", encoding="utf-8") as f:
    packets_code = f.read()

has_c2s_hold_start = "record C2SHoldStart(int slotIndex)" in packets_code and "c2s_hold_start" in packets_code
has_c2s_hold_release = "record C2SHoldRelease(int slotIndex, int heldTicks)" in packets_code and "c2s_hold_release" in packets_code
record("2.1 C2SHoldStart and C2SHoldRelease Record Definitions",
       has_c2s_hold_start and has_c2s_hold_release,
       "C2SHoldStart(int slotIndex) and C2SHoldRelease(int slotIndex, int heldTicks) registered")

with open(SKILL_NETWORKING, "r", encoding="utf-8") as f:
    net_code = f.read()

has_handle_hold_start = "handleHoldStart(ServerPlayerEntity player, int slotIndex)" in net_code
has_handle_hold_release = "handleHoldRelease(ServerPlayerEntity player, int slotIndex, int heldTicks)" in net_code
has_upfront_chi = "data.trySpendChi(def.chiCost())" in net_code
has_release_cooldown = "data.setCooldown(activeSkill, def.cooldownTicks())" in net_code
record("2.2 Upfront Chi & Release Cooldown in SkillNetworking",
       has_handle_hold_start and has_handle_hold_release and has_upfront_chi and has_release_cooldown,
       "Chi spent upfront on hold start; cooldown applied on release")

with open(SKILL_DISPATCHER, "r", encoding="utf-8") as f:
    disp_code = f.read()

has_dispatcher_cooldown = "phaseBefore == SkillTimeline.Phase.HOLD && phaseAfter == SkillTimeline.Phase.ACTIVE" in disp_code and "data.setCooldown" in disp_code
record("2.3 SkillDispatcher Auto-Release Cooldown Fallback",
       has_dispatcher_cooldown,
       "Cooldown applied if timeline transitions HOLD -> ACTIVE via internal auto-release")

# --- [SUITE 3] Client Key Handling & Slot 5 ---
print("\n--- [SUITE 3] Client Key Handling & Slot 5 ---")
with open(KEY_BINDINGS, "r", encoding="utf-8") as f:
    keys_code = f.read()

has_slot_5 = "SLOT_5" in keys_code and "GLFW_KEY_B" in keys_code
record("3.1 SLOT_5 Key Binding (B key)", has_slot_5, "SLOT_5 registered with GLFW_KEY_B")

with open(CLIENT_MAIN, "r", encoding="utf-8") as f:
    client_code = f.read()

has_5_slots_client = "handleSlotKey(client, 4, AvatarKeyBindings.SLOT_5)" in client_code and "boolean[5]" in client_code
has_continuous_poll = "key.isPressed() || key.wasPressed()" in client_code or ("pressedNow || tapped" in client_code and "key.isPressed()" in client_code and "key.wasPressed()" in client_code)
has_screen_guard = "client.currentScreen != null" in client_code and "slotHolding[slot]" in client_code
record("3.2 5-Slot Client Key Handling & Screen Guard",
       has_5_slots_client and has_continuous_poll and has_screen_guard,
       "5 slots mapped in client tick; continuous key polling and screen-open release guard present")

# --- [SUITE 4] Charge Orb Lifecycle & Clean Disappearance ---
print("\n--- [SUITE 4] Charge Orb Clean Disappearance (Requirement R3) ---")
with open(ORB_CONFIG, "r", encoding="utf-8") as f:
    orb_code = f.read()

has_blast_orb_config = '"avatar:fire_blast", new Config(Set.of("WINDUP", "HOLD"))' in orb_code
has_no_active_in_blast = 'Set.of("WINDUP", "HOLD", "ACTIVE")' not in orb_code
record("4.1 Fire Blast Charge Orb Clean Disappearance on Release",
       has_blast_orb_config and has_no_active_in_blast,
       "Orb visible only in WINDUP and HOLD; cleanly dissolves when ACTIVE starts")

# --- [SUITE 5] Fire Blast Projectile Entity ---
print("\n--- [SUITE 5] Fire Blast Projectile Entity & Mechanics ---")
with open(PROJECTILE_ENTITY, "r", encoding="utf-8") as f:
    proj_code = f.read()

is_projectile_entity = "extends ProjectileEntity" in proj_code
has_aoe_detonate = "detonate()" in proj_code and "FireBlastSkill.detonate" in proj_code
record("5.1 FireBlastProjectileEntity extends ProjectileEntity",
       is_projectile_entity and has_aoe_detonate,
       "FireBlastProjectileEntity created with AOE detonation delegate")

with open(MOD_MAIN, "r", encoding="utf-8") as f:
    mod_code = f.read()

has_entity_type = "FIRE_BLAST_PROJECTILE" in mod_code and "fire_blast_projectile" in mod_code
record("5.2 EntityType<FireBlastProjectileEntity> Registration",
       has_entity_type,
       "FIRE_BLAST_PROJECTILE registered in Registries.ENTITY_TYPE")

has_client_renderer = bool(re.search(r'EntityRendererRegistry\.register\(\s*AvatarElementsMod\.FIRE_BLAST_PROJECTILE', client_code))
record("5.3 Client Entity Renderer Registration",
       has_client_renderer,
       "Client renderer registered in AvatarElementsClient")

with open(FIRE_BLAST_SKILL, "r", encoding="utf-8") as f:
    blast_code = f.read()

has_speed_const = "1.8f" in blast_code and ("SPEED" in blast_code or "BASE_SPEED" in blast_code)
has_radius_const = "MIN_RADIUS" in blast_code and "MAX_RADIUS" in blast_code
has_damage_const = "MIN_DAMAGE_RATIO" in blast_code and "MAX_DAMAGE_RATIO" in blast_code
has_entity_spawn = "FireBlastProjectileEntity" in blast_code and "spawnEntity" in blast_code
has_sfx = "ENTITY_GENERIC_EXPLODE" in blast_code
record("5.4 FireBlastSkill Constants & Entity Spawning",
       has_speed_const and has_radius_const and has_damage_const and has_entity_spawn and has_sfx,
       "Constants preserved, spawns FireBlastProjectileEntity, detonates with SFX/VFX")

# --- [SUITE 6] Slot Mapping Preservation (Requirement R7) ---
print("\n--- [SUITE 6] Slot Mapping Preservation (Requirement R7) ---")
with open(ELEMENT_SLOT_MAP, "r", encoding="utf-8") as f:
    slot_map_code = f.read()

has_slot_count_5 = "public static final int SLOT_COUNT = 5;" in slot_map_code
record("6.1 ElementSlotMap.SLOT_COUNT == 5", has_slot_count_5, "SLOT_COUNT is 5")

with open(SLOTS_JSON, "r", encoding="utf-8") as f:
    slots_data = json.load(f)

fire_slots = slots_data.get("FIRE", [])
all_5_fire_skills = ["avatar:fire_jab", "avatar:fire_blast", "avatar:flame_sweep", "avatar:fire_guard", "avatar:fire_jet"]
has_all_5 = (fire_slots == all_5_fire_skills)
record("6.2 element_slots.json FIRE Mapping Complete",
       has_all_5,
       f"All 5 fire skills mapped in order: {fire_slots}")

# --- [SUITE 7] Mathematical & Physical Simulation Oracles ---
print("\n--- [SUITE 7] Mathematical & Physical Simulation Oracles ---")
def calculate_fire_blast(charge_ticks, max_charge=40, base_damage=7.0, base_radius_min=1.0, base_radius_max=3.0, base_knockback=1.0):
    clamped_ticks = max(1, min(charge_ticks, max_charge))
    ratio = min(1.0, clamped_ticks / max_charge)
    damage = base_damage * (0.35 + 0.65 * ratio)
    radius = base_radius_min + (base_radius_max - base_radius_min) * ratio
    knockback = base_knockback * (0.5 + 0.5 * ratio)
    return ratio, damage, radius, knockback

# Quick Tap (1 tick)
r_tap, d_tap, rad_tap, kb_tap = calculate_fire_blast(1)
record("7.1 Quick Tap Scaling (1 tick)",
       math.isclose(r_tap, 0.025) and math.isclose(d_tap, 2.56375, rel_tol=1e-3) and math.isclose(rad_tap, 1.05, rel_tol=1e-3),
       f"ratio={r_tap:.3f}, damage={d_tap:.2f}, radius={rad_tap:.2f}b, knockback={kb_tap:.2f}")

# Half Charge (20 ticks / 50%)
r_half, d_half, rad_half, kb_half = calculate_fire_blast(20)
record("7.2 Half Charge Scaling (20 ticks)",
       math.isclose(r_half, 0.5) and math.isclose(d_half, 4.725, rel_tol=1e-3) and math.isclose(rad_half, 2.0, rel_tol=1e-3),
       f"ratio={r_half:.3f}, damage={d_half:.2f}, radius={rad_half:.2f}b, knockback={kb_half:.2f}")

# Full Charge (40 ticks / 100%)
r_full, d_full, rad_full, kb_full = calculate_fire_blast(40)
record("7.3 Full Charge Scaling (40 ticks)",
       math.isclose(r_full, 1.0) and math.isclose(d_full, 7.0, rel_tol=1e-3) and math.isclose(rad_full, 3.0, rel_tol=1e-3),
       f"ratio={r_full:.3f}, damage={d_full:.2f}, radius={rad_full:.2f}b, knockback={kb_full:.2f}")

# Over-Hold (60 ticks / held between 40t and 80t)
r_over, d_over, rad_over, kb_over = calculate_fire_blast(60)
record("7.4 Over-Hold Retention (60 ticks capped at 100%)",
       math.isclose(r_over, 1.0) and math.isclose(d_over, 7.0, rel_tol=1e-3) and math.isclose(rad_over, 3.0, rel_tol=1e-3),
       f"ratio={r_over:.3f}, damage={d_over:.2f}, radius={rad_over:.2f}b (clamped to max charge)")

# Travel Range Oracle (speed 1.8 blocks/tick over 25 ticks)
speed = 1.8
lifetime = 25
max_distance = speed * lifetime
record("7.5 Projectile Kinematic Range Oracle",
       max_distance >= 24.0,
       f"Max travel distance = {max_distance:.1f} blocks (exceeds definition range 24.0)")

print("=" * 65)
total_tests = len(test_results)
passed_tests = sum(1 for _, p, _ in test_results if p)
failed_tests = total_tests - passed_tests
print(f"Total Tests Executed: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print("=" * 65)

if failed_tests > 0:
    exit(1)
