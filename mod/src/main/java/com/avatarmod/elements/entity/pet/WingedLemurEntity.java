package com.avatarmod.elements.entity.pet;

import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.passive.PassiveEntity;
import net.minecraft.entity.passive.TameableEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

/**
 * Winged Lemur (Momo) — Intelligent, playful winged companion of the Southern Air Temple.
 *
 * Characteristics:
 * - Tameable with Sweet Berries, Apples, or Glow Berries.
 * - Glides down smoothly when descending (Slow Falling).
 * - Follows owner, plays ambient chattering sounds.
 */
public class WingedLemurEntity extends TameableEntity {

    public WingedLemurEntity(EntityType<? extends TameableEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 5;
    }

    public static DefaultAttributeContainer.Builder createLemurAttributes() {
        return TameableEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 24.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.35)
                .add(EntityAttributes.GENERIC_FLYING_SPEED, 0.45)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 24.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new SitGoal(this));
        this.goalSelector.add(3, new FollowOwnerGoal(this, 1.25, 6.0f, 2.0f));
        this.goalSelector.add(4, new WanderAroundFarGoal(this, 0.9));
        this.goalSelector.add(5, new LookAtEntityGoal(this, PlayerEntity.class, 10.0f));
        this.goalSelector.add(6, new LookAroundGoal(this));
    }

    @Override
    public boolean handleFallDamage(float fallDistance, float damageMultiplier, DamageSource damageSource) {
        return false;
    }

    @Override
    public void tick() {
        super.tick();

        // Slow gliding when airborne
        if (!this.isOnGround() && this.getVelocity().y < -0.1) {
            this.setVelocity(this.getVelocity().x, -0.08, this.getVelocity().z);
            this.velocityModified = true;
        }
    }

    @Override
    public ActionResult interactMob(PlayerEntity player, Hand hand) {
        ItemStack itemStack = player.getStackInHand(hand);

        if (!this.isTamed()) {
            if (itemStack.isOf(Items.SWEET_BERRIES) || itemStack.isOf(Items.APPLE) || itemStack.isOf(Items.GLOW_BERRIES)) {
                if (!player.getAbilities().creativeMode) {
                    itemStack.decrement(1);
                }
                if (this.random.nextInt(3) == 0) {
                    this.setOwner(player);
                    this.getWorld().sendEntityStatus(this, (byte) 7);
                } else {
                    this.getWorld().sendEntityStatus(this, (byte) 6);
                }
                this.getWorld().playSound(null, this.getBlockPos(), SoundEvents.ENTITY_PARROT_EAT, SoundCategory.NEUTRAL, 1.0f, 1.2f);
                return ActionResult.SUCCESS;
            }
        } else if (this.isOwner(player)) {
            if (player.isSneaking()) {
                this.setSitting(!this.isSitting());
                return ActionResult.SUCCESS;
            }
        }

        return super.interactMob(player, hand);
    }

    @Override
    public boolean isBreedingItem(ItemStack stack) {
        return stack.isOf(Items.SWEET_BERRIES) || stack.isOf(Items.APPLE);
    }

    @Nullable
    @Override
    public PassiveEntity createChild(ServerWorld world, PassiveEntity entity) {
        return null;
    }
}
