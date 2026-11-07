package com.avatarmod.elements.client.orb;

import java.util.Map;
import java.util.Set;

/**
 * Opt-in registry for skills that display a charge orb.
 * A skill NOT listed here never gets an orb regardless of its phase.
 *
 * orbPhases defines during which timeline phases the orb is visible.
 * fire_jab: orb only during WINDUP (small burst — it's a jab, not a held charge).
 * fire_jet: orb during WINDUP + ACTIVE (held channel).
 * air_blast: same as fire_jet but air element.
 */
public final class OrbVisualConfig {

    public record Config(Set<String> orbPhases) {
        public boolean visible(String phase) {
            return orbPhases.contains(phase);
        }
    }

    private static final Map<String, Config> REGISTRY = Map.of(
        "avatar:fire_jab",  new Config(Set.of("WINDUP")),
        "avatar:fire_jet",  new Config(Set.of("WINDUP", "ACTIVE")),
        "avatar:air_blast", new Config(Set.of("WINDUP", "ACTIVE"))
    );

    /** Returns true if this skill+phase combination should show an orb. */
    public static boolean shouldShow(String skillId, String phase) {
        Config cfg = REGISTRY.get(skillId);
        return cfg != null && cfg.visible(phase);
    }

    /** Null-safe: returns null if the skill has no orb config. */
    public static Config get(String skillId) {
        return REGISTRY.get(skillId);
    }

    private OrbVisualConfig() {}
}
