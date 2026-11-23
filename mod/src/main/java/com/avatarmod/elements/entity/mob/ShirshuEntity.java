package com.avatarmod.elements.entity.mob;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.mob.Monster;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.world.World;

/**
 * Shirshu — Legendary blind quadruped predator and tracking beast.
 *
 * Characteristics:
 * - Extremely keen scent tracking: Follow range of 48 blocks.
 * - Star-nosed sensory tentacles.
 * - Paralytic whip tongue / claw strike: Inflicts Slowness III (paralysis), Weakness, and Blindness.
 */
public class ShirshuEntity extends HostileEntity {

    private int sniffCooldown = 0;

    public ShirshuEntity(EntityType<? extends HostileEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 25;
    }

    public static DefaultAttributeContainer.Builder createShirshuAttributes() {
        return MobEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 65.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.33)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 8.5)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 48.0)
                .add(EntityAttributes.GENERIC_KNOCKBACK_RESISTANCE, 0.4)
                .add(EntityAttributes.GENERIC_ARMOR, 4.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new PounceAtTargetGoal(this, 0.45f));
        this.goalSelector.add(3, new MeleeAttackGoal(this, 1.25, true));
        this.goalSelector.add(4, new WanderAroundFarGoal(this, 0.95));
        this.goalSelector.add(5, new LookAtEntityGoal(this, PlayerEntity.class, 14.0f));
        this.goalSelector.add(6, new LookAroundGoal(this));

        this.targetSelector.add(1, new RevengeGoal(this));
        this.targetSelector.add(2, new ActiveTargetGoal<>(this, PlayerEntity.class, true));
        this.targetSelector.add(3, new ActiveTargetGoal<>(this, HostileEntity.class, 10, true, false, e -> !(e instanceof ShirshuEntity)));
    }

    @Override
    public boolean tryAttack(Entity target) {
        boolean success = super.tryAttack(target);
        if (success && target instanceof LivingEntity living) {
            // Paralytic neurotoxin strike: Slowness III (5 seconds), Weakness II, and sensory blackout
            living.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 100, 2), this);
            living.addStatusEffect(new StatusEffectInstance(StatusEffects.WEAKNESS, 100, 1), this);
            living.addStatusEffect(new StatusEffectInstance(StatusEffects.BLINDNESS, 50, 0), this);

            if (this.getWorld() instanceof ServerWorld serverWorld) {
                serverWorld.spawnParticles(
                        AvatarParticles.BLOOD_CHI_FILAMENT,
                        living.getX(), living.getY() + living.getHeight() * 0.5, living.getZ(),
                        8, 0.25, 0.25, 0.25, 0.05
                );
                serverWorld.spawnParticles(
                        AvatarParticles.IMPACT_FLASH,
                        living.getX(), living.getY() + living.getHeight() * 0.5, living.getZ(),
                        1, 0.0, 0.0, 0.0, 0.0
                );
            }

            this.getWorld().playSound(
                    null, this.getBlockPos(),
                    SoundEvents.ENTITY_PLAYER_ATTACK_CRIT,
                    SoundCategory.HOSTILE, 1.3f, 0.85f
            );
        }
        return success;
    }

    @Override
    public void tick() {
        super.tick();

        // Ambient sniffing behavior
        if (!this.getWorld().isClient()) {
            if (--sniffCooldown <= 0) {
                sniffCooldown = 120 + this.random.nextInt(100);
                if (this.getTarget() != null) {
                    this.getWorld().playSound(
                            null, this.getBlockPos(),
                            SoundEvents.ENTITY_SNIFFER_SNIFFING,
                            SoundCategory.HOSTILE, 1.0f, 1.2f
                    );
                }
            }
        }
    }
}
