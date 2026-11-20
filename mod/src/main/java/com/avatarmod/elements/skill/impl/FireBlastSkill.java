package com.avatarmod.elements.skill.impl;

import com.avatarmod.elements.data.PlayerBendingData;
import com.avatarmod.elements.data.SkillTimeline;
import com.avatarmod.elements.entity.FireBlastProjectileEntity;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.ElementalInteractions;
import com.avatarmod.elements.skill.SkillDefinition;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.MinecraftServer;
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
 * Fire Blast — Hold-and-release fireball projectile.
 * Hold to charge up size, damage, and blast radius.
 * Release spawns a high-speed projectile that travels in look direction.
 * Detonates on entity or block impact with AOE damage.
 */
public final class FireBlastSkill {

    public static final float BASE_SPEED = 1.8f;      // blocks per tick
    public static final int   MAX_LIFETIME = 25;      // ticks
    public static final float MIN_DAMAGE_RATIO = 0.35f;
    public static final float MAX_DAMAGE_RATIO = 1.0f;
    public static final float MIN_RADIUS = 1.0f;
    public static final float MAX_RADIUS = 3.0f;

    public record FireBall(
            UUID ownerUuid,
            Vec3d pos,
            Vec3d velocity,
            int ticksLeft,
            float damage,
            float radius,
            float knockback,
            float chargeRatio
    ) {}

    private static final Map<UUID, FireBlastProjectileEntity> ACTIVE_PROJECTILES = new ConcurrentHashMap<>();

    public static void tick(ServerPlayerEntity player, SkillDefinition def) {
        PlayerBendingData data = PlayerBendingData.get(player);
        SkillTimeline timeline = data.getTimeline();

        // Spawn fireball on the first tick of ACTIVE phase (right after HOLD is released)
        if (timeline.phase() == SkillTimeline.Phase.ACTIVE && timeline.ticksInPhase() == 1) {
            spawnFireball(player, def, timeline.getChargeRatio());
        }
    }

    /**
     * Advances and manages all in-flight fireballs globally. Called on END_SERVER_TICK so
     * projectiles continue their trajectory even if the caster switches skills,
     * enters recovery, or is cancelled.
     */
    public static void tickAllFireballs(MinecraftServer server) {
        if (ACTIVE_PROJECTILES.isEmpty()) return;

        for (Map.Entry<UUID, FireBlastProjectileEntity> entry : ACTIVE_PROJECTILES.entrySet()) {
            UUID ownerId = entry.getKey();
            FireBlastProjectileEntity entity = entry.getValue();
            if (entity == null || entity.isRemoved() || !entity.isAlive()) {
                ACTIVE_PROJECTILES.remove(ownerId);
            }
        }
    }

    private static void spawnFireball(ServerPlayerEntity player, SkillDefinition def, float chargeRatio) {
        chargeRatio = Math.max(0.1f, Math.min(1.0f, chargeRatio));

        float damage = def.damage() * (MIN_DAMAGE_RATIO + (MAX_DAMAGE_RATIO - MIN_DAMAGE_RATIO) * chargeRatio);
        float radius = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * chargeRatio;
        float knockback = def.knockback() * (0.5f + 0.5f * chargeRatio);

        Vec3d eyePos = player.getEyePos();
        Vec3d look = player.getRotationVec(1.0f);
        Vec3d spawnPos = eyePos.add(look.multiply(0.6));
        Vec3d vel = look.multiply(BASE_SPEED);

        ServerWorld world = player.getServerWorld();
        FireBlastProjectileEntity entity =
                new FireBlastProjectileEntity(
                        world, player, damage, radius, knockback, chargeRatio);
        entity.setPosition(spawnPos.x, spawnPos.y, spawnPos.z);
        entity.setVelocity(vel);
        world.spawnEntity(entity);

        ACTIVE_PROJECTILES.put(player.getUuid(), entity);

        // Launch SFX: blazing launch sound, pitch deeper with higher charge
        float pitch = 1.2f - (0.4f * chargeRatio);
        world.playSound(null, player.getBlockPos(),
                SoundEvents.ENTITY_BLAZE_SHOOT, SoundCategory.PLAYERS, 0.8f, pitch);
    }

    /** Solid collision check helper: ignores passable foliage/air. */
    public static boolean isSolidBlockCollision(ServerWorld world, BlockPos blockPos) {
        return !world.getBlockState(blockPos).getCollisionShape(world, blockPos).isEmpty();
    }

    public static void detonate(ServerPlayerEntity player, ServerWorld world, Vec3d center,
                                float damage, float radius, float knockback, float chargeRatio) {
        // AOE blast damage
        double r = radius;
        Box blastBox = Box.of(center, r * 2, r * 2, r * 2);
        List<LivingEntity> blastTargets = world.getEntitiesByClass(
                LivingEntity.class, blastBox,
                e -> e != player && e.isAlive() && e.squaredDistanceTo(center) <= r * r
        );

        DamageSource source = (player != null) ? world.getDamageSources().playerAttack(player) : world.getDamageSources().magic();
        for (LivingEntity target : blastTargets) {
            target.damage(source, damage);
            ElementalInteractions.applyFire(target, (int) (60 + 80 * chargeRatio));
            Vec3d knockDir = target.getPos().subtract(center).normalize();
            if (knockDir.lengthSquared() < 0.001) knockDir = new Vec3d(0, 1, 0);
            target.addVelocity(
                    knockDir.x * knockback,
                    0.15 + knockback * 0.35,
                    knockDir.z * knockback
            );
            target.velocityModified = true;
        }

        ElementalInteractions.igniteBlocks(world, center, r * 0.8, player);

        // Detonation VFX
        int flameCount = (int) (20 + 25 * chargeRatio);
        world.spawnParticles(ParticleTypes.EXPLOSION,
                center.x, center.y, center.z, 1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(ParticleTypes.FLAME,
                center.x, center.y, center.z,
                flameCount, r * 0.4, r * 0.4, r * 0.4, 0.08);
        world.spawnParticles(AvatarParticles.FLAME_BURST,
                center.x, center.y, center.z, (int) (4 + 6 * chargeRatio), r * 0.3, r * 0.3, r * 0.3, 0.05);
        world.spawnParticles(AvatarParticles.IMPACT_FLASH,
                center.x, center.y, center.z, 1, 0.0, 0.0, 0.0, 0.0);
        world.spawnParticles(AvatarParticles.SMOKE_EXPANSION,
                center.x, center.y, center.z, (int) (3 + 3 * chargeRatio), r * 0.2, r * 0.2, r * 0.2, 0.02);
        world.spawnParticles(ParticleTypes.LAVA,
                center.x, center.y, center.z,
                (int) (3 + 5 * chargeRatio), r * 0.3, r * 0.3, r * 0.3, 0.0);
        world.spawnParticles(ParticleTypes.LARGE_SMOKE,
                center.x, center.y, center.z,
                (int) (6 + 6 * chargeRatio), r * 0.3, r * 0.3, r * 0.3, 0.02);

        // Detonation SFX
        float volume = 0.8f + 0.4f * chargeRatio;
        float pitch = 1.3f - 0.3f * chargeRatio;
        world.playSound(null, BlockPos.ofFloored(center),
                SoundEvents.ENTITY_GENERIC_EXPLODE.value(),
                SoundCategory.PLAYERS, volume, pitch);
    }

    public static FireBall getActiveFireball(UUID playerId) {
        FireBlastProjectileEntity entity = ACTIVE_PROJECTILES.get(playerId);
        if (entity == null || entity.isRemoved() || !entity.isAlive()) return null;
        return new FireBall(playerId, entity.getPos(), entity.getVelocity(),
                Math.max(0, MAX_LIFETIME - entity.getAge()),
                entity.getDamage(), entity.getRadius(), entity.getKnockback(), entity.getChargeRatio());
    }

    public static void clearFireball(UUID playerId) {
        FireBlastProjectileEntity entity = ACTIVE_PROJECTILES.remove(playerId);
        if (entity != null && !entity.isRemoved()) {
            entity.discard();
        }
    }

    public static void onProjectileDiscarded(UUID playerId) {
        ACTIVE_PROJECTILES.remove(playerId);
    }

    private FireBlastSkill() {}
}
