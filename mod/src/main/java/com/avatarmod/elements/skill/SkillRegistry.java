package com.avatarmod.elements.skill;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * In-memory registry of skill definitions.
 * Populated at mod init from hard-coded values (matches CONTENT_SPEC.md).
 * T1-9 will replace populate() with a JSON loader.
 */
public final class SkillRegistry {

    private static final Map<String, SkillDefinition> SKILLS = new LinkedHashMap<>();

    public static void populate() {
        register(new SkillDefinition(
                "avatar:fire_jab", SkillDefinition.Element.FIRE,
                0, 8, 0, 6, 2, 3, 4, 4.0f, 2.5f, false, 6));
        register(new SkillDefinition(
                "avatar:flame_sweep", SkillDefinition.Element.FIRE,
                0, 15, 0, 12, 3, 8, 6, 6.0f, 5.0f, false, 8));
        register(new SkillDefinition(
                "avatar:fire_jet", SkillDefinition.Element.FIRE,
                1, 25, 0, 30, 1, 1, 10, 0.0f, 0.0f, false, 0));
        register(new SkillDefinition(
                "avatar:fire_guard", SkillDefinition.Element.FIRE,
                0, 10, 2, 8, 2, 60, 5, 0.0f, 0.0f, false, 0));
        register(new SkillDefinition(
                "avatar:air_palm", SkillDefinition.Element.AIR,
                0, 6, 0, 5, 2, 2, 4, 2.0f, 3.0f, false, 6));
        register(new SkillDefinition(
                "avatar:air_blast", SkillDefinition.Element.AIR,
                0, 12, 0, 10, 3, 4, 6, 3.0f, 8.0f, false, 8));
    }

    private static void register(SkillDefinition def) {
        SKILLS.put(def.id(), def);
    }

    public static Optional<SkillDefinition> get(String skillId) {
        return Optional.ofNullable(SKILLS.get(skillId));
    }

    public static boolean exists(String skillId) {
        return SKILLS.containsKey(skillId);
    }

    private SkillRegistry() {}
}
