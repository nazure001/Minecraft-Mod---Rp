package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.network.packet.s2c.play.EntityVelocityUpdateS2CPacket;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Vec3d;

/** Propulsion dash in look direction. No hitbox — pure mobility. */
public final class FireJetSkill {

    private static final float LAUNCH_FORCE = 2.2f;
    private static final float VERTICAL_BOOST = 0.4f;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();

        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        // ticksInPhase == 0: first moment of ACTIVE phase (phase just advanced from WINDUP)
        if (timeline.ticksInPhase() == 0) {
            launch(player);
        }

        // Flame trail every 2 ticks (0, 2, 4, …)
        if (timeline.ticksInPhase() % 2 == 0) {
            trail(player);
        }
    }

    private static void launch(ServerPlayerEntity player) {
        Vec3d look = player.getRotationVec(1.0f);
        // Horizontal force in look dir + upward kick
        player.setVelocity(
                look.x * LAUNCH_FORCE,
                VERTICAL_BOOST,
                look.z * LAUNCH_FORCE
        );
        player.velocityModified = true;
        // Push velocity to client — server-set velocity isn't auto-synced for the controlled player
        player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));

        ServerWorld world = player.getServerWorld();
        // Explosive launch burst at feet
        world.spawnParticles(ParticleTypes.EXPLOSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                player.getX(), player.getY() + 0.3, player.getZ(), 6, 0.2, 0.2, 0.2, 0.05);
        world.spawnParticles(AvatarParticles.SMOKE_EXPANSION,
                player.getX(), player.getY() + 0.2, player.getZ(), 4, 0.2, 0.2, 0.2, 0.02);

        // Multi-layered rocket thrust SFX
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_FIREWORK_ROCKET_LAUNCH,
                SoundCategory.PLAYERS, 1.5f, 0.8f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ITEM_FIRECHARGE_USE,
                SoundCategory.PLAYERS, 1.2f, 0.9f);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BLAZE_SHOOT,
                SoundCategory.PLAYERS, 1.2f, 0.7f);
    }

    private static void trail(ServerPlayerEntity player) {
        ServerWorld world = player.getServerWorld();
        Vec3d pos = player.getPos().add(0, 0.4, 0);
        world.spawnParticles(AvatarParticles.FLAME_TONGUE,
                pos.x, pos.y, pos.z, 8, 0.2, 0.2, 0.2, 0.04);
        world.spawnParticles(AvatarParticles.EMBER,
                pos.x, pos.y, pos.z, 5, 0.15, 0.15, 0.15, 0.02);
        world.spawnParticles(ParticleTypes.FLAME,
                pos.x, pos.y, pos.z, 10, 0.2, 0.2, 0.2, 0.05);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                pos.x, pos.y, pos.z, 3, 0.1, 0.1, 0.1, 0.01);
    }

    private FireJetSkill() {}
}
