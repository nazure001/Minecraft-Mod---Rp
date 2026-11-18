package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
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

        ServerWorld world = player.getServerWorld();
        int t = timeline.ticksInPhase();

        // Initial barrier activation whoosh & flash
        if (t == 1) {
            world.spawnParticles(AvatarParticles.FLAME_BURST,
                    player.getX(), player.getY() + 1.0, player.getZ(), 4, 0.4, 0.4, 0.4, 0.05);
            world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                    player.getX(), player.getY() + 1.0, player.getZ(), 1, 0.0, 0.0, 0.0, 0.0);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ITEM_FIRECHARGE_USE,
                    SoundCategory.PLAYERS, 1.2f, 0.8f);
        }

        // Orbiting flame shield ring every 2 ticks
        if (t % 2 == 0) {
            double angleOffset = t * 0.35;
            for (int i = 0; i < 8; i++) {
                double angle = (Math.PI * 2 * i) / 8 + angleOffset;
                double px = player.getX() + Math.cos(angle) * 1.5;
                double pz = player.getZ() + Math.sin(angle) * 1.5;
                world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                        px, player.getY() + 0.8 + (i % 2) * 0.4, pz, 2, 0.05, 0.1, 0.05, 0.02);
                world.spawnParticles(ParticleTypes.FLAME,
                        px, player.getY() + 0.8 + (i % 2) * 0.4, pz, 2, 0.05, 0.1, 0.05, 0.02);
                world.spawnParticles(AvatarParticles.EMBER,
                        px, player.getY() + 0.8 + (i % 2) * 0.4, pz, 1, 0.03, 0.05, 0.03, 0.01);
            }
        }
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

        ServerWorld world = player.getServerWorld();
        // Play layered block sound once per hit
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_SHIELD_BLOCK,
                SoundCategory.PLAYERS, 1.2f, 1.0f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 1.0f, 1.2f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.BLOCK_ANVIL_LAND,
                SoundCategory.PLAYERS, 0.6f, 1.8f);

        // Deflection sparks
        world.spawnParticles(AvatarParticles.SPARK,
                player.getX(), player.getY() + 1.2, player.getZ(), 16, 0.4, 0.4, 0.4, 0.1);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                player.getX(), player.getY() + 1.2, player.getZ(), 3, 0.2, 0.2, 0.2, 0.05);

        return true;
    }

    private FireGuardSkill() {}
}
