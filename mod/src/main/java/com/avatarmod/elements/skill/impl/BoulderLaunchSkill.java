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
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Boulder Launch — hold-and-release rock projectile.
 * Charge grows the boulder: bigger hitbox, more damage, wider impact AOE.
 * Dynamically scales damage and particle visuals from extracted block hardness!
 */
public final class BoulderLaunchSkill {

    public static final float MIN_SPEED = 1.0f;          // blocks per tick at zero charge
    public static final float MAX_SPEED = 1.4f;
    public static final float MIN_DAMAGE_RATIO = 0.40f;
    public static final float MAX_DAMAGE_RATIO = 1.0f;
    public static final float MIN_HITBOX = 0.5f;         // boulder radius at zero charge
    public static final float MAX_HITBOX = 1.2f;
    public static final float MIN_AOE = 1.0f;            // impact AOE radius
    public static final float MAX_AOE = 2.5f;
    public static final int   LIFETIME = 24;             // ticks (≤ activeTicks so dispatch keeps advancing it)

    private record BoulderState(
            Vec3d pos, Vec3d velocity, int ticksLeft,
            float damage, float knockback, float hitboxRadius, float aoeRadius, float chargeRatio,
            BlockState blockState
    ) {}

    private static final Map<UUID, BoulderState> BOULDERS = new ConcurrentHashMap<>();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        if (timeline.phase() == SkillTimeline.Phase.HOLD) {
            tickHoldCharging(player, def, timeline);
        } else if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 1) {
            launch(player, def, timeline.getChargeRatio());
        }
    }

    private static void tickHoldCharging(ServerPlayerEntity player, SkillDefinition def, SkillTimeline timeline) {
        float chargeRatio = timeline.getChargeRatio();
        ServerWorld world = player.getServerWorld();
        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d chargePos = eyePos.add(look.multiply(1.8));

        boolean hasHammer = ElementalInteractions.isWeaponAffinity(player.getMainHandStack(), "EARTH");

        // 1. Excavation & Suction: find ground block in front and pull earth debris upwards
        BlockPos groundPos = ElementalInteractions.findSolidGroundBelow(
                world, player.getBlockPos().add((int)(look.x * 2.0), 0, (int)(look.z * 2.0)), 6);
        BlockState groundState = world.getBlockState(groundPos);
        if (groundState.isAir()) groundState = Blocks.STONE.getDefaultState();

        Vec3d groundCenter = Vec3d.ofCenter(groundPos).add(0, 0.4, 0);
        Vec3d suctionVec = chargePos.subtract(groundCenter).normalize();

        // Particles of rock and soil wrenched upwards from the ground into the hovering boulder
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, groundState),
                groundCenter.x + (world.random.nextDouble() - 0.5) * 1.2,
                groundCenter.y + 0.2,
                groundCenter.z + (world.random.nextDouble() - 0.5) * 1.2,
                (int)(4 + 6 * chargeRatio),
                suctionVec.x * 0.4, 0.60 + 0.25 * chargeRatio, suctionVec.z * 0.4, 0.12);

        // Ground fracture dust at the source
        world.spawnParticles(AvatarParticles.DUST,
                groundCenter.x, groundCenter.y, groundCenter.z,
                (int)(3 + 4 * chargeRatio), 0.5, 0.2, 0.5, 0.03);

        // 2. Swirling dust and stone chips condensing into the growing megalith
        double spread = 0.3 + 0.8 * chargeRatio;
        world.spawnParticles(AvatarParticles.STONE_CHIP,
                chargePos.x, chargePos.y, chargePos.z,
                (int) (5 + 8 * chargeRatio), spread, spread, spread, 0.05);
        world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, groundState),
                chargePos.x, chargePos.y, chargePos.z,
                (int) (4 + 6 * chargeRatio), spread * 0.7, spread * 0.7, spread * 0.7, 0.07);
        world.spawnParticles(AvatarParticles.DUST,
                chargePos.x, chargePos.y, chargePos.z,
                (int) (4 + 8 * chargeRatio), spread, spread, spread, 0.02);

        // 3. Periodic deep stone grinding rumble
        if (timeline.ticksInPhase() % 6 == 0) {
            float pitch = 1.3f - 0.7f * chargeRatio;
            world.playSound(null, groundPos,
                    SoundEvents.BLOCK_STONE_HIT, SoundCategory.PLAYERS, 0.85f, pitch);
            world.playSound(null, player.getBlockPos(),
                    SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 0.6f, pitch + 0.2f);
        }

        // Actionbar charge indicator
        if (timeline.ticksInPhase() % 4 == 0) {
            int pct = (int) (chargeRatio * 100);
            int bars = (int) (chargeRatio * 10);
            String barStr = "█".repeat(bars) + "░".repeat(Math.max(0, 10 - bars));
            String title = hasHammer ? "§6[Earth Hammer Megalith] " : "§6[Boulder Launch] ";
            player.sendMessage(Text.literal(title + "§e[" + barStr + "] " + pct + "%"), true);
        }
    }

    public static void tickAllBoulders(net.minecraft.server.MinecraftServer server) {
        if (BOULDERS.isEmpty()) return;
        for (UUID id : BOULDERS.keySet()) {
            ServerPlayerEntity player = server.getPlayerManager().getPlayer(id);
            if (player != null) {
                advanceBoulder(player);
            } else {
                BOULDERS.remove(id);
            }
        }
    }

    private static void launch(ServerPlayerEntity player, SkillDefinition def, float chargeRatio) {
        // If player has an active Earth Pillar in front, launch that pillar as a Megalith Wave!
        if (EarthPillarSkill.hasNearbyPillar(player, EarthPillarSkill.INTERACTION_RADIUS)) {
            boolean kicked = EarthPillarSkill.kickPillar(player);
            if (kicked) {
                return;
            }
        }

        chargeRatio = Math.max(0.1f, Math.min(1.0f, chargeRatio));

        ServerWorld world = player.getServerWorld();
        BlockPos groundPos = ElementalInteractions.findSolidGroundBelow(world, player.getBlockPos(), 6);
        BlockState groundState = world.getBlockState(groundPos);
        if (groundState.isAir()) groundState = Blocks.STONE.getDefaultState();

        float baseDamage = def.damage() * (MIN_DAMAGE_RATIO + (MAX_DAMAGE_RATIO - MIN_DAMAGE_RATIO) * chargeRatio);
        float damage = ElementalInteractions.calculateEarthHardnessDamage(world, groundPos, baseDamage);
        float knockback = def.knockback() * (0.5f + 0.5f * chargeRatio);
        float hitbox = MIN_HITBOX + (MAX_HITBOX - MIN_HITBOX) * chargeRatio;
        float aoe = MIN_AOE + (MAX_AOE - MIN_AOE) * chargeRatio;
        float speed = MIN_SPEED + (MAX_SPEED - MIN_SPEED) * chargeRatio;

        boolean hasHammer = ElementalInteractions.isWeaponAffinity(player.getMainHandStack(), "EARTH");
        if (hasHammer) {
            damage *= 1.30f;
            speed *= 1.15f;
            aoe += 1.0f;
        }

        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d spawnPos = eyePos.add(look.multiply(1.0));
        Vec3d vel = look.multiply(speed);

        BOULDERS.put(player.getUuid(),
                new BoulderState(spawnPos, vel, LIFETIME, damage, knockback, hitbox, aoe, chargeRatio, groundState));

        float bonus = damage - baseDamage;
        if (bonus > 0.5f) {
            String hammerNote = hasHammer ? " §e[Hammer +30%]" : "";
            player.sendMessage(Text.literal("§6[Earth] Megalith dipadatkan dari " + groundState.getBlock().getName().getString() + " §e(+" + String.format(Locale.ROOT, "%.1f", bonus) + " DMG)" + hammerNote), true);
        }

        float pitch = 0.9f - 0.3f * chargeRatio;
        world.playSound(null, player.getBlockPos(),
                SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 1.2f, pitch);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_PLAYER_ATTACK_SWEEP, SoundCategory.PLAYERS, 0.7f, 0.6f);
    }

    private static void advanceBoulder(ServerPlayerEntity player) {
        UUID id = player.getUuid();
        BoulderState state = BOULDERS.get(id);
        if (state == null) return;

        ServerWorld world = player.getServerWorld();

        // Auto-targeting guidance (soft homing): gently steer trajectory toward hostile targets in front
        Vec3d curVel = state.velocity();
        double curSpeed = curVel.length();
        if (curSpeed > 0.05) {
            Vec3d forwardDir = curVel.normalize();
            Box searchBox = Box.of(state.pos().add(forwardDir.multiply(8.0)), 24.0, 16.0, 24.0);
            List<LivingEntity> potentialTargets = world.getEntitiesByClass(
                    LivingEntity.class, searchBox,
                    e -> e != player && e.isAlive() && !e.isTeammate(player) && !e.isSpectator()
            );

            LivingEntity bestTarget = null;
            double bestScore = -1.0;

            for (LivingEntity entity : potentialTargets) {
                Vec3d toTarget = entity.getBoundingBox().getCenter().subtract(state.pos());
                double dist = toTarget.length();
                if (dist > 0.5 && dist <= 24.0) {
                    Vec3d dirToTarget = toTarget.normalize();
                    double dot = forwardDir.dotProduct(dirToTarget);
                    // Within a 50-degree forward cone (dot > 0.64)
                    if (dot > 0.64) {
                        double score = dot / Math.sqrt(dist);
                        if (score > bestScore) {
                            bestScore = score;
                            bestTarget = entity;
                        }
                    }
                }
            }

            if (bestTarget != null) {
                Vec3d targetCenter = bestTarget.getBoundingBox().getCenter();
                Vec3d desiredDir = targetCenter.subtract(state.pos()).normalize();
                boolean hasHammer = ElementalInteractions.isWeaponAffinity(player.getMainHandStack(), "EARTH");
                float steerStrength = hasHammer ? 0.22f : 0.16f;
                Vec3d steeredDir = forwardDir.multiply(1.0 - steerStrength).add(desiredDir.multiply(steerStrength)).normalize();
                curVel = steeredDir.multiply(curSpeed);
            }
        }

        Vec3d nextPos = state.pos().add(curVel);
        float r = state.hitboxRadius();

        // Trail VFX: debris sized by boulder radius and colored by block type
        BlockStateParticleEffect debris = new BlockStateParticleEffect(
                ParticleTypes.BLOCK, state.blockState());
        world.spawnParticles(debris,
                state.pos().x, state.pos().y, state.pos().z,
                (int) (6 + 8 * state.chargeRatio()), r * 0.5, r * 0.5, r * 0.5, 0.05);
        world.spawnParticles(ParticleTypes.SMOKE,
                state.pos().x, state.pos().y, state.pos().z,
                3, r * 0.4, r * 0.4, r * 0.4, 0.01);

        // Collision: entities in the boulder's path
        Box hitboxBox = Box.of(nextPos, r * 2, r * 2, r * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitboxBox, e -> e != player && e.isAlive());
        if (!targets.isEmpty()) {
            detonate(player, world, nextPos, state);
            BOULDERS.remove(id);
            return;
        }

        // Collision: solid blocks (ignores grass/foliage without collision shape)
        BlockPos blockPos = BlockPos.ofFloored(nextPos);
        if (!world.getBlockState(blockPos).getCollisionShape(world, blockPos).isEmpty()) {
            detonate(player, world, state.pos(), state);
            BOULDERS.remove(id);
            return;
        }

        int ticksLeft = state.ticksLeft() - 1;
        if (ticksLeft <= 0) {
            // Expire with a small crumble, no impact damage
            world.spawnParticles(debris, nextPos.x, nextPos.y, nextPos.z, 12, r * 0.5, r * 0.5, r * 0.5, 0.1);
            BOULDERS.remove(id);
        } else {
            BOULDERS.put(id, new BoulderState(nextPos, curVel, ticksLeft,
                    state.damage(), state.knockback(), r, state.aoeRadius(), state.chargeRatio(), state.blockState()));
        }
    }

    private static void detonate(ServerPlayerEntity player, ServerWorld world, Vec3d center, BoulderState state) {
        double aoe = state.aoeRadius();
        Box blastBox = Box.of(center, aoe * 2, aoe * 2, aoe * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, blastBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= aoe * aoe);

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, state.damage());
            Vec3d knockDir = target.getPos().subtract(center).normalize();
            if (knockDir.lengthSquared() < 0.001) knockDir = new Vec3d(0, 1, 0);
            target.addVelocity(
                    knockDir.x * state.knockback(),
                    0.2 + state.knockback() * 0.25,
                    knockDir.z * state.knockback());
            target.velocityModified = true;
        }

        // Impact VFX: stone shrapnel burst scaled by charge and block type
        BlockStateParticleEffect debris = new BlockStateParticleEffect(
                ParticleTypes.BLOCK, state.blockState());
        world.spawnParticles(debris, center.x, center.y, center.z,
                (int) (30 + 30 * state.chargeRatio()), aoe * 0.4, aoe * 0.4, aoe * 0.4, 0.25);
        world.spawnParticles(AvatarParticles.STONE_CHIP, center.x, center.y, center.z,
                (int) (20 + 20 * state.chargeRatio()), aoe * 0.4, aoe * 0.4, aoe * 0.4, 0.18);
        world.spawnParticles(AvatarParticles.DUST, center.x, center.y, center.z,
                (int) (25 + 25 * state.chargeRatio()), aoe * 0.5, aoe * 0.5, aoe * 0.5, 0.10);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE, center.x, center.y, center.z,
                (int) (8 + 8 * state.chargeRatio()), aoe * 0.3, aoe * 0.3, aoe * 0.3, 0.05);
        BlockState below = world.getBlockState(BlockPos.ofFloored(center).down());
        if (!below.isAir()) {
            world.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, below),
                    center.x, center.y, center.z, 12, aoe * 0.3, 0.2, aoe * 0.3, 0.15);
        }

        float volume = 1.0f + 0.4f * state.chargeRatio();
        world.playSound(null, BlockPos.ofFloored(center),
                SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.PLAYERS, volume, 0.6f);
        world.playSound(null, BlockPos.ofFloored(center),
                SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.PLAYERS, volume, 0.5f);
        world.playSound(null, BlockPos.ofFloored(center),
                SoundEvents.ENTITY_GENERIC_EXPLODE.value(), SoundCategory.PLAYERS, 0.7f, 1.2f);
    }

    /** Clears any in-flight boulder (caster cancelled, disconnected, etc.). */
    public static void clear(UUID playerId) {
        BOULDERS.remove(playerId);
    }

    private BoulderLaunchSkill() {}
}
