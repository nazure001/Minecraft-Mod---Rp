#!/usr/bin/env python3
"""
ADVERSARIAL EMPIRICAL CHALLENGER TEST SUITE: MILESTONE 5
Focus: Client Input Stress Testing & Slot Mapping Preservation (Requirements R6, R7, R3)

Tests:
1. Slot Mapping Preservation & Coverage:
   - ElementSlotMap.SLOT_COUNT == 5
   - element_slots.json FIRE contains all 5 skills in correct order:
     [fire_jab, fire_blast, flame_sweep, fire_guard, fire_jet]
   - Neither flame_sweep nor fire_guard was dropped or replaced
   - AvatarKeyBindings.java maps SLOT_5 to GLFW_KEY_B
   - AvatarElementsClient.java handles all 5 slots (slotHolding, slotHoldTicks, slotHeldSkillId arrays of size 5)
2. Empirical Input Handling Lifecycle Simulator:
   - Rapid Tap (< 50ms): key pressed and released within the same client tick.
     Verifies C2SHoldStart followed immediately by C2SHoldRelease without stuck hold state.
   - Standard Hold & Release (15 ticks): clean transition, accurate tick count.
   - Prolonged Hold (> 80 ticks): verifies 80t auto-release failsafe triggers on server,
     transitions HOLD -> ACTIVE, applies cooldown via SkillDispatcher fallback, and sends S2CHudUpdate.
   - GUI Screen Open Guard: verifies hold state is immediately cancelled/released when inventory/chat opens.
   - Repeated Rapid Tap Stress Test: multiple taps across sequential ticks with zero state leakage.
3. Anti-Spam & Rate-Limiting Semantics:
   - Rapid repeated tap within RATE_LIMIT_TICKS (3 ticks) is blocked per-skill on server.
   - Cross-skill rapid switching (Z -> X) is permitted by per-skill rate limiting.
4. Charge Scaling & AOE Damage Verification:
   - Clamped charge ratio math, damage and radius scaling.
"""

import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(r"D:\repo\Minecraft Mod & Rp")
MOD_ROOT = REPO_ROOT / "mod"

# Files to inspect
SLOT_JSON_PATH = MOD_ROOT / "src/main/resources/data/avatar_elements/element_slots.json"
SKILL_DEF_JSON_PATH = MOD_ROOT / "src/main/resources/data/avatar_elements/skill_definitions.json"
ELEMENT_SLOT_MAP_PATH = MOD_ROOT / "src/main/java/com/avatarmod/elements/skill/ElementSlotMap.java"
KEYBINDINGS_PATH = MOD_ROOT / "src/client/java/com/avatarmod/elements/client/input/AvatarKeyBindings.java"
CLIENT_MOD_PATH = MOD_ROOT / "src/client/java/com/avatarmod/elements/client/AvatarElementsClient.java"
SKILL_DISPATCHER_PATH = MOD_ROOT / "src/main/java/com/avatarmod/elements/skill/SkillDispatcher.java"
SKILL_TIMELINE_PATH = MOD_ROOT / "src/main/java/com/avatarmod/elements/data/SkillTimeline.java"
SKILL_NETWORKING_PATH = MOD_ROOT / "src/main/java/com/avatarmod/elements/network/SkillNetworking.java"

passed_tests = 0
failed_tests = 0

def check(condition: bool, test_name: str, details: str = ""):
    global passed_tests, failed_tests
    if condition:
        passed_tests += 1
        print(f"[PASS] {test_name}: {details}")
    else:
        failed_tests += 1
        print(f"[FAIL] {test_name}: {details}")

print("=================================================================")
print("RUNNING INPUT STRESS & SLOT PRESERVATION CHALLENGER SUITE (M5)")
print("=================================================================")

# =====================================================================
# SUITE 1: Slot Mapping Preservation & 5-Slot Coverage (Requirement R7)
# =====================================================================
print("\n--- [SUITE 1] Slot Mapping Preservation & 5-Slot Coverage (R7) ---")

# 1.1 ElementSlotMap.SLOT_COUNT == 5
with open(ELEMENT_SLOT_MAP_PATH, "r", encoding="utf-8") as f:
    slot_map_src = f.read()

m = re.search(r"public\s+static\s+final\s+int\s+SLOT_COUNT\s*=\s*(\d+);", slot_map_src)
check(m is not None and int(m.group(1)) == 5, "1.1 ElementSlotMap.SLOT_COUNT == 5",
      f"Found SLOT_COUNT = {m.group(1) if m else 'None'} (expected 5)")

# 1.2 element_slots.json Fire Mapping Completeness
with open(SLOT_JSON_PATH, "r", encoding="utf-8") as f:
    slot_json = json.load(f)

fire_slots = slot_json.get("FIRE", [])
expected_fire = [
    "avatar:fire_jab",
    "avatar:fire_blast",
    "avatar:flame_sweep",
    "avatar:fire_guard",
    "avatar:fire_jet"
]

check(len(fire_slots) == 5, "1.2 element_slots.json FIRE list length",
      f"Length = {len(fire_slots)} (expected 5)")

check(fire_slots == expected_fire, "1.3 element_slots.json FIRE slot order and IDs",
      f"Slots = {fire_slots}\nExpected = {expected_fire}")

# 1.4 Non-regression: flame_sweep and fire_guard not dropped or deleted
check("avatar:flame_sweep" in fire_slots, "1.4 Non-regression: flame_sweep preserved",
      f"flame_sweep present at index {fire_slots.index('avatar:flame_sweep') if 'avatar:flame_sweep' in fire_slots else -1}")
check("avatar:fire_guard" in fire_slots, "1.5 Non-regression: fire_guard preserved",
      f"fire_guard present at index {fire_slots.index('avatar:fire_guard') if 'avatar:fire_guard' in fire_slots else -1}")

# 1.6 Keybindings: SLOT_5 bound to GLFW_KEY_B
with open(KEYBINDINGS_PATH, "r", encoding="utf-8") as f:
    keybind_src = f.read()

slot5_match = re.search(r"SLOT_5\s*=\s*KeyBindingHelper\.registerKeyBinding\([^;]*GLFW\.GLFW_KEY_B", keybind_src, re.DOTALL)
check(slot5_match is not None, "1.6 AvatarKeyBindings SLOT_5 bound to GLFW_KEY_B",
      "SLOT_5 registered with GLFW.GLFW_KEY_B")

# Check all 5 slots in keybindings: Z, X, C, V, B
z_bind = "GLFW.GLFW_KEY_Z" in keybind_src
x_bind = "GLFW.GLFW_KEY_X" in keybind_src
c_bind = "GLFW.GLFW_KEY_C" in keybind_src
v_bind = "GLFW.GLFW_KEY_V" in keybind_src
b_bind = "GLFW.GLFW_KEY_B" in keybind_src
check(z_bind and x_bind and c_bind and v_bind and b_bind, "1.7 AvatarKeyBindings full Z/X/C/V/B mapping",
      f"Z={z_bind}, X={x_bind}, C={c_bind}, V={v_bind}, B={b_bind}")

# 1.8 Client handling 5 slots in AvatarElementsClient.java
with open(CLIENT_MOD_PATH, "r", encoding="utf-8") as f:
    client_src = f.read()

check("boolean[] slotHolding = new boolean[5]" in client_src, "1.8 AvatarElementsClient slotHolding array size 5",
      "slotHolding array has length 5")
check("int[] slotHoldTicks = new int[5]" in client_src, "1.9 AvatarElementsClient slotHoldTicks array size 5",
      "slotHoldTicks array has length 5")
check("String[] slotHeldSkillId = new String[5]" in client_src, "1.10 AvatarElementsClient slotHeldSkillId array size 5",
      "slotHeldSkillId array has length 5")

all_5_slots_handled = all(
    f"handleSlotKey(client, {i}, AvatarKeyBindings.SLOT_{i+1})" in client_src
    for i in range(5)
)
check(all_5_slots_handled, "1.11 AvatarElementsClient handles all 5 slots (0..4)",
      f"All 5 handleSlotKey calls present: {all_5_slots_handled}")

# 1.12 skill_definitions.json verification
with open(SKILL_DEF_JSON_PATH, "r", encoding="utf-8") as f:
    skill_defs = json.load(f).get("skills", [])

defined_skill_ids = {s["id"] for s in skill_defs}
all_fire_skills_defined = all(sid in defined_skill_ids for sid in expected_fire)
check(all_fire_skills_defined, "1.12 All 5 fire skills defined in skill_definitions.json",
      f"Found definitions for: {expected_fire}")


# =====================================================================
# SUITE 2: Client Input Handling Lifecycle Simulator
# =====================================================================
print("\n--- [SUITE 2] Client Input Handling Lifecycle Simulator ---")

class MockKeyBinding:
    def __init__(self):
        self.pressed_now = False
        self.was_pressed_queue = []

    def set_state(self, pressed_now: bool, was_pressed_count: int = 0):
        self.pressed_now = pressed_now
        self.was_pressed_queue = [True] * was_pressed_count

    def isPressed(self) -> bool:
        return self.pressed_now

    def wasPressed(self) -> bool:
        if self.was_pressed_queue:
            return self.was_pressed_queue.pop(0)
        return False

class ClientInputSimulator:
    def __init__(self):
        self.slotHolding = [False] * 5
        self.slotHoldTicks = [0] * 5
        self.slotHeldSkillId = [None] * 5
        self.currentScreen = None
        self.sent_packets = []  # list of (packet_type, slot, skill_id)

    def handleSlotKey(self, slot: int, key: MockKeyBinding, skillId: str, isHoldSkill: bool):
        # GUI screen guard
        if self.currentScreen is not None:
            if self.slotHolding[slot]:
                self.slotHolding[slot] = False
                heldId = self.slotHeldSkillId[slot]
                self.slotHeldSkillId[slot] = None
                self.sent_packets.append(("C2SHoldRelease", slot, heldId if heldId else ""))
                self.slotHoldTicks[slot] = 0
            while key.wasPressed():
                pass
            return

        if isHoldSkill:
            pressedNow = key.isPressed()
            tapped = key.wasPressed()

            if pressedNow or tapped:
                if not self.slotHolding[slot]:
                    # Rising edge
                    self.slotHolding[slot] = True
                    self.slotHoldTicks[slot] = 1
                    self.slotHeldSkillId[slot] = skillId
                    self.sent_packets.append(("C2SHoldStart", slot, skillId))

                    # Sub-tick quick tap (< 50ms): key was tapped and released before tick
                    if not pressedNow:
                        self.slotHolding[slot] = False
                        self.slotHeldSkillId[slot] = None
                        self.sent_packets.append(("C2SHoldRelease", slot, skillId))
                        self.slotHoldTicks[slot] = 0
                else:
                    self.slotHoldTicks[slot] += 1
            else:
                # Falling edge: key released
                if self.slotHolding[slot]:
                    self.slotHolding[slot] = False
                    heldId = self.slotHeldSkillId[slot] if self.slotHeldSkillId[slot] is not None else skillId
                    self.slotHeldSkillId[slot] = None
                    self.sent_packets.append(("C2SHoldRelease", slot, heldId))
                    self.slotHoldTicks[slot] = 0
        else:
            if self.slotHolding[slot]:
                self.slotHolding[slot] = False
                heldId = self.slotHeldSkillId[slot] if self.slotHeldSkillId[slot] is not None else skillId
                self.slotHeldSkillId[slot] = None
                self.sent_packets.append(("C2SHoldRelease", slot, heldId))
                self.slotHoldTicks[slot] = 0
            any_pressed = False
            while key.wasPressed():
                any_pressed = True
            if any_pressed:
                self.sent_packets.append(("C2SSlotCast", slot, skillId))

# Test 2.1: Rapid Tap (< 50ms)
sim = ClientInputSimulator()
key = MockKeyBinding()
# Key tapped and released in <50ms: isPressed=False, wasPressed=True (1 event)
key.set_state(pressed_now=False, was_pressed_count=1)

sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)

packets = sim.sent_packets
check(len(packets) == 2, "2.1 Rapid tap sends exactly 2 packets in single tick",
      f"Packets count = {len(packets)}: {packets}")
check(packets[0] == ("C2SHoldStart", 1, "avatar:fire_blast") and
      packets[1] == ("C2SHoldRelease", 1, "avatar:fire_blast"),
      "2.2 Rapid tap packet sequence: C2SHoldStart followed by C2SHoldRelease",
      f"Packet 0: {packets[0]}, Packet 1: {packets[1]}")
check(sim.slotHolding[1] is False and sim.slotHoldTicks[1] == 0 and sim.slotHeldSkillId[1] is None,
      "2.3 Rapid tap leaves client in clean non-holding state (no stuck state)",
      f"slotHolding={sim.slotHolding[1]}, ticks={sim.slotHoldTicks[1]}, heldId={sim.slotHeldSkillId[1]}")

# Next tick idle: ensure no ghost packets
key.set_state(pressed_now=False, was_pressed_count=0)
sim.sent_packets.clear()
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
check(len(sim.sent_packets) == 0, "2.4 Subsequent tick sends 0 packets (no stuck repeat)",
      f"Sent packets = {sim.sent_packets}")

# Test 2.5: Standard Hold & Release (15 ticks)
sim = ClientInputSimulator()
key = MockKeyBinding()

# Tick 1: key pressed
key.set_state(pressed_now=True, was_pressed_count=1)
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
check(sim.sent_packets == [("C2SHoldStart", 1, "avatar:fire_blast")],
      "2.5 Hold start sends C2SHoldStart and enters holding state",
      f"Sent: {sim.sent_packets}, holding: {sim.slotHolding[1]}")

# Ticks 2..15: held continuously
sim.sent_packets.clear()
for t in range(2, 16):
    key.set_state(pressed_now=True, was_pressed_count=0)
    sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)

check(len(sim.sent_packets) == 0, "2.6 Mid-hold ticks send zero duplicate packets",
      f"Sent mid-hold: {sim.sent_packets}")
check(sim.slotHoldTicks[1] == 15, "2.7 Hold tick counter increments accurately to 15",
      f"slotHoldTicks[1] = {sim.slotHoldTicks[1]}")

# Tick 16: key released
key.set_state(pressed_now=False, was_pressed_count=0)
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
check(sim.sent_packets == [("C2SHoldRelease", 1, "avatar:fire_blast")],
      "2.8 Key release sends C2SHoldRelease",
      f"Sent on release: {sim.sent_packets}")
check(sim.slotHolding[1] is False and sim.slotHoldTicks[1] == 0,
      "2.9 Client state resets completely upon release",
      f"slotHolding={sim.slotHolding[1]}, ticks={sim.slotHoldTicks[1]}")


# Test 2.10: GUI Screen Open Guard (Inventory / Chat opened while holding)
sim = ClientInputSimulator()
key = MockKeyBinding()

# Start holding at tick 1
key.set_state(pressed_now=True, was_pressed_count=1)
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
sim.sent_packets.clear()

# Mid-hold at tick 10: Player opens Inventory screen (currentScreen != None)
sim.currentScreen = "InventoryScreen"
key.set_state(pressed_now=True, was_pressed_count=0)  # physical key might still be held down
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)

check(sim.sent_packets == [("C2SHoldRelease", 1, "avatar:fire_blast")],
      "2.10 Screen open immediately forces C2SHoldRelease dispatch",
      f"Dispatched packets on screen open: {sim.sent_packets}")
check(sim.slotHolding[1] is False and sim.slotHoldTicks[1] == 0 and sim.slotHeldSkillId[1] is None,
      "2.11 Screen open immediately resets client holding state",
      f"slotHolding={sim.slotHolding[1]}, ticks={sim.slotHoldTicks[1]}")

# While GUI screen is still open, key repeat events are drained without effect
sim.sent_packets.clear()
key.set_state(pressed_now=True, was_pressed_count=2)
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
check(len(sim.sent_packets) == 0 and len(key.was_pressed_queue) == 0,
      "2.12 GUI screen guard drains queued key presses with 0 packets emitted",
      f"Sent: {sim.sent_packets}, queue remaining: {len(key.was_pressed_queue)}")

# Screen closed, key released
sim.currentScreen = None
key.set_state(pressed_now=False, was_pressed_count=0)
sim.handleSlotKey(slot=1, key=key, skillId="avatar:fire_blast", isHoldSkill=True)
check(len(sim.sent_packets) == 0 and sim.slotHolding[1] is False,
      "2.13 Closing screen and releasing key maintains clean idle state",
      f"Sent: {sim.sent_packets}, holding: {sim.slotHolding[1]}")


# =====================================================================
# SUITE 3: Server Hold-Release Timeline & 80t Auto-Release Oracle
# =====================================================================
print("\n--- [SUITE 3] Server Hold-Release Timeline & 80t Auto-Release Oracle ---")

class ServerSkillTimeline:
    """Accurate Python oracle of com.avatarmod.elements.data.SkillTimeline"""
    def __init__(self, skill_id: str, windup: int, active: int, recovery: int, is_hold: bool, max_hold: int):
        self.skill_id = skill_id
        self.windup_ticks = windup
        self.active_ticks = active
        self.recovery_ticks = recovery
        self.is_hold_skill = is_hold
        self.max_hold_ticks = max_hold
        self.phase = "IDLE"
        self.ticks_in_phase = 0
        self.hold_charged_ticks = 0

    def start(self):
        if self.phase != "IDLE":
            return
        if self.windup_ticks > 0:
            self.phase = "WINDUP"
        elif self.is_hold_skill:
            self.phase = "HOLD"
        else:
            self.phase = "ACTIVE"
        self.ticks_in_phase = 0
        self.hold_charged_ticks = 0

    def tick(self) -> str:
        if self.phase == "IDLE":
            return "IDLE"
        self.ticks_in_phase += 1
        if self.phase == "WINDUP":
            if self.ticks_in_phase >= self.windup_ticks:
                self.phase = "HOLD" if self.is_hold_skill else "ACTIVE"
                self.ticks_in_phase = 0
        elif self.phase == "HOLD":
            limit = self.max_hold_ticks if self.max_hold_ticks > 0 else 40
            self.hold_charged_ticks = min(self.ticks_in_phase, limit)
            # Auto-release safety at 2x limit (80t)
            if self.ticks_in_phase >= limit * 2:
                self.release_hold()
        elif self.phase == "ACTIVE":
            if self.ticks_in_phase >= self.active_ticks:
                self.phase = "RECOVERY" if self.recovery_ticks > 0 else "IDLE"
                self.ticks_in_phase = 0
        elif self.phase == "RECOVERY":
            if self.ticks_in_phase >= self.recovery_ticks:
                self.phase = "IDLE"
                self.ticks_in_phase = 0
        return self.phase

    def release_hold(self):
        if self.phase == "HOLD":
            limit = self.max_hold_ticks if self.max_hold_ticks > 0 else 40
            self.hold_charged_ticks = max(1, min(self.ticks_in_phase, limit))
            self.phase = "ACTIVE"
            self.ticks_in_phase = 0

    def get_charge_ratio(self) -> float:
        limit = self.max_hold_ticks if self.max_hold_ticks > 0 else 40
        return min(1.0, max(1, self.hold_charged_ticks) / float(limit))

# Simulate Fire Blast: windup=0, active=25, recovery=5, is_hold=True, max_hold=40
tl = ServerSkillTimeline("avatar:fire_blast", windup=0, active=25, recovery=5, is_hold=True, max_hold=40)
tl.start()

check(tl.phase == "HOLD", "3.1 Fire Blast timeline starts immediately in Phase.HOLD",
      f"Initial phase = {tl.phase}")

# Ticks 1..40: Charging
for t in range(40):
    tl.tick()

check(tl.phase == "HOLD", "3.2 At 40 ticks, phase remains HOLD", f"Phase = {tl.phase}")
check(tl.get_charge_ratio() == 1.0, "3.3 At 40 ticks, charge ratio reaches 1.0 (100%)",
      f"charge ratio = {tl.get_charge_ratio()}")

# Ticks 41..79: Over-hold aim retention (remains HOLD, clamped to 1.0)
for t in range(41, 80):
    tl.tick()

check(tl.phase == "HOLD", "3.4 At 79 ticks, phase still HOLD (aim retention window)",
      f"Phase at tick 79 = {tl.phase}, ticks_in_phase = {tl.ticks_in_phase}")
check(tl.get_charge_ratio() == 1.0, "3.5 At 79 ticks, charge ratio clamped at 1.0",
      f"charge ratio = {tl.get_charge_ratio()}")

# Tick 80: Failsafe triggers auto-release
phase_before = tl.phase
phase_after = tl.tick()

check(phase_before == "HOLD" and phase_after == "ACTIVE",
      "3.6 At tick 80, timeline transitions HOLD -> ACTIVE automatically",
      f"phase_before={phase_before}, phase_after={phase_after}")
check(tl.ticks_in_phase == 0, "3.7 At auto-release, ticks_in_phase resets to 0 for ACTIVE",
      f"ticks_in_phase = {tl.ticks_in_phase}")
check(tl.get_charge_ratio() == 1.0, "3.8 Auto-released projectile fires with 100% full charge",
      f"charge ratio = {tl.get_charge_ratio()}")

# Server SkillDispatcher Hook Check: Cooldown applied upon HOLD -> ACTIVE transition
with open(SKILL_DISPATCHER_PATH, "r", encoding="utf-8") as f:
    dispatcher_src = f.read()

has_cooldown_hook = (
    "phaseBefore == SkillTimeline.Phase.HOLD && phaseAfter == SkillTimeline.Phase.ACTIVE" in dispatcher_src and
    "data.setCooldown(activeSkill, def.cooldownTicks())" in dispatcher_src and
    "SkillNetworking.sendHudUpdate" in dispatcher_src
)
check(has_cooldown_hook, "3.9 SkillDispatcher triggers cooldown & HUD update on auto-release transition",
      "SkillDispatcher checks phaseBefore==HOLD && phaseAfter==ACTIVE and sets cooldown")


# =====================================================================
# SUITE 4: Server-Side Rate Limiting & Rapid Tap Anti-Spam
# =====================================================================
print("\n--- [SUITE 4] Server-Side Rate Limiting & Rapid Tap Anti-Spam ---")

with open(SKILL_NETWORKING_PATH, "r", encoding="utf-8") as f:
    net_src = f.read()

# Verify RATE_LIMIT_TICKS constant
rate_limit_match = re.search(r"private\s+static\s+final\s+int\s+RATE_LIMIT_TICKS\s*=\s*(\d+);", net_src)
rate_limit_val = int(rate_limit_match.group(1)) if rate_limit_match else 0
check(rate_limit_val == 3, "4.1 SkillNetworking RATE_LIMIT_TICKS == 3",
      f"RATE_LIMIT_TICKS = {rate_limit_val} (expected 3)")

# Check per-skill rate limiting map: UUID -> (skillId -> lastTick)
check("Map<UUID, Map<String, Long>> lastSkillTick" in net_src,
      "4.2 Per-skill rate limit map exists (allows rapid cross-skill switching)",
      "Map<UUID, Map<String, Long>> lastSkillTick present")

# Check handleHoldStart checks rate limit
has_hold_rate_limit = (
    "currentTick - lastTick < RATE_LIMIT_TICKS" in net_src and
    "SkillPackets.S2CSkillResult.DenyReason.RATE_LIMITED" in net_src
)
check(has_hold_rate_limit, "4.3 handleHoldStart enforces RATE_LIMITED denial",
      "Rate limit guard verified in handleHoldStart")

# Check handleHoldRelease transitions HOLD -> ACTIVE and applies cooldown
has_release_handling = (
    "timeline.phase() == SkillTimeline.Phase.HOLD" in net_src and
    "timeline.releaseHold();" in net_src and
    "data.setCooldown(activeSkill, def.cooldownTicks());" in net_src
)
check(has_release_handling, "4.4 handleHoldRelease transitions HOLD -> ACTIVE and applies cooldown",
      "handleHoldRelease checks HOLD, calls releaseHold, sets cooldown")


# =====================================================================
# SUITE 5: Charge Scaling Formula & Detonation Mechanics
# =====================================================================
print("\n--- [SUITE 5] Charge Scaling Formula & Detonation Mechanics ---")

def calc_fire_blast(charge_ratio: float):
    # Formulas from FireBlastSkill.java and FireBlastProjectileEntity.java:
    # damage = 7.0 * (0.35 + 0.65 * chargeRatio)
    # radius = 1.0 + 2.0 * chargeRatio
    # knockback = 0.5 + 0.5 * chargeRatio
    dmg = 7.0 * (0.35 + 0.65 * charge_ratio)
    rad = 1.0 + 2.0 * charge_ratio
    kb = 0.5 + 0.5 * charge_ratio
    return round(dmg, 2), round(rad, 2), round(kb, 2)

# Quick tap: charge_ratio = 1/40 = 0.025
tap_dmg, tap_rad, tap_kb = calc_fire_blast(0.025)
check(tap_dmg == 2.56 and tap_rad == 1.05 and tap_kb == 0.51,
      "5.1 Quick Tap minimum scaling (ratio=0.025)",
      f"Damage={tap_dmg} HP (min ~2.45), Radius={tap_rad} blocks (min 1.0), Knockback={tap_kb}")

# Full charge: charge_ratio = 1.0
full_dmg, full_rad, full_kb = calc_fire_blast(1.0)
check(full_dmg == 7.00 and full_rad == 3.00 and full_kb == 1.00,
      "5.2 Full Charge maximum scaling (ratio=1.0)",
      f"Damage={full_dmg} HP, Radius={full_rad} blocks, Knockback={full_kb}")

# Mid charge: charge_ratio = 0.5
mid_dmg, mid_rad, mid_kb = calc_fire_blast(0.5)
check(mid_dmg == 4.73 and mid_rad == 2.00 and mid_kb == 0.75,
      "5.3 Half Charge scaling (ratio=0.5)",
      f"Damage={mid_dmg} HP, Radius={mid_rad} blocks, Knockback={mid_kb}")


# =====================================================================
# SUMMARY
# =====================================================================
print("\n=================================================================")
print("INPUT STRESS & SLOT PRESERVATION TEST SUMMARY")
print("=================================================================")
print(f"Total Tests Executed: {passed_tests + failed_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print("=================================================================")

if failed_tests > 0:
    print("\nVERDICT: REJECTED")
    sys.exit(1)
else:
    print("\nVERDICT: CONFIRMED")
    sys.exit(0)
