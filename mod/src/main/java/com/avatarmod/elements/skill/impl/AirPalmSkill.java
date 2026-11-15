package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
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
 * Air Palm — Baguazhang open palm thrust creating a short cone shockwave.
 */
public final class AirPalmSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        if (timeline.ticksInPhase() != 1) return;

        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();

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
            target.damage(source, def.damage());
            Vec3d knockDir = target.getPos().subtract(player.getPos()).normalize();
            target.addVelocity(
                    knockDir.x * def.knockback(),
                    0.15 + def.knockback() * 0.1,
                    knockDir.z * def.knockback()
            );
            target.velocityModified = true;
        }

        // VFX: palm shockwave
        world.spawnParticles(AvatarParticles.GUST_CURL,
                center.x, center.y, center.z, 6, 0.25, 0.25, 0.25, 0.05);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                center.x, center.y, center.z, 1, 0.0, 0.0, 0.0, 0.0);

        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BREEZE_SLIDE,
                SoundCategory.PLAYERS, 0.8f, 1.4f);
    }

    private AirPalmSkill() {}
}
