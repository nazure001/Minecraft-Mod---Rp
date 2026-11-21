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
 * Octopus Form — Mastery Waterbending Stance.
 * The waterbender constructs 8 fluid water tentacles radiating 360 degrees around themselves.
 * While active, deflects all incoming projectiles, douses fires, whips approaching enemies
 * for 8.0 damage, and forcefully repels them!
 */
public final class OctopusFormSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();
        ServerWorld world = player.getServerWorld();
        Vec3d center = player.getPos().add(0, 0.8, 0);
        double radius = def.range();

        // 1. Deflect all incoming projectiles within octopus radius every tick
        ElementalInteractions.deflectProjectiles(world, player, center, player.getRotationVec(1.0f), radius + 1.0, 1.5);

        // 2. Continuous rotating water tentacles VFX (8 tentacles)
        double baseAngle = (t * 0.45);
        for (int tentacle = 0; tentacle < 8; tentacle++) {
            double angle = baseAngle + (tentacle * (Math.PI / 4.0));
            double tx = Math.cos(angle);
            double tz = Math.sin(angle);

            for (double d = 1.0; d <= radius; d += 0.8) {
                double wave = Math.sin((t * 0.5) + d) * 0.35;
                Vec3d pt = center.add(tx * d, wave, tz * d);
                world.spawnParticles(ParticleTypes.SPLASH, pt.x, pt.y, pt.z, 2, 0.05, 0.05, 0.05, 0.02);
                world.spawnParticles(ParticleTypes.FALLING_WATER, pt.x, pt.y, pt.z, 1, 0.04, 0.04, 0.04, 0.01);
                world.spawnParticles(AvatarParticles.DROPLET, pt.x, pt.y, pt.z, 1, 0.03, 0.03, 0.03, 0.01);
            }
        }

        // 3. Periodic whip damage and knockback on nearby mobs (every 4 ticks)
        if (t % 4 == 0) {
            Box box = Box.of(center, radius * 2, 2.5, radius * 2);
            List<LivingEntity> enemies = world.getEntitiesByClass(
                    LivingEntity.class, box,
                    e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= radius * radius
            );

            DamageSource source = world.getDamageSources().playerAttack(player);
            for (LivingEntity e : enemies) {
                e.damage(source, def.damage());
                ElementalInteractions.applyWater(e, 80, 2);
                Vec3d push = e.getPos().subtract(player.getPos()).normalize().multiply(def.knockback());
                e.addVelocity(push.x, 0.25, push.z);
                e.velocityModified = true;
            }

            // Douse fires within radius
            ElementalInteractions.douseFireBlocks(world, center, radius + 1.0);

            // Water splashing audio
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PLAYER_SPLASH_HIGH_SPEED,
                    SoundCategory.PLAYERS, 1.2f, 1.2f);
        }
    }

    private OctopusFormSkill() {}
}
