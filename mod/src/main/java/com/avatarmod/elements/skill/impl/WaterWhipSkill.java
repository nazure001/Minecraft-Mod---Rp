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
 * Water Whip — LINE hitbox in look direction, hits first entity in path.
 * Pulls target slightly toward player on hit.
 * No water-source requirement for prototype.
 */
public final class WaterWhipSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        if (!ElementalInteractions.hasWaterSource(player)) {
            player.sendMessage(Text.literal("§c[Avatar] Perlu sumber air terdekat atau kantong/ember air!"), true);
            PlayerBendingData.get(player).regenChi(def.chiCost());
            timeline.cancel();
            return;
        }

        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getPos().add(0, player.getStandingEyeHeight(), 0);
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();

        double padding = 1.4;
        Vec3d end = origin.add(look.multiply(range + 0.5));
        Box searchBounds = SkillTargeting.segmentBounds(origin, end, padding);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, searchBounds,
                e -> e != player && e.isAlive()
                        && SkillTargeting.intersectsSegment(origin, end, e.getBoundingBox(), padding)
                        && SkillTargeting.hasLineOfSight(world, origin, e.getBoundingBox(), player)
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());
            ElementalInteractions.applyWater(target, 80, 1);
            // Pull toward player
            Vec3d pull = player.getPos().subtract(target.getPos()).normalize().multiply(def.knockback());
            target.addVelocity(pull.x, 0.15 + pull.y * 0.5, pull.z);
            target.velocityModified = true;
        }

        ElementalInteractions.douseFireBlocks(world, end, 2.5);

        // VFX: Serpentine Double-Helix Water Whip (Katara Spiraling Flow)
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-5
                ? new Vec3d(-look.z / horizLen, 0.0, look.x / horizLen)
                : new Vec3d(1.0, 0.0, 0.0);
        Vec3d upVec = right.crossProduct(look).normalize();

        for (double d = 1.0; d <= range; d += 0.5) {
            double angle = d * 1.6;
            double rHelix = 0.38 * (1.0 - (d / (range * 1.5)));
            Vec3d basePt = origin.add(look.multiply(d));

            // Strand A
            Vec3d ptA = basePt.add(right.multiply(Math.cos(angle) * rHelix))
                    .add(upVec.multiply(Math.sin(angle) * rHelix));
            // Strand B (180° opposite)
            Vec3d ptB = basePt.add(right.multiply(-Math.cos(angle) * rHelix))
                    .add(upVec.multiply(-Math.sin(angle) * rHelix));

            world.spawnParticles(ParticleTypes.SPLASH, ptA.x, ptA.y, ptA.z, 3, 0.04, 0.04, 0.04, 0.02);
            world.spawnParticles(ParticleTypes.FALLING_WATER, ptA.x, ptA.y, ptA.z, 2, 0.04, 0.04, 0.04, 0.01);
            world.spawnParticles(ParticleTypes.BUBBLE, ptA.x, ptA.y, ptA.z, 2, 0.04, 0.04, 0.04, 0.02);
            world.spawnParticles(AvatarParticles.DROPLET, ptA.x, ptA.y, ptA.z, 2, 0.04, 0.04, 0.04, 0.01);

            world.spawnParticles(ParticleTypes.SPLASH, ptB.x, ptB.y, ptB.z, 3, 0.04, 0.04, 0.04, 0.02);
            world.spawnParticles(ParticleTypes.FALLING_WATER, ptB.x, ptB.y, ptB.z, 2, 0.04, 0.04, 0.04, 0.01);
            world.spawnParticles(AvatarParticles.FOAM, ptB.x, ptB.y, ptB.z, 1, 0.03, 0.03, 0.03, 0.01);
        }

        // Whip tip impact burst
        world.spawnParticles(ParticleTypes.SPLASH,
                end.x, end.y, end.z, 24, 0.35, 0.35, 0.35, 0.12);
        world.spawnParticles(AvatarParticles.SMALL_SPLASH,
                end.x, end.y, end.z, 12, 0.25, 0.25, 0.25, 0.08);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                end.x, end.y, end.z, 1, 0.0, 0.0, 0.0, 0.0);

        // Multi-layered punchy water SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_GENERIC_SPLASH,
                SoundCategory.PLAYERS, 1.8f, 1.3f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_SPLASH_HIGH_SPEED,
                SoundCategory.PLAYERS, 1.5f, 1.5f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP,
                SoundCategory.PLAYERS, 1.0f, 1.4f);
    }

    private WaterWhipSkill() {}
}
