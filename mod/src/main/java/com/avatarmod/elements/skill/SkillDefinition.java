package com.avatarmod.elements.skill;

/**
 * Immutable data for one skill, sourced from CONTENT_SPEC.md.
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
        int comboWindowTicks,
        CastType castType,
        int maxChargeTicks
) {
    public enum Element { FIRE, WATER, EARTH, AIR }
    public enum HitboxShape { SPHERE, ARC, LINE, CONE }
    public enum CastType { INSTANT, HOLD_RELEASE, CHANNEL, TOGGLE }

    public SkillDefinition(
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
        this(id, element, masteryRequired, chiCost, chiPerTick, cooldownTicks, windupTicks,
                activeTicks, recoveryTicks, damage, range, knockback, hitboxShape, cancelOnHit,
                comboWindowTicks, CastType.INSTANT, 0);
    }

    public boolean isHoldRelease() {
        return castType == CastType.HOLD_RELEASE;
    }
}
