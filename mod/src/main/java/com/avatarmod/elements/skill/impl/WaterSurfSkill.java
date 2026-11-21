package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
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
import net.minecraft.text.Text;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Water Surf & Ice Scooter — Master Waterbending Traversal.
 *
 * Adaptive Dual-Mode Mobility:
 * 1. Water Surf (over water/rivers/oceans):
 *    Surfs atop a surging wave crest at high speed (+120% velocity) with buoyant surface locking.
 * 2. Ice Scooter / Frost Skating (over land/terrain):
 *    Freezes ambient moisture into a slick temporary Frosted Ice runway beneath player's feet,
 *    allowing high-speed frictionless skating across plains, deserts, mountains, and snow.
 */
public final class WaterSurfSkill {

    public static final String ID = "avatar:water_surf";
    private static final double BASE_SPEED = 0.95;

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.HOLD && timeline.phase() != SkillTimeline.Phase.ACTIVE) return;

        int t = timeline.ticksInPhase();
        ServerWorld world = player.getServerWorld();
        BlockPos playerPos = player.getBlockPos();

        // 0. Water/Moisture validation on initial tick
        if (t == 0 && !hasWaterOrIceEnvironment(player, world, playerPos)) {
            player.sendMessage(Text.literal("§c[Avatar] Perlu sumber air terdekat, salju/es, atau kantong air!"), true);
            data.regenChi(def.chiCost());
            timeline.cancel();
            return;
        }

        // 1. Chi sustain consumption during hold phase (1 Chi every 3 ticks)
        if (timeline.phase() == SkillTimeline.Phase.HOLD && t > 0 && t % 3 == 0) {
            if (!data.trySpendChi(1)) {
                timeline.releaseHold();
                return;
            }
        }

        // 2. Absolute fall damage immunity while surfing/skating
        player.fallDistance = 0.0f;

        // 3. Direction & Speed calculation with Water Spear synergy
        Vec3d look = player.getRotationVec(1.0f);
        double horizLen = Math.sqrt(look.x * look.x + look.z * look.z);
        Vec3d forward = horizLen > 1e-4
                ? new Vec3d(look.x / horizLen, 0, look.z / horizLen)
                : new Vec3d(0, 0, 1);

        double speedMultiplier = ElementalInteractions.getWeaponSpeedMultiplier(player.getMainHandStack(), "WATER");
        double speed = BASE_SPEED * speedMultiplier;

        // Check if riding on water vs skating over solid land
        boolean onWater = isWaterSurface(world, playerPos);

        if (onWater) {
            // === MODE A: WATER SURF ===
            double surfaceY = findWaterSurfaceY(world, playerPos);
            double vy = 0.08;
            if (!Double.isNaN(surfaceY)) {
                double diff = (surfaceY + 0.35) - player.getY();
                vy = Math.min(Math.max(diff * 0.45, -0.30), 0.40);
            }
            player.setVelocity(forward.x * speed * 1.15, vy, forward.z * speed * 1.15);
            player.velocityModified = true;

            // Water wake & splash particle spray
            world.spawnParticles(ParticleTypes.SPLASH,
                    player.getX(), player.getY() + 0.1, player.getZ(),
                    6, 0.35, 0.1, 0.35, 0.08);
            world.spawnParticles(ParticleTypes.BUBBLE,
                    player.getX(), player.getY() + 0.05, player.getZ(),
                    4, 0.25, 0.05, 0.25, 0.04);
            world.spawnParticles(AvatarParticles.DROPLET,
                    player.getX(), player.getY() + 0.2, player.getZ(),
                    3, 0.25, 0.1, 0.25, 0.03);

            if (t % 5 == 0) {
                world.playSound(null, playerPos,
                        SoundEvents.ENTITY_GENERIC_SPLASH, SoundCategory.PLAYERS, 0.75f, 1.35f);
                world.playSound(null, playerPos,
                        SoundEvents.BLOCK_WATER_AMBIENT, SoundCategory.PLAYERS, 0.85f, 1.15f);
            }
        } else {
            // === MODE B: ICE SCOOTER / FROST SKATING ===
            // Lay down a temporary Frosted Ice path beneath player feet for true ice sliding physics
            placeFrostedIceTrail(world, playerPos);

            // Ground glide velocity with gentle slope handling
            double vy = player.getVelocity().y;
            if (player.isOnGround()) {
                vy = 0.02;
            }
            player.setVelocity(forward.x * speed, vy, forward.z * speed);
            player.velocityModified = true;

            // Ice crystals & frost particles
            world.spawnParticles(ParticleTypes.SNOWFLAKE,
                    player.getX(), player.getY() + 0.1, player.getZ(),
                    5, 0.2, 0.1, 0.2, 0.02);
            world.spawnParticles(AvatarParticles.FROST,
                    player.getX(), player.getY() + 0.15, player.getZ(),
                    3, 0.15, 0.1, 0.15, 0.02);

            if (t % 6 == 0) {
                world.playSound(null, playerPos,
                        SoundEvents.BLOCK_GLASS_STEP, SoundCategory.PLAYERS, 0.65f, 1.55f);
                world.playSound(null, playerPos,
                        SoundEvents.BLOCK_POWDER_SNOW_STEP, SoundCategory.PLAYERS, 0.75f, 1.35f);
            }
        }

        // Extinguish fires and clear loose vegetation along trajectory
        ElementalInteractions.douseFireBlocks(world, player.getPos(), 2.0);
        ElementalInteractions.clearVegetation(world, player.getPos(), 1.5);

        // Displace and damage mobs encountered along path
        Box bumpBox = Box.of(player.getPos().add(0, 0.5, 0), 1.8, 1.8, 1.8);
        List<LivingEntity> obstacles = world.getEntitiesByClass(
                LivingEntity.class, bumpBox,
                e -> e != player && e.isAlive()
        );
        DamageSource bumpSource = world.getDamageSources().playerAttack(player);
        for (LivingEntity e : obstacles) {
            Vec3d push = e.getPos().subtract(player.getPos()).normalize().multiply(def.knockback());
            e.addVelocity(push.x, 0.22, push.z);
            e.velocityModified = true;
            if (def.damage() > 0) {
                e.damage(bumpSource, def.damage());
            }
            if (onWater) {
                ElementalInteractions.applyWater(e, 50, 1);
            } else {
                ElementalInteractions.applyFreezing(e, 60, 40);
            }
        }

        // Periodic velocity packet sync to client
        if (t % 2 == 0) {
            player.networkHandler.sendPacket(new EntityVelocityUpdateS2CPacket(player.getId(), player.getVelocity()));
        }
    }

    private static boolean hasWaterOrIceEnvironment(ServerPlayerEntity player, ServerWorld world, BlockPos pos) {
        if (ElementalInteractions.hasWaterSource(player)) return true;
        BlockState below = world.getBlockState(pos.down());
        return below.isOf(Blocks.ICE) || below.isOf(Blocks.PACKED_ICE) || below.isOf(Blocks.BLUE_ICE)
                || below.isOf(Blocks.SNOW_BLOCK) || below.isOf(Blocks.SNOW) || below.isOf(Blocks.FROSTED_ICE);
    }

    private static boolean isWaterSurface(ServerWorld world, BlockPos pos) {
        return world.getFluidState(pos).isIn(FluidTags.WATER)
                || world.getFluidState(pos.down()).isIn(FluidTags.WATER)
                || world.getFluidState(pos.down(2)).isIn(FluidTags.WATER);
    }

    private static double findWaterSurfaceY(ServerWorld world, BlockPos pos) {
        for (int dy = 1; dy >= -3; dy--) {
            BlockPos check = pos.add(0, dy, 0);
            FluidState fluid = world.getFluidState(check);
            if (fluid.isIn(FluidTags.WATER)) {
                return check.getY() + fluid.getHeight();
            }
        }
        return Double.NaN;
    }

    private static void placeFrostedIceTrail(ServerWorld world, BlockPos playerPos) {
        BlockPos under = playerPos.down();
        BlockState underState = world.getBlockState(under);
        BlockState atState = world.getBlockState(playerPos);

        // Place temporary frosted ice beneath feet on solid ground
        if (underState.isSolidBlock(world, under) && atState.isAir()) {
            world.setBlockState(playerPos, Blocks.FROSTED_ICE.getDefaultState());
        } else if (underState.isAir() && world.getBlockState(under.down()).isSolidBlock(world, under.down())) {
            world.setBlockState(under, Blocks.FROSTED_ICE.getDefaultState());
        }
    }

    private WaterSurfSkill() {}
}
