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
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Air Blast — Concentrated gust of wind that pushes entities back with high knockback.
 */
public final class AirBlastSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();
        final double padding = Math.min(1.0 + range * 0.1, 2.0);
        Vec3d end = origin.add(look.multiply(range));

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
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            target.addVelocity(
                    knockDir.x * def.knockback(),
                    0.25 + def.knockback() * 0.15,
                    knockDir.z * def.knockback()
            );
            target.velocityModified = true;
        }

        // Clear loose grass and flowers along wind path
        ElementalInteractions.clearVegetation(world, origin.add(look.multiply(range * 0.5)), 2.5);

        // Deflect incoming hostile projectiles in blast path
        Box deflectBox = Box.of(origin.add(look.multiply(range * 0.5)), range, range, range);
        List<net.minecraft.entity.projectile.ProjectileEntity> projectiles = world.getEntitiesByClass(
                net.minecraft.entity.projectile.ProjectileEntity.class, deflectBox,
                p -> p.getOwner() != player
        );
        for (net.minecraft.entity.projectile.ProjectileEntity proj : projectiles) {
            Vec3d reflect = proj.getVelocity().multiply(-0.8).add(look.multiply(1.2));
            proj.setVelocity(reflect);
            proj.velocityModified = true;
        }

        // Coordinate frame for sonic rings perpendicular to look direction
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-5
                ? new Vec3d(-look.z / horizLen, 0.0, look.x / horizLen)
                : new Vec3d(1.0, 0.0, 0.0);
        Vec3d upVec = right.crossProduct(look).normalize();

        // 3 concentric expanding sonic rings (Datapack style)
        double[][] ringSpecs = {
                {2.5, 0.9, 8},   // dist 2.5, r=0.9, 8 points
                {5.0, 1.8, 12},  // dist 5.0, r=1.8, 12 points
                {7.5, 2.7, 16}   // dist 7.5, r=2.7, 16 points
        };

        for (double[] spec : ringSpecs) {
            double dist = spec[0];
            double ringRadius = spec[1];
            int count = (int) spec[2];
            if (dist > range + 1.0) continue;

            Vec3d ringCenter = origin.add(look.multiply(dist));
            for (int i = 0; i < count; i++) {
                double theta = (Math.PI * 2 * i) / count;
                Vec3d ringPt = ringCenter.add(right.multiply(Math.cos(theta) * ringRadius))
                        .add(upVec.multiply(Math.sin(theta) * ringRadius));

                world.spawnParticles(AvatarParticles.GUST_CURL, ringPt.x, ringPt.y, ringPt.z, 2, 0.06, 0.06, 0.06, 0.03);
                world.spawnParticles(ParticleTypes.CLOUD, ringPt.x, ringPt.y, ringPt.z, 2, 0.08, 0.08, 0.08, 0.02);
                world.spawnParticles(ParticleTypes.POOF, ringPt.x, ringPt.y, ringPt.z, 1, 0.05, 0.05, 0.05, 0.02);
                world.spawnParticles(AvatarParticles.SMOKE_PUFF, ringPt.x, ringPt.y, ringPt.z, 1, 0.05, 0.05, 0.05, 0.02);
            }
        }

        // Center blast core particles along beam
        for (double d = 1.0; d <= range; d += 0.8) {
            Vec3d pt = origin.add(look.multiply(d));
            world.spawnParticles(AvatarParticles.GUST_CURL, pt.x, pt.y, pt.z, 3, 0.15, 0.15, 0.15, 0.05);
            world.spawnParticles(AvatarParticles.SMOKE_PUFF, pt.x, pt.y, pt.z, 1, 0.1, 0.1, 0.1, 0.02);
        }
        world.spawnParticles(AvatarParticles.IMPACT_FLASH, end.x, end.y, end.z, 1, 0.0, 0.0, 0.0, 0.0);

        // Multi-layered punchy air burst SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_WIND_CHARGE_WIND_BURST.value(),
                SoundCategory.PLAYERS, 2.0f, 1.2f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP,
                SoundCategory.PLAYERS, 1.8f, 0.7f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BREEZE_SHOOT,
                SoundCategory.PLAYERS, 1.2f, 1.3f);
    }

    private AirBlastSkill() {}
}
