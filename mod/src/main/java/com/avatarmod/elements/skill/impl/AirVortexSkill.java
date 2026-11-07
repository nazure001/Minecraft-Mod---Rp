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
 * Air Vortex — pulls all entities within range toward player center each ACTIVE tick.
 * Deals light damage per tick. Lasts 40 ticks (2 seconds).
 */
public final class AirVortexSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();

        // Pull every 2 ticks
        if (t % 2 == 0) {
            pullEntities(player, def);
        }

        // Spiral particle ring every 4 ticks
        if (t % 4 == 0) {
            spawnSpiralVFX(player, def, t);
        }

        // Looping wind sound every 20 ticks
        if (t % 20 == 1) {
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PHANTOM_FLAP,
                    SoundCategory.PLAYERS, 0.6f, 1.4f);
        }
    }

    private static void pullEntities(ServerPlayerEntity player, SkillDefinition def) {
        ServerWorld world = player.getServerWorld();
        Vec3d center = player.getPos().add(0, 1.0, 0);
        double r = def.range();

        Box box = Box.of(center, r * 2, r * 2, r * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, box,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= r * r
        );

        DamageSource source = world.getDamageSources().playerAttack(player);
        double pullForce = def.knockback(); // used as pull magnitude

        for (LivingEntity target : targets) {
            // Pull direction = toward center
            Vec3d toCenter = center.subtract(target.getPos()).normalize();
            target.addVelocity(
                    toCenter.x * pullForce,
                    toCenter.y * pullForce * 0.3,
                    toCenter.z * pullForce
            );
            target.velocityModified = true;

            // Light damage per hit interval
            if (def.damage() > 0) {
                target.damage(source, def.damage());
            }
        }
    }

    private static void spawnSpiralVFX(ServerPlayerEntity player, SkillDefinition def, int tick) {
        ServerWorld world = player.getServerWorld();
        Vec3d center = player.getPos().add(0, 1.0, 0);
        double r = def.range() * 0.8;
        double angleOffset = tick * 15.0; // rotate over time

        for (int i = 0; i < 8; i++) {
            double angle = Math.toRadians(i * 45 + angleOffset);
            double px = center.x + Math.cos(angle) * r;
            double pz = center.z + Math.sin(angle) * r;
            world.spawnParticles(ParticleTypes.CLOUD,
                    px, center.y + (i % 2) * 0.5, pz,
                    1, 0.05, 0.05, 0.05, 0.02);
        }
    }

    private AirVortexSkill() {}
}
