package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import com.avatarmod.elements.skill.SkillTargeting;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
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
        double padding = 0.9;
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

        // VFX: trail of gust curls along path
        for (double d = 1.0; d <= range; d += 0.8) {
            Vec3d pt = origin.add(look.multiply(d));
            world.spawnParticles(AvatarParticles.GUST_CURL, pt.x, pt.y, pt.z, 3, 0.2, 0.2, 0.2, 0.05);
            world.spawnParticles(AvatarParticles.SMOKE_PUFF, pt.x, pt.y, pt.z, 1, 0.1, 0.1, 0.1, 0.02);
        }

        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BREEZE_SHOOT,
                SoundCategory.PLAYERS, 0.9f, 1.2f);
    }

    private AirBlastSkill() {}
}
