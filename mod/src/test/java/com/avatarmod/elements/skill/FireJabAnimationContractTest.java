package com.avatarmod.elements.skill;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FireJabAnimationContractTest {

    @Test
    void palClipUsesPlayerBonesAndReturnsToItsStartingPose() throws IOException {
        Path assetPath = Path.of(
                "src/client/resources/assets/avatar_elements/player_animations/fire_jab_test.json");
        JsonObject clip = JsonParser.parseString(Files.readString(assetPath))
                .getAsJsonObject()
                .getAsJsonObject("animations")
                .getAsJsonObject("fire_jab_test");
        JsonObject bones = clip.getAsJsonObject("bones");

        assertEquals(0.45, clip.get("animation_length").getAsDouble(), 0.000001);
        assertEquals(Set.of("body", "head", "right_arm", "left_arm", "right_leg", "left_leg"),
                bones.keySet());
        assertFalse(bones.has("torso"));
        assertTrue(bones.getAsJsonObject("right_arm").getAsJsonObject("rotation").has("0.15"));

        for (String boneName : bones.keySet()) {
            JsonObject rotation = bones.getAsJsonObject(boneName).getAsJsonObject("rotation");
            assertEquals(rotation.get("0.00"), rotation.get("0.45"), boneName);
        }
    }
}
