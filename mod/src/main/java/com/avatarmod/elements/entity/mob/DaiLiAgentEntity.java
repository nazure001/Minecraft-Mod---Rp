package com.avatarmod.elements.entity.mob;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

/**
 * Dai Li Agent — Covert earthbending enforcers of Ba Sing Se.
 *
 * Characteristics:
 * - Wields stone rock gloves: Melee strike (7.5 dmg) inflicts Slowness (stone shackles).
 * - Earth shard projectile fling when at range.
 */
public class DaiLiAgentEntity extends HostileEntity {

    private int attackCooldown = 20;

    public DaiLiAgentEntity(EntityType<? extends HostileEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 30;
    }

    public static DefaultAttributeContainer.Builder createDaiLiAttributes() {
        return HostileEntity.createHostileAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 55.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.31)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 7.5)
                .add(EntityAttributes.GENERIC_ARMOR, 6.0)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 32.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new MeleeAttackGoal(this, 1.25, false));
        this.goalSelector.add(3, new WanderAroundFarGoal(this, 0.9));
        this.goalSelector.add(4, new LookAtEntityGoal(this, PlayerEntity.class, 16.0f));
        this.goalSelector.add(5, new LookAroundGoal(this));

        this.targetSelector.add(1, new RevengeGoal(this));
        this.targetSelector.add(2, new ActiveTargetGoal<>(this, PlayerEntity.class, true));
    }

    @Override
    public boolean tryAttack(Entity target) {
        boolean success = super.tryAttack(target);
        if (success && target instanceof LivingEntity living) {
            living.addStatusEffect(new StatusEffectInstance(StatusEffects.SLOWNESS, 60, 1), this);
            this.getWorld().playSound(null, this.getBlockPos(), SoundEvents.BLOCK_STONE_HIT, SoundCategory.HOSTILE, 1.4f, 0.9f);
            if (this.getWorld() instanceof ServerWorld sw) {
                sw.spawnParticles(AvatarParticles.STONE_CHIP,
                        living.getX(), living.getY() + 0.5, living.getZ(), 8, 0.2, 0.2, 0.2, 0.05);
            }
        }
        return success;
    }
}
