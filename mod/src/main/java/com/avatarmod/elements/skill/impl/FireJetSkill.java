package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.network.packet.s2c.play.EntityVelocityUpdateS2CPacket;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Vec3d;

/**
 * Fire Jet — Sustained rocket thruster propulsion in look direction.
 * Propels player with high velocity, complete fall damage immunity, and incendiary foot trail.
 */
public final class FireJetSkill {

    private static final float THRUST_SPEED = 0.95f;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();

        // 1. Initial explosive launch burst on tick 0
        if (t == 0) {
            initialBurst(player);
        }

        // 2. Sustained rocket flight propulsion across all active ticks
        sustainThrust(player, t);

        // 3. Flame thruster trail & ignition every tick
        trail(player);

        // 4. Periodic thruster roar sound
        if (t % 3 == 0) {
            player.getServerWorld().playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_BLAZE_SHOOT,
                    SoundCategory.PLAYERS, 1.1f, 0.85f);
        }
    }

    private static void initialBurst(ServerPlayerEntity player) {
        ServerWorld world = player.getServerWorld();
        world.spawnParticles(ParticleTypes.EXPLOSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                player.getX(), player.getY() + 0.3, player.getZ(), 8, 0.2, 0.2, 0.2, 0.05);
        world.spawnParticles(AvatarParticles.SMOKE_EXPANSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 6, 0.2, 0.2, 0.2, 0.02);

        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_FIREWORK_ROCKET_LAUNCH,
                SoundCategory.PLAYERS, 1.6f, 0.8f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 1.3f, 0.9f);
    }

    private static void sustainThrust(ServerPlayerEntity player, int t) {
        Vec3d look = player.getRotationVec(1.0f);
        double vy = Math.max(look.y * 0.85 + 0.12, 0.08);
        player.setVelocity(look.x * THRUST_SPEED, vy, look.z * THRUST_SPEED);
        player.velocityModified = true;
        player.fallDistance = 0.0f;

        if (t % 2 == 0) {
            player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));
        }
    }

    private static void trail(ServerPlayerEntity player) {
        ServerWorld world = player.getServerWorld();
        Vec3d pos = player.getPos().add(0, 0.2, 0);

        world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                pos.x, pos.y, pos.z, 8, 0.2, 0.2, 0.2, 0.04);
        world.spawnParticles(AvatarParticles.EMBER,
                pos.x, pos.y, pos.z, 5, 0.15, 0.15, 0.15, 0.02);
        world.spawnParticles(ParticleTypes.FLAME,
                pos.x, pos.y, pos.z, 10, 0.2, 0.2, 0.2, 0.05);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                pos.x, pos.y, pos.z, 3, 0.1, 0.1, 0.1, 0.01);

        // Ignites ground/vegetation directly under rocket thrusters
        ElementalInteractions.igniteBlocks(world, player.getPos().subtract(0, 0.5, 0), 1.0);
    }

    private FireJetSkill() {}
}
