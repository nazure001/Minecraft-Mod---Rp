package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillTargeting;
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
 * Water Jet — Sustained channel/stream skill.
 * Continuously emits a focused high-pressure stream of water in the look direction.
 * Consumes chi per interval (1 chi per 3 ticks), deals 1.5 damage per hit interval,
 * and pushes targets away with directional knockback.
 */
public final class WaterJetSkill {

    public static final String ID = "avatar:water_jet";
    public static final int CHI_CONSUMPTION_INTERVAL = 3;
    public static final int CHI_PER_PULSE = 1;
    public static final int DAMAGE_INTERVAL = 3;
    public static final double STREAM_PADDING = 1.2;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();

        // 1. Chi sustain consumption — cancel stream if out of chi
        if (shouldConsumeChi(t)) {
            if (!data.trySpendChi(CHI_PER_PULSE)) {
                timeline.cancel();
                return;
            }
        }

        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getPos().add(0, player.getStandingEyeHeight() - 0.1, 0);
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();
        Vec3d end = origin.add(look.multiply(range));

        // 2. Hitbox check & damage tick
        if (shouldDealDamage(t)) {
            Box searchBounds = SkillTargeting.segmentBounds(origin, end, STREAM_PADDING);
            List<LivingEntity> targets = world.getEntitiesByClass(
                    LivingEntity.class, searchBounds,
                    e -> e != player && e.isAlive()
                            && SkillTargeting.intersectsSegment(origin, end, e.getBoundingBox(), STREAM_PADDING)
                            && SkillTargeting.hasLineOfSight(world, origin, e.getBoundingBox(), player)
            );

            DamageSource source = world.getDamageSources().playerAttack(player);
            for (LivingEntity target : targets) {
                target.damage(source, def.damage());

                // Directional push knockback along water jet stream
                Vec3d push = calculatePushVector(look, def.knockback());
                target.addVelocity(push.x, push.y, push.z);
                target.velocityModified = true;
            }
        }

        // 3. VFX: High-pressure water particles streaming forward
        spawnStreamParticles(world, origin, look, range);

        // 4. Looping rushing water SFX
        if (t % 10 == 1) {
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ITEM_BUCKET_EMPTY,
                    SoundCategory.PLAYERS, 0.7f, 1.3f);
        }
    }

    public static boolean shouldConsumeChi(int ticksInPhase) {
        return ticksInPhase > 0 && ticksInPhase % CHI_CONSUMPTION_INTERVAL == 0;
    }

    public static boolean shouldDealDamage(int ticksInPhase) {
        return ticksInPhase > 0 && ticksInPhase % DAMAGE_INTERVAL == 0;
    }

    public static Vec3d calculatePushVector(Vec3d look, double knockback) {
        return new Vec3d(
                look.x * knockback,
                0.1 + Math.max(0.0, look.y * knockback * 0.4),
                look.z * knockback
        );
    }

    public static int calculateTotalChiCost(int activeTicks) {
        int cost = 0;
        for (int t = 1; t <= activeTicks; t++) {
            if (shouldConsumeChi(t)) {
                cost += CHI_PER_PULSE;
            }
        }
        return cost;
    }

    private static void spawnStreamParticles(ServerWorld world, Vec3d origin, Vec3d look, double range) {
        int steps = Math.max(4, (int) (range * 2));
        for (int i = 1; i <= steps; i++) {
            double dist = (range * i) / steps;
            Vec3d pt = origin.add(look.multiply(dist));
            world.spawnParticles(ParticleTypes.SPLASH,
                    pt.x, pt.y, pt.z, 2, 0.08, 0.08, 0.08, 0.02);
            if (i % 2 == 0) {
                world.spawnParticles(ParticleTypes.FALLING_WATER,
                        pt.x, pt.y, pt.z, 1, 0.05, 0.05, 0.05, 0.01);
            }
        }
    }

    private WaterJetSkill() {}
}
