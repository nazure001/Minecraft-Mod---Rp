package com.avatarmod.elements.entity.pet;

import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.passive.AnimalEntity;
import net.minecraft.entity.passive.PassiveEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

import java.util.List;

/**
 * Flying Bison (Appa) — Sacred six-legged aerial creature of the Air Nomads.
 *
 * Capabilities:
 * - Mountable & Rideable: Right-click to mount. Steered with jump / movement keys.
 * - Soaring Flight: Glides and ascends through the air when ridden.
 * - Tail Gust Attack: Whacks air with colossal flat tail, producing a blast of wind that pushes foes away.
 * - High Vitality: 180 HP, natural fall damage immunity.
 */
public class FlyingBisonEntity extends AnimalEntity {

    private int tailGustCooldown = 0;

    public FlyingBisonEntity(EntityType<? extends AnimalEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 20;
    }

    public static DefaultAttributeContainer.Builder createBisonAttributes() {
        return AnimalEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 180.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.28)
                .add(EntityAttributes.GENERIC_FLYING_SPEED, 0.40)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 12.0)
                .add(EntityAttributes.GENERIC_KNOCKBACK_RESISTANCE, 0.9)
                .add(EntityAttributes.GENERIC_ARMOR, 6.0)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 32.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new EscapeDangerGoal(this, 1.25));
        this.goalSelector.add(3, new TemptGoal(this, 1.15, stack -> stack.isOf(Items.HAY_BLOCK) || stack.isOf(Items.WHEAT) || stack.isOf(Items.APPLE), false));
        this.goalSelector.add(4, new FollowParentGoal(this, 1.1));
        this.goalSelector.add(5, new WanderAroundFarGoal(this, 0.85));
        this.goalSelector.add(6, new LookAtEntityGoal(this, PlayerEntity.class, 12.0f));
        this.goalSelector.add(7, new LookAroundGoal(this));
    }

    @Override
    public boolean handleFallDamage(float fallDistance, float damageMultiplier, DamageSource damageSource) {
        // Airbenders' mounts take zero fall damage
        return false;
    }

    @Override
    public ActionResult interactMob(PlayerEntity player, Hand hand) {
        ItemStack itemStack = player.getStackInHand(hand);

        if (itemStack.isOf(Items.HAY_BLOCK) || itemStack.isOf(Items.WHEAT)) {
            if (this.getHealth() < this.getMaxHealth()) {
                this.heal(itemStack.isOf(Items.HAY_BLOCK) ? 30.0f : 8.0f);
                if (!player.getAbilities().creativeMode) {
                    itemStack.decrement(1);
                }
                this.getWorld().playSound(null, this.getBlockPos(), SoundEvents.ENTITY_COW_AMBIENT, SoundCategory.NEUTRAL, 1.0f, 0.7f);
                return ActionResult.SUCCESS;
            }
        }

        if (!this.getWorld().isClient() && !this.hasPassengers() && !player.isSneaking()) {
            player.startRiding(this);
            return ActionResult.SUCCESS;
        }

        return super.interactMob(player, hand);
    }

    @Override
    public void tick() {
        super.tick();

        if (tailGustCooldown > 0) tailGustCooldown--;

        // Flight & riding physics
        if (this.hasPassengers() && this.getFirstPassenger() instanceof PlayerEntity rider) {
            this.setYaw(rider.getYaw());
            this.prevYaw = this.getYaw();
            this.setPitch(rider.getPitch() * 0.5f);
            this.setRotation(this.getYaw(), this.getPitch());
            this.bodyYaw = this.getYaw();
            this.headYaw = this.bodyYaw;

            float forward = rider.forwardSpeed;
            float sideways = rider.sidewaysSpeed;

            Vec3d look = rider.getRotationVec(1.0f);
            double speed = 0.38;

            if (forward > 0) {
                double vy = this.getVelocity().y;
                if (rider.getPitch() < -15.0f) {
                    vy = Math.min(0.35, -look.y * 0.45); // Ascend into air!
                } else if (rider.getPitch() > 15.0f) {
                    vy = Math.max(-0.40, -look.y * 0.40); // Glide downward
                } else {
                    vy = Math.max(-0.04, vy * 0.85); // Gentle soaring hover
                }
                this.setVelocity(look.x * speed, vy, look.z * speed);
                this.velocityModified = true;

                // Air trail particles under huge bison body
                if (this.getWorld() instanceof ServerWorld sw && this.age % 3 == 0) {
                    sw.spawnParticles(ParticleTypes.CLOUD,
                            this.getX(), this.getY() + 0.2, this.getZ(),
                            2, 1.2, 0.2, 1.2, 0.02);
                }
            }

            // Tail Gust when sneaking/dismounting or in combat
            if (rider.isSneaking() && tailGustCooldown <= 0) {
                performTailGust();
                tailGustCooldown = 60; // 3 second cooldown
            }
        }
    }

    public void performTailGust() {
        if (this.getWorld() instanceof ServerWorld sw) {
            Vec3d rear = this.getPos().subtract(this.getRotationVec(1.0f).multiply(3.0));
            sw.spawnParticles(ParticleTypes.GUST_EMITTER_LARGE != null ? ParticleTypes.GUST_EMITTER_LARGE : ParticleTypes.CLOUD,
                    rear.x, rear.y + 1.0, rear.z, 3, 0.8, 0.4, 0.8, 0.1);

            sw.playSound(null, this.getBlockPos(), SoundEvents.ENTITY_BREEZE_WIND_BURST.value(), SoundCategory.NEUTRAL, 1.8f, 0.7f);

            Box knockBox = Box.of(rear, 5.0, 3.0, 5.0);
            List<LivingEntity> targets = sw.getEntitiesByClass(LivingEntity.class, knockBox,
                    e -> e != this && !(this.hasPassenger(e)) && e.isAlive());
            for (LivingEntity target : targets) {
                Vec3d push = target.getPos().subtract(this.getPos()).normalize().multiply(1.8);
                target.addVelocity(push.x, 0.4, push.z);
                target.velocityModified = true;
            }
        }
    }

    @Override
    public boolean isBreedingItem(ItemStack stack) {
        return stack.isOf(Items.HAY_BLOCK) || stack.isOf(Items.WHEAT);
    }

    @Nullable
    @Override
    public PassiveEntity createChild(ServerWorld world, PassiveEntity entity) {
        return null;
    }
}
