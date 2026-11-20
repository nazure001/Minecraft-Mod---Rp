package com.avatarmod.elements.skill;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Validates PAL (Player Animation Library) Bedrock clips for all 14 skills and 4 canonical weapons:
 * 1. Strict 6-bone biped rig ("body", "head", "right_arm", "left_arm", "right_leg", "left_leg").
 * 2. Explicit prohibition of the "torso" bone.
 * 3. Zero-Snap Contract: rotation and position at timestamp 0.0s match the end keyframe exactly.
 * 4. Dual key registration in the animations block: "animation.avatar_elements.<name>" and "<name>".
 * 5. Strict synchronization between SkillTimeline tick durations and animation_length seconds.
 */
class PalAnimationContractTest {

    private static final Set<String> ALLOWED_BONES = Set.of(
            "body", "head", "right_arm", "left_arm", "right_leg", "left_leg");

    private static final Path ANIMATION_DIR = Path.of(
            "src/client/resources/assets/avatar_elements/player_animations");

    @ParameterizedTest(name = "Skill animation {0} matches duration {1}s and rig contract")
    @CsvSource({
            "fire_jab, 0.45",
            "fire_blast, 1.50",
            "flame_sweep, 0.85",
            "fire_jet, 1.05",
            "fire_guard, 3.35",
            "air_palm, 0.40",
            "air_blast, 0.65",
            "air_staff_attack, 0.30",
            "water_whip, 0.40",
            "water_jet, 1.90",
            "earth_boulder, 1.45",
            "earth_pillar, 0.75",
            "boulder_launch, 1.55",
            "air_vortex, 2.50",
            "air_scooter, 1.00"
    })
    void testSkillAnimationContract(String animName, double expectedDuration) throws IOException {
        verifyAnimationFile(animName, expectedDuration);
    }

    @ParameterizedTest(name = "Canonical weapon animation {0} matches duration {1}s and rig contract")
    @CsvSource({
            "dual_swords, 0.60",
            "war_fan, 0.55",
            "earth_hammer, 0.85",
            "water_spear, 0.60"
    })
    void testCanonicalWeaponAnimationContract(String weaponName, double expectedDuration) throws IOException {
        verifyAnimationFile(weaponName, expectedDuration);
    }

    @Test
    @DisplayName("Verify all 14 skills in skill_definitions.json align with their PAL animation durations")
    void testAllSkillsInDefinitionsAlignWithAnimationDurations() throws IOException {
        Path skillDefPath = Path.of("src/main/resources/data/avatar_elements/skill_definitions.json");
        assertTrue(Files.exists(skillDefPath), "skill_definitions.json must exist");

        JsonObject root = JsonParser.parseString(Files.readString(skillDefPath)).getAsJsonObject();
        JsonArray skills = root.getAsJsonArray("skills");
        assertNotNull(skills);

        for (JsonElement elem : skills) {
            JsonObject skill = elem.getAsJsonObject();
            String id = skill.get("id").getAsString();
            String animName = id.replace("avatar:", "");

            int windup = skill.get("windupTicks").getAsInt();
            int active = skill.get("activeTicks").getAsInt();
            int recovery = skill.get("recoveryTicks").getAsInt();
            double expectedDuration = (windup + active + recovery) * 0.05;

            verifyAnimationFile(animName, expectedDuration);
        }
    }

    private void verifyAnimationFile(String animName, double expectedDuration) throws IOException {
        Path assetPath = ANIMATION_DIR.resolve(animName + ".animation.json");
        assertTrue(Files.exists(assetPath), "Animation file must exist: " + assetPath);

        JsonObject root = JsonParser.parseString(Files.readString(assetPath)).getAsJsonObject();
        assertEquals("1.8.0", root.get("format_version").getAsString(), "format_version must be 1.8.0");

        JsonObject animations = root.getAsJsonObject("animations");
        assertNotNull(animations, "animations block must exist");

        // Dual key contract: declare both "animation.avatar_elements.<name>" and "<name>"
        String fullKey = "animation.avatar_elements." + animName;
        assertTrue(animations.has(fullKey), "animations must declare full key: " + fullKey);
        assertTrue(animations.has(animName), "animations must declare short key: " + animName);

        JsonObject clip = animations.getAsJsonObject(fullKey);
        assertNotNull(clip);

        assertEquals(expectedDuration, clip.get("animation_length").getAsDouble(), 0.0001,
                animName + " duration mismatch");

        JsonObject bones = clip.getAsJsonObject("bones");
        assertNotNull(bones, animName + " missing bones");

        // Strict 6-bone biped rig
        assertEquals(ALLOWED_BONES, bones.keySet(),
                animName + " must contain exactly the 6 player biped bones");
        assertFalse(bones.has("torso"), animName + " must NEVER use the forbidden 'torso' bone");

        String durFmt2 = String.format(Locale.ROOT, "%.2f", expectedDuration);
        String durFmtG = String.format(Locale.ROOT, "%g", expectedDuration);

        // Zero-Snap Contract verification across all animated channels
        for (String boneName : bones.keySet()) {
            JsonObject bone = bones.getAsJsonObject(boneName);
            for (String channel : Set.of("rotation", "position")) {
                if (!bone.has(channel)) continue;
                JsonObject keyframes = bone.getAsJsonObject(channel);

                assertTrue(keyframes.has("0.0"),
                        animName + " " + boneName + " " + channel + " missing 0.0s keyframe");

                String endKey = null;
                if (keyframes.has(durFmt2)) {
                    endKey = durFmt2;
                } else if (keyframes.has(durFmtG)) {
                    endKey = durFmtG;
                }

                assertNotNull(endKey, animName + " " + boneName + " " + channel
                        + " missing end keyframe for duration " + expectedDuration);

                JsonArray startVal = keyframes.getAsJsonArray("0.0");
                JsonArray endVal = keyframes.getAsJsonArray(endKey);

                assertEquals(startVal, endVal,
                        animName + " " + boneName + " " + channel
                                + " Zero-Snap violation: start " + startVal + " != end " + endVal);
            }
        }
    }
}
