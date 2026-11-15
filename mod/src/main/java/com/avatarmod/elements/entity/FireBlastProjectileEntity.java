package com.avatarmod.elements.entity;

import com.avatarmod.elements.AvatarElementsMod;
import com.avatarmod.elements.particle.AvatarParticles;
import com.avatarmod.elements.skill.impl.FireBlastSkill;
import net.minecraft.entity.EntityType;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.data.DataTracker;
import net.minecraft.entity.projectile.ProjectileEntity;
import net.minecraft.entity.projectile.ProjectileUtil;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.EntityHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

public class FireBlastProjectileEntity extends ProjectileEntity {

    private float damage;
    private float radius = 1.0f;
    private float knockback = 0.5f;
    private float chargeRatio = 0.0f;
    private int maxLifetime = FireBlastSkill.MAX_LIFETIME;
    private int age = 0;

    public FireBlastProjectileEntity(EntityType<? extends ProjectileEntity> entityType, World world) {
        super(entityType, world);
        this.noClip = false;
    }

    public FireBlastProjectileEntity(World world, LivingEntity owner,
                                     float damage, float radius, float knockback, float chargeRatio) {
        this(AvatarElementsMod.FIRE_BLAST_PROJECTILE, world);
        this.setOwner(owner);
        this.damage = damage;
        this.radius = radius;
        this.knockback = knockback;
        this.chargeRatio = chargeRatio;
        this.maxLifetime = FireBlastSkill.MAX_LIFETIME;
    }

    @Override
    protected void initDataTracker(DataTracker.Builder builder) {
    }

    @Override
    protected void readCustomDataFromNbt(NbtCompound nbt) {
        super.readCustomDataFromNbt(nbt);
        this.damage = nbt.getFloat("Damage");
        this.radius = nbt.getFloat("Radius");
        this.knockback = nbt.getFloat("Knockback");
        this.chargeRatio = nbt.getFloat("ChargeRatio");
        this.age = nbt.getInt("Age");
        if (nbt.contains("MaxLifetime")) {
            this.maxLifetime = nbt.getInt("MaxLifetime");
        }
    }

    @Override
    protected void writeCustomDataToNbt(NbtCompound nbt) {
        super.writeCustomDataToNbt(nbt);
        nbt.putFloat("Damage", this.damage);
        nbt.putFloat("Radius", this.radius);
        nbt.putFloat("Knockback", this.knockback);
        nbt.putFloat("ChargeRatio", this.chargeRatio);
        nbt.putInt("Age", this.age);
        nbt.putInt("MaxLifetime", this.maxLifetime);
    }

    @Override
    public void tick() {
        super.tick();

        HitResult hitResult = ProjectileUtil.getCollision(this, this::canHit);
        if (hitResult.getType() != HitResult.Type.MISS) {
            onCollision(hitResult);
            return;
        }

        Vec3d vel = this.getVelocity();
        double nextX = this.getX() + vel.x;
        double nextY = this.getY() + vel.y;
        double nextZ = this.getZ() + vel.z;
        this.setPosition(nextX, nextY, nextZ);

        if (this.getWorld() instanceof ServerWorld serverWorld) {
            int particleCount = (int) (6 + 8 * chargeRatio);
            serverWorld.spawnParticles(ParticleTypes.FLAME,
                    this.getX(), this.getY(), this.getZ(),
                    particleCount, radius * 0.15, radius * 0.15, radius * 0.15, 0.03);
            serverWorld.spawnParticles(AvatarParticles.FLAME_TONGUE,
                    this.getX(), this.getY(), this.getZ(),
                    (int) (4 + 6 * chargeRatio), radius * 0.12, radius * 0.12, radius * 0.12, 0.03);
            serverWorld.spawnParticles(AvatarParticles.EMBER,
                    this.getX(), this.getY(), this.getZ(),
                    3, radius * 0.1, radius * 0.1, radius * 0.1, 0.02);
            serverWorld.spawnParticles(ParticleTypes.SMOKE,
                    this.getX(), this.getY(), this.getZ(),
                    3, radius * 0.1, radius * 0.1, radius * 0.1, 0.01);
            if (chargeRatio > 0.6f) {
                serverWorld.spawnParticles(ParticleTypes.LAVA,
                        this.getX(), this.getY(), this.getZ(),
                        1, 0.05, 0.05, 0.05, 0.0);
            }
        }

        this.age++;
        if (this.age >= this.maxLifetime) {
            detonate();
            this.discard();
        }
    }

    @Override
    protected void onEntityHit(EntityHitResult entityHitResult) {
        super.onEntityHit(entityHitResult);
        if (!this.getWorld().isClient()) {
            detonate();
            this.discard();
        }
    }

    @Override
    protected void onBlockHit(BlockHitResult blockHitResult) {
        super.onBlockHit(blockHitResult);
        if (!this.getWorld().isClient()) {
            BlockPos blockPos = blockHitResult.getBlockPos();
            if (this.getWorld() instanceof ServerWorld sw && FireBlastSkill.isSolidBlockCollision(sw, blockPos)) {
                detonate();
                this.discard();
            }
        }
    }

    @Override
    public void onRemoved() {
        super.onRemoved();
        if (this.getOwner() != null) {
            FireBlastSkill.onProjectileDiscarded(this.getOwner().getUuid());
        }
    }

    public void detonate() {
        if (this.getWorld() instanceof ServerWorld serverWorld) {
            ServerPlayerEntity ownerPlayer = (this.getOwner() instanceof ServerPlayerEntity sp) ? sp : null;
            FireBlastSkill.detonate(ownerPlayer, serverWorld, this.getPos(), this.damage, this.radius, this.knockback, this.chargeRatio);
        }
    }

    public int getAge() { return age; }
    public float getDamage() { return damage; }
    public float getRadius() { return radius; }
    public float getKnockback() { return knockback; }
    public float getChargeRatio() { return chargeRatio; }
}
