package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Earth Wall — Master Earthbending Defensive Terraforming Construct.
 *
 * Manipulates the REAL SURROUNDING BLOCKS of the terrain into a solid defensive wall:
 * 1. Samples the true geological surface block beneath each column (Grass, Dirt, Stone, Cobble, Sandstone, Deepslate).
 * 2. Directly raises real solid blocks into the world, forming an impenetrable curved barricade.
 * 3. Channeled cast (HOLD): Sweeps with player gaze to construct continuous tactical fortifications or circular fortresses.
 * 4. Anti-Griefing Reversion: Blocks automatically crumble back with dust particles and sound after their defensive duration.
 */
public final class EarthWallSkill {

    public static final int WALL_DURATION_TICKS = 240; // 12 seconds defensive barricade
    public static final int MAX_WALL_BLOCKS_PER_PLAYER = 48;

    public record WallBlockRecord(
            BlockPos pos,
            BlockState originalState,
            BlockState wallState,
            long expiryTick,
            UUID casterUuid
    ) {}

    private static final Map<BlockPos, WallBlockRecord> ACTIVE_WALL_BLOCKS = new ConcurrentHashMap<>();
    private static final Map<UUID, List<BlockPos>> PLAYER_WALL_INDEX = new ConcurrentHashMap<>();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 0) {
            // Instant cast: raise a 5-block curved protective wall of real blocks
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

        boolean hasHammer = ElementalInteractions.isWeaponAffinity(player.getMainHandStack(), "EARTH");
        int height = hasHammer ? 3 : 2;

        for (int i = 0; i < segments; i++) {
            double angle = startAngle + (i * step);
            Vec3d wallPos = player.getPos().add(Math.cos(angle) * radius, 0, Math.sin(angle) * radius);
            BlockPos ground = snapToGround(world, wallPos);
            eruptRealWallColumn(world, player, ground, height);
        }

        // Deflect incoming projectiles across defensive arc
        ElementalInteractions.deflectProjectiles(world, player, eye, look, radius + 2.0, 1.4);
    }

    private static void channelWallSegment(ServerPlayerEntity player, SkillDefinition def, double radius) {
        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d wallPos = player.getPos().add(look.x * radius, 0, look.z * radius);
        BlockPos ground = snapToGround(world, wallPos);

        boolean hasHammer = ElementalInteractions.isWeaponAffinity(player.getMainHandStack(), "EARTH");
        int height = hasHammer ? 3 : 2;

        eruptRealWallColumn(world, player, ground, height);
    }

    private static void eruptRealWallColumn(ServerWorld world, ServerPlayerEntity player, BlockPos ground, int height) {
        if (ground == null) return;

        BlockState surfaceState = world.getBlockState(ground);
        BlockState wallState = deriveWallBlock(surfaceState);

        long expiryTick = world.getTime() + WALL_DURATION_TICKS;
        UUID casterUuid = player.getUuid();

        List<BlockPos> playerBlocks = PLAYER_WALL_INDEX.computeIfAbsent(casterUuid, k -> new ArrayList<>());

        for (int dy = 1; dy <= height; dy++) {
            BlockPos targetPos = ground.up(dy);
            BlockState existing = world.getBlockState(targetPos);

            // Only replace air, liquid, or non-solid replaceable blocks
            if (existing.isAir() || !existing.getFluidState().isEmpty() || existing.isReplaceable()) {
                if (ACTIVE_WALL_BLOCKS.containsKey(targetPos)) {
                    // Refresh existing wall block
                    ACTIVE_WALL_BLOCKS.put(targetPos, new WallBlockRecord(targetPos, existing, wallState, expiryTick, casterUuid));
                    continue;
                }

                // If player exceeded max blocks, crumble oldest
                if (playerBlocks.size() >= MAX_WALL_BLOCKS_PER_PLAYER) {
                    BlockPos oldest = playerBlocks.remove(0);
                    crumbleSingleBlock(world, oldest);
                }

                world.setBlockState(targetPos, wallState, Block.NOTIFY_ALL);
                ACTIVE_WALL_BLOCKS.put(targetPos, new WallBlockRecord(targetPos, existing, wallState, expiryTick, casterUuid));
                playerBlocks.add(targetPos);

                // Particle explosion of the derived rock/soil
                world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, wallState),
                        targetPos.getX() + 0.5, targetPos.getY() + 0.5, targetPos.getZ() + 0.5,
                        18, 0.35, 0.35, 0.35, 0.08);
                world.spawnParticles(AvatarParticles.STONE_CHIP,
                        targetPos.getX() + 0.5, targetPos.getY() + 0.5, targetPos.getZ() + 0.5,
                        8, 0.25, 0.25, 0.25, 0.05);
                world.spawnParticles(AvatarParticles.DUST,
                        targetPos.getX() + 0.5, targetPos.getY() + 0.2, targetPos.getZ() + 0.5,
                        10, 0.3, 0.2, 0.3, 0.03);
            }
        }

        // Tectonic stone emergence sounds
        world.playSound(null, ground.up(1), SoundEvents.BLOCK_STONE_PLACE, SoundCategory.BLOCKS, 1.2f, 0.70f);
        world.playSound(null, ground.up(1), SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.BLOCKS, 1.0f, 0.85f);

        // Knock back any mobs inside or adjacent to the rising wall
        Box box = new Box(ground.getX() - 0.5, ground.getY(), ground.getZ() - 0.5,
                ground.getX() + 1.5, ground.getY() + height + 1.5, ground.getZ() + 1.5);
        List<LivingEntity> mobs = world.getEntitiesByClass(LivingEntity.class, box, e -> e != player && e.isAlive());
        for (LivingEntity mob : mobs) {
            Vec3d push = mob.getPos().subtract(player.getPos()).normalize().multiply(0.85);
            mob.addVelocity(push.x, 0.35, push.z);
            mob.velocityModified = true;
        }

        // Clear loose surface vegetation
        ElementalInteractions.clearVegetation(world, Vec3d.ofCenter(ground), 1.5);
    }

    /**
     * Derives an authentic real Minecraft block state based on the local terrain geology.
     */
    private static BlockState deriveWallBlock(BlockState ground) {
        if (ground == null || ground.isAir()) {
            return Blocks.COBBLESTONE.getDefaultState();
        }

        Block b = ground.getBlock();
        if (b == Blocks.GRASS_BLOCK || b == Blocks.DIRT || b == Blocks.COARSE_DIRT || b == Blocks.ROOTED_DIRT || b == Blocks.PODZOL) {
            return Blocks.DIRT.getDefaultState();
        } else if (b == Blocks.STONE || b == Blocks.COBBLESTONE || b == Blocks.STONE_BRICKS || b == Blocks.MOSSY_COBBLESTONE) {
            return Blocks.COBBLESTONE.getDefaultState();
        } else if (b == Blocks.DEEPSLATE || b == Blocks.COBBLED_DEEPSLATE || b == Blocks.DEEPSLATE_BRICKS) {
            return Blocks.COBBLED_DEEPSLATE.getDefaultState();
        } else if (b == Blocks.SAND || b == Blocks.SANDSTONE) {
            return Blocks.SANDSTONE.getDefaultState();
        } else if (b == Blocks.RED_SAND || b == Blocks.RED_SANDSTONE) {
            return Blocks.RED_SANDSTONE.getDefaultState();
        } else if (b == Blocks.MUD || b == Blocks.MUD_BRICKS || b == Blocks.PACKED_MUD) {
            return Blocks.MUD_BRICKS.getDefaultState();
        } else if (b == Blocks.ANDESITE || b == Blocks.POLISHED_ANDESITE) {
            return Blocks.ANDESITE.getDefaultState();
        } else if (b == Blocks.GRANITE || b == Blocks.POLISHED_GRANITE) {
            return Blocks.GRANITE.getDefaultState();
        } else if (b == Blocks.DIORITE || b == Blocks.POLISHED_DIORITE) {
            return Blocks.DIORITE.getDefaultState();
        } else if (b == Blocks.TUFF || b == Blocks.POLISHED_TUFF) {
            return Blocks.TUFF.getDefaultState();
        } else if (b == Blocks.NETHERRACK || b == Blocks.BLACKSTONE) {
            return Blocks.BLACKSTONE.getDefaultState();
        } else if (b == Blocks.END_STONE || b == Blocks.END_STONE_BRICKS) {
            return Blocks.END_STONE_BRICKS.getDefaultState();
        }

        return Blocks.COBBLESTONE.getDefaultState();
    }

    private static BlockPos snapToGround(ServerWorld world, Vec3d pos) {
        BlockPos cursor = BlockPos.ofFloored(pos);
        if (!world.getBlockState(cursor).getCollisionShape(world, cursor).isEmpty()) {
            for (int dy = 0; dy <= 4; dy++) {
                BlockPos check = cursor.up(dy);
                if (world.getBlockState(check.up()).getCollisionShape(world, check.up()).isEmpty()) {
                    return check;
                }
            }
        }

        for (int dy = 0; dy >= -8; dy--) {
            BlockPos check = cursor.add(0, dy, 0);
            if (!world.getBlockState(check).getCollisionShape(world, check).isEmpty()) {
                return check;
            }
        }
        return cursor.down();
    }

    public static void tickAllWalls(MinecraftServer server) {
        long time = -1;
        List<BlockPos> expired = new ArrayList<>();

        for (WallBlockRecord record : ACTIVE_WALL_BLOCKS.values()) {
            if (time < 0) {
                ServerWorld overworld = server.getOverworld();
                if (overworld != null) time = overworld.getTime();
                else return;
            }
            if (time >= record.expiryTick()) {
                expired.add(record.pos());
            }
        }

        for (BlockPos pos : expired) {
            for (ServerWorld world : server.getWorlds()) {
                if (world.isChunkLoaded(pos)) {
                    crumbleSingleBlock(world, pos);
                    break;
                }
            }
        }
    }

    private static void crumbleSingleBlock(ServerWorld world, BlockPos pos) {
        WallBlockRecord record = ACTIVE_WALL_BLOCKS.remove(pos);
        if (record == null) return;

        List<BlockPos> list = PLAYER_WALL_INDEX.get(record.casterUuid());
        if (list != null) list.remove(pos);

        // Revert back to original state (Air / vegetation)
        world.setBlockState(pos, record.originalState(), Block.NOTIFY_ALL);

        // Crumbly disintegration particles and audio
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, record.wallState()),
                pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5,
                16, 0.35, 0.35, 0.35, 0.08);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5,
                10, 0.25, 0.25, 0.25, 0.05);
        world.spawnParticles(AvatarParticles.DUST,
                pos.getX() + 0.5, pos.getY() + 0.2, pos.getZ() + 0.5,
                12, 0.3, 0.2, 0.3, 0.02);

        world.playSound(null, pos, SoundEvents.BLOCK_STONE_BREAK, SoundCategory.BLOCKS, 0.8f, 0.8f);
    }

    public static void clear(UUID casterUuid) {
        List<BlockPos> blocks = PLAYER_WALL_INDEX.remove(casterUuid);
        if (blocks != null) {
            for (BlockPos pos : blocks) {
                ACTIVE_WALL_BLOCKS.remove(pos);
            }
        }
    }

    private EarthWallSkill() {}
}
