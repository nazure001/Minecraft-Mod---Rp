package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
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

import com.avatarmod.elements.network.SkillNetworking;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Earth Pillar — interactive martial arts stone construct.
 *
 * Lifecycle & Manipulation:
 * 1. Eruption: A stone column erupts under target or in front of caster, launching enemies.
 * 2. Persistent Stance: The pillar remains standing in the world for 140 ticks (7.0 seconds).
 * 3. Manipulation — Tendang Sekali (Single Power Kick):
 *    Player strikes or kicks the standing pillar. The pillar detaches and launches forward
 *    at high velocity (1.4 blocks/tick) as a flying megalith boulder projectile dealing 16.0
 *    blunt damage + massive seismic AOE shockwave upon impact.
 * 4. Manipulation — Bertubi-tubi (Rapid Barrage / Shard Gatling):
 *    Player punches or attacks the standing pillar repeatedly. Each strike shatters off a volley
 *    of 3-4 razor-sharp rock shard projectiles (4.0 dmg each) flying towards the crosshair,
 *    degrading pillar durability until it crumbles into a final stone burst.
 */
public final class EarthPillarSkill {

    public static final float FOOTPRINT_RADIUS = 1.6f;
    public static final float LAUNCH_VELOCITY = 1.05f;
    public static final float PILLAR_HEIGHT = 2.5f;
    public static final int   GROUND_SEARCH_DEPTH = 4;
    public static final int   PILLAR_DURATION_TICKS = 140; // 7.0 seconds
    public static final int   PILLAR_MAX_HITS = 4;        // 4 rapid barrage strikes
    public static final double INTERACTION_RADIUS = 6.0;   // blocks distance to interact

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
        private final Vec3d center;
        private int remainingTicks;
        private int hitsRemaining;

        public ActivePillar(UUID id, UUID casterUuid, Vec3d center, int remainingTicks, int hitsRemaining) {
            this.id = id;
            this.casterUuid = casterUuid;
            this.center = center;
            this.remainingTicks = remainingTicks;
            this.hitsRemaining = hitsRemaining;
        }

        public UUID id() { return id; }
        public UUID casterUuid() { return casterUuid; }
        public Vec3d center() { return center; }
        public int remainingTicks() { return remainingTicks; }
        public int hitsRemaining() { return hitsRemaining; }
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
            float knockback
    ) {}

    public record FlyingShard(
            UUID casterUuid,
            Vec3d pos,
            Vec3d velocity,
            int ticksLeft,
            float damage
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
            Vec3d center = findPillarCenter(player, world, def.range());
            ActivePillar pillar = new ActivePillar(UUID.randomUUID(), player.getUuid(), center, PILLAR_DURATION_TICKS, PILLAR_MAX_HITS);
            ACTIVE_PILLARS.put(player.getUuid(), pillar);

            int serial = SkillNetworking.currentSerial(player.getUuid());
            SkillNetworking.broadcastSkillPosition(player, "avatar:earth_pillar",
                    serial, center.x, center.y, center.z);
            erupt(player, world, center, def);
        }

        ActivePillar active = ACTIVE_PILLARS.get(player.getUuid());
        if (active != null) {
            spawnColumnParticles(world, active.center(), timeline.ticksInPhase());
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
            Vec3d toPillar = p.center().add(0, 1.25, 0).subtract(eye);
            double distSq = toPillar.lengthSquared();
            if (distSq <= bestDist) {
                // Check if roughly in front of player
                if (distSq < 4.0 || toPillar.normalize().dotProduct(look) > 0.3) {
                    bestDist = distSq;
                    best = p;
                }
            }
        }
        return best;
    }

    public static boolean hasNearbyPillar(ServerPlayerEntity player, double maxDist) {
        return findNearestPillar(player, maxDist) != null;
    }

    /**
     * Tendang Sekali (Single Power Kick) — kicks the standing pillar, launching it
     * forward as a high-speed flying megalith projectile that detonates with massive damage.
     */
    public static boolean kickPillar(ServerPlayerEntity player) {
        ActivePillar pillar = findNearestPillar(player, INTERACTION_RADIUS);
        if (pillar == null) return false;

        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d dir = new Vec3d(look.x, Math.max(-0.2, look.y), look.z).normalize();
        Vec3d spawnPos = pillar.center().add(0, 1.25, 0);
        Vec3d vel = dir.multiply(MEGALITH_SPEED);

        // Convert pillar into flying megalith projectile
        ACTIVE_PILLARS.remove(pillar.casterUuid());
        FLYING_MEGALITHS.add(new FlyingMegalith(player.getUuid(), spawnPos, vel,
                MEGALITH_LIFETIME, MEGALITH_DAMAGE, MEGALITH_AOE, MEGALITH_KNOCKBACK));

        // Multi-layered heavy kick launch SFX
        BlockPos groundPos = BlockPos.ofFloored(pillar.center());
        world.playSound(null, groundPos,
                SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.55f);
        world.playSound(null, groundPos,
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 2.0f, 0.6f);
        world.playSound(null, groundPos,
                SoundEvents.ENTITY_PLAYER_ATTACK_STRONG, SoundCategory.PLAYERS, 1.6f, 0.7f);

        // Launch dust kick wave VFX
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.STONE.getDefaultState()),
                spawnPos.x, spawnPos.y, spawnPos.z, 35, 0.6, 0.6, 0.6, 0.15);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                spawnPos.x, spawnPos.y, spawnPos.z, 25, 0.5, 0.5, 0.5, 0.2);
        world.spawnParticles(ParticleTypes.EXPLOSION,
                spawnPos.x, spawnPos.y, spawnPos.z, 1, 0.1, 0.1, 0.1, 0.0);

        // Broadcast action to clients (actionType 0 = KICK)
        SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 0,
                pillar.center().x, pillar.center().y, pillar.center().z, dir.x, dir.y, dir.z);

        return true;
    }

    /**
     * Bertubi-tubi (Rapid Barrage) — rapid punch strike shatters off a burst of 3-4
     * sharp flying stone shard projectiles towards crosshair, reducing pillar durability.
     */
    public static boolean strikePillar(ServerPlayerEntity player) {
        ActivePillar pillar = findNearestPillar(player, INTERACTION_RADIUS);
        if (pillar == null) return false;

        ServerWorld world = player.getServerWorld();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d origin = pillar.center().add(0, 1.25, 0);

        // Fire 3-4 sharp rock shard projectiles with slight spread
        int shardCount = 3 + RNG.nextInt(2);
        for (int i = 0; i < shardCount; i++) {
            double spreadX = (RNG.nextDouble() - 0.5) * 0.18;
            double spreadY = (RNG.nextDouble() - 0.5) * 0.18;
            double spreadZ = (RNG.nextDouble() - 0.5) * 0.18;
            Vec3d shardDir = look.add(spreadX, spreadY, spreadZ).normalize();
            FLYING_SHARDS.add(new FlyingShard(player.getUuid(), origin,
                    shardDir.multiply(SHARD_SPEED), SHARD_LIFETIME, SHARD_DAMAGE));
        }

        pillar.decrementHits();

        // Shard spray SFX
        BlockPos pos = BlockPos.ofFloored(pillar.center());
        world.playSound(null, pos,
                SoundEvents.BLOCK_STONE_HIT, SoundCategory.PLAYERS, 1.8f, 1.1f + (RNG.nextFloat() * 0.2f));
        world.playSound(null, pos,
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 1.2f, 1.4f);

        // Shard spray particles
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                origin.x, origin.y, origin.z, 20, 0.3, 0.3, 0.3, 0.15);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.COBBLESTONE.getDefaultState()),
                origin.x, origin.y, origin.z, 15, 0.3, 0.3, 0.3, 0.1);

        // Broadcast action to clients (actionType 1 = STRIKE)
        SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 1,
                pillar.center().x, pillar.center().y, pillar.center().z, look.x, look.y, look.z);

        // Final collapse when durability depleted
        if (pillar.hitsRemaining() <= 0) {
            crumblePillar(world, pillar);
        }

        return true;
    }

    private static void crumblePillar(ServerWorld world, ActivePillar pillar) {
        ACTIVE_PILLARS.remove(pillar.casterUuid());
        Vec3d center = pillar.center().add(0, 1.25, 0);
        BlockPos pos = BlockPos.ofFloored(center);

        world.playSound(null, pos,
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, 2.0f, 0.5f);
        world.playSound(null, pos,
                SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 1.8f, 0.7f);

        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.STONE.getDefaultState()),
                center.x, center.y, center.z, 45, 0.7, 1.0, 0.7, 0.15);
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                center.x, center.y, center.z, 30, 0.6, 0.8, 0.6, 0.15);
        world.spawnParticles(AvatarParticles.DUST,
                center.x, center.y, center.z, 35, 0.8, 0.5, 0.8, 0.08);

        // Broadcast action to clients (actionType 2 = CRUMBLE)
        SkillNetworking.broadcastPillarAction(world, pillar.casterUuid(), 2,
                pillar.center().x, pillar.center().y, pillar.center().z, 0, 0, 0);
    }

    /**
     * Ticked every server tick by ServerTickEvents.END_SERVER_TICK.
     * Advances active pillars, flying megaliths, and flying shards.
     */
    public static void tickAllPillars(MinecraftServer server) {
        // 1. Tick active pillars
        List<UUID> toCrumble = new ArrayList<>();
        for (ActivePillar pillar : ACTIVE_PILLARS.values()) {
            pillar.decrementTicks();
            if (pillar.remainingTicks() <= 0) {
                toCrumble.add(pillar.casterUuid());
            } else if (pillar.remainingTicks() % 8 == 0) {
                // Ambient dust/pebbles around base
                for (ServerWorld world : server.getWorlds()) {
                    if (world.isChunkLoaded(BlockPos.ofFloored(pillar.center()))) {
                        world.spawnParticles(AvatarParticles.DUST,
                                pillar.center().x, pillar.center().y + 0.2, pillar.center().z,
                                3, FOOTPRINT_RADIUS * 0.4, 0.1, FOOTPRINT_RADIUS * 0.4, 0.02);
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

        // 2. Tick flying megaliths
        List<FlyingMegalith> megalithsRemaining = new ArrayList<>();
        for (FlyingMegalith m : FLYING_MEGALITHS) {
            ServerPlayerEntity caster = server.getPlayerManager().getPlayer(m.casterUuid());
            ServerWorld world = caster != null ? caster.getServerWorld() : server.getOverworld();
            Vec3d nextPos = m.pos().add(m.velocity());

            // Projectile trail VFX
            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.STONE.getDefaultState()),
                    m.pos().x, m.pos().y, m.pos().z, 8, 0.4, 0.4, 0.4, 0.05);
            world.spawnParticles(AvatarParticles.STONE_CHIP,
                    m.pos().x, m.pos().y, m.pos().z, 5, 0.3, 0.3, 0.3, 0.05);
            world.spawnParticles(ParticleTypes.POOF,
                    m.pos().x, m.pos().y, m.pos().z, 2, 0.2, 0.2, 0.2, 0.01);

            // Check collision with entities
            Box hitBox = Box.of(nextPos, 1.8, 1.8, 1.8);
            List<LivingEntity> hits = world.getEntitiesByClass(
                    LivingEntity.class, hitBox, e -> (caster == null || e != caster) && e.isAlive());

            // Check collision with solid blocks
            BlockPos blockPos = BlockPos.ofFloored(nextPos);
            boolean hitBlock = !world.getBlockState(blockPos).getCollisionShape(world, blockPos).isEmpty();

            if (!hits.isEmpty() || hitBlock) {
                detonateMegalith(world, caster, nextPos, m);
            } else if (m.ticksLeft() > 1) {
                megalithsRemaining.add(new FlyingMegalith(m.casterUuid(), nextPos, m.velocity(),
                        m.ticksLeft() - 1, m.damage(), m.aoeRadius(), m.knockback()));
            } else {
                detonateMegalith(world, caster, nextPos, m);
            }
        }
        FLYING_MEGALITHS.clear();
        FLYING_MEGALITHS.addAll(megalithsRemaining);

        // 3. Tick flying shards
        List<FlyingShard> shardsRemaining = new ArrayList<>();
        for (FlyingShard s : FLYING_SHARDS) {
            ServerPlayerEntity caster = server.getPlayerManager().getPlayer(s.casterUuid());
            ServerWorld world = caster != null ? caster.getServerWorld() : server.getOverworld();
            Vec3d nextPos = s.pos().add(s.velocity());

            // Shard trail VFX
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
                        s.ticksLeft() - 1, s.damage()));
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
            Vec3d diff = target.getPos().subtract(pos);
            Vec3d knockDir = diff.lengthSquared() < 0.001 ? new Vec3d(0, 1, 0) : diff.normalize();
            target.addVelocity(knockDir.x * m.knockback(), 0.35 + m.knockback() * 0.2, knockDir.z * m.knockback());
            target.velocityModified = true;
        }

        // Cataclysmic detonation VFX & SFX
        BlockPos bp = BlockPos.ofFloored(pos);
        world.playSound(null, bp, SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 2.0f, 0.7f);
        world.playSound(null, bp, SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 2.5f, 0.6f);
        world.playSound(null, bp, SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, 2.0f, 0.5f);

        world.spawnParticles(ParticleTypes.EXPLOSION, pos.x, pos.y, pos.z, 2, 0.3, 0.3, 0.3, 0.0);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE, pos.x, pos.y, pos.z, 20, 0.6, 0.6, 0.6, 0.1);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.STONE.getDefaultState()),
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

        BlockPos groundPos = BlockPos.ofFloored(center.subtract(0, 0.5, 0));
        BlockState ground = world.getBlockState(groundPos);
        if (ground.isAir()) {
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
        world.spawnParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE,
                center.x, center.y + 0.1, center.z,
                8, FOOTPRINT_RADIUS * 0.6, 0.1, FOOTPRINT_RADIUS * 0.6, 0.02);

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
        if (ground.isAir()) {
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
