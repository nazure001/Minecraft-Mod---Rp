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
        if (target instanceof net.minecraft.server.network.ServerPlayerEntity sp) {
            var data = com.avatarmod.elements.data.PlayerBendingData.get(sp);
            if (data != null && "FIRE".equals(data.getActiveElement())) {
                return; // Firebenders are immune to fire ignition
            }
        }
        target.setOnFireForTicks(fireTicks);
    }

    /**
     * Ignites flammable blocks or places fire on solid surfaces within an AOE.
     */
    public static void igniteBlocks(ServerWorld world, Vec3d center, double radius) {
        igniteBlocks(world, center, radius, null);
    }

    /**
     * Ignites flammable blocks or places fire on solid surfaces within an AOE,
     * protecting the caster from having fire placed under their own feet.
     */
    public static void igniteBlocks(ServerWorld world, Vec3d center, double radius, LivingEntity caster) {
        BlockPos base = BlockPos.ofFloored(center);
        int r = (int) Math.ceil(radius);
        double rSq = radius * radius;

        for (int x = -r; x <= r; x++) {
            for (int y = -1; y <= 2; y++) {
                for (int z = -r; z <= r; z++) {
                    if (x * x + z * z > rSq) continue;
                    BlockPos p = base.add(x, y, z);
                    // Do not ignite the block the caster is standing on or near their feet
                    if (caster != null && p.getSquaredDistance(caster.getPos()) < 2.5) {
                        continue;
                    }
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
     * Calculates bonus damage based on the hardness of the earth block extracted.
     * Formula: min(15.0f, Hardness * 1.5f)
     * Dirt (0.5) -> +0.75 dmg
     * Stone (1.5) -> +2.25 dmg
     * Cobble (2.0) -> +3.0 dmg
     * Deepslate (3.0-4.5) -> +4.5 - +6.75 dmg
     * Obsidian (50.0) -> capped at +15.0 dmg
     */
    public static float computeHardnessDamageBonus(float hardness) {
        if (hardness < 0) hardness = 5.0f; // Unbreakable fallback (e.g. Bedrock)
        return Math.min(15.0f, hardness * 1.5f);
    }

    public static float calculateEarthHardnessDamage(ServerWorld world, BlockPos groundPos, float baseDamage) {
        BlockState state = world.getBlockState(groundPos);
        float hardness = state.getHardness(world, groundPos);
        return baseDamage + computeHardnessDamageBonus(hardness);
    }

    /**
     * Scans downwards from startPos to locate the nearest solid opaque block.
     */
    public static BlockPos findSolidGroundBelow(ServerWorld world, BlockPos startPos, int maxDepth) {
        BlockPos current = startPos;
        for (int i = 0; i < maxDepth; i++) {
            BlockState state = world.getBlockState(current);
            if (!state.isAir() && state.getFluidState().isEmpty() && !state.getCollisionShape(world, current).isEmpty()) {
                return current;
            }
            current = current.down();
        }
        return startPos.down();
    }

    /**
     * Applies seismic stagger slowness to target caught in earth eruption/shockwave.
     */
    public static void applySeismicStagger(LivingEntity target, int ticks) {
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, ticks, 1, false, false, true));
    }

    // --- ICE & FREEZING INTERACTIONS ---

    /**
     * Transforms water into frosted ice (which naturally melts over time) and dusts surfaces with snow.
     */
    public static void freezeWaterArea(ServerWorld world, Vec3d center, double radius) {
        BlockPos base = BlockPos.ofFloored(center);
        int r = (int) Math.ceil(radius);
        double rSq = radius * radius;

        for (int x = -r; x <= r; x++) {
            for (int y = -1; y <= 1; y++) {
                for (int z = -r; z <= r; z++) {
                    if (x * x + z * z > rSq) continue;
                    BlockPos p = base.add(x, y, z);
                    BlockState state = world.getBlockState(p);
                    if (state.isOf(Blocks.WATER)) {
                        world.setBlockState(p, Blocks.FROSTED_ICE.getDefaultState());
                        world.playSound(null, p, SoundEvents.BLOCK_GLASS_BREAK, SoundCategory.BLOCKS, 0.6f, 1.4f);
                        world.spawnParticles(ParticleTypes.SNOWFLAKE, p.getX() + 0.5, p.getY() + 0.5, p.getZ() + 0.5, 4, 0.2, 0.2, 0.2, 0.02);
                    }
                }
            }
        }
    }

    /**
     * Applies freeze ticks (Powder snow freezing visual) and slowness to target.
     */
    public static void applyFreezing(LivingEntity target, int freezeTicks, int slownessTicks) {
        target.setFrozenTicks(Math.max(target.getFrozenTicks(), freezeTicks));
        target.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, slownessTicks, 1, false, true, true));
        if (target.getWorld() instanceof ServerWorld sw) {
            sw.spawnParticles(ParticleTypes.SNOWFLAKE, target.getX(), target.getY() + 1.0, target.getZ(), 8, 0.3, 0.4, 0.3, 0.03);
            sw.playSound(null, target.getBlockPos(), SoundEvents.ENTITY_PLAYER_HURT_FREEZE, SoundCategory.PLAYERS, 0.8f, 1.2f);
        }
    }

    // --- WEAPON AFFINITY & BENDING SYNERGY ---

    /**
     * Checks if the held weapon matches and amplifies the active bending element:
     * - Fire: Zuko Dual Broadswords (DualSwordsItem)
     * - Earth: Earth Kingdom Warhammer (EarthHammerItem)
     * - Air: Kyoshi War Fan (WarFanItem) or Air Nomad Staff (AirStaffItem)
     * - Water: Water Tribe Harpoon Spear (WaterSpearItem)
     */
    public static boolean isWeaponAffinity(net.minecraft.item.ItemStack stack, String element) {
        if (stack == null || stack.isEmpty() || element == null) return false;
        var item = stack.getItem();
        return switch (element.toUpperCase()) {
            case "FIRE"  -> item instanceof com.avatarmod.elements.item.DualSwordsItem;
            case "EARTH" -> item instanceof com.avatarmod.elements.item.EarthHammerItem;
            case "AIR"   -> item instanceof com.avatarmod.elements.item.WarFanItem || item instanceof com.avatarmod.elements.item.AirStaffItem;
            case "WATER" -> item instanceof com.avatarmod.elements.item.WaterSpearItem;
            default      -> false;
        };
    }

    public static float getWeaponDamageMultiplier(net.minecraft.item.ItemStack stack, String element) {
        return isWeaponAffinity(stack, element) ? 1.25f : 1.0f;
    }

    public static float getWeaponSpeedMultiplier(net.minecraft.item.ItemStack stack, String element) {
        return isWeaponAffinity(stack, element) ? 1.20f : 1.0f;
    }

    /**
     * Identifies bendable earth materials that earthbenders can shape, burrow through, or fling:
     * - Overworld rock, dirt, sand, terracotta, mud, clay, gravel, sandstone, and standard ores.
     * Explicitly protects unbreakable or complex blocks (Bedrock, Obsidian, Barriers, Tile Entities).
     */
    public static boolean isBendableEarth(BlockState state) {
        if (state == null || state.isAir() || state.hasBlockEntity()) return false;
        if (state.isOf(Blocks.BEDROCK) || state.isOf(Blocks.OBSIDIAN) || state.isOf(Blocks.BARRIER)) return false;
        return state.isIn(BlockTags.BASE_STONE_OVERWORLD)
                || state.isIn(BlockTags.DIRT)
                || state.isIn(BlockTags.SAND)
                || state.isIn(BlockTags.TERRACOTTA)
                || isOreBlock(state)
                || state.isOf(Blocks.GRAVEL)
                || state.isOf(Blocks.COBBLESTONE)
                || state.isOf(Blocks.COBBLED_DEEPSLATE)
                || state.isOf(Blocks.CLAY)
                || state.isOf(Blocks.MUD)
                || state.isOf(Blocks.SANDSTONE)
                || state.isOf(Blocks.RED_SANDSTONE)
                || state.isOf(Blocks.MUD_BRICKS)
                || state.isOf(Blocks.NETHERRACK)
                || state.isOf(Blocks.SOUL_SAND)
                || state.isOf(Blocks.SOUL_SOIL)
                || state.isOf(Blocks.BLACKSTONE);
    }

    /**
     * Detects mineral and metal ores to ensure valuable resources drop rather than being pulverized.
     */
    public static boolean isOreBlock(BlockState state) {
        if (state == null) return false;
        return state.isIn(BlockTags.COAL_ORES)
                || state.isIn(BlockTags.IRON_ORES)
                || state.isIn(BlockTags.COPPER_ORES)
                || state.isIn(BlockTags.GOLD_ORES)
                || state.isIn(BlockTags.REDSTONE_ORES)
                || state.isIn(BlockTags.LAPIS_ORES)
                || state.isIn(BlockTags.DIAMOND_ORES)
                || state.isIn(BlockTags.EMERALD_ORES)
                || state.isOf(Blocks.ANCIENT_DEBRIS);
    }
}
