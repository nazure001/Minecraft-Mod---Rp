package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
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

        // Helical cyclone particles every 2 ticks
        if (t % 2 == 0) {
            spawnSpiralVFX(player, def, t);
        }

        // Looping howling wind & breeze sounds
        if (t % 12 == 1) {
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_BREEZE_IDLE_AIR,
                    SoundCategory.PLAYERS, 1.2f, 1.1f);
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PHANTOM_FLAP,
                    SoundCategory.PLAYERS, 0.8f, 1.4f);
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

        // Clear vegetation in vortex funnel
        ElementalInteractions.clearVegetation(world, center, r * 0.8);

        for (LivingEntity target : targets) {
            // Pull direction = toward center
            Vec3d diff = center.subtract(target.getPos());
            if (diff.lengthSquared() < 0.001) continue;
            Vec3d toCenter = diff.normalize();
            target.addVelocity(
                    toCenter.x * pullForce,
                    toCenter.y * pullForce * 0.3 + 0.1,
                    toCenter.z * pullForce
            );
            target.velocityModified = true;

            // Lift mob into air vortex
            ElementalInteractions.applyAirLevitation(target, 20);

            // Light damage per hit interval
            if (def.damage() > 0) {
                target.damage(source, def.damage());
            }
        }
    }

    private static void spawnSpiralVFX(ServerPlayerEntity player, SkillDefinition def, int tick) {
        ServerWorld world = player.getServerWorld();
        Vec3d center = player.getPos().add(0, 0.2, 0);
        double maxR = def.range() * 0.85;

        // 4 ascending spiral arms forming a volumetric cyclone funnel
        for (int arm = 0; arm < 4; arm++) {
            for (double h = 0.2; h <= 2.6; h += 0.8) {
                double r = maxR * (0.35 + (h / 2.6) * 0.65);
                double angle = Math.toRadians(arm * 90.0 + tick * 22.0 + h * 45.0);
                double px = center.x + Math.cos(angle) * r;
                double pz = center.z + Math.sin(angle) * r;

                world.spawnParticles(AvatarParticles.GUST_CURL,
                        px, center.y + h, pz, 2, 0.08, 0.08, 0.08, 0.03);
                world.spawnParticles(ParticleTypes.CLOUD,
                        px, center.y + h, pz, 2, 0.08, 0.08, 0.08, 0.02);
                world.spawnParticles(AvatarParticles.SMOKE_PUFF,
                        px, center.y + h, pz, 1, 0.05, 0.05, 0.05, 0.01);
            }
        }
    }

    private AirVortexSkill() {}
}
