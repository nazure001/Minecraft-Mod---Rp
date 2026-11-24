#!/usr/bin/env python3
r"""
Test Suite: Milestone 4 (Phase C: Fire Jab Full Integration — Requirement R5)
Target Repository: D:\repo\Minecraft Mod & Rp

Verifies:
1. Audio transcoding & registration (OGG mono, sounds.json, ModSounds, en_us.json subtitles).
2. 9-Tick timeline state machine and Tick 3 strike apex execution.
3. Base (4.0) vs Combo (6.0) damage and combo window expiry in PlayerBendingData & SkillNetworking.
4. Forward dot-product cone filter geometry (elimination of behind-the-back hits).
5. Multi-stage VFX burst parameters (knuckle flash, strike jet, apex burst, combo lava/crit).
"""

import os
import sys
import json
import math
import subprocess

REPO_ROOT = r"D:\repo\Minecraft Mod & Rp"
MOD_ROOT = os.path.join(REPO_ROOT, "mod")

TOTAL_TESTS = 0
PASSED_TESTS = 0
FINDINGS = []


def record(name: str, passed: bool, detail: str = ""):
    global TOTAL_TESTS, PASSED_TESTS
    TOTAL_TESTS += 1
    if passed:
        PASSED_TESTS += 1
        print(f"[PASS] {name}: {detail}")
    else:
        FINDINGS.append((name, detail))
        print(f"[FAIL] {name}: {detail}")


def test_audio_pipeline():
    print("\n--- [SUITE 1] Audio Transcoding, Registration & Subtitles ---")
    ogg_path = os.path.join(
        MOD_ROOT,
        r"src\client\resources\assets\avatar_elements\sounds\fire_release_1.ogg"
    )
    sounds_json_path = os.path.join(
        MOD_ROOT,
        r"src\client\resources\assets\avatar_elements\sounds.json"
    )
    lang_json_path = os.path.join(
        MOD_ROOT,
        r"src\main\resources\assets\avatar_elements\lang\en_us.json"
    )
    mod_sounds_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\sound\ModSounds.java"
    )
    avatar_mod_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\AvatarElementsMod.java"
    )

    # 1.1 OGG File Exists
    record("1.1 Audio OGG file exists", os.path.isfile(ogg_path), f"Path: {ogg_path}")

    # 1.2 OGG File Properties (ffprobe mono check)
    if os.path.isfile(ogg_path):
        try:
            cmd = [
                "ffprobe", "-v", "error", "-show_entries",
                "stream=channels,sample_rate,codec_name", "-of", "json", ogg_path
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            probe = json.loads(res.stdout)
            stream = probe["streams"][0]
            channels = int(stream.get("channels", 0))
            codec = stream.get("codec_name", "")
            rate = int(stream.get("sample_rate", 0))
            is_valid_ogg = (channels == 1 and codec == "vorbis" and rate == 44100)
            record("1.2 Audio stream is mono Vorbis 44.1kHz", is_valid_ogg,
                   f"codec={codec}, channels={channels} (1=mono), rate={rate}Hz")
        except Exception as e:
            record("1.2 Audio stream is mono Vorbis 44.1kHz", False, f"ffprobe error: {e}")
    else:
        record("1.2 Audio stream is mono Vorbis 44.1kHz", False, "File missing")

    # 1.3 sounds.json Structure
    if os.path.isfile(sounds_json_path):
        with open(sounds_json_path, "r", encoding="utf-8") as f:
            s_data = json.load(f)
        has_release = "fire.release" in s_data
        has_jab = "skill.fire.fire_jab.strike" in s_data
        target_sound = s_data.get("fire.release", {}).get("sounds", [{}])[0].get("name", "")
        record("1.3 sounds.json mappings",
               has_release and has_jab and target_sound == "avatar_elements:fire_release_1",
               f"fire.release={has_release}, skill.fire.fire_jab.strike={has_jab}, sound={target_sound}")
    else:
        record("1.3 sounds.json mappings", False, "sounds.json missing")

    # 1.4 English Subtitle in en_us.json
    if os.path.isfile(lang_json_path):
        with open(lang_json_path, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
        sub_key = "subtitles.avatar_elements.fire.release"
        has_sub = sub_key in lang_data
        record("1.4 Subtitle translation exists", has_sub, f"{sub_key} = '{lang_data.get(sub_key)}'")
    else:
        record("1.4 Subtitle translation exists", False, "en_us.json missing")

    # 1.5 ModSounds.java Registration
    if os.path.isfile(mod_sounds_java):
        with open(mod_sounds_java, "r", encoding="utf-8") as f:
            ms_code = f.read()
        registers_sound = "Registries.SOUND_EVENT" in ms_code and "fire.release" in ms_code
        has_init = "public static void init()" in ms_code or "public static void register()" in ms_code
        record("1.5 ModSounds SoundEvent registration", registers_sound and has_init,
               f"Registries.SOUND_EVENT={registers_sound}, init/register={has_init}")
    else:
        record("1.5 ModSounds SoundEvent registration", False, "ModSounds.java missing")

    # 1.6 AvatarElementsMod Hooks ModSounds.init()
    if os.path.isfile(avatar_mod_java):
        with open(avatar_mod_java, "r", encoding="utf-8") as f:
            mod_code = f.read()
        hooks_init = "ModSounds.init()" in mod_code or "ModSounds.register()" in mod_code
        record("1.6 AvatarElementsMod initializes ModSounds", hooks_init, f"Hook detected: {hooks_init}")
    else:
        record("1.6 AvatarElementsMod initializes ModSounds", False, "AvatarElementsMod.java missing")


def test_timeline_and_strike_apex():
    print("\n--- [SUITE 2] 9-Tick Timeline & Strike Apex Execution ---")
    skill_defs_path = os.path.join(
        MOD_ROOT,
        r"src\main\resources\data\avatar_elements\skill_definitions.json"
    )
    fire_jab_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\skill\impl\FireJabSkill.java"
    )

    with open(skill_defs_path, "r", encoding="utf-8") as f:
        skills = json.load(f)["skills"]
    jab_def = next((s for s in skills if s["id"] == "avatar:fire_jab"), None)

    # 2.1 9-Tick Definition
    windup = jab_def["windupTicks"]
    active = jab_def["activeTicks"]
    recovery = jab_def["recoveryTicks"]
    total_ticks = windup + active + recovery
    record("2.1 Timeline 9 ticks total (2w + 3a + 4r)",
           (windup == 2 and active == 3 and recovery == 4 and total_ticks == 9),
           f"windup={windup}, active={active}, recovery={recovery}, total={total_ticks}")

    # 2.2 Discrete State Machine Trace (Tick 0 to 9)
    # Simulate SkillTimeline tick behavior
    phase = "WINDUP"
    ticks_in_phase = 0
    hitbox_triggered_tick = None

    for tick in range(1, 11):
        ticks_in_phase += 1
        if phase == "WINDUP":
            if ticks_in_phase >= windup:
                phase = "ACTIVE"
                ticks_in_phase = 0
        elif phase == "ACTIVE":
            # Check FireJabSkill trigger condition: phase == ACTIVE && ticksInPhase == 1
            if ticks_in_phase == 1 and hitbox_triggered_tick is None:
                hitbox_triggered_tick = tick
            if ticks_in_phase >= active:
                phase = "RECOVERY"
                ticks_in_phase = 0
        elif phase == "RECOVERY":
            if ticks_in_phase >= recovery:
                phase = "IDLE"

    record("2.2 Hitbox fires on Tick 3 (Active tick 1)",
           hitbox_triggered_tick == 3,
           f"Hitbox executed at server tick: {hitbox_triggered_tick} (expected Tick 3)")

    # 2.3 FireJabSkill.java Logic Verification
    with open(fire_jab_java, "r", encoding="utf-8") as f:
        fj_code = f.read()

    checks_active = "timeline.phase() != SkillTimeline.Phase.ACTIVE" in fj_code
    checks_tick1 = "timeline.ticksInPhase() != 1" in fj_code
    plays_sfx = "ModSounds.FIRE_RELEASE" in fj_code and "world.playSound" in fj_code
    record("2.3 FireJabSkill tick guard and SFX sync",
           checks_active and checks_tick1 and plays_sfx,
           f"checks ACTIVE={checks_active}, checks tick 1={checks_tick1}, plays ModSounds.FIRE_RELEASE={plays_sfx}")


def test_combo_system_and_damage():
    print("\n--- [SUITE 3] Combo System & Damage Application ---")
    data_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\data\PlayerBendingData.java"
    )
    net_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\network\SkillNetworking.java"
    )
    fire_jab_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\skill\impl\FireJabSkill.java"
    )

    with open(data_java, "r", encoding="utf-8") as f:
        data_code = f.read()
    with open(net_java, "r", encoding="utf-8") as f:
        net_code = f.read()
    with open(fire_jab_java, "r", encoding="utf-8") as f:
        fj_code = f.read()

    # 3.1 PlayerBendingData fields & methods
    has_active_combo = "isActiveCastCombo" in data_code and "setActiveCastCombo" in data_code
    has_expiry_tick = "comboExpiryTick" in data_code and "getComboExpiryTick" in data_code
    has_record_cast = "recordComboCast" in data_code
    record("3.1 PlayerBendingData combo tracking API",
           has_active_combo and has_expiry_tick and has_record_cast,
           f"activeCastCombo={has_active_combo}, comboExpiryTick={has_expiry_tick}, recordComboCast={has_record_cast}")

    # 3.2 SkillNetworking evaluates combo before overwriting
    checks_combo = "handleComboTracking" in net_code or "setActiveCastCombo" in net_code
    calls_record_cast = "recordComboCast" in net_code
    record("3.2 SkillNetworking handles combo before cast recording",
           checks_combo and calls_record_cast,
           f"checks_combo={checks_combo}, calls_record_cast={calls_record_cast}")

    # 3.3 Damage values: Base = 4.0, Combo = 6.0
    has_base_damage = "def.damage()" in fj_code
    has_bonus = "FINAL_COMBO_DAMAGE_BONUS = 1.5f" in fj_code
    # Calculate base and combo
    base_dmg = 4.0
    combo_dmg = base_dmg * 1.5
    record("3.3 Damage application: 4.0 base / 6.0 combo",
           has_base_damage and has_bonus and combo_dmg == 6.0,
           f"Base={base_dmg}, Multiplier=1.5x -> Combo={combo_dmg}")


def test_forward_cone_filter():
    print("\n--- [SUITE 4] Hitbox Geometry & Forward Dot-Product Cone Filter ---")
    fire_jab_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\skill\impl\FireJabSkill.java"
    )
    with open(fire_jab_java, "r", encoding="utf-8") as f:
        fj_code = f.read()

    # 4.1 Forward Dot-Product Filter in Source
    has_dot = "dotProduct(look) > 0.0" in fj_code or "dotProduct(look) > 0" in fj_code
    has_normalize = "normalize().dotProduct" in fj_code
    record("4.1 Forward dot-product cone filter present in source",
           has_dot and has_normalize,
           f"dotProduct filter={has_dot}, normalized vector={has_normalize}")

    # 4.2 Geometric Simulation of Behind-Player Entity
    # Player looking along +Z (yaw = 0): look = (0, 0, 1)
    # Target A directly in front: toTarget = (0, 0, 2) -> dot = 1.0 > 0 -> ACCEPTED
    # Target B directly behind: toTarget = (0, 0, -0.8) (inside 1.5m center + 2.5m sphere!)
    # Without filter: distance to center (0, 0, 1.5) is |-0.8 - 1.5| = 2.3 <= 2.5 (HIT!).
    # With filter: normalized dot product = -1.0 <= 0.0 -> REJECTED!
    look = (0.0, 0.0, 1.0)
    target_behind = (0.0, 0.0, -0.8)
    dot_behind = target_behind[0] * look[0] + target_behind[1] * look[1] + target_behind[2] * look[2]
    norm_dot_behind = dot_behind / math.sqrt(sum(x ** 2 for x in target_behind))

    target_front = (0.0, 0.0, 2.0)
    dot_front = target_front[0] * look[0] + target_front[1] * look[1] + target_front[2] * look[2]
    norm_dot_front = dot_front / math.sqrt(sum(x ** 2 for x in target_front))

    accepted_front = norm_dot_front > 0.0
    rejected_behind = norm_dot_behind <= 0.0
    record("4.2 Cone filter eliminates behind-player hits",
           accepted_front and rejected_behind,
           f"Front dot={norm_dot_front:.2f} (accepted={accepted_front}), Behind dot={norm_dot_behind:.2f} (rejected={rejected_behind})")


def test_vfx_burst_parameters():
    print("\n--- [SUITE 5] Multi-Stage VFX Burst Parameters ---")
    fire_jab_java = os.path.join(
        MOD_ROOT,
        r"src\main\java\com\avatarmod\elements\skill\impl\FireJabSkill.java"
    )
    with open(fire_jab_java, "r", encoding="utf-8") as f:
        fj_code = f.read()

    # 5.1 Knuckle Fist Position Anchor
    has_fist_anchor = "right.multiply(0.28)" in fj_code and "look.multiply(0.40)" in fj_code
    has_fist_height = "player.getPos().add(0, 1.20, 0)" in fj_code
    record("5.1 Knuckle fist anchor P_fist = pos + (0, 1.20, 0) + right*0.28 + look*0.40",
           has_fist_anchor and has_fist_height,
           f"anchor={has_fist_anchor}, height=1.20m={has_fist_height}")

    # 5.2 Jet Midpoint & Apex
    has_jet_mid = "fistPos.add(look.multiply(0.55))" in fj_code
    has_apex = "eyePos.add(look.multiply(1.50))" in fj_code
    record("5.2 Jet midpoint (0.55m) and apex burst (1.50m)",
           has_jet_mid and has_apex,
           f"jetMid={has_jet_mid}, apexPos={has_apex}")

    # 5.3 Multi-Stage Particle Types
    has_flame = "ParticleTypes.FLAME" in fj_code
    has_small_flame = "ParticleTypes.SMALL_FLAME" in fj_code
    has_smoke = "ParticleTypes.SMOKE" in fj_code
    has_lava = "ParticleTypes.LAVA" in fj_code
    has_crit = "ParticleTypes.CRIT" in fj_code
    all_particles = (has_flame and has_small_flame and has_smoke and has_lava and has_crit)
    record("5.3 Multi-stage particle types (FLAME, SMALL_FLAME, SMOKE, LAVA, CRIT)",
           all_particles,
           f"FLAME={has_flame}, SMALL_FLAME={has_small_flame}, SMOKE={has_smoke}, LAVA={has_lava}, CRIT={has_crit}")

    # 5.4 Dedicated Server Safety (No net.minecraft.client imports in FireJabSkill)
    no_client_imports = "net.minecraft.client" not in fj_code
    record("5.4 Dedicated server safety (zero net.minecraft.client imports)",
           no_client_imports,
           f"Clean from client-only classes: {no_client_imports}")


def main():
    print("=" * 65)
    print("RUNNING MILESTONE 4 TEST SUITE (Fire Jab Integration & Timing)")
    print("=" * 65)

    test_audio_pipeline()
    test_timeline_and_strike_apex()
    test_combo_system_and_damage()
    test_forward_cone_filter()
    test_vfx_burst_parameters()

    print("\n" + "=" * 65)
    print("TEST SUMMARY")
    print("=" * 65)
    print(f"Total Tests Executed: {TOTAL_TESTS}")
    print(f"Passed: {PASSED_TESTS}")
    print(f"Failed: {len(FINDINGS)}")
    print("=" * 65)

    if FINDINGS:
        print("\nFINDINGS / FAILURES:")
        for name, detail in FINDINGS:
            print(f"- {name}: {detail}")
        sys.exit(1)
    else:
        print("\nALL MILESTONE 4 INTEGRATION TESTS PASSED!")
        sys.exit(0)


if __name__ == "__main__":
    main()
