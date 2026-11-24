package com.avatarmod.elements.entity.mob;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.block.Blocks;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.particle.BlockStateParticleEffect;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

import java.util.List;

/**
 * Platypus Bear — Ferocious Earth Kingdom hybrid carnivore.
 *
 * Characteristics:
 * - Huge muscular quad bear with a wide flat platypus bill and beaver paddle tail.
 * - Territorial aggression: Charges and performs heavy paw strikes (10.5 damage).
 * - Ground Slam: Periodically rears up and slams both front paws, cracking the earth and staggering players.
 */
public class PlatypusBearEntity extends HostileEntity {

    private int slamCooldown = 40;

    public PlatypusBearEntity(EntityType<? extends HostileEntity> entityType, World world) {
        super(entityType, world);
        this.experiencePoints = 35;
    }

    public static DefaultAttributeContainer.Builder createPlatypusBearAttributes() {
        return HostileEntity.createHostileAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 80.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.29)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 10.5)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 36.0)
                .add(EntityAttributes.GENERIC_KNOCKBACK_RESISTANCE, 0.6)
                .add(EntityAttributes.GENERIC_ARMOR, 5.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new MeleeAttackGoal(this, 1.25, true));
        this.goalSelector.add(3, new WanderAroundFarGoal(this, 0.9));
        this.goalSelector.add(4, new LookAtEntityGoal(this, PlayerEntity.class, 16.0f));
        this.goalSelector.add(5, new LookAroundGoal(this));

        this.targetSelector.add(1, new RevengeGoal(this));
        this.targetSelector.add(2, new ActiveTargetGoal<>(this, PlayerEntity.class, true));
    }

    @Override
    public boolean tryAttack(Entity target) {
        boolean hit = super.tryAttack(target);
        if (hit && target instanceof LivingEntity living) {
            Vec3d push = living.getPos().subtract(this.getPos()).normalize().multiply(0.7);
            living.addVelocity(push.x, 0.25, push.z);
            living.velocityModified = true;

            this.getWorld().playSound(null, this.getBlockPos(),
                    SoundEvents.ENTITY_POLAR_BEAR_WARNING, SoundCategory.HOSTILE, 1.4f, 0.7f);
        }
        return hit;
    }

    @Override
    public void tick() {
        super.tick();

        if (!this.getWorld().isClient()) {
            if (--slamCooldown <= 0) {
                LivingEntity target = this.getTarget();
                if (target != null && this.squaredDistanceTo(target) < 16.0 && this.isOnGround()) {
                    performGroundSlam();
                    slamCooldown = 100; // 5 second cooldown
                }
            }
        }
    }

    private void performGroundSlam() {
        if (this.getWorld() instanceof ServerWorld sw) {
            sw.playSound(null, this.getBlockPos(), SoundEvents.ENTITY_IRON_GOLEM_ATTACK, SoundCategory.HOSTILE, 1.8f, 0.6f);
            sw.playSound(null, this.getBlockPos(), SoundEvents.BLOCK_DEEPSLATE_BREAK, SoundCategory.HOSTILE, 1.4f, 0.7f);

            sw.spawnParticles(new BlockStateParticleEffect(ParticleTypes.BLOCK, Blocks.COBBLESTONE.getDefaultState()),
                    this.getX(), this.getY() + 0.2, this.getZ(),
                    25, 1.0, 0.2, 1.0, 0.12);
            sw.spawnParticles(AvatarParticles.STONE_CHIP,
                    this.getX(), this.getY() + 0.2, this.getZ(),
                    15, 0.8, 0.2, 0.8, 0.08);

            Box aoe = Box.of(this.getPos(), 4.5, 2.5, 4.5);
            List<LivingEntity> enemies = sw.getEntitiesByClass(LivingEntity.class, aoe, e -> e != this && e.isAlive());
            DamageSource src = sw.getDamageSources().mobAttack(this);
            for (LivingEntity e : enemies) {
                e.damage(src, 8.0f);
                Vec3d push = e.getPos().subtract(this.getPos()).normalize().multiply(1.1);
                e.addVelocity(push.x, 0.35, push.z);
                e.velocityModified = true;
            }
        }
    }
}
