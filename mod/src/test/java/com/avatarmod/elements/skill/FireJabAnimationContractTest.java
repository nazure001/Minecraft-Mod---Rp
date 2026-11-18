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
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FireJabAnimationContractTest {

    @Test
    void runtimePalClipUsesPlayerBonesAndReturnsToItsStartingPose() throws IOException {
        Path assetPath = Path.of(
                "src/client/resources/assets/avatar_elements/player_animations/fire_jab.animation.json");
        JsonObject animations = JsonParser.parseString(Files.readString(assetPath))
                .getAsJsonObject()
                .getAsJsonObject("animations");
        assertNotNull(animations);

        JsonObject clip = animations.getAsJsonObject("animation.avatar_elements.fire_jab");
        assertNotNull(clip);
        JsonObject bones = clip.getAsJsonObject("bones");

        assertEquals(0.45, clip.get("animation_length").getAsDouble(), 0.000001);
        assertEquals(Set.of("body", "head", "right_arm", "left_arm", "right_leg", "left_leg"),
                bones.keySet());
        assertFalse(bones.has("torso"));
        assertTrue(bones.getAsJsonObject("right_arm").getAsJsonObject("rotation").has("0.18"));
        assertTrue(bones.getAsJsonObject("right_arm").getAsJsonObject("position").has("0.18"));

        for (String boneName : bones.keySet()) {
            JsonObject bone = bones.getAsJsonObject(boneName);
            for (String channel : Set.of("rotation", "position")) {
                if (!bone.has(channel)) continue;
                JsonObject keyframes = bone.getAsJsonObject(channel);
                assertTrue(keyframes.has("0.0"), boneName + " " + channel + " start");
                assertTrue(keyframes.has("0.45"), boneName + " " + channel + " end");
                assertEquals(
                        keyframes.get("0.0"),
                        keyframes.get("0.45"),
                        boneName + " " + channel + " returns to its starting pose");
            }
        }
    }
}
