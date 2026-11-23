package com.avatarmod.elements.entity;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Validates Pilot Entity assets, Bedrock Geo models, animations, and localization bindings.
 */
class AvatarEntitiesTest {

    private static final Path ASSETS_DIR = Path.of("src/main/resources/assets/avatar_elements");

    @Test
    @DisplayName("Verify Shirshu and Vaatu model geometry files exist and have valid bones")
    void testEntityGeoModels() throws IOException {
        Path shirshuGeo = ASSETS_DIR.resolve("models/entity/shirshu.geo.json");
        Path vaatuGeo = ASSETS_DIR.resolve("models/entity/vaatu_spirit_titan.geo.json");

        assertTrue(Files.exists(shirshuGeo), "Shirshu geo model must exist at " + shirshuGeo);
        assertTrue(Files.exists(vaatuGeo), "Vaatu geo model must exist at " + vaatuGeo);

        JsonObject shirshuJson = JsonParser.parseString(Files.readString(shirshuGeo)).getAsJsonObject();
        assertTrue(shirshuJson.has("minecraft:geometry"), "Shirshu geo must have minecraft:geometry");
        var shirshuBones = shirshuJson.getAsJsonArray("minecraft:geometry").get(0).getAsJsonObject().getAsJsonArray("bones");
        assertTrue(shirshuBones.size() >= 20, "Shirshu must have at least 20 bones (found: " + shirshuBones.size() + ")");

        JsonObject vaatuJson = JsonParser.parseString(Files.readString(vaatuGeo)).getAsJsonObject();
        assertTrue(vaatuJson.has("minecraft:geometry"), "Vaatu geo must have minecraft:geometry");
        var vaatuBones = vaatuJson.getAsJsonArray("minecraft:geometry").get(0).getAsJsonObject().getAsJsonArray("bones");
        assertTrue(vaatuBones.size() >= 20, "Vaatu must have at least 20 bones (found: " + vaatuBones.size() + ")");
    }

    @Test
    @DisplayName("Verify Shirshu and Vaatu animation files exist and define core animations")
    void testEntityAnimations() throws IOException {
        Path shirshuAnim = ASSETS_DIR.resolve("animations/entity/shirshu.animation.json");
        Path vaatuAnim = ASSETS_DIR.resolve("animations/entity/vaatu_spirit_titan.animation.json");

        assertTrue(Files.exists(shirshuAnim), "Shirshu animations must exist at " + shirshuAnim);
        assertTrue(Files.exists(vaatuAnim), "Vaatu animations must exist at " + vaatuAnim);

        JsonObject shirshuJson = JsonParser.parseString(Files.readString(shirshuAnim)).getAsJsonObject();
        JsonObject sAnims = shirshuJson.getAsJsonObject("animations");
        assertTrue(sAnims.has("animation.shirshu.idle"), "Must contain animation.shirshu.idle");
        assertTrue(sAnims.has("animation.shirshu.walk"), "Must contain animation.shirshu.walk");

        JsonObject vaatuJson = JsonParser.parseString(Files.readString(vaatuAnim)).getAsJsonObject();
        JsonObject vAnims = vaatuJson.getAsJsonObject("animations");
        assertTrue(vAnims.has("animation.vaatu_spirit_titan.idle"), "Must contain animation.vaatu_spirit_titan.idle");
        assertTrue(vAnims.has("animation.vaatu_spirit_titan.energy_cannon"), "Must contain animation.vaatu_spirit_titan.energy_cannon");
    }

    @Test
    @DisplayName("Verify Entity textures and emissive glow layers exist")
    void testEntityTextures() {
        Path shirshuTexture = ASSETS_DIR.resolve("textures/entity/mobs/shirshu.png");
        Path vaatuTexture = ASSETS_DIR.resolve("textures/entity/boss/vaatu_spirit_titan.png");
        Path vaatuGlow = ASSETS_DIR.resolve("textures/entity/boss/vaatu_spirit_titan_glow.png");

        assertTrue(Files.exists(shirshuTexture), "Shirshu texture must exist: " + shirshuTexture);
        assertTrue(Files.exists(vaatuTexture), "Vaatu texture must exist: " + vaatuTexture);
        assertTrue(Files.exists(vaatuGlow), "Vaatu emissive glow texture must exist: " + vaatuGlow);
    }

    @ParameterizedTest(name = "Lang key {0} is registered in en_us.json")
    @ValueSource(strings = {
            "entity.avatar_elements.shirshu",
            "entity.avatar_elements.vaatu_spirit_titan",
            "item.avatar_elements.shirshu_spawn_egg",
            "item.avatar_elements.vaatu_spirit_titan_spawn_egg"
    })
    void testLocalizationKeys(String key) throws IOException {
        Path langFile = ASSETS_DIR.resolve("lang/en_us.json");
        assertTrue(Files.exists(langFile), "en_us.json must exist");

        JsonObject lang = JsonParser.parseString(Files.readString(langFile)).getAsJsonObject();
        assertTrue(lang.has(key), "Localization file must have key: " + key);
        assertFalse(lang.get(key).getAsString().isBlank(), "Value for " + key + " must not be empty");
    }
}
