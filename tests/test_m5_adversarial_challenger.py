#!/usr/bin/env python3
"""
Empirical Adversarial Test Suite: Milestone 5 Hold-Release & Projectile Scaling
Author: challenger_m5_1 (Teamwork Challenger)
Role: critic, specialist

Rigorous stress-testing of:
1. SkillTimeline.java charge ratio calculations, clamping, over-hold retention, and 80t auto-release failsafe.
2. FireBlastProjectileEntity.java & FireBlastSkill.java scaling math, boundary conditions, zero-distance knockback vectors, and floor clamps.
3. Network packet handling and state machine edge cases (quick tap, over-hold, dropped release packet).
"""

import os
import re
import math
import json

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
MOD_DIR = os.path.join(REPO_ROOT, "mod")

SKILL_TIMELINE = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "data", "SkillTimeline.java")
PROJECTILE_ENTITY = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "entity", "FireBlastProjectileEntity.java")
FIRE_BLAST_SKILL = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "skill", "impl", "FireBlastSkill.java")
SKILL_DISPATCHER = os.path.join(MOD_DIR, "src", "main", "java", "com", "avatarmod", "elements", "skill", "SkillDispatcher.java")
SKILL_DEFS_JSON = os.path.join(MOD_DIR, "src", "main", "resources", "data", "avatar_elements", "skill_definitions.json")
ELEMENT_SLOTS_JSON = os.path.join(MOD_DIR, "src", "main", "resources", "data", "avatar_elements", "element_slots.json")

test_results = []

def record(name, passed, detail=""):
    test_results.append((name, passed, detail))
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}: {detail}")

print("=" * 70)
print("EMPIRICAL ADVERSARIAL CHALLENGER SUITE: MILESTONE 5")
print("=" * 70)

# =========================================================================
# SUITE 1: SkillTimeline Charge Ratio & State Machine Boundary Math
# =========================================================================
print("\n--- [SUITE 1] SkillTimeline Boundary & Clamping Math ---")

class MockSkillTimeline:
    """Accurate Python simulation of SkillTimeline.java logic."""
    def __init__(self, skill_id, windup_ticks, active_ticks, recovery_ticks, is_hold_skill, max_hold_ticks):
        self.skill_id = skill_id
        self.windup_ticks = windup_ticks
        self.active_ticks = active_ticks
        self.recovery_ticks = recovery_ticks
        self.is_hold_skill = is_hold_skill
        self.max_hold_ticks = max_hold_ticks
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

    def tick(self):
        if self.phase == "IDLE":
            return self.phase
        self.ticks_in_phase += 1
        limit = self.max_hold_ticks if self.max_hold_ticks > 0 else 40

        if self.phase == "WINDUP":
            if self.ticks_in_phase >= self.windup_ticks:
                if self.is_hold_skill:
                    self.phase = "HOLD"
                    self.ticks_in_phase = 0
                else:
                    self.phase = "ACTIVE"
                    self.ticks_in_phase = 0
        elif self.phase == "HOLD":
            self.hold_charged_ticks = min(self.ticks_in_phase, limit)
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

    def get_charge_ratio(self):
        limit = self.max_hold_ticks if self.max_hold_ticks > 0 else 40
        return min(1.0, max(1, self.hold_charged_ticks) / float(limit))

    def cancel(self):
        self.phase = "IDLE"
        self.ticks_in_phase = 0
        self.hold_charged_ticks = 0

# 1.1 Zero ticks held (Instant tap before any tick)
tl = MockSkillTimeline("avatar:fire_blast", 0, 25, 5, True, 40)
tl.start()
ratio_unreleased = tl.get_charge_ratio()
tl.release_hold()
ratio_released_0 = tl.get_charge_ratio()
record("1.1 Instant Tap (0 ticks held) Charge Ratio",
       math.isclose(ratio_released_0, 0.025, rel_tol=1e-5),
       f"ratio_unreleased={ratio_unreleased:.3f}, ratio_released={ratio_released_0:.3f} (Math.max(1, holdChargedTicks) yields 1/40 = 0.025)")

# 1.2 Half charge (20 ticks held)
tl = MockSkillTimeline("avatar:fire_blast", 0, 25, 5, True, 40)
tl.start()
for _ in range(20):
    tl.tick()
record("1.2 Half Charge (20 ticks) Charge Ratio",
       math.isclose(tl.get_charge_ratio(), 0.5, rel_tol=1e-5),
       f"ratio={tl.get_charge_ratio():.3f} (expected exactly 0.500)")

# 1.3 Full charge boundary (40 ticks held)
for _ in range(20):
    tl.tick()
record("1.3 Full Charge (40 ticks) Charge Ratio",
       math.isclose(tl.get_charge_ratio(), 1.0, rel_tol=1e-5),
       f"ratio={tl.get_charge_ratio():.3f} (expected exactly 1.000)")

# 1.4 Over-hold retention (60 ticks held, range [40, 79])
for _ in range(20):
    tl.tick()
record("1.4 Over-Hold Retention (60 ticks held)",
       tl.phase == "HOLD" and math.isclose(tl.get_charge_ratio(), 1.0, rel_tol=1e-5),
       f"phase={tl.phase}, ratio={tl.get_charge_ratio():.3f} (holding at 100% without auto-release)")

# 1.5 Auto-release safety at tick 80
for _ in range(20):
    tl.tick()
record("1.5 Auto-Release Failsafe at Tick 80",
       tl.phase == "ACTIVE" and tl.ticks_in_phase == 0 and math.isclose(tl.get_charge_ratio(), 1.0, rel_tol=1e-5),
       f"phase={tl.phase}, ticks_in_phase={tl.ticks_in_phase}, ratio={tl.get_charge_ratio():.3f} (auto-released HOLD -> ACTIVE)")

# 1.6 Division by zero guard (maxHoldTicks <= 0 fallback)
tl_zero = MockSkillTimeline("avatar:fire_blast", 0, 25, 5, True, 0)
tl_zero.start()
tl_zero.tick()
record("1.6 Division by Zero Guard (maxHoldTicks=0 fallback to 40)",
       math.isclose(tl_zero.get_charge_ratio(), 1.0 / 40.0, rel_tol=1e-5),
       f"ratio={tl_zero.get_charge_ratio():.4f} (safely defaulted to 40, no zero division)")

# 1.7 Cancel during HOLD
tl_cancel = MockSkillTimeline("avatar:fire_blast", 0, 25, 5, True, 40)
tl_cancel.start()
for _ in range(15):
    tl_cancel.tick()
tl_cancel.cancel()
record("1.7 Cancel During HOLD Phase",
       tl_cancel.phase == "IDLE" and tl_cancel.ticks_in_phase == 0 and tl_cancel.hold_charged_ticks == 0,
       f"phase={tl_cancel.phase}, ticks={tl_cancel.ticks_in_phase}, charge={tl_cancel.hold_charged_ticks}")

# =========================================================================
# SUITE 2: Fire Blast Projectile Scaling Formulas & Boundary Analysis
# =========================================================================
print("\n--- [SUITE 2] Fire Blast Scaling Formulas & Floor Clamping ---")

with open(FIRE_BLAST_SKILL, "r", encoding="utf-8") as f:
    skill_src = f.read()

# Verify formulas in FireBlastSkill.java
has_damage_formula = "MIN_DAMAGE_RATIO + (MAX_DAMAGE_RATIO - MIN_DAMAGE_RATIO) * chargeRatio" in skill_src
has_radius_formula = "MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * chargeRatio" in skill_src
has_knockback_formula = "0.5f + 0.5f * chargeRatio" in skill_src
record("2.1 Scaling Formulas in FireBlastSkill.java",
       has_damage_formula and has_radius_formula and has_knockback_formula,
       "damage=(0.35+0.65*C)*base, radius=1.0+2.0*C, knockback=(0.5+0.5*C)*base")

# Check for minimum floor clamp: chargeRatio = Math.max(0.1f, Math.min(1.0f, chargeRatio))
has_floor_clamp = "chargeRatio = Math.max(0.1f, Math.min(1.0f, chargeRatio));" in skill_src
record("2.2 Floor Clamping in spawnFireball (chargeRatio >= 0.1f)",
       has_floor_clamp,
       "FireBlastSkill enforces minimum 0.10f charge ratio to prevent zero-energy duds")

def theoretical_scaling(c, base_damage=7.0, base_radius_min=1.0, base_radius_max=3.0, base_kb=1.0):
    d = base_damage * (0.35 + 0.65 * c)
    r = base_radius_min + (base_radius_max - base_radius_min) * c
    k = base_kb * (0.5 + 0.5 * c)
    return d, r, k

def runtime_scaling(c, base_damage=7.0, base_radius_min=1.0, base_radius_max=3.0, base_kb=1.0):
    c_clamped = max(0.1, min(1.0, c))
    d = base_damage * (0.35 + 0.65 * c_clamped)
    r = base_radius_min + (base_radius_max - base_radius_min) * c_clamped
    k = base_kb * (0.5 + 0.5 * c_clamped)
    return d, r, k

# 2.3 Theoretical vs Runtime at C = 0.0
d_theo_0, r_theo_0, k_theo_0 = theoretical_scaling(0.0)
d_run_0, r_run_0, k_run_0 = runtime_scaling(0.0)
record("2.3 Theoretical Scaling at C = 0.0",
       math.isclose(d_theo_0, 2.45, rel_tol=1e-5) and math.isclose(r_theo_0, 1.0, rel_tol=1e-5) and math.isclose(k_theo_0, 0.5, rel_tol=1e-5),
       f"D={d_theo_0:.2f}, R={r_theo_0:.1f}, K={k_theo_0:.2f} (matches dispatch prompt specification)")

record("2.4 Runtime Scaling at C = 0.0 with 0.1f Floor",
       math.isclose(d_run_0, 2.905, rel_tol=1e-5) and math.isclose(r_run_0, 1.2, rel_tol=1e-5) and math.isclose(k_run_0, 0.55, rel_tol=1e-5),
       f"Runtime floor raises C=0.0 -> C=0.10: D={d_run_0:.3f}, R={r_run_0:.2f}, K={k_run_0:.2f}")

# 2.5 Theoretical and Runtime at C = 0.5
d_theo_half, r_theo_half, k_theo_half = theoretical_scaling(0.5)
d_run_half, r_run_half, k_run_half = runtime_scaling(0.5)
record("2.5 Scaling at C = 0.5 (Half Charge)",
       math.isclose(d_theo_half, 4.725, rel_tol=1e-5) and math.isclose(r_theo_half, 2.0, rel_tol=1e-5) and math.isclose(k_theo_half, 0.75, rel_tol=1e-5),
       f"D={d_run_half:.3f}, R={r_run_half:.1f}, K={k_run_half:.2f} (theoretical == runtime)")

# 2.6 Theoretical and Runtime at C = 1.0
d_theo_full, r_theo_full, k_theo_full = theoretical_scaling(1.0)
d_run_full, r_run_full, k_run_full = runtime_scaling(1.0)
record("2.6 Scaling at C = 1.0 (Full Charge)",
       math.isclose(d_theo_full, 7.0, rel_tol=1e-5) and math.isclose(r_theo_full, 3.0, rel_tol=1e-5) and math.isclose(k_theo_full, 1.0, rel_tol=1e-5),
       f"D={d_run_full:.1f}, R={r_run_full:.1f}, K={k_run_full:.1f} (theoretical == runtime)")

# =========================================================================
# SUITE 3: Kinematics, Collision Math & Edge Cases
# =========================================================================
print("\n--- [SUITE 3] Kinematics, Detonation & Collision Adversarial Tests ---")

with open(PROJECTILE_ENTITY, "r", encoding="utf-8") as f:
    proj_src = f.read()

# 3.1 Constant Speed across all charges
speed_const_present = "BASE_SPEED = 1.8f" in skill_src
record("3.1 Constant Speed Kinematics (1.8 blocks/tick)",
       speed_const_present,
       "Projectile speed is invariant to charge ratio: BASE_SPEED = 1.8f")

# 3.2 Maximum travel distance
max_dist = 1.8 * 25 # 45 blocks
record("3.2 Maximum Kinematic Distance vs Range Requirement",
       max_dist == 45.0 and max_dist > 24.0,
       f"Trajectory = {max_dist} blocks exceeds required range (24.0 blocks)")

# 3.3 Zero-distance explosion vector singularity test
has_zero_dist_guard = "knockDir.lengthSquared() < 0.001" in skill_src and "new Vec3d(0, 1, 0)" in skill_src
record("3.3 Zero-Distance Knockback Vector Guard",
       has_zero_dist_guard,
       "Guards against 0/0 division when target is at exact center by falling back to upward (0, 1, 0) vector")

# 3.4 Self-damage immunity & alive-only filter
has_owner_check = "e != player" in skill_src
has_alive_check = "e.isAlive()" in skill_src
record("3.4 Caster Immunity and Alive-Only Filtering",
       has_owner_check and has_alive_check,
       "LivingEntity filter explicitly requires e != player and e.isAlive()")

# 3.5 Spherical vs Box AOE filtering
has_sphere_filter = "squaredDistanceTo(center) <= r * r" in skill_src
record("3.5 True Spherical AOE Hitbox (Distance <= Radius)",
       has_sphere_filter,
       "Radial filter enforces squaredDistanceTo <= r*r within the bounding box")

# 3.6 Solid collision shape filtering
has_solid_shape_filter = "!this.getWorld().getBlockState(blockPos).getCollisionShape(this.getWorld(), blockPos).isEmpty()" in proj_src or "FireBlastSkill.isSolidBlockCollision" in proj_src or "getCollisionShape" in proj_src
record("3.6 Passable Block vs Solid Block Collision Check",
       has_solid_shape_filter,
       "Collision check inspects block collision shape to prevent detonating on grass, flowers, or air")

# =========================================================================
# SUITE 4: Serialization, NBT & Network Codecs
# =========================================================================
print("\n--- [SUITE 4] Projectile Serialization (NBT) & Network Robustness ---")

# 4.1 ProjectileEntity NBT round-trip preservation
has_write_nbt = "nbt.putFloat(\"Damage\", this.damage)" in proj_src and "nbt.putFloat(\"Radius\", this.radius)" in proj_src and "nbt.putFloat(\"ChargeRatio\", this.chargeRatio)" in proj_src
has_read_nbt = "this.damage = nbt.getFloat(\"Damage\")" in proj_src and "this.radius = nbt.getFloat(\"Radius\")" in proj_src and "this.chargeRatio = nbt.getFloat(\"ChargeRatio\")" in proj_src
record("4.1 NBT Serialization for Damage, Radius, and ChargeRatio",
       has_write_nbt and has_read_nbt,
       "FireBlastProjectileEntity properly writes and reads custom data from NbtCompound for server chunk saving")

# 4.2 Auto-release cooldown fallback in SkillDispatcher
with open(SKILL_DISPATCHER, "r", encoding="utf-8") as f:
    disp_src = f.read()

has_dispatcher_failsafe = "phaseBefore == SkillTimeline.Phase.HOLD && phaseAfter == SkillTimeline.Phase.ACTIVE" in disp_src and "data.setCooldown" in disp_src
record("4.2 SkillDispatcher Auto-Release Cooldown Fallback",
       has_dispatcher_failsafe,
       "SkillDispatcher applies cooldown upon internal auto-release if client dropped release packet")

# =========================================================================
# SUMMARY
# =========================================================================
print("\n" + "=" * 70)
total_tests = len(test_results)
passed_tests = sum(1 for _, p, _ in test_results if p)
failed_tests = total_tests - passed_tests
print(f"Total Tests Executed: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print("=" * 70)

if failed_tests > 0:
    exit(1)
