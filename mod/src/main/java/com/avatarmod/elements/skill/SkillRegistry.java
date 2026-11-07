package com.avatarmod.elements.skill;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/** In-memory registry of skill definitions loaded from JSON at mod init. */
public final class SkillRegistry {

    private static final Map<String, SkillDefinition> SKILLS = new LinkedHashMap<>();

    public static void populate() {
        SkillConfigLoader.load().forEach(SkillRegistry::register);
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
