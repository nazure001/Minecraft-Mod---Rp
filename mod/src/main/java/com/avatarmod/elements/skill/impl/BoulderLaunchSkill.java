package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.particle.AvatarParticles;
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
 * Boulder Launch — hold-and-release rock projectile.
 * Charge grows the boulder: bigger hitbox, more damage, wider impact AOE.
 * Uses the generic hold-release framework (Phase.HOLD via C2SHoldStart/C2SHoldRelease).
 * The boulder advances during the caster's ACTIVE/RECOVERY ticks and does NOT
 * modify world blocks (prototype rule).
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
            float damage, float knockback, float hitboxRadius, float aoeRadius, float chargeRatio
    ) {}

    private static final Map<UUID, BoulderState> BOULDERS = new ConcurrentHashMap<>();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        // Launch on the first dispatched tick of ACTIVE (right after HOLD release)
        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 1) {
            launch(player, def, timeline.getChargeRatio());
        }

        advanceBoulder(player);
    }

    private static void launch(ServerPlayerEntity player, SkillDefinition def, float chargeRatio) {
        chargeRatio = Math.max(0.1f, Math.min(1.0f, chargeRatio));

        float damage = def.damage() * (MIN_DAMAGE_RATIO + (MAX_DAMAGE_RATIO - MIN_DAMAGE_RATIO) * chargeRatio);
        float knockback = def.knockback() * (0.5f + 0.5f * chargeRatio);
        float hitbox = MIN_HITBOX + (MAX_HITBOX - MIN_HITBOX) * chargeRatio;
        float aoe = MIN_AOE + (MAX_AOE - MIN_AOE) * chargeRatio;
        float speed = MIN_SPEED + (MAX_SPEED - MIN_SPEED) * chargeRatio;

        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d spawnPos = eyePos.add(look.multiply(1.0));
        Vec3d vel = look.multiply(speed);

        BOULDERS.put(player.getUuid(),
                new BoulderState(spawnPos, vel, LIFETIME, damage, knockback, hitbox, aoe, chargeRatio));

        ServerWorld world = player.getServerWorld();
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
        Vec3d nextPos = state.pos().add(state.velocity());
        float r = state.hitboxRadius();

        // Trail VFX: stone debris sized by boulder radius
        BlockStateParticleEffect debris = new BlockStateParticleEffect(
                ParticleTypes.BLOCK, net.minecraft.block.Blocks.STONE.getDefaultState());
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
            BOULDERS.put(id, new BoulderState(nextPos, state.velocity(), ticksLeft,
                    state.damage(), state.knockback(), r, state.aoeRadius(), state.chargeRatio()));
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

        // Impact VFX: stone shrapnel burst scaled by charge
        BlockStateParticleEffect debris = new BlockStateParticleEffect(
                ParticleTypes.BLOCK, net.minecraft.block.Blocks.STONE.getDefaultState());
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
