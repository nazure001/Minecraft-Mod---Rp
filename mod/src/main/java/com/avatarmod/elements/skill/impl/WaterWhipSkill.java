package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
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
 * Water Whip — LINE hitbox in look direction, hits first entity in path.
 * Pulls target slightly toward player on hit.
 * No water-source requirement for prototype.
 */
public final class WaterWhipSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;
        // Fire on first ACTIVE tick (ticksInPhase == 0 at phase entry)
        if (timeline.ticksInPhase() != 0) return;

        ServerWorld world = player.getServerWorld();
        Vec3d origin = player.getPos().add(0, player.getStandingEyeHeight(), 0);
        Vec3d look = player.getRotationVec(1.0f);
        double range = def.range();

        // LINE hitbox: thin box along look vector
        Vec3d end = origin.add(look.multiply(range));
        Vec3d mid = origin.add(look.multiply(range * 0.5));
        double width = 0.6;
        Box box = Box.of(mid, range + width, width * 2, range + width);

        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive() && isInLine(origin, look, e, range, width)
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());
            // Pull toward player
            Vec3d pull = player.getPos().subtract(target.getPos()).normalize().multiply(def.knockback());
            target.addVelocity(pull.x, 0.15 + pull.y * 0.5, pull.z);
            target.velocityModified = true;
        }

        // VFX: water droplet trail along whip path
        int steps = 8;
        for (int i = 1; i <= steps; i++) {
            double t = (double) i / steps;
            Vec3d pt = origin.add(look.multiply(range * t));
            world.spawnParticles(ParticleTypes.DRIPPING_WATER,
                    pt.x, pt.y, pt.z, 2, 0.1, 0.1, 0.1, 0.0);
        }
        world.spawnParticles(ParticleTypes.SPLASH,
                end.x, end.y, end.z, 12, 0.3, 0.3, 0.3, 0.1);

        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP,
                SoundCategory.PLAYERS, 0.9f, 0.6f);
    }

    private static boolean isInLine(Vec3d origin, Vec3d look, LivingEntity e, double range, double width) {
        Vec3d toEntity = e.getPos().add(0, e.getHeight() / 2.0, 0).subtract(origin);
        double dot = toEntity.dotProduct(look);
        if (dot < 0 || dot > range) return false;
        Vec3d proj = look.multiply(dot);
        double perpDist = toEntity.subtract(proj).length();
        return perpDist <= width + 0.5;
    }

    private WaterWhipSkill() {}
}
