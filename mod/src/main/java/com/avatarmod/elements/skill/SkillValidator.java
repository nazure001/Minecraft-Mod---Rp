package com.avatarmod.elements.skill;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.network.SkillPackets;
import net.minecraft.server.network.ServerPlayerEntity;

/**
 * Server-side validation for skill use requests.
 * All gameplay rules live here; SkillNetworking delegates to this class.
 */
public final class SkillValidator {

    public record ValidationResult(
            boolean allowed,
            SkillPackets.S2CSkillResult.DenyReason denyReason,
            int cooldownTicks
    ) {
        public static ValidationResult ok() {
            return new ValidationResult(true, SkillPackets.S2CSkillResult.DenyReason.NONE, 0);
        }
        public static ValidationResult deny(SkillPackets.S2CSkillResult.DenyReason reason, int cd) {
            return new ValidationResult(false, reason, cd);
        }
    }

    /**
     * Validates whether {@code player} may use {@code skillId} right now.
     * Does NOT mutate any state — callers apply the result.
     */
    public static ValidationResult validate(ServerPlayerEntity player, String skillId) {
        // 1. Skill must exist in registry
        var optDef = SkillRegistry.get(skillId);
        if (optDef.isEmpty()) {
            return ValidationResult.deny(SkillPackets.S2CSkillResult.DenyReason.NONE, 0);
        }
        SkillDefinition def = optDef.get();
        PlayerBendingData data = PlayerBendingData.get(player);

        // 2. Mastery check
        if (data.getMasteryLevel() < def.masteryRequired()) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.WRONG_MASTERY, 0);
        }

        // 3. Cooldown check
        int cd = data.getCooldown(skillId);
        if (cd > 0) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.COOLDOWN, cd);
        }

        // 4. Chi check
        if (data.getChi() < def.chiCost()) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.NOT_ENOUGH_CHI, 0);
        }

        // 5. Timeline: cannot start new skill while one is in WINDUP or ACTIVE
        if (data.hasActiveTimeline()) {
            var tl = data.getActiveTimeline();
            if (tl.phase() == com.avatarmod.elements.data.SkillTimeline.Phase.WINDUP
                    || tl.phase() == com.avatarmod.elements.data.SkillTimeline.Phase.ACTIVE) {
                return ValidationResult.deny(
                        SkillPackets.S2CSkillResult.DenyReason.COOLDOWN,
                        tl.ticksInPhase());
            }
        }

        return ValidationResult.ok();
    }

    /**
     * Apply the effects of an accepted skill: spend chi, set cooldown, start timeline.
     */
    public static void apply(ServerPlayerEntity player, String skillId, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        data.trySpendChi(def.chiCost());
        data.setCooldown(skillId, def.cooldownTicks());
        data.startTimeline(skillId, def.windupTicks(), def.activeTicks(), def.recoveryTicks());
    }

    private SkillValidator() {}
}
