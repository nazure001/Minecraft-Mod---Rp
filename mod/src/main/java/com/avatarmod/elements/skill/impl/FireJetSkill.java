package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.network.packet.s2c.play.EntityVelocityUpdateS2CPacket;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Fire Jet — Sustained 3D rocket thruster propulsion in full look direction.
 * Propels player with exhilarating speed, complete fall damage immunity,
 * twin boot flame trails, and incendiary contact scorch damage.
 */
public final class FireJetSkill {

    private static final float FLIGHT_SPEED = 1.15f;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.HOLD && timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();

        // Spend Chi during sustained hold flight (1 Chi every 4 ticks)
        if (timeline.phase() == SkillTimeline.Phase.HOLD && t > 0 && t % 4 == 0) {
            if (!data.trySpendChi(1)) {
                timeline.releaseHold();
                return;
            }
        }

        // 1. Initial explosive ignition burst on tick 0
        if (t == 0) {
            initialBurst(player);
        }

        // 2. True 3D rocket flight propulsion across all active/hold ticks
        sustainThrust(player, t);

        // 3. Flame thruster twin trails every tick
        twinThrusterTrail(player);

        // 4. Periodic thruster roar sound
        if (t % 4 == 0) {
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_BLAZE_SHOOT,
                    SoundCategory.PLAYERS, 1.2f, 0.85f);
        }
    }

    private static void initialBurst(ServerPlayerEntity player) {
        ServerWorld world = player.getServerWorld();
        world.spawnParticles(ParticleTypes.EXPLOSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                player.getX(), player.getY() + 0.3, player.getZ(), 12, 0.2, 0.2, 0.2, 0.06);
        world.spawnParticles(AvatarParticles.SMOKE_EXPANSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 8, 0.2, 0.2, 0.2, 0.02);

        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_FIREWORK_ROCKET_LAUNCH,
                SoundCategory.PLAYERS, 1.6f, 0.8f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 1.4f, 0.9f);
    }

    private static void sustainThrust(ServerPlayerEntity player, int t) {
        Vec3d look = player.getRotationVec(1.0f);
        double speedMultiplier = ElementalInteractions.getWeaponSpeedMultiplier(player.getMainHandStack(), "FIRE");
        double thrust = FLIGHT_SPEED * speedMultiplier;

        // True 3D vector thrust: look straight up -> vertical rocket ascent!
        // Counteract gravity with +0.08 hover bias
        double vy = look.y * thrust + 0.08;
        player.setVelocity(look.x * thrust, vy, look.z * thrust);
        player.velocityModified = true;
        player.fallDistance = 0.0f;

        if (t % 2 == 0) {
            player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));
        }

        // Contact scorch: incinerate and knock away mobs in path
        ServerWorld world = player.getServerWorld();
        Box box = Box.of(player.getPos().add(0, 0.5, 0), 2.0, 2.0, 2.0);
        List<LivingEntity> mobs = world.getEntitiesByClass(LivingEntity.class, box, e -> e != player && e.isAlive());
        for (LivingEntity e : mobs) {
            ElementalInteractions.applyFire(e, 80);
            e.damage(world.getDamageSources().playerAttack(player), 4.0f);
            Vec3d push = look.multiply(0.9);
            e.addVelocity(push.x, 0.25, push.z);
            e.velocityModified = true;
        }
    }

    private static void twinThrusterTrail(ServerPlayerEntity player) {
        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d right = horizLen > 1e-4 ? new Vec3d(-look.z / horizLen, 0, look.x / horizLen) : new Vec3d(1, 0, 0);

        Vec3d base = player.getPos().add(0, 0.2, 0);
        Vec3d leftBoot = base.subtract(right.multiply(0.32));
        Vec3d rightBoot = base.add(right.multiply(0.32));

        spawnBootFlame(world, leftBoot, look);
        spawnBootFlame(world, rightBoot, look);

        // Ground ignition directly under low-altitude flybys
        ElementalInteractions.igniteBlocks(world, player.getPos().subtract(0, 0.5, 0), 1.0, player);
    }

    private static void spawnBootFlame(ServerWorld world, Vec3d pos, Vec3d look) {
        Vec3d exhaust = look.multiply(-0.3);
        world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                pos.x, pos.y, pos.z, 5, 0.12, 0.12, 0.12, 0.04);
        world.spawnParticles(ParticleTypes.FLAME,
                pos.x, pos.y, pos.z, 6, 0.15, 0.15, 0.15, 0.05);
        world.spawnParticles(AvatarParticles.EMBER,
                pos.x, pos.y, pos.z, 3, 0.1, 0.1, 0.1, 0.02);
        world.spawnParticles(ParticleTypes.SMOKE,
                pos.x + exhaust.x, pos.y + exhaust.y, pos.z + exhaust.z, 3, 0.1, 0.1, 0.1, 0.02);
    }

    private FireJetSkill() {}
}
