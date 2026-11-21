package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.RaycastContext;

import java.util.List;

/**
 * Grapple Wire — Equalist / Non-Bender high-tensile metal cable tether.
 * Can latch onto distant surfaces to pull the user forward, or latch onto
 * an enemy to rip them toward the player, dealing damage and immobilizing them.
 */
public final class GrappleWireSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range(); // 18.0m
        Vec3d targetPos = eyePos.add(look.multiply(range));

        // Check entity raycast along wire path first
        Box scanBox = new Box(eyePos, targetPos).expand(1.5);
        List<LivingEntity> potentialTargets = world.getEntitiesByClass(
                LivingEntity.class, scanBox,
                e -> e != player && e.isAlive()
        );

        LivingEntity bestTarget = null;
        double bestDistSq = range * range;

        for (LivingEntity entity : potentialTargets) {
            Box eBox = entity.getBoundingBox().expand(0.5);
            var optHit = eBox.raycast(eyePos, targetPos);
            if (optHit.isPresent()) {
                double distSq = eyePos.squaredDistanceTo(optHit.get());
                if (distSq < bestDistSq) {
                    bestDistSq = distSq;
                    bestTarget = entity;
                }
            }
        }

        if (bestTarget != null) {
            // Target caught: drag toward player, deal damage and apply slowness
            DamageSource source = world.getDamageSources().playerAttack(player);
            bestTarget.damage(source, def.damage());
            bestTarget.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 40, 2));

            Vec3d pullDir = eyePos.subtract(bestTarget.getEyePos()).normalize();
            bestTarget.setVelocity(pullDir.multiply(1.35).add(0.0, 0.25, 0.0));
            bestTarget.velocityModified = true;

            spawnWireParticles(world, eyePos, bestTarget.getEyePos());
            world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_FISHING_BOBBER_RETRIEVE, SoundCategory.PLAYERS, 1.2f, 1.4f);
            world.playSound(null, bestTarget.getBlockPos(), SoundEvents.BLOCK_TRIPWIRE_ATTACH, SoundCategory.PLAYERS, 1.2f, 1.2f);
            return;
        }

        // Otherwise check block hit for grapple traversal
        BlockHitResult blockHit = world.raycast(new RaycastContext(
                eyePos, targetPos,
                RaycastContext.ShapeType.COLLIDER,
                RaycastContext.FluidHandling.NONE,
                player
        ));

        if (blockHit.getType() == HitResult.Type.BLOCK) {
            Vec3d hit = blockHit.getPos();
            Vec3d pullVec = hit.subtract(eyePos).normalize();
            double dist = eyePos.distanceTo(hit);
            double speed = Math.min(1.8, Math.max(1.1, dist * 0.12));

            player.setVelocity(pullVec.multiply(speed).add(0.0, 0.20, 0.0));
            player.velocityModified = true;
            player.fallDistance = 0.0f;

            spawnWireParticles(world, eyePos, hit);
            world.playSound(null, player.getBlockPos(), SoundEvents.ENTITY_ARROW_SHOOT, SoundCategory.PLAYERS, 1.0f, 1.6f);
            world.playSound(null, blockHit.getBlockPos(), SoundEvents.BLOCK_ANVIL_HIT, SoundCategory.PLAYERS, 0.8f, 1.8f);
        }
    }

    private static void spawnWireParticles(ServerWorld world, Vec3d start, Vec3d end) {
        int steps = 14;
        Vec3d delta = end.subtract(start).multiply(1.0 / steps);
        for (int i = 0; i <= steps; i++) {
            Vec3d p = start.add(delta.multiply(i));
            world.spawnParticles(ParticleTypes.CRIT, p.x, p.y, p.z, 1, 0.02, 0.02, 0.02, 0.0);
        }
    }

    private GrappleWireSkill() {}
}
