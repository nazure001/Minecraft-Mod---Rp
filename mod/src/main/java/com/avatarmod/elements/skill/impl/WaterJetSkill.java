package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillTargeting;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
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

        // 0. Water source check on initiation
        if (t == 0 && !ElementalInteractions.hasWaterSource(player)) {
            player.sendMessage(Text.literal("§c[Avatar] Perlu sumber air terdekat atau kantong/ember air!"), true);
            data.regenChi(def.chiCost());
            timeline.cancel();
            return;
        }

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
            boolean isSneaking = player.isSneaking();
            for (LivingEntity target : targets) {
                target.damage(source, def.damage());
                if (isSneaking) {
                    ElementalInteractions.applyFreezing(target, 80, 50);
                } else {
                    ElementalInteractions.applyWater(target, 60, 1);
                }

                // Directional push knockback along water jet stream
                Vec3d push = calculatePushVector(look, def.knockback());
                target.addVelocity(push.x, push.y, push.z);
                target.velocityModified = true;
            }

            ElementalInteractions.douseFireBlocks(world, end, 3.0);
            ElementalInteractions.clearVegetation(world, end, 1.5);
            if (isSneaking) {
                ElementalInteractions.freezeWaterArea(world, end, 1.6);
            }
        }

        // 3. VFX: High-pressure water particles streaming forward (with snowflakes if sneaking)
        spawnStreamParticles(world, origin, look, range, t, player.isSneaking());

        // 4. Looping rushing water SFX
        if (t % 6 == 1) {
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ITEM_BUCKET_EMPTY,
                    SoundCategory.PLAYERS, 0.9f, 1.4f);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_GENERIC_SPLASH,
                    SoundCategory.PLAYERS, 0.7f, 1.6f);
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

    private static void spawnStreamParticles(ServerWorld world, Vec3d origin, Vec3d look, double range, int tick, boolean isSneaking) {
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-5
                ? new Vec3d(-look.z / horizLen, 0.0, look.x / horizLen)
                : new Vec3d(1.0, 0.0, 0.0);
        Vec3d upVec = right.crossProduct(look).normalize();

        int steps = Math.max(8, (int) (range * 3));
        for (int i = 1; i <= steps; i++) {
            double dist = (range * i) / steps;
            double spiralAngle = tick * 0.5 + i * 0.4;
            double rSpiral = 0.22 * Math.min(1.0, dist * 0.5);

            Vec3d basePt = origin.add(look.multiply(dist));
            Vec3d spiralPt = basePt.add(right.multiply(Math.cos(spiralAngle) * rSpiral))
                    .add(upVec.multiply(Math.sin(spiralAngle) * rSpiral));

            if (isSneaking) {
                world.spawnParticles(ParticleTypes.SNOWFLAKE, spiralPt.x, spiralPt.y, spiralPt.z, 2, 0.04, 0.04, 0.04, 0.01);
                world.spawnParticles(ParticleTypes.SPLASH, spiralPt.x, spiralPt.y, spiralPt.z, 1, 0.03, 0.03, 0.03, 0.01);
            } else {
                world.spawnParticles(ParticleTypes.SPLASH, spiralPt.x, spiralPt.y, spiralPt.z, 2, 0.04, 0.04, 0.04, 0.02);
                world.spawnParticles(ParticleTypes.FALLING_WATER, spiralPt.x, spiralPt.y, spiralPt.z, 1, 0.03, 0.03, 0.03, 0.01);
            }
            world.spawnParticles(AvatarParticles.DROPLET, spiralPt.x, spiralPt.y, spiralPt.z, 2, 0.04, 0.04, 0.04, 0.01);

            if (i % 3 == 0) {
                world.spawnParticles(ParticleTypes.BUBBLE, spiralPt.x, spiralPt.y, spiralPt.z, 1, 0.03, 0.03, 0.03, 0.02);
                world.spawnParticles(AvatarParticles.FOAM, spiralPt.x, spiralPt.y, spiralPt.z, 1, 0.03, 0.03, 0.03, 0.01);
            }
        }

        // Stream terminal burst
        Vec3d end = origin.add(look.multiply(range));
        if (isSneaking) {
            world.spawnParticles(ParticleTypes.SNOWFLAKE, end.x, end.y, end.z, 12, 0.25, 0.25, 0.25, 0.05);
        }
        world.spawnParticles(ParticleTypes.SPLASH, end.x, end.y, end.z, 6, 0.2, 0.2, 0.2, 0.08);
        world.spawnParticles(AvatarParticles.SMALL_SPLASH, end.x, end.y, end.z, 4, 0.15, 0.15, 0.15, 0.05);
    }

    private WaterJetSkill() {}
}
