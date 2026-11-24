package com.avatarmod.elements.entity.boss;

import com.avatarmod.elements.particle.AvatarParticles;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LightningEntity;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.ai.goal.*;
import net.minecraft.entity.attribute.DefaultAttributeContainer;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.entity.boss.BossBar;
import net.minecraft.entity.boss.ServerBossBar;
import net.minecraft.entity.damage.DamageSource;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.math.Box;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

import java.util.List;

/**
 * Phoenix King Ozai — Supreme Ruler of the Fire Nation.
 *
 * Boss Encounter Design:
 * - BossBar: "Phoenix King Ozai - Supreme Fire Lord" (Red, Notched 10).
 * - Sozin's Comet Empowered: Dual-wielding compressed fire jets, continuous fire blast volleys.
 * - Deadly Lightning Strike: Gathers dual lightning and strikes target position with real lightning!
 * - High Mobility: Fire jet dashes towards or around opponents.
 * - Emissive golden crown and glowing fire eyes.
 */
public class PhoenixKingOzaiEntity extends HostileEntity {

    private final ServerBossBar bossBar;
    private int attackCycleTimer = 30;
    private int fireJetCooldown = 60;

    public PhoenixKingOzaiEntity(EntityType<? extends HostileEntity> entityType, World world) {
        super(entityType, world);
        this.bossBar = (ServerBossBar) new ServerBossBar(
                Text.literal("§c§lPhoenix King Ozai §6§l- Supreme Fire Lord"),
                BossBar.Color.RED,
                BossBar.Style.NOTCHED_10
        ).setDarkenSky(true);
        this.experiencePoints = 300;
    }

    public static DefaultAttributeContainer.Builder createOzaiAttributes() {
        return MobEntity.createMobAttributes()
                .add(EntityAttributes.GENERIC_MAX_HEALTH, 320.0)
                .add(EntityAttributes.GENERIC_MOVEMENT_SPEED, 0.34)
                .add(EntityAttributes.GENERIC_ATTACK_DAMAGE, 14.0)
                .add(EntityAttributes.GENERIC_FOLLOW_RANGE, 54.0)
                .add(EntityAttributes.GENERIC_KNOCKBACK_RESISTANCE, 0.75)
                .add(EntityAttributes.GENERIC_ARMOR, 12.0);
    }

    @Override
    protected void initGoals() {
        this.goalSelector.add(1, new SwimGoal(this));
        this.goalSelector.add(2, new MeleeAttackGoal(this, 1.35, true));
        this.goalSelector.add(3, new WanderAroundFarGoal(this, 1.0));
        this.goalSelector.add(4, new LookAtEntityGoal(this, PlayerEntity.class, 24.0f));
        this.goalSelector.add(5, new LookAroundGoal(this));

        this.targetSelector.add(1, new RevengeGoal(this));
        this.targetSelector.add(2, new ActiveTargetGoal<>(this, PlayerEntity.class, true));
    }

    @Override
    public boolean isFireImmune() {
        return true;
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

        this.bossBar.setPercent(this.getHealth() / this.getMaxHealth());

        if (!this.getWorld().isClient()) {
            LivingEntity target = this.getTarget();
            if (target != null && target.isAlive()) {
                // Combat fire aura particles
                if (this.getWorld() instanceof ServerWorld sw && this.age % 2 == 0) {
                    sw.spawnParticles(ParticleTypes.FLAME,
                            this.getX(), this.getY() + 1.0, this.getZ(),
                            4, 0.3, 0.5, 0.3, 0.05);
                    sw.spawnParticles(AvatarParticles.FIRE_EMBER,
                            this.getX(), this.getY() + 1.2, this.getZ(),
                            2, 0.2, 0.4, 0.2, 0.02);
                }

                // Attack cycle
                if (--attackCycleTimer <= 0) {
                    double distSq = this.squaredDistanceTo(target);
                    if (distSq > 16.0 && distSq < 900.0) {
                        if (this.random.nextFloat() < 0.35f) {
                            castLightningBolt(target);
                        } else {
                            castFireBlastVolley(target);
                        }
                    }
                    attackCycleTimer = 40;
                }

                // Fire Jet repositioning
                if (--fireJetCooldown <= 0) {
                    Vec3d toTarget = target.getPos().subtract(this.getPos()).normalize();
                    this.setVelocity(toTarget.x * 0.95, 0.35, toTarget.z * 0.95);
                    this.velocityModified = true;
                    this.getWorld().playSound(null, this.getBlockPos(), SoundEvents.ITEM_FIRECHARGE_USE, SoundCategory.HOSTILE, 1.6f, 0.9f);
                    fireJetCooldown = 120;
                }
            }
        }
    }

    private void castFireBlastVolley(LivingEntity target) {
        if (this.getWorld() instanceof ServerWorld sw) {
            Vec3d dir = target.getEyePos().subtract(this.getEyePos()).normalize();
            sw.playSound(null, this.getBlockPos(), SoundEvents.ENTITY_GHAST_SHOOT, SoundCategory.HOSTILE, 1.8f, 1.1f);

            // Spawns fireball particle stream and applies burn damage
            for (int i = 1; i <= 10; i++) {
                Vec3d step = this.getEyePos().add(dir.multiply(i * 1.5));
                sw.spawnParticles(ParticleTypes.FLAME, step.x, step.y, step.z, 6, 0.2, 0.2, 0.2, 0.04);
                sw.spawnParticles(ParticleTypes.LAVA, step.x, step.y, step.z, 2, 0.1, 0.1, 0.1, 0.0);

                Box hitBox = Box.of(step, 1.8, 1.8, 1.8);
                List<LivingEntity> hits = sw.getEntitiesByClass(LivingEntity.class, hitBox, e -> e != this && e.isAlive());
                DamageSource src = sw.getDamageSources().onFire();
                for (LivingEntity hit : hits) {
                    hit.damage(src, 12.0f);
                    hit.setOnFireFor(5);
                }
            }
        }
    }

    private void castLightningBolt(LivingEntity target) {
        if (this.getWorld() instanceof ServerWorld sw) {
            sw.playSound(null, this.getBlockPos(), SoundEvents.ITEM_TRIDENT_THUNDER.value(), SoundCategory.HOSTILE, 2.0f, 1.2f);
            LightningEntity bolt = EntityType.LIGHTNING_BOLT.create(sw);
            if (bolt != null) {
                bolt.refreshPositionAfterTeleport(target.getX(), target.getY(), target.getZ());
                sw.spawnEntity(bolt);
            }
        }
    }
}
