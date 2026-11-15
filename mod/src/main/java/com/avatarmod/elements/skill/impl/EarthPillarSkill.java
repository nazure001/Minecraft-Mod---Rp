package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
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
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Earth Pillar — instant skill. A stone column erupts from the ground under the
 * nearest target in front of the caster (or at max range if nothing is hit),
 * damaging entities in its footprint and launching them upward.
 * Does NOT modify world blocks (prototype rule); the column is VFX-only.
 */
public final class EarthPillarSkill {

    private static final float FOOTPRINT_RADIUS = 1.6f;   // blocks around pillar center
    private static final float LAUNCH_VELOCITY = 1.05f;    // upward boost (~4-5 block hop)
    private static final float PILLAR_HEIGHT = 2.5f;      // visual column height
    private static final int   GROUND_SEARCH_DEPTH = 4;   // blocks to scan down for ground

    // Pillar center per caster, kept while ACTIVE phase animates the eruption
    private static final Map<UUID, Vec3d> ACTIVE_PILLARS = new ConcurrentHashMap<>();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) {
            ACTIVE_PILLARS.remove(player.getUuid());
            return;
        }

        ServerWorld world = player.getServerWorld();

        if (timeline.ticksInPhase() == 0) {
            Vec3d center = findPillarCenter(player, world, def.range());
            ACTIVE_PILLARS.put(player.getUuid(), center);
            erupt(player, world, center, def);
        }

        // Rising dust column over the short ACTIVE window
        Vec3d center = ACTIVE_PILLARS.get(player.getUuid());
        if (center != null) {
            spawnColumnParticles(world, center, timeline.ticksInPhase());
        }
    }

    /**
     * Walks the caster's horizontal look direction in 1-block steps up to range.
     * Returns the ground-snapped position of the first living entity found,
     * or the ground-snapped point at max range when nothing is in the path.
     */
    private static Vec3d findPillarCenter(ServerPlayerEntity player, ServerWorld world, float range) {
        Vec3d origin = player.getPos();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d dir = new Vec3d(look.x, 0, look.z);
        if (dir.lengthSquared() < 1.0e-4) dir = Vec3d.fromPolar(0, player.getYaw());
        dir = dir.normalize();

        for (double d = 1.5; d <= range; d += 1.0) {
            Vec3d probe = origin.add(dir.multiply(d));
            Box box = Box.of(probe.add(0, 1, 0), 2.2, 3.0, 2.2);
            List<LivingEntity> hits = world.getEntitiesByClass(
                    LivingEntity.class, box, e -> e != player && e.isAlive());
            if (!hits.isEmpty()) {
                LivingEntity target = hits.get(0);
                return snapToGround(world, target.getPos());
            }
        }
        return snapToGround(world, origin.add(dir.multiply(range)));
    }

    /** Snaps a position down to the first solid block surface below it. */
    private static Vec3d snapToGround(ServerWorld world, Vec3d pos) {
        BlockPos cursor = BlockPos.ofFloored(pos);
        for (int i = 0; i <= GROUND_SEARCH_DEPTH; i++) {
            BlockPos below = cursor.down(i);
            if (!world.getBlockState(below).getCollisionShape(world, below).isEmpty()) {
                return new Vec3d(pos.x, below.getY() + 1.0, pos.z);
            }
        }
        return pos;
    }

    private static void erupt(ServerPlayerEntity player, ServerWorld world, Vec3d center, SkillDefinition def) {
        // Damage + upward launch for everything standing in the footprint
        Box footprint = new Box(
                center.x - FOOTPRINT_RADIUS, center.y - 0.5, center.z - FOOTPRINT_RADIUS,
                center.x + FOOTPRINT_RADIUS, center.y + PILLAR_HEIGHT + 0.5, center.z + FOOTPRINT_RADIUS);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, footprint, e -> e != player && e.isAlive());

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());
            Vec3d vel = target.getVelocity();
            target.setVelocity(vel.x * 0.4, LAUNCH_VELOCITY, vel.z * 0.4);
            target.velocityModified = true;
        }

        // Eruption VFX: crack burst of the actual ground block + dust ring
        BlockPos groundPos = BlockPos.ofFloored(center.subtract(0, 0.5, 0));
        BlockState ground = world.getBlockState(groundPos);
        if (!ground.isAir()) {
            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, ground),
                    center.x, center.y + 0.3, center.z,
                    40, FOOTPRINT_RADIUS * 0.5, 0.4, FOOTPRINT_RADIUS * 0.5, 0.15);
        }
        world.spawnParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE,
                center.x, center.y + 0.1, center.z,
                6, FOOTPRINT_RADIUS * 0.6, 0.1, FOOTPRINT_RADIUS * 0.6, 0.01);

        // Heavy stone SFX
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 1.3f, 0.6f);
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_GRAVEL_BREAK, SoundCategory.PLAYERS, 1.0f, 0.7f);
    }

    /** Rising volumetric pillar column with core + perimeter rings at multiple heights. */
    private static void spawnColumnParticles(ServerWorld world, Vec3d center, int tickInActive) {
        double maxHeight = Math.min(PILLAR_HEIGHT, 1.0 + tickInActive * 1.0);
        BlockPos groundPos = BlockPos.ofFloored(center.subtract(0, 0.5, 0));
        BlockState ground = world.getBlockState(groundPos);
        if (ground.isAir()) {
            ground = net.minecraft.block.Blocks.STONE.getDefaultState();
        }

        BlockStateParticleEffect dust = new BlockStateParticleEffect(ParticleTypes.BLOCK, ground);

        // Render stacked horizontal cross-sections from ground up to current height
        for (double h = 0.2; h <= maxHeight; h += 0.6) {
            // Core pillar center
            world.spawnParticles(dust, center.x, center.y + h, center.z, 4, 0.15, 0.15, 0.15, 0.05);

            // Perimeter ring
            int points = 12;
            for (int i = 0; i < points; i++) {
                double angle = (Math.PI * 2 * i) / points;
                double px = center.x + Math.cos(angle) * (FOOTPRINT_RADIUS * 0.6);
                double pz = center.z + Math.sin(angle) * (FOOTPRINT_RADIUS * 0.6);
                world.spawnParticles(dust, px, center.y + h, pz, 2, 0.08, 0.15, 0.08, 0.04);
            }
        }

        // Top impact cap
        world.spawnParticles(ParticleTypes.POOF, center.x, center.y + maxHeight, center.z, 3, 0.3, 0.1, 0.3, 0.02);
    }

    private EarthPillarSkill() {}
}
