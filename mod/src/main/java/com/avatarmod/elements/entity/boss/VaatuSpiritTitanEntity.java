package com.avatarmod.elements.entity.boss;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.boss.BossBar;
import net.minecraft.entity.boss.ServerBossBar;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

/**
 * Vaatu — Spirit Titan of Chaos & Darkness.
 *
 * Characteristics:
 * - Colosal flying dark kite spirit with undulating tentacles and a central glowing core.
 * - BossBar: "Vaatu - Spirit of Chaos and Darkness" (Purple, Notched 10).
 * - Phase 1: High-mobility aerial hovering, homing dark void projectiles.
 * - Phase 2 (< 50% HP): Enraged frenzy, rapid tendril slams and dark energy vortexes.
 */
public class VaatuSpiritTitanEntity extends HostileEntity {

    private final ServerBossBar bossBar;
    private int attackCooldown = 40;

    public VaatuSpiritTitanEntity(EntityType<? extends HostileEntity> entityType, World world) {
        super(entityType, world);
        this.bossBar = (ServerBossBar) new ServerBossBar(
                Text.literal("§5§lVaatu §c§l- Spirit of Chaos and Darkness"),
                BossBar.Color.PURPLE,
                BossBar.Style.NOTCHED_10
        ).setDarkenSky(true);
        this.setNoGravity(true);
        this.experiencePoints = 250;
    }

    public static DefaultAttributeContainer.Builder createVaatuAttributes() {
        return MobEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 350.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.28)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 16.0)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 64.0)
                .add(EntityAttributes.GENERIC_KNOCKBACK_RESISTANCE, 1.0)
                .add(EntityAttributes.GENERIC_FLYING_SPEED, 0.35)
                .add(EntityAttributes.GENERIC_ARMOR, 10.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new MeleeAttackGoal(this, 1.3, false));
        this.goalSelector.add(3, new WanderAroundFarGoal(this, 1.0));
        this.goalSelector.add(4, new LookAtEntityGoal(this, PlayerEntity.class, 24.0f));
        this.goalSelector.add(5, new LookAroundGoal(this));

        this.targetSelector.add(1, new RevengeGoal(this));
        this.targetSelector.add(2, new ActiveTargetGoal<>(this, PlayerEntity.class, true));
    }

    @Override
    public void onStartedTrackingBy(ServerPlayerEntity player) {
        super.onStartedTrackingBy(player);
        this.bossBar.addPlayer(player);
    }

    @Override
    public void onStoppedTrackingBy(ServerPlayerEntity player) {
        super.onStoppedTrackingBy(player);
        this.bossBar.removePlayer(player);
    }

    @Override
    public void tick() {
        super.tick();

        // Update Boss Bar HP
        this.bossBar.setPercent(this.getHealth() / this.getMaxHealth());

        // Ambient hovering flight physics
        if (!this.getWorld().isClient()) {
            LivingEntity target = this.getTarget();
            if (target != null) {
                Vec3d toTarget = target.getPos().add(0, 2.5, 0).subtract(this.getPos());
                double dist = toTarget.length();
                if (dist > 2.0) {
                    Vec3d move = toTarget.normalize().multiply(0.25);
                    this.setVelocity(this.getVelocity().multiply(0.75).add(move));
                    this.velocityModified = true;
                }

                // Periodic Dark Void Energy projectile attack
                if (--attackCooldown <= 0) {
                    castDarkVoidBlast(target);
                    boolean enraged = this.getHealth() < this.getMaxHealth() * 0.5f;
                    attackCooldown = enraged ? 25 : 45;
                }
            } else {
                // Gentle floating hover
                this.setVelocity(this.getVelocity().x * 0.9, Math.sin(this.age * 0.05) * 0.05, this.getVelocity().z * 0.9);
                this.velocityModified = true;
            }

            // Ambient dark spirit particles swirling around Vaatu
            if (this.age % 3 == 0 && this.getWorld() instanceof ServerWorld serverWorld) {
                serverWorld.spawnParticles(
                        AvatarParticles.VAATU_VOID_ENERGY,
                        this.getX() + (this.random.nextDouble() - 0.5) * 2.5,
                        this.getY() + 1.5 + (this.random.nextDouble() - 0.5) * 2.0,
                        this.getZ() + (this.random.nextDouble() - 0.5) * 2.5,
                        2, 0.2, 0.2, 0.2, 0.02
                );
            }
        }
    }

    private void castDarkVoidBlast(LivingEntity target) {
        if (!(this.getWorld() instanceof ServerWorld serverWorld)) return;

        Vec3d origin = this.getPos().add(0, 2.0, 0);
        Vec3d dir = target.getEyePos().subtract(origin).normalize();

        // High-velocity raycast void blast
        for (double d = 1.0; d <= 24.0; d += 0.8) {
            Vec3d p = origin.add(dir.multiply(d));
            serverWorld.spawnParticles(
                    AvatarParticles.VAATU_VOID_ENERGY,
                    p.x, p.y, p.z,
                    3, 0.15, 0.15, 0.15, 0.04
            );
        }

        // Hit target
        double dist = target.squaredDistanceTo(this);
        if (dist <= 24.0 * 24.0) {
            target.damage(this.getDamageSources().magic(), 12.0f);
            target.addStatusEffect(new StatusEffectInstance(StatusEffects.WITHER, 100, 1), this);
            target.addStatusEffect(new StatusEffectInstance(StatusEffects.DARKNESS, 120, 0), this);

            Vec3d knock = dir.multiply(1.2);
            target.addVelocity(knock.x, 0.35, knock.z);
            target.velocityModified = true;

            serverWorld.spawnParticles(
                    AvatarParticles.IMPACT_FLASH,
                    target.getX(), target.getY() + 1.0, target.getZ(),
                    2, 0.0, 0.0, 0.0, 0.0
            );
        }

        this.getWorld().playSound(
                null, this.getBlockPos(),
                SoundEvents.ENTITY_WITHER_SHOOT,
                SoundCategory.HOSTILE, 2.0f, 0.65f
        );
    }
}
