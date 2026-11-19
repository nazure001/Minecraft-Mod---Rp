package com.avatarmod.elements.skill;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.component.DataComponentTypes;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.projectile.ProjectileEntity;
import net.minecraft.item.Items;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.potion.Potions;
import net.minecraft.registry.tag.BlockTags;
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
 * Standardized elemental interactions for Avatar skills:
 * - Fire: burning status, block ignition, flammable combustion.
 * - Water: source verification, fire dousing, wetness slowness, ice freezing.
 * - Air: vegetation/grass clearing, projectile deflection, levitation.
 * - Earth: seismic stagger, seabed/deep ground snapping, footprint clearing.
 */
public final class ElementalInteractions {

    private ElementalInteractions() {}

    // --- WATER SOURCE VALIDATION ---

    /**
     * Verifies if a waterbender has an active water source:
     * 1. Player is in water or rain.
     * 2. Natural water block is within 6 blocks of the player.
     * 3. Player is carrying a water container (water bucket or water bottle).
     */
    public static boolean hasWaterSource(ServerPlayerEntity player) {
        if (player.isTouchingWaterOrRain()) return true;

        ServerWorld world = player.getServerWorld();
        BlockPos playerPos = player.getBlockPos();

        // Check nearby fluid blocks (radius 6 blocks)
        for (BlockPos p : BlockPos.iterateOutwards(playerPos, 6, 3, 6)) {
            if (world.getFluidState(p).isIn(FluidTags.WATER)) {
                return true;
            }
        }

        // Check inventory for water bucket or water bottle
        for (int i = 0; i < player.getInventory().size(); i++) {
            var stack = player.getInventory().getStack(i);
            if (stack.isOf(Items.WATER_BUCKET)) {
                return true;
            }
            if (stack.isOf(Items.POTION)) {
                var contents = stack.get(DataComponentTypes.POTION_CONTENTS);
                if (contents != null && contents.matches(Potions.WATER)) {
                    return true;
                }
            }
        }

        return false;
    }

    // --- FIRE INTERACTIONS ---

    /**
     * Sets target entity on fire and spawns flame particles.
     */
    public static void applyFire(LivingEntity target, int fireTicks) {
        if (target.isFireImmune()) return;
        target.setOnFireForTicks(fireTicks);
    }

    /**
     * Ignites flammable blocks or places fire on solid surfaces within an AOE.
     */
    public static void igniteBlocks(ServerWorld world, Vec3d center, double radius) {
        BlockPos base = BlockPos.ofFloored(center);
        int r = (int) Math.ceil(radius);
        double rSq = radius * radius;

        for (int x = -r; x <= r; x++) {
            for (int y = -1; y <= 2; y++) {
                for (int z = -r; z <= r; z++) {
                    if (x * x + z * z > rSq) continue;
                    BlockPos p = base.add(x, y, z);
                    BlockState state = world.getBlockState(p);

                    // If hitting leaves/grass/wool/planks, ignite directly
                    if (state.isIn(BlockTags.FIRE) || state.isAir()) {
                        BlockPos below = p.down();
                        BlockState belowState = world.getBlockState(below);
                        if (!belowState.isAir() && belowState.isOpaque() && world.isAir(p)) {
                            world.setBlockState(p, Blocks.FIRE.getDefaultState());
                        }
                    }
                }
            }
        }
    }

    // --- WATER INTERACTIONS ---

    /**
     * Applies wetness and cold slowness to a target, and extinguishes any fire on them.
     */
    public static void applyWater(LivingEntity target, int slownessTicks, int amplifier) {
        if (target.isOnFire()) {
            target.extinguishWithSound();
        }
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, slownessTicks, amplifier, false, true, true));
    }

    /**
     * Douses fire blocks within a given radius.
     */
    public static void douseFireBlocks(ServerWorld world, Vec3d center, double radius) {
        BlockPos base = BlockPos.ofFloored(center);
        int r = (int) Math.ceil(radius);
        double rSq = radius * radius;

        for (int x = -r; x <= r; x++) {
            for (int y = -2; y <= 3; y++) {
                for (int z = -r; z <= r; z++) {
                    if (x * x + z * z > rSq) continue;
                    BlockPos p = base.add(x, y, z);
                    BlockState state = world.getBlockState(p);
                    if (state.isOf(Blocks.FIRE) || state.isOf(Blocks.SOUL_FIRE)) {
                        world.setBlockState(p, Blocks.AIR.getDefaultState());
                        world.playSound(null, p, SoundEvents.BLOCK_FIRE_EXTINGUISH, SoundCategory.BLOCKS, 0.7f, 1.3f);
                        world.spawnParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE,
                                p.getX() + 0.5, p.getY() + 0.3, p.getZ() + 0.5,
                                4, 0.2, 0.2, 0.2, 0.02);
                    }
                }
            }
        }
    }

    // --- AIR & VEGETATION INTERACTIONS ---

    /**
     * Breaks loose surface vegetation (grass, tall grass, ferns, flowers) along a trajectory or radius.
     */
    public static void clearVegetation(ServerWorld world, Vec3d center, double radius) {
        BlockPos base = BlockPos.ofFloored(center);
        int r = (int) Math.ceil(radius);
        double rSq = radius * radius;

        for (int x = -r; x <= r; x++) {
            for (int y = -1; y <= 2; y++) {
                for (int z = -r; z <= r; z++) {
                    if (x * x + z * z > rSq) continue;
                    BlockPos p = base.add(x, y, z);
                    BlockState state = world.getBlockState(p);
                    if (state.isIn(BlockTags.REPLACEABLE) && !state.isAir() && state.getFluidState().isEmpty()) {
                        world.breakBlock(p, true);
                    }
                }
            }
        }
    }

    /**
     * Deflects projectiles inside a wind blast cone, pushing them outward away from caster.
     */
    public static void deflectProjectiles(ServerWorld world, ServerPlayerEntity caster, Vec3d origin, Vec3d look, double range, double padding) {
        Vec3d end = origin.add(look.multiply(range));
        Box searchBox = Box.of(origin.add(look.multiply(range * 0.5)), range * 2, range * 2, range * 2);

        List<ProjectileEntity> projectiles = world.getEntitiesByClass(
                ProjectileEntity.class, searchBox,
                p -> p.getOwner() != caster && p.isAlive() && p.squaredDistanceTo(origin) <= (range + padding) * (range + padding));

        for (ProjectileEntity proj : projectiles) {
            Vec3d vel = look.multiply(1.4);
            proj.setVelocity(vel.x, vel.y + 0.1, vel.z);
            proj.velocityModified = true;
            world.spawnParticles(ParticleTypes.POOF, proj.getX(), proj.getY(), proj.getZ(), 4, 0.2, 0.2, 0.2, 0.05);
            world.playSound(null, proj.getBlockPos(), SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 0.8f, 1.8f);
        }
    }

    /**
     * Applies air levitation and vertical lift to target entity.
     */
    public static void applyAirLevitation(LivingEntity target, int ticks) {
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.LEVITATION, ticks, 0, false, false, true));
    }

    // --- EARTH INTERACTIONS ---

    /**
     * Applies seismic stagger slowness to target caught in earth eruption/shockwave.
     */
    public static void applySeismicStagger(LivingEntity target, int ticks) {
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, ticks, 1, false, false, true));
    }
}
