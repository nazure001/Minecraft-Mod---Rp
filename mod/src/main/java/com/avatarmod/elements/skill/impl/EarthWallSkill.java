package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;

/**
 * Earth Wall — Defensive fortification construct.
 * Raises a solid curved barrier of stone slabs in front of caster.
 * While channeled (HOLD), sweeps along the cursor path to construct continuous defensive fortifications
 * or an impenetrable 360-degree circular fortress!
 */
public final class EarthWallSkill {

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 1) {
            // Instant cast: raise a 5-block curved protective wall in front
            raiseCurvedWall(player, def, 3.5, 5);
        } else if (timeline.phase() == SkillTimeline.Phase.HOLD) {
            // Channeled cast: continuously sweeps and places wall segments along cursor
            int t = timeline.ticksInPhase();
            if (t % 3 == 0) {
                if (data.trySpendChi(2)) {
                    channelWallSegment(player, def, 3.8);
                } else {
                    timeline.releaseHold();
                }
            }
        }
    }

    private static void raiseCurvedWall(ServerPlayerEntity player, SkillDefinition def, double radius, int segments) {
        ServerWorld world = player.getServerWorld();
        Vec3d eye = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        double centerYaw = Math.atan2(look.z, look.x);

        double arcSpread = Math.PI * 0.45; // ~80 degree defensive arc
        double step = arcSpread / (segments - 1);
        double startAngle = centerYaw - (arcSpread / 2.0);

        BlockPos groundRef = ElementalInteractions.findSolidGroundBelow(world, player.getBlockPos(), 6);
        BlockState groundState = world.getBlockState(groundRef);
        if (groundState.isAir()) groundState = Blocks.STONE.getDefaultState();

        for (int i = 0; i < segments; i++) {
            double angle = startAngle + (i * step);
            Vec3d wallPos = player.getPos().add(Math.cos(angle) * radius, 0, Math.sin(angle) * radius);
            wallPos = snapToGround(world, wallPos);
            eruptWallSegment(world, player, wallPos, groundState);
        }

        // Deflect incoming projectiles across defensive arc
        ElementalInteractions.deflectProjectiles(world, player, eye, look, radius + 2.0, 1.4);
    }

    private static void channelWallSegment(ServerPlayerEntity player, SkillDefinition def, double radius) {
        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d wallPos = player.getPos().add(look.x * radius, 0, look.z * radius);
        wallPos = snapToGround(world, wallPos);

        BlockPos groundRef = ElementalInteractions.findSolidGroundBelow(world, BlockPos.ofFloored(wallPos), 6);
        BlockState groundState = world.getBlockState(groundRef);
        if (groundState.isAir()) groundState = Blocks.STONE.getDefaultState();

        eruptWallSegment(world, player, wallPos, groundState);
    }

    private static void eruptWallSegment(ServerWorld world, ServerPlayerEntity player, Vec3d pos, BlockState state) {
        BlockPos bp = BlockPos.ofFloored(pos);

        // Sound of tectonic stone shifting
        world.playSound(null, bp, SoundEvents.BLOCK_STONE_PLACE, SoundCategory.PLAYERS, 1.2f, 0.75f);
        world.playSound(null, bp, SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 0.9f, 0.9f);

        // Dense stone and dust eruption particles
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, state),
                pos.x, pos.y + 0.8, pos.z, 20, 0.4, 0.8, 0.4, 0.08);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                pos.x, pos.y + 0.5, pos.z, 10, 0.3, 0.5, 0.3, 0.05);
        world.spawnParticles(AvatarParticles.DUST,
                pos.x, pos.y + 0.2, pos.z, 12, 0.4, 0.3, 0.4, 0.03);

        // Knock back any mobs attempting to breach the wall position
        Box box = Box.of(pos.add(0, 0.75, 0), 1.8, 2.0, 1.8);
        List<LivingEntity> mobs = world.getEntitiesByClass(LivingEntity.class, box, e -> e != player && e.isAlive());
        for (LivingEntity mob : mobs) {
            Vec3d push = mob.getPos().subtract(player.getPos()).normalize().multiply(0.8);
            mob.addVelocity(push.x, 0.2, push.z);
            mob.velocityModified = true;
        }

        // Clear loose surface vegetation
        ElementalInteractions.clearVegetation(world, pos, 1.5);
    }

    private static Vec3d snapToGround(ServerWorld world, Vec3d pos) {
        BlockPos bp = BlockPos.ofFloored(pos);
        for (int dy = 3; dy >= -6; dy--) {
            BlockPos check = bp.add(0, dy, 0);
            if (!world.getBlockState(check).getCollisionShape(world, check).isEmpty()) {
                return new Vec3d(pos.x, check.getY() + 1.0, pos.z);
            }
        }
        return pos;
    }

    private EarthWallSkill() {}
}
