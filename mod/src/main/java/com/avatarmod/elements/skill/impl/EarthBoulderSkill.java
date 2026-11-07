package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Earth Boulder — projectile that travels in look direction each tick.
 * Hits first entity in path; detonates on block collision or after lifetime.
 * Does NOT modify world blocks (prototype).
 */
public final class EarthBoulderSkill {

    private static final float SPEED = 0.8f;       // blocks per tick
    private static final int   LIFETIME = 20;      // ticks
    private static final float HITBOX_RADIUS = 0.7f;

    // Active boulders keyed by player UUID
    private static final Map<UUID, BoulderState> BOULDERS = new ConcurrentHashMap<>();

    private record BoulderState(Vec3d pos, Vec3d velocity, int ticksLeft, float damage, float knockback) {}

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        SkillTimeline timeline = PlayerBendingData.get(player).getTimeline();

        // Spawn boulder at start of ACTIVE phase
        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 0) {
            Vec3d spawnPos = player.getPos().add(0, player.getStandingEyeHeight() * 0.8, 0);
            Vec3d vel = player.getRotationVec(1.0f).multiply(SPEED);
            BOULDERS.put(player.getUuid(), new BoulderState(spawnPos, vel, LIFETIME, def.damage(), def.knockback()));
        }

        // Advance boulder each tick during ACTIVE/RECOVERY while it exists
        UUID id = player.getUuid();
        BoulderState state = BOULDERS.get(id);
        if (state == null) return;

        ServerWorld world = player.getServerWorld();
        Vec3d nextPos = state.pos().add(state.velocity());

        // VFX at current position
        world.spawnParticles(ParticleTypes.SMOKE,
                state.pos().x, state.pos().y, state.pos().z,
                6, HITBOX_RADIUS * 0.5, HITBOX_RADIUS * 0.5, HITBOX_RADIUS * 0.5, 0.02);

        // Collision check: entities
        Box hitbox = Box.of(nextPos, HITBOX_RADIUS * 2, HITBOX_RADIUS * 2, HITBOX_RADIUS * 2);
        List<LivingEntity> targets = world.getEntitiesByClass(
                LivingEntity.class, hitbox,
                e -> e != player && e.isAlive()
        );
        if (!targets.isEmpty()) {
            detonate(player, world, nextPos, targets, state);
            BOULDERS.remove(id);
            return;
        }

        // Collision check: blocks
        if (!world.isAir(net.minecraft.util.math.BlockPos.ofFloored(nextPos))) {
            detonate(player, world, state.pos(), List.of(), state);
            BOULDERS.remove(id);
            return;
        }

        // Advance or expire
        int ticksLeft = state.ticksLeft() - 1;
        if (ticksLeft <= 0) {
            BOULDERS.remove(id);
        } else {
            BOULDERS.put(id, new BoulderState(nextPos, state.velocity(), ticksLeft, state.damage(), state.knockback()));
        }
    }

    private static void detonate(ServerPlayerEntity player, ServerWorld world, Vec3d pos,
                                  List<LivingEntity> targets, BoulderState state) {
        // Impact VFX
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                pos.x, pos.y, pos.z, 24, 0.5, 0.5, 0.5, 0.15);
        world.spawnParticles(ParticleTypes.SMOKE,
                pos.x, pos.y, pos.z, 8, 0.3, 0.3, 0.3, 0.05);
        world.playSound(null, net.minecraft.util.math.BlockPos.ofFloored(pos),
                SoundEvents.BLOCK_STONE_BREAK, SoundCategory.PLAYERS, 1.2f, 0.6f);

        DamageSource source = world.getDamageSources().playerAttack(player);
        for (LivingEntity target : targets) {
            target.damage(source, state.damage());
            Vec3d knockDir = target.getPos().subtract(pos).normalize();
            target.addVelocity(knockDir.x * state.knockback(), 0.3, knockDir.z * state.knockback());
            target.velocityModified = true;
        }
    }

    // Called from AvatarServerEvents each tick (even outside ACTIVE, to advance in-flight boulders)
    public static void tickBoulders(ServerPlayerEntity player) {
        // Boulders are advanced in tick() above; this is a no-op hook for future use
    }

    private EarthBoulderSkill() {}
}
