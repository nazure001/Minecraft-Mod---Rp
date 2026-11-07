package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;

/**
 * Defensive stance — blocks all physical damage while ACTIVE.
 * Damage interception is registered separately via ServerLivingEntityEvents.ALLOW_DAMAGE
 * in AvatarServerEvents. This class handles VFX ticking only.
 */
public final class FireGuardSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        // Particle shield shimmer every 5 ticks
        if (timeline.ticksInPhase() % 5 != 0) return;

        ServerWorld world = player.getServerWorld();
        double x = player.getX(), y = player.getY() + 1.0, z = player.getZ();
        world.spawnParticles(ParticleTypes.FLAME,
                x, y, z, 4, 0.4, 0.5, 0.4, 0.01);
        world.spawnParticles(ParticleTypes.SMOKE,
                x, y, z, 2, 0.3, 0.4, 0.3, 0.005);
    }

    /**
     * Called from the ALLOW_DAMAGE event. Returns false to block damage.
     * Only blocks physical / projectile / player-attack damage while guard is ACTIVE.
     */
    public static boolean shouldBlockDamage(ServerPlayerEntity player, DamageSource source) {
        // Only block damage from entities (attacks, projectiles) — let env damage pass
        if (source.getAttacker() == null && source.getSource() == null) return false;
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (!timeline.isActive()) return false;
        if (!"avatar:fire_guard".equals(timeline.skillId())) return false;

        // Play block sound once per hit
        player.getServerWorld().playSound(null, player.getBlockPos(),
                SoundEvents.BLOCK_ANVIL_LAND,
                SoundCategory.PLAYERS, 0.4f, 1.8f);
        return true;
    }

    private FireGuardSkill() {}
}
