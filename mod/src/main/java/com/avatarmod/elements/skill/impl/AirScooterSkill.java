package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.fluid.FluidState;
import net.minecraft.network.packet.s2c.play.EntityVelocityUpdateS2CPacket;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.registry.tag.FluidTags;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Air Scooter — Signature traversal technique invented by Avatar Aang.
 * Player rides a spinning sphere of compressed air, gliding rapidly over land and water
 * with complete fall damage immunity, vegetation clearing, and directional momentum.
 * Rides continuously while held without arbitrary time cutoffs until dismissed or interrupted.
 */
public final class AirScooterSkill {

    public static final String ID = "avatar:air_scooter";
    private static final double GLIDE_SPEED = 0.90;
    private static final double DESIRED_HOVER_HEIGHT = 0.75;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.HOLD && timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();
        ServerWorld world = player.getServerWorld();

        // Sustain Chi consumption during hold phase (1 Chi every 10 ticks — basic accessible mobility)
        if (timeline.phase() == SkillTimeline.Phase.HOLD && t > 0 && t % 10 == 0) {
            if (!data.trySpendChi(1)) {
                timeline.releaseHold();
                return;
            }
        }

        // 1. Fall damage immunity while riding
        player.fallDistance = 0.0f;

        // 2. Traversal propulsion & ground/water hover calculation
        Vec3d look = player.getRotationVec(1.0f);
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d forward = horizLen > 1e-4
                ? new Vec3d(look.x / horizLen, 0, look.z / horizLen)
                : new Vec3d(0, 0, 1);

        double speedMultiplier = ElementalInteractions.getWeaponSpeedMultiplier(player.getMainHandStack(), "AIR");
        double speed = GLIDE_SPEED * speedMultiplier;

        BlockPos playerPos = player.getBlockPos();
        double surfaceY = Double.NaN;
        for (int dy = 0; dy >= -4; dy--) {
            BlockPos check = playerPos.add(0, dy, 0);
            BlockState state = world.getBlockState(check);
            FluidState fluid = world.getFluidState(check);
            if (!state.getCollisionShape(world, check).isEmpty() || !fluid.isEmpty()) {
                surfaceY = check.getY() + (fluid.isEmpty() ? 1.0 : fluid.getHeight());
                break;
            }
        }

        double vy;
        if (!Double.isNaN(surfaceY)) {
            double currentAbove = player.getY() - surfaceY;
            double diff = DESIRED_HOVER_HEIGHT - currentAbove;
            vy = Math.min(Math.max(diff * 0.45, -0.35), 0.35);
        } else {
            vy = -0.06; // very slow, safe gliding descent over ravines & chasms
        }

        player.setVelocity(forward.x * speed, vy, forward.z * speed);
        player.velocityModified = true;

        if (t % 2 == 0) {
            player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));
        }

        // 3. Clear loose surface vegetation along traversal path
        ElementalInteractions.clearVegetation(world, player.getPos(), 1.8);

        // 4. Mobs collision: bump away entities in path
        Box bumpBox = Box.of(player.getPos().add(0, 0.5, 0), 1.8, 1.8, 1.8);
        List<LivingEntity> obstacles = world.getEntitiesByClass(
                LivingEntity.class, bumpBox,
                e -> e != player && e.isAlive()
        );
        DamageSource bumpSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : obstacles) {
            Vec3d push = e.getPos().subtract(player.getPos()).normalize().multiply(def.knockback());
            e.addVelocity(push.x, 0.2, push.z);
            e.velocityModified = true;
            if (def.damage() > 0) {
                e.damage(bumpSource, def.damage());
            }
        }

        // 5. VFX: Rotating compressed air sphere beneath player's feet
        double rotAngle = (t * 0.5) % (Math.PI * 2);
        for (int i = 0; i < 4; i++) {
            double a = rotAngle + (i * Math.PI / 2.0);
            double rx = Math.cos(a) * 0.70;
            double rz = Math.sin(a) * 0.70;
            world.spawnParticles(AvatarParticles.GUST_CURL,
                    player.getX() + rx, player.getY() + 0.25, player.getZ() + rz,
                    1, 0.0, 0.0, 0.0, 0.02);
            world.spawnParticles(ParticleTypes.CLOUD,
                    player.getX() + rx, player.getY() + 0.1, player.getZ() + rz,
                    1, 0.0, 0.0, 0.0, 0.02);
        }
        world.spawnParticles(ParticleTypes.CLOUD,
                player.getX(), player.getY() + 0.1, player.getZ(),
                2, 0.2, 0.08, 0.2, 0.01);
        world.spawnParticles(ParticleTypes.POOF,
                player.getX(), player.getY() + 0.05, player.getZ(),
                1, 0.15, 0.05, 0.15, 0.01);

        // Water wake if skimming water
        if (world.getFluidState(playerPos).isIn(FluidTags.WATER) || world.getFluidState(playerPos.down()).isIn(FluidTags.WATER)) {
            world.spawnParticles(ParticleTypes.SPLASH,
                    player.getX(), player.getY(), player.getZ(),
                    4, 0.3, 0.05, 0.3, 0.06);
        }

        // 6. SFX: Continuous whooshing wind sound
        if (t % 8 == 1) {
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ITEM_ELYTRA_FLYING, SoundCategory.PLAYERS, 0.75f, 1.4f);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.ENTITY_PHANTOM_FLAP, SoundCategory.PLAYERS, 0.55f, 1.3f);
        }
    }

    private AirScooterSkill() {}
}
