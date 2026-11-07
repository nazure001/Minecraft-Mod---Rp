package com.avatarmod.elements.skill;

import com.avatarmod.elements.AvatarElementsMod;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class SkillConfigLoader {

    private static final Gson GSON = new Gson();
    private static final String RESOURCE_PATH = "/data/avatar_elements/skill_definitions.json";

    /**
     * Loads skill definitions. Checks config/ folder first (for user overrides),
     * falls back to the bundled resource inside the jar.
     */
    public static List<SkillDefinition> load() {
        Path configFile = FabricLoader.getInstance().getConfigDir()
                .resolve("avatar_elements/skill_definitions.json");

        if (Files.exists(configFile)) {
            try (var reader = Files.newBufferedReader(configFile)) {
                AvatarElementsMod.LOGGER.info("[Avatar] Loading skill definitions from config: {}", configFile);
                return parse(GSON.fromJson(reader, JsonObject.class));
            } catch (IOException e) {
                AvatarElementsMod.LOGGER.error("[Avatar] Failed to read config skill_definitions.json, falling back to bundled", e);
            }
        }

        try (InputStream is = SkillConfigLoader.class.getResourceAsStream(RESOURCE_PATH)) {
            if (is == null) throw new IllegalStateException("Bundled skill_definitions.json not found at " + RESOURCE_PATH);
            AvatarElementsMod.LOGGER.info("[Avatar] Loading skill definitions from bundled resource");
            return parse(GSON.fromJson(new InputStreamReader(is), JsonObject.class));
        } catch (IOException e) {
            throw new RuntimeException("Failed to load bundled skill_definitions.json", e);
        }
    }

    private static List<SkillDefinition> parse(JsonObject root) {
        JsonArray arr = root.getAsJsonArray("skills");
        List<SkillDefinition> list = new ArrayList<>(arr.size());
        for (JsonElement el : arr) {
            JsonObject o = el.getAsJsonObject();
            list.add(new SkillDefinition(
                    o.get("id").getAsString(),
                    SkillDefinition.Element.valueOf(o.get("element").getAsString()),
                    o.get("masteryRequired").getAsInt(),
                    o.get("chiCost").getAsInt(),
                    o.get("chiPerTick").getAsInt(),
                    o.get("cooldownTicks").getAsInt(),
                    o.get("windupTicks").getAsInt(),
                    o.get("activeTicks").getAsInt(),
                    o.get("recoveryTicks").getAsInt(),
                    o.get("damage").getAsFloat(),
                    o.get("range").getAsFloat(),
                    o.has("knockback") ? o.get("knockback").getAsFloat() : 0f,
                    o.has("hitboxShape")
                            ? SkillDefinition.HitboxShape.valueOf(o.get("hitboxShape").getAsString())
                            : SkillDefinition.HitboxShape.SPHERE,
                    o.get("cancelOnHit").getAsBoolean(),
                    o.get("comboWindowTicks").getAsInt()
            ));
        }
        AvatarElementsMod.LOGGER.info("[Avatar] Loaded {} skill definitions", list.size());
        return list;
    }

    private SkillConfigLoader() {}
}
