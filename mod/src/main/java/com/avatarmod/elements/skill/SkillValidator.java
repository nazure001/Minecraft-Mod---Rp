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

        // Creative mode or sandbox bypass allows testing everything immediately
        boolean creativeTesting = player.isCreative() || data.isSandboxBypass();

        // 1.5. Chi Blocked check (Ty Lee / Equalist pressure point strikes)
        if (!creativeTesting && data.isChiBlocked()) {
            player.sendMessage(net.minecraft.text.Text.literal("§c[Avatar] Aliran Chi Anda tersumbat! Jurus tidak dapat dikeluarkan!"), true);
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    net.minecraft.sound.SoundEvents.BLOCK_RESPAWN_ANCHOR_DEPLETE.value(),
                    net.minecraft.sound.SoundCategory.PLAYERS, 1.2f, 0.6f);
            return ValidationResult.deny(SkillPackets.S2CSkillResult.DenyReason.NOT_ENOUGH_CHI, 0);
        }

        // 1.6. Element selection check
        if ("NONE".equals(data.getActiveElement())) {
            player.sendMessage(net.minecraft.text.Text.literal("§e[Avatar] Tekan [G] untuk memilih elemen atau jalur Anda terlebih dahulu!"), true);
            return ValidationResult.deny(SkillPackets.S2CSkillResult.DenyReason.NONE, 0);
        }

        // 2. Mastery check (bypassed in creative testing)
        if (!creativeTesting && data.getMasteryLevel() < def.masteryRequired()) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.WRONG_MASTERY, 0);
        }

        // 3. Cooldown check (bypassed in creative testing)
        int cd = data.getCooldown(skillId);
        if (!creativeTesting && cd > 0) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.COOLDOWN, cd);
        }

        // 4. Chi check (bypassed in creative testing)
        if (!creativeTesting && data.getChi() < def.chiCost()) {
            return ValidationResult.deny(
                    SkillPackets.S2CSkillResult.DenyReason.NOT_ENOUGH_CHI, 0);
        }

        // 5. Timeline: cannot start new skill while one is in WINDUP, HOLD, or ACTIVE
        if (data.hasActiveTimeline()) {
            var tl = data.getActiveTimeline();
            if (tl.phase() == com.avatarmod.elements.data.SkillTimeline.Phase.WINDUP
                    || tl.phase() == com.avatarmod.elements.data.SkillTimeline.Phase.HOLD
                    || tl.phase() == com.avatarmod.elements.data.SkillTimeline.Phase.ACTIVE) {
                return ValidationResult.deny(
                        SkillPackets.S2CSkillResult.DenyReason.COOLDOWN,
                        tl.ticksInPhase());
            }
        }

        // 6. Weapon requirement check
        if ("avatar:air_staff_attack".equals(skillId)) {
            boolean holdingStaff = player.getMainHandStack().isOf(com.avatarmod.elements.item.AvatarItems.AIR_STAFF)
                    || player.getOffHandStack().isOf(com.avatarmod.elements.item.AvatarItems.AIR_STAFF);
            if (!holdingStaff) {
                player.sendMessage(net.minecraft.text.Text.literal("§c[Avatar] Perlu memegang Air Staff untuk melakukan jurus ini!"), true);
                return ValidationResult.deny(SkillPackets.S2CSkillResult.DenyReason.NONE, 0);
            }
        }

        return ValidationResult.ok();
    }

    /**
     * Apply the effects of an accepted skill: spend chi, set cooldown, start timeline.
     */
    public static void apply(ServerPlayerEntity player, String skillId, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        boolean creativeTesting = player.isCreative() || data.isSandboxBypass();
        if (!creativeTesting) {
            data.trySpendChi(def.chiCost());
            data.setCooldown(skillId, def.cooldownTicks());
        }
        data.startTimeline(skillId, def.windupTicks(), def.activeTicks(), def.recoveryTicks(),
                def.isHoldRelease(), def.maxChargeTicks());
    }

    private SkillValidator() {}
}
