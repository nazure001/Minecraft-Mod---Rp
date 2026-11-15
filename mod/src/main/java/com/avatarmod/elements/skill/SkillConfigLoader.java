package com.avatarmod.elements.skill;

import com.avatarmod.elements.AvatarElementsMod;
import com.google.gson.JsonElement;
import com.google.gson.JsonIOException;
import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class SkillConfigLoader {
    private static final String RESOURCE_PATH = "/data/avatar_elements/skill_definitions.json";

    /**
     * Loads skill definitions. Checks config/ folder first (for user overrides),
     * falls back to the bundled resource only when the override cannot be read.
     * Invalid configuration is reported with its source and is not silently replaced.
     */
    public static List<SkillDefinition> load() {
        Path configFile = FabricLoader.getInstance().getConfigDir()
                .resolve("avatar_elements/skill_definitions.json");

        if (Files.exists(configFile)) {
            try (var reader = Files.newBufferedReader(configFile, StandardCharsets.UTF_8)) {
                return parseReader(reader, configFile.toString());
            } catch (IOException e) {
                AvatarElementsMod.LOGGER.error(
                        "[Avatar] Failed to read skill config {}; falling back to bundled resource",
                        configFile, e);
            }
        }

        try (InputStream is = SkillConfigLoader.class.getResourceAsStream(RESOURCE_PATH)) {
            if (is == null) {
                throw new IllegalStateException(
                        "Bundled skill_definitions.json not found at " + RESOURCE_PATH);
            }
            return parseReader(new InputStreamReader(is, StandardCharsets.UTF_8),
                    "bundled resource " + RESOURCE_PATH);
        } catch (IOException e) {
            throw new IllegalStateException("Failed to read bundled " + RESOURCE_PATH, e);
        }
    }

    private static List<SkillDefinition> parseReader(
            Reader reader, String source
    ) throws IOException {
        try {
            return parse(JsonParser.parseReader(reader), source);
        } catch (JsonIOException e) {
            if (e.getCause() instanceof IOException ioException) {
                throw ioException;
            }
            throw new IOException("Unable to read skill configuration from " + source, e);
        } catch (JsonParseException e) {
            AvatarElementsMod.LOGGER.error(
                    "[Avatar] Malformed skill configuration from {}: {}",
                    source, e.getMessage());
            throw new IllegalStateException(
                    "Malformed skill configuration from " + source + ": " + e.getMessage(), e);
        }
    }

    private static List<SkillDefinition> parse(JsonElement root, String source) {
        try {
            List<SkillDefinition> skills = SkillConfigParser.parseSkills(source, root);
            ElementSlotMap.validateSkillReferences(skills);
            AvatarElementsMod.LOGGER.info("[Avatar] Loaded {} skill definitions from {}",
                    skills.size(), source);
            return skills;
        } catch (IllegalArgumentException e) {
            AvatarElementsMod.LOGGER.error("[Avatar] Invalid skill configuration from {}: {}",
                    source, e.getMessage());
            throw new IllegalStateException(
                    "Invalid skill configuration from " + source + ": " + e.getMessage(), e);
        }
    }

    private SkillConfigLoader() {}
}
