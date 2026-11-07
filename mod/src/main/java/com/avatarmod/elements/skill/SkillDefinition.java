package com.avatarmod.elements.skill;

/**
 * Immutable data for one skill, sourced from CONTENT_SPEC.md.
 * T1-9 will load these from JSON; for now they are hard-coded here.
 */
public record SkillDefinition(
        String id,
        Element element,
        int masteryRequired,
        int chiCost,
        int chiPerTick,
        int cooldownTicks,
        int windupTicks,
        int activeTicks,
        int recoveryTicks,
        float damage,
        float range,
        float knockback,
        HitboxShape hitboxShape,
        boolean cancelOnHit,
        int comboWindowTicks
) {
    public enum Element { FIRE, WATER, EARTH, AIR }
    public enum HitboxShape { SPHERE, ARC, LINE, CONE }
}
