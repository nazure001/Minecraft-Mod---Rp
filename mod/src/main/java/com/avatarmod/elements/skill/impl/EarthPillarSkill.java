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
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.registry.tag.FluidTags;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import com.avatarmod.elements.network.SkillNetworking;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Earth Pillar & Earth Wall — interactive martial arts stone construct.
 *
 * Lifecycle & Manipulation:
 * 1. Deep Ground / Seabed Snapping: Erupts from the true solid rock/seabed even when cast in deep water or rivers.
 * 2. Stance-Based Formation:
 *    - Normal Cast (Standing): Erupts 1 single Pillar (cost: 15 Chi).
 *    - Sneak Cast (Shift + C): Erupts an Earth Wall (3 connected pillars forming a defensive curved barricade).
 * 3. Manipulation — Tendang Sekali (Power Kick):
 *    Launches the pillar(s) as high-velocity flying megalith boulder projectiles (16.0 dmg + seismic shockwave).
 *    If an Earth Wall was raised, launches a 3-boulder Megalith Wave!
 * 4. Manipulation — Bertubi-tubi (Rapid Barrage):
 *    Punches the wall/pillar into a volley of razor-sharp stone shards (4.0 dmg each).
 */
public final class EarthPillarSkill {

    public static final float FOOTPRINT_RADIUS = 1.6f;
    public static final float LAUNCH_VELOCITY = 1.05f;
    public static final float PILLAR_HEIGHT = 2.5f;
    public static final int   GROUND_SEARCH_DEPTH = 24;   // Deep scan through air & water to find true seabed/ground
    public static final int   PILLAR_DURATION_TICKS = 140; // 7.0 seconds interactive stance
    public static final int   PILLAR_MAX_HITS = 4;        // 4 rapid barrage strikes
    public static final double INTERACTION_RADIUS = 6.0;   // Blocks distance to interact

    public static final float MEGALITH_SPEED = 1.4f;
    public static final float MEGALITH_DAMAGE = 16.0f;
    public static final float MEGALITH_AOE = 2.5f;
    public static final float MEGALITH_KNOCKBACK = 1.4f;
    public static final int   MEGALITH_LIFETIME = 30;

    public static final float SHARD_SPEED = 1.8f;
    public static final float SHARD_DAMAGE = 4.0f;
    public static final int   SHARD_LIFETIME = 20;

    public static final class ActivePillar {
        private final UUID id;
        private final UUID casterUuid;
        private final List<Vec3d> positions;
        private final BlockState blockState;
        private int remainingTicks;
        private int hitsRemaining;

        public ActivePillar(UUID id, UUID casterUuid, List<Vec3d> positions, int remainingTicks, int hitsRemaining, BlockState blockState) {
            this.id = id;
            this.casterUuid = casterUuid;
            this.positions = new ArrayList<>(positions);
            this.remainingTicks = remainingTicks;
            this.hitsRemaining = hitsRemaining;
            this.blockState = blockState != null ? blockState : Blocks.STONE.getDefaultState();
        }

        public UUID id() { return id; }
        public UUID casterUuid() { return casterUuid; }
        public List<Vec3d> positions() { return positions; }
        public Vec3d center() { return positions.isEmpty() ? Vec3d.ZERO : positions.get(0); }
        public int remainingTicks() { return remainingTicks; }
        public int hitsRemaining() { return hitsRemaining; }
        public BlockState blockState() { return blockState; }
        public void decrementTicks() { this.remainingTicks--; }
        public void decrementHits() { this.hitsRemaining--; }
    }

    public record FlyingMegalith(
            UUID casterUuid,
            Vec3d pos,
            Vec3d velocity,
            int ticksLeft,
            float damage,
            float aoeRadius,
            float knockback,
            BlockState blockState
    ) {}

    public record FlyingShard(
            UUID casterUuid,
            Vec3d pos,
            Vec3d velocity,
            int ticksLeft,
            float damage,
            BlockState blockState
    ) {}

    private static final Map<UUID, ActivePillar> ACTIVE_PILLARS = new ConcurrentHashMap<>();
    private static final List<FlyingMegalith> FLYING_MEGALITHS = new CopyOnWriteArrayList<>();
    private static final List<FlyingShard> FLYING_SHARDS = new CopyOnWriteArrayList<>();
    private static final Random RNG = new Random();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();
        if (timeline.phase() != SkillTimeline.Phase.ACTIVE) {
            return;
        }

        ServerWorld world = player.getServerWorld();

        if (timeline.ticksInPhase() == 0) {
            // Check if player has an active pillar nearby to manipulate immediately
            if (hasNearbyPillar(player, INTERACTION_RADIUS)) {
                boolean manipulated;
                if (player.isSneaking() || player.isSprinting()) {
                    manipulated = kickPillar(player);
                } else {
                    manipulated = strikePillar(player);
                }
                if (manipulated) {
                    PlayerBendingData.get(player).regenChi(def.chiCost() / 2);
                    return;
                }
            }

            Vec3d center = findPillarCenter(player, world, def.range());
            List<Vec3d> positions = new ArrayList<>();
            positions.add(center);

            // Shift-Cast / Sneak Cast: Forms an Earth Wall (3 connected pillars)
            boolean isWall = player.isSneaking();
            if (isWall) {
                Vec3d look = player.getRotationVec(1.0f);
                Vec3d right = new Vec3d(-look.z, 0, look.x).normalize();
                Vec3d leftPos = snapToGround(world, center.subtract(right.multiply(1.8)));
                Vec3d rightPos = snapToGround(world, center.add(right.multiply(1.8)));
                positions.add(leftPos);
                positions.add(rightPos);
            }

            BlockPos groundPos = BlockPos.ofFloored(center);
            BlockState groundState = world.getBlockState(groundPos.down());
            if (groundState.isAir() || groundState.getFluidState().isIn(FluidTags.WATER)) {
                groundState = world.getBlockState(groundPos);
            }
            if (groundState.isAir() || groundState.getFluidState().isIn(FluidTags.WATER)) {
                groundState = Blocks.STONE.getDefaultState();
            }

            ActivePillar pillar = new ActivePillar(UUID.randomUUID(), player.getUuid(), positions, PILLAR_DURATION_TICKS, PILLAR_MAX_HITS, groundState);
            ACTIVE_PILLARS.put(player.getUuid(), pillar);

            int serial = SkillNetworking.currentSerial(player.getUuid());
            for (Vec3d pos : positions) {
                SkillNetworking.broadcastSkillPosition(player, "avatar:earth_pillar",
                        serial, pos.x, pos.y, pos.z);
                erupt(player, world, pos, def);
            }
        }

        ActivePillar active = ACTIVE_PILLARS.get(player.getUuid());
        if (active != null) {
            for (Vec3d pos : active.positions()) {
                spawnColumnParticles(world, pos, timeline.ticksInPhase());
            }
        }
    }

    public static ActivePillar getActivePillar(UUID casterUuid) {
        return ACTIVE_PILLARS.get(casterUuid);
    }

    public static ActivePillar findNearestPillar(ServerPlayerEntity player, double maxDist) {
        Vec3d eye = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        ActivePillar best = null;
        double bestDist = maxDist * maxDist;

        for (ActivePillar p : ACTIVE_PILLARS.values()) {
            for (Vec3d pos : p.positions()) {
                Vec3d toPillar = pos.add(0, 1.25, 0).subtract(eye);
                double distSq = toPillar.lengthSquared();
                if (distSq <= bestDist) {
                    if (distSq < 4.0 || toPillar.normalize().dotProduct(look) > 0.2) {
                        bestDist = distSq;
                        best = p;
                        break;
                    }
                }
            }
        }
        return best;
    }

    public static boolean hasNearbyPillar(ServerPlayerEntity player, double maxDist) {
        return findNearestPillar(player, maxDist) != null;
    }

    /**
     * Tendang Sekali (Single Power Kick / Megalith Wave) — launches all active pillars
     * forward as high-speed megalith projectiles towards the player's crosshair.
     */
    public static boolean kickPillar(ServerPlayerEntity player) {
        ActivePillar pillar = findNearestPillar(player, INTERACTION_RADIUS);
        if (pillar == null) return false;

        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d dir = new Vec3d(look.x, Math.max(-0.2, look.y), look.z).normalize();
        Vec3d vel = dir.multiply(MEGALITH_SPEED);

        BlockPos groundPos = BlockPos.ofFloored(pillar.center());
        float megalithDmg = ElementalInteractions.calculateEarthHardnessDamage(world, groundPos, MEGALITH_DAMAGE);

        ACTIVE_PILLARS.remove(pillar.casterUuid());

        // Launch all pillars in this construct (1 if pillar, 3 if earth wall)
        for (Vec3d pos : pillar.positions()) {
            Vec3d spawnPos = pos.add(0, 1.25, 0);
            FLYING_MEGALITHS.add(new FlyingMegalith(player.getUuid(), spawnPos, vel,
                    MEGALITH_LIFETIME, megalithDmg, MEGALITH_AOE, MEGALITH_KNOCKBACK, pillar.blockState()));

            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, pillar.blockState()),
                    spawnPos.x, spawnPos.y, spawnPos.z, 35, 0.6, 0.6, 0.6, 0.15);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    spawnPos.x, spawnPos.y, spawnPos.z, 25, 0.5, 0.5, 0.5, 0.2);
            world.spawnParticles(ParticleTypes.EXPLOSION,
                    spawnPos.x, spawnPos.y, spawnPos.z, 1, 0.1, 0.1, 0.1, 0.0);

            SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 0,
                    pos.x, pos.y, pos.z, dir.x, dir.y, dir.z);
        }

        world.playSound(null, groundPos,
                SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.55f);
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 2.0f, 0.6f);
        world.playSound(null, groundPos,
                SoundEvents.ENTITY_PLAYER_ATTACK_STRONG, SoundCategory.PLAYERS, 1.6f, 0.7f);

        return true;
    }

    /**
     * Bertubi-tubi (Rapid Barrage) — strikes the pillar/wall into a rapid spray of sharp stone shards.
     */
    public static boolean strikePillar(ServerPlayerEntity player) {
        ActivePillar pillar = findNearestPillar(player, INTERACTION_RADIUS);
        if (pillar == null) return false;

        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);

        BlockPos pPos = BlockPos.ofFloored(pillar.center());
        float shardDmg = ElementalInteractions.calculateEarthHardnessDamage(world, pPos, SHARD_DAMAGE);

        for (Vec3d pos : pillar.positions()) {
            Vec3d origin = pos.add(0, 1.25, 0);
            int shardCount = 3 + RNG.nextInt(2);
            for (int i = 0; i < shardCount; i++) {
                double spreadX = (RNG.nextDouble() - 0.5) * 0.18;
                double spreadY = (RNG.nextDouble() - 0.5) * 0.18;
                double spreadZ = (RNG.nextDouble() - 0.5) * 0.18;
                Vec3d shardDir = look.add(spreadX, spreadY, spreadZ).normalize();
                FLYING_SHARDS.add(new FlyingShard(player.getUuid(), origin,
                        shardDir.multiply(SHARD_SPEED), SHARD_LIFETIME, shardDmg, pillar.blockState()));
            }

            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, pillar.blockState()),
                    origin.x, origin.y, origin.z, 10, 0.2, 0.2, 0.2, 0.1);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    origin.x, origin.y, origin.z, 15, 0.3, 0.3, 0.3, 0.15);

            SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 1,
                    pos.x, pos.y, pos.z, look.x, look.y, look.z);
        }

        pillar.decrementHits();

        world.playSound(null, pPos,
                SoundEvents.BLOCK_STONE_HIT, SoundCategory.PLAYERS, 1.8f, 1.1f + (RNG.nextFloat() * 0.2f));
        world.playSound(null, pPos,
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 1.2f, 1.4f);

        if (pillar.hitsRemaining() <= 0) {
            crumblePillar(world, pillar);
        }

        return true;
    }

    private static void crumblePillar(ServerWorld world, ActivePillar pillar) {
        ACTIVE_PILLARS.remove(pillar.casterUuid());

        for (Vec3d pos : pillar.positions()) {
            Vec3d center = pos.add(0, 1.25, 0);
            BlockPos bp = BlockPos.ofFloored(center);

            world.playSound(null, bp,
                    SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 2.0f, 0.5f);
            world.playSound(null, bp,
                    SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 1.8f, 0.7f);

            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, pillar.blockState()),
                    center.x, center.y, center.z, 40, 0.7, 1.0, 0.7, 0.15);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    center.x, center.y, center.z, 25, 0.6, 0.8, 0.6, 0.15);
            world.spawnParticles(AvatarParticles.DUST,
                    center.x, center.y, center.z, 30, 0.8, 0.5, 0.8, 0.08);

            SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 2,
                    pos.x, pos.y, pos.z, 0, 0, 0);
        }
    }

    public static void tickAllPillars(MinecraftServer server) {
        List<UUID> toCrumble = new ArrayList<>();
        for (ActivePillar pillar : ACTIVE_PILLARS.values()) {
            pillar.decrementTicks();
            if (pillar.remainingTicks() <= 0) {
                toCrumble.add(pillar.casterUuid());
            } else if (pillar.remainingTicks() % 8 == 0) {
                for (ServerWorld world : server.getWorlds()) {
                    if (world.isChunkLoaded(BlockPos.ofFloored(pillar.center()))) {
                        for (Vec3d pos : pillar.positions()) {
                            world.spawnParticles(AvatarParticles.DUST,
                                    pos.x, pos.y + 0.2, pos.z,
                                    2, FOOTPRINT_RADIUS * 0.4, 0.1, FOOTPRINT_RADIUS * 0.4, 0.02);
                        }
                        break;
                    }
                }
            }
        }
        for (UUID id : toCrumble) {
            ActivePillar pillar = ACTIVE_PILLARS.get(id);
            if (pillar != null) {
                for (ServerWorld world : server.getWorlds()) {
                    if (world.isChunkLoaded(BlockPos.ofFloored(pillar.center()))) {
                        crumblePillar(world, pillar);
                        break;
                    }
                }
            }
        }

        // Advance flying megaliths
        List<FlyingMegalith> megalithsRemaining = new ArrayList<>();
        for (FlyingMegalith m : FLYING_MEGALITHS) {
            ServerPlayerEntity caster = server.getPlayerManager().getPlayer(m.casterUuid());
            ServerWorld world = caster != null ? caster.getServerWorld() : server.getOverworld();
            Vec3d nextPos = m.pos().add(m.velocity());

            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, m.blockState()),
                    m.pos().x, m.pos().y, m.pos().z, 8, 0.4, 0.4, 0.4, 0.05);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    m.pos().x, m.pos().y, m.pos().z, 5, 0.3, 0.3, 0.3, 0.05);
            world.spawnParticles(ParticleTypes.POOF,
                    m.pos().x, m.pos().y, m.pos().z, 2, 0.2, 0.2, 0.2, 0.01);

            Box hitBox = Box.of(nextPos, 1.8, 1.8, 1.8);
            List<LivingEntity> hits = world.getEntitiesByClass(
                    LivingEntity.class, hitBox, e -> (caster == null || e != caster) && e.isAlive());

            BlockPos blockPos = BlockPos.ofFloored(nextPos);
            boolean hitBlock = !world.getBlockState(blockPos).getCollisionShape(world, blockPos).isEmpty();

            if (!hits.isEmpty() || hitBlock) {
                detonateMegalith(world, caster, nextPos, m);
            } else if (m.ticksLeft() > 1) {
                megalithsRemaining.add(new FlyingMegalith(m.casterUuid(), nextPos, m.velocity(),
                        m.ticksLeft() - 1, m.damage(), m.aoeRadius(), m.knockback(), m.blockState()));
            } else {
                detonateMegalith(world, caster, nextPos, m);
            }
        }
        FLYING_MEGALITHS.clear();
        FLYING_MEGALITHS.addAll(megalithsRemaining);

        // Advance flying shards
        List<FlyingShard> shardsRemaining = new ArrayList<>();
        for (FlyingShard s : FLYING_SHARDS) {
            ServerPlayerEntity caster = server.getPlayerManager().getPlayer(s.casterUuid());
            ServerWorld world = caster != null ? caster.getServerWorld() : server.getOverworld();
            Vec3d nextPos = s.pos().add(s.velocity());

            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, s.blockState()),
                    s.pos().x, s.pos().y, s.pos().z, 2, 0.05, 0.05, 0.05, 0.01);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    s.pos().x, s.pos().y, s.pos().z, 2, 0.1, 0.1, 0.1, 0.02);

            Box hitBox = Box.of(nextPos, 0.8, 0.8, 0.8);
            List<LivingEntity> hits = world.getEntitiesByClass(
                    LivingEntity.class, hitBox, e -> (caster == null || e != caster) && e.isAlive());

            BlockPos blockPos = BlockPos.ofFloored(nextPos);
            boolean hitBlock = !world.getBlockState(blockPos).getCollisionShape(world, blockPos).isEmpty();

            if (!hits.isEmpty() || hitBlock) {
                detonateShard(world, caster, nextPos, hits, s.damage());
            } else if (s.ticksLeft() > 1) {
                shardsRemaining.add(new FlyingShard(s.casterUuid(), nextPos, s.velocity(),
                        s.ticksLeft() - 1, s.damage(), s.blockState()));
            } else {
                world.spawnParticles(AvatarParticles.STONE_CHIP, nextPos.x, nextPos.y, nextPos.z, 3, 0.1, 0.1, 0.1, 0.05);
            }
        }
        FLYING_SHARDS.clear();
        FLYING_SHARDS.addAll(shardsRemaining);
    }

    private static void detonateMegalith(ServerWorld world, ServerPlayerEntity caster, Vec3d pos, FlyingMegalith m) {
        Box aoeBox = Box.of(pos, m.aoeRadius() * 2, m.aoeRadius() * 2, m.aoeRadius() * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, aoeBox, e -> (caster == null || e != caster) && e.isAlive());

        DamageSource source = caster != null ? world.getDamageSources().playerAttack(caster) : world.getDamageSources().magic();
        for (LivingEntity target : targets) {
            target.damage(source, m.damage());
            ElementalInteractions.applySeismicStagger(target, 60);
            Vec3d diff = target.getPos().subtract(pos);
            Vec3d knockDir = diff.lengthSquared() < 0.001 ? new Vec3d(0, 1, 0) : diff.normalize();
            target.addVelocity(knockDir.x * m.knockback(), 0.35 + m.knockback() * 0.2, knockDir.z * m.knockback());
            target.velocityModified = true;
        }

        // Clear vegetation at impact site
        ElementalInteractions.clearVegetation(world, pos, m.aoeRadius());

        BlockPos bp = BlockPos.ofFloored(pos);
        world.playSound(null, bp, SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 2.0f, 0.7f);
        world.playSound(null, bp, SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 2.5f, 0.6f);
        world.playSound(null, bp, SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.5f);

        float hardness = m.blockState().getHardness(world, bp);
        if (hardness >= 10.0f) {
            world.playSound(null, bp, SoundEvents.BLOCK_ANVIL_LAND, SoundCategory.PLAYERS, 2.0f, 0.5f);
        }

        world.spawnParticles(ParticleTypes.EXPLOSION, pos.x, pos.y, pos.z, 2, 0.3, 0.3, 0.3, 0.0);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE, pos.x, pos.y, pos.z, 20, 0.6, 0.6, 0.6, 0.1);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, m.blockState()),
                pos.x, pos.y, pos.z, 50, 0.8, 0.8, 0.8, 0.2);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                pos.x, pos.y, pos.z, 35, 0.8, 0.8, 0.8, 0.2);
        world.spawnParticles(AvatarParticles.DUST,
                pos.x, pos.y, pos.z, 40, 1.0, 0.6, 1.0, 0.1);
    }

    private static void detonateShard(ServerWorld world, ServerPlayerEntity caster, Vec3d pos, List<LivingEntity> hits, float damage) {
        DamageSource source = caster != null ? world.getDamageSources().playerAttack(caster) : world.getDamageSources().magic();
        for (LivingEntity hit : hits) {
            hit.damage(source, damage);
            Vec3d vel = hit.getVelocity();
            hit.setVelocity(vel.x * 0.8, vel.y + 0.1, vel.z * 0.8);
            hit.velocityModified = true;
        }

        BlockPos bp = BlockPos.ofFloored(pos);
        world.playSound(null, bp, SoundEvents.BLOCK_STONE_HIT, SoundCategory.PLAYERS, 1.2f, 1.3f);
        world.spawnParticles(AvatarParticles.STONE_CHIP, pos.x, pos.y, pos.z, 8, 0.2, 0.2, 0.2, 0.1);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.COBBLESTONE.getDefaultState()),
                pos.x, pos.y, pos.z, 6, 0.15, 0.15, 0.15, 0.08);
    }

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

    /**
     * Deep ground scanning: scans down through air AND water/fluids up to 24 blocks
     * to find the true solid ground surface (rock/dirt/sand/gravel seabed).
     */
    private static Vec3d snapToGround(ServerWorld world, Vec3d pos) {
        BlockPos cursor = BlockPos.ofFloored(pos);

        // If cursor is buried deep inside solid block, scan upward to find top surface
        if (!world.getBlockState(cursor).getCollisionShape(world, cursor).isEmpty()) {
            for (int i = 0; i <= 8; i++) {
                BlockPos above = cursor.up(i);
                if (world.getBlockState(above).getCollisionShape(world, above).isEmpty()) {
                    return new Vec3d(pos.x, above.getY(), pos.z);
                }
            }
        }

        // Scan downward through air and water up to GROUND_SEARCH_DEPTH blocks to find true solid ground
        for (int i = 0; i <= GROUND_SEARCH_DEPTH; i++) {
            BlockPos below = cursor.down(i);
            BlockState state = world.getBlockState(below);
            // Solid ground has collision shape and is not liquid
            if (!state.getCollisionShape(world, below).isEmpty() && state.getFluidState().isEmpty()) {
                return new Vec3d(pos.x, below.getY() + 1.0, pos.z);
            }
        }
        return pos;
    }

    private static void erupt(ServerPlayerEntity player, ServerWorld world, Vec3d center, SkillDefinition def) {
        Box footprint = new Box(
                center.x - FOOTPRINT_RADIUS, center.y - 0.5, center.z - FOOTPRINT_RADIUS,
                center.x + FOOTPRINT_RADIUS, center.y + PILLAR_HEIGHT + 0.5, center.z + FOOTPRINT_RADIUS);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, footprint, e -> e != player && e.isAlive());

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, def.damage());
            ElementalInteractions.applySeismicStagger(target, 40);
            Vec3d vel = target.getVelocity();
            target.setVelocity(vel.x * 0.4, LAUNCH_VELOCITY, vel.z * 0.4);
            target.velocityModified = true;
        }

        // Clear loose grass and flowers under the pillar footprint
        ElementalInteractions.clearVegetation(world, center, FOOTPRINT_RADIUS);

        BlockPos groundPos = BlockPos.ofFloored(center.subtract(0, 0.5, 0));
        BlockState ground = world.getBlockState(groundPos);
        if (ground.isAir() || !ground.getFluidState().isEmpty()) {
            ground = Blocks.STONE.getDefaultState();
        }

        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, ground),
                center.x, center.y + 0.3, center.z,
                50, FOOTPRINT_RADIUS * 0.6, 0.5, FOOTPRINT_RADIUS * 0.6, 0.2);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                center.x, center.y + 0.3, center.z,
                25, FOOTPRINT_RADIUS * 0.5, 0.4, FOOTPRINT_RADIUS * 0.5, 0.15);
        world.spawnParticles(AvatarParticles.DUST,
                center.x, center.y + 0.2, center.z,
                35, FOOTPRINT_RADIUS * 0.7, 0.3, FOOTPRINT_RADIUS * 0.7, 0.08);

        // Check if erupting underwater / through water body: spawn water geyser particles
        BlockPos waterCheck = BlockPos.ofFloored(center.add(0, 1.0, 0));
        if (world.getFluidState(waterCheck).isIn(FluidTags.WATER) || world.getFluidState(groundPos.up()).isIn(FluidTags.WATER)) {
            world.spawnParticles(ParticleTypes.SPLASH, center.x, center.y + 1.0, center.z,
                    40, 0.5, 1.0, 0.5, 0.15);
            world.spawnParticles(ParticleTypes.BUBBLE, center.x, center.y + 0.5, center.z,
                    30, 0.4, 0.8, 0.4, 0.1);
            world.playSound(null, groundPos, SoundEvents.ENTITY_GENERIC_SPLASH, SoundCategory.PLAYERS, 2.0f, 1.0f);
        }

        world.playSound(null, groundPos,
                SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.55f);
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 1.6f, 0.6f);
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_GRAVEL_BREAK, SoundCategory.PLAYERS, 1.2f, 0.7f);
        world.playSound(null, groundPos,
                SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 0.9f, 0.8f);
    }

    private static void spawnColumnParticles(ServerWorld world, Vec3d center, int tickInActive) {
        double maxHeight = Math.min(PILLAR_HEIGHT, 1.0 + tickInActive * 1.0);
        BlockPos groundPos = BlockPos.ofFloored(center.subtract(0, 0.5, 0));
        BlockState ground = world.getBlockState(groundPos);
        if (ground.isAir() || !ground.getFluidState().isEmpty()) {
            ground = Blocks.STONE.getDefaultState();
        }

        BlockStateParticleEffect dust = new BlockStateParticleEffect(ParticleTypes.BLOCK, ground);

        for (double h = 0.2; h <= maxHeight; h += 0.6) {
            world.spawnParticles(dust, center.x, center.y + h, center.z, 4, 0.15, 0.15, 0.15, 0.05);

            int points = 12;
            for (int i = 0; i < points; i++) {
                double angle = (Math.PI * 2 * i) / points;
                double px = center.x + Math.cos(angle) * (FOOTPRINT_RADIUS * 0.6);
                double pz = center.z + Math.sin(angle) * (FOOTPRINT_RADIUS * 0.6);
                world.spawnParticles(dust, px, center.y + h, pz, 2, 0.08, 0.15, 0.08, 0.04);
            }
        }

        world.spawnParticles(ParticleTypes.POOF, center.x, center.y + maxHeight, center.z, 3, 0.3, 0.1, 0.3, 0.02);
    }

    public static void clear(UUID casterUuid) {
        ACTIVE_PILLARS.remove(casterUuid);
        FLYING_MEGALITHS.removeIf(m -> m.casterUuid().equals(casterUuid));
        FLYING_SHARDS.removeIf(s -> s.casterUuid().equals(casterUuid));
    }

    private EarthPillarSkill() {}
}
