package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Air Staff 3-hit combo:
 *   Step 1 — quick forward strike (range 2.0, dmg 3.0, knockback 0.4)
 *   Step 2 — wider sweep (range 2.5, dmg 4.5, knockback 0.6)
 *   Step 3 — heavy upward slam (range 3.0, dmg 7.0, knockback 1.5 upward)
 *
 * Requires holding the air_staff item. Combo resets after comboWindowTicks gap.
 */
public final class AirStaffAttackSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        int step = PlayerBendingData.get(player).getAirStaffComboStep();
        executeComboStep(player, def, step);
    }

    private static void executeComboStep(ServerPlayerEntity player, SkillDefinition def, int step) {
        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);

        float damage;
        double range;
        float knockback;
        boolean upwardSlam = false;

        switch (step) {
            case 2 -> { damage = 4.5f; range = 2.5; knockback = 0.6f; }
            case 3 -> { damage = 7.0f; range = 3.0; knockback = 1.5f; upwardSlam = true; }
            default -> { damage = def.damage(); range = def.range(); knockback = def.knockback(); }
        }

        Vec3d center = origin.add(look.multiply(range * 0.6));
        Box box = Box.of(center, (range + 1.0) * 2, (range + 1.0) * 2, (range + 1.0) * 2);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> {
                    if (e == player || !e.isAlive()) return false;
                    Vec3d targetCenter = e.getBoundingBox().getCenter();
                    double distSq = origin.squaredDistanceTo(targetCenter);
                    if (distSq <= 1.44) return true;
                    if (distSq > (range + 0.5) * (range + 0.5)) return false;
                    Vec3d toTarget = targetCenter.subtract(origin);
                    return toTarget.normalize().dotProduct(look) > 0.0;
                }
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, damage);
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            double vy = upwardSlam ? knockback * 0.9 : 0.1 + knockback * 0.2;
            target.addVelocity(
                    knockDir.x * knockback * (upwardSlam ? 0.3 : 1.0),
                    vy,
                    knockDir.z * knockback * (upwardSlam ? 0.3 : 1.0)
            );
            target.velocityModified = true;
        }

        // Multi-stage authentic Baguazhang staff VFX
        if (step == 1) {
            world.spawnParticles(AvatarParticles.GUST_CURL,
                    center.x, center.y, center.z, 8, range * 0.25, range * 0.25, range * 0.25, 0.05);
            world.spawnParticles(ParticleTypes.CLOUD,
                    center.x, center.y, center.z, 4, range * 0.2, range * 0.2, range * 0.2, 0.02);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 0.9f, 1.3f);
        } else if (step == 2) {
            world.spawnParticles(AvatarParticles.GUST_CURL,
                    center.x, center.y, center.z, 14, range * 0.35, range * 0.35, range * 0.35, 0.06);
            world.spawnParticles(AvatarParticles.SMOKE_PUFF,
                    center.x, center.y, center.z, 6, range * 0.25, range * 0.25, range * 0.25, 0.03);
            world.spawnParticles(ParticleTypes.CLOUD,
                    center.x, center.y, center.z, 8, range * 0.3, range * 0.3, range * 0.3, 0.03);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_BREEZE_SHOOT, SoundCategory.PLAYERS, 1.0f, 1.2f);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 0.8f, 1.1f);
        } else {
            // Step 3: Upward slam cyclone burst
            world.spawnParticles(AvatarParticles.GUST_CURL,
                    center.x, center.y, center.z, 20, range * 0.4, range * 0.4, range * 0.4, 0.08);
            world.spawnParticles(ParticleTypes.CLOUD,
                    center.x, center.y, center.z, 12, range * 0.35, range * 0.35, range * 0.35, 0.04);
            world.spawnParticles(ParticleTypes.SWEEP_ATTACK,
                    center.x, center.y + 0.3, center.z, 3, range * 0.3, 0.2, range * 0.3, 0.0);
            world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                    center.x, center.y + 0.5, center.z, 1, 0.0, 0.0, 0.0, 0.0);

            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_WIND_CHARGE_WIND_BURST.value(), SoundCategory.PLAYERS, 1.5f, 1.1f);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_STRONG, SoundCategory.PLAYERS, 1.2f, 0.8f);
        }
    }

    private AirStaffAttackSkill() {}
}
